from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from core.utils.sqlite_db import sql_read, delete_product
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from core.settings import settings


async def delete_item(message: Message, bot: Bot):
    if message.from_user.id not in (settings.bots.admin_id, settings.bots.admin2_id):
        return
    read = await sql_read()
    await message.answer('🗣🗣🗣 Внимание‼ Удаляем товары‼')
    for ret in read:
        await bot.send_photo(chat_id=message.from_user.id,
                             photo=ret[1],
                             caption=f'Название: {ret[0]}\nЦена: {ret[2]}\nОписание: {ret[-1]}')
        await bot.send_message(chat_id=message.from_user.id,
                               text='‼‼‼‼‼‼‼',
                               reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                                              [InlineKeyboardButton(text=f'Удалить {ret[0]}',
                                                                                    callback_data=f'del {ret[0]}')]]))
    await message.delete()


async def del_callback_run(callback_query: CallbackQuery):
    await delete_product(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("del ", "")} удален.', show_alert=True)
    await callback_query.message.delete()
    await callback_query.answer()

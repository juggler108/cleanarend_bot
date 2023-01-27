from aiogram import Bot
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from core.utils.sqlite_db import sql_read, add_user_sqlite, sql_read_users
from core.keyboards.inline import get_main_menu_ikb, get_main_menu_button, get_about_us_ikb


async def get_start(message: Message, bot: Bot):
    await add_user_sqlite(message.from_user.id, message.from_user.first_name)
    await message.answer(text=f'Привет <b>{message.from_user.first_name}</b>. Рад тебя видеть!\n\n'
                              f'🤖 Я могу помочь:\n'
                              f'✔ Забронировать оборудование\n'
                              f'✔ Ответить на вопросы\n'
                              f'✔ Перевести в чат со специалистом\n\n'
                              f'Это <b>Основное меню</b> ⤵⤵⤵',
                         reply_markup=get_main_menu_ikb())
    await message.delete()


async def get_help(message: Message):
    await message.answer(f'Здесь будет информация о том как пользоваться ботом')
    await message.delete()


async def get_main_menu(callback: CallbackQuery, bot: Bot):
    await bot.send_message(chat_id=callback.from_user.id,
                           text='🧰 Основное меню ⤵⤵⤵',
                           reply_markup=get_main_menu_ikb())
    await callback.message.delete()
    await callback.answer()


async def get_our_product(callback: CallbackQuery, bot: Bot):
    products = await sql_read()
    await bot.send_message(chat_id=callback.from_user.id,
                           text='🚀 Список нашего оборудования ⤵⤵⤵')
    for ret in products:
        await bot.send_photo(chat_id=callback.from_user.id,
                             photo=ret[1],
                             caption=f'Название: {ret[0]}\nЦена: {ret[2]} ₽\nОписание: {ret[3]}')
    await bot.send_message(chat_id=callback.from_user.id,
                           text=f'❗ {callback.from_user.first_name}\n'
                                f'🤖 Забронировать товар можно в Основном меню ⤵⤵⤵',
                           reply_markup=get_main_menu_button())
    await callback.message.delete()
    await callback.answer()


async def get_about_us_menu(callback: CallbackQuery, bot: Bot):
    await bot.send_message(chat_id=callback.from_user.id,
                           text='Занимаемся арендой оборудования с 2019 года. Лучшая химия. Знаем где, что и как. '
                                'Если возникают какие нибудь трудности или вопросы, всегда готовы помочь и '
                                'проконсультировать.\n\n😇 Здесь вы можете больше узнать о нас ⤵⤵⤵',
                           reply_markup=get_about_us_ikb())
    await callback.message.delete()
    await callback.answer()


async def get_faq(callback: CallbackQuery):
    await callback.message.answer(text=f'🚗 Доставка:\n'
                                       f'- Доставка и забор по Волгограду бесплатно\n'
                                       f'- Волжский +500р\n\n'
                                       f'⭐ Условия:\n'
                                       f'- Составляется договор по паспорту, залог не требуется\n\n'
                                       f'🧪 Химия:\n'
                                       f'- 1 пакетик - 100р\n'
                                       f'- Химия для использования моющего пылесоса\n'
                                       f'- Разводится на 10 литров тёплой воды, хватает на чистку до 10кв.м'
                                       f' (небольшой 3-4местный диванчик)\n'
                                       f'- Химии даём 10 пакетиков. Это с запасом. Всю неиспользованную забираем' 
                                       f' (оплата в конце, по факту)\n\n'
                                       f'🧽 Что можно чистить моющим пылесосом?\n'
                                       f'- Диван\n'
                                       f'- Матрас\n'
                                       f'- Кресло\n'
                                       f'- Ковры\n'
                                       f'- Салон авто\n\n'
                                       f'❓ Если у вас остались вопросы, '
                                       f'то вы можете задать их в разделе "Получить консультацию" в основном меню',
                                  reply_markup=get_main_menu_button())
    await callback.message.delete()


async def get_users_list(message: Message):
    users = await sql_read_users()
    for user in users:
        await message.answer(str(user))
    await message.delete()

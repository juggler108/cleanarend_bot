from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from core.utils.statesform import StepsForm, ClientRentForm
from aiogram import Bot
from core.keyboards.reply import reply_cancel_keyboard, reply_location_keyboard, reply_phone_keyboard
from core.keyboards.inline import start_checkout_ikb, get_vacuum_list_ikb, get_steam_list_ikb, get_dry_list_ikb, \
    get_main_menu_ikb, get_product_list_ikb, get_choose_time_ikb, get_main_menu_button, get_cancel_button_ikb
from core.utils.sqlite_db import db_create_product
from core.aiogram3_calendar.simple_calendar import SimpleCalendar
from core.settings import settings
from core.utils.googlesheets import create_new_sheet, open_and_update_sheet, show_free_dates, get_is_free_date, open_and_update_vacuums_sheet
import datetime

"""Admin"""


async def cmd_cancel(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await message.reply(text='❌ Загрузка товара отменена ❌',
                        reply_markup=ReplyKeyboardRemove())
    await state.clear()


async def get_form(message: Message, state: FSMContext):
    if message.from_user.id not in (settings.bots.admin_id, settings.bots.admin2_id):
        return
    await message.answer(text=f'♻♻♻♻♻♻♻♻\n🤖  Загружаем новый товар'
                              f'\n🏄‍♂  Отправь название\n♻♻♻♻♻♻♻♻\n'
                              f'❗ <b>Внимание</b> ❗\n'
                              f'Название должно быть в формате [КАТЕГОРИЯ][НАИМЕНОВАНИЕ]\n'
                              f'Например: <b>Пылесос Karcher Puzzi 8/1</b>\n'
                              f'На данный момент категория может быть:\n'
                              f'<b>Пылесос</b>, <b>Пароочиститель</b> и <b>Фен</b>\n'
                              f'Категория должна быть написана ОДНИМ словом, без пробелов\n'
                              f'Наименование может быть любым, но имейте ввиду, что это же наименование будет иметь '
                              f'кнопка в меню, поэтому лучше ограничиться 1-3 словами\n'
                              f'Чтобы отменить загрузку товара - нажмите кнопку Отменить\n'
                              f'А теперь <b>Напиши</b> и <b>Отправь</b> название товара',
                         reply_markup=reply_cancel_keyboard)
    await state.set_state(StepsForm.GET_NAME)
    await message.delete()


async def get_name(message: Message, state: FSMContext):
    await message.answer(f'♻♻♻♻♻♻♻♻\n🏄‍♂  Теперь отправь фото\n♻♻♻♻♻♻♻♻')
    await state.update_data(name=message.text)
    await state.set_state(StepsForm.GET_PHOTO)
    await message.delete()


async def get_photo(message: Message, state: FSMContext):
    await message.answer(f'♻♻♻♻♻♻♻♻\n🏄‍♂  Теперь напиши цену\n♻♻♻♻♻♻♻♻')
    await state.update_data(photo=message.photo[-1].file_id)
    await state.set_state(StepsForm.GET_PRICE)
    await message.delete()


async def get_price(message: Message, state: FSMContext):
    await message.answer(f'♻♻♻♻♻♻♻♻\n🏄‍♂  Теперь напиши описание\n♻♻♻♻♻♻♻♻')
    await state.update_data(price=message.text)
    await state.set_state(StepsForm.GET_DESCRIPTION)
    await message.delete()


async def get_description(message: Message, bot: Bot, state: FSMContext):
    context_data = await state.get_data()
    name = context_data.get('name')
    photo = context_data.get('photo')
    price = context_data.get('price')
    create_new_sheet(' '.join(name.split()[1:]))  # create new sheet in google sheet
    await bot.send_photo(chat_id=message.from_user.id,
                         photo=photo,
                         caption=f'Название: {name}\nЦена: {price}\nОписание товара: {message.text}',
                         reply_markup=ReplyKeyboardRemove())
    await db_create_product((name, photo, price, message.text))
    await message.delete()
    await state.clear()


"""Client"""


async def cmd_cancel_checkout(callback: CallbackQuery, state: FSMContext, bot: Bot):
    current_state = await state.get_state()
    if current_state is None:
        return

    await callback.answer(text='❌ Оформление заказа отменено ❌',
                          show_alert=True)
    await state.clear()
    await bot.send_message(chat_id=callback.from_user.id,
                           text='🧰 Основное меню ⤵⤵⤵',
                           reply_markup=get_main_menu_ikb())
    await callback.message.delete()
    await callback.answer()


async def get_start_checkout(callback: CallbackQuery, bot: Bot):
    await bot.send_message(chat_id=callback.from_user.id,
                           text='✅ Отлично! Начинаем оформление заказа.',
                           reply_markup=start_checkout_ikb())
    await callback.message.delete()
    await callback.answer()


async def get_our_prod_call(callback: CallbackQuery, bot: Bot):
    await bot.send_message(chat_id=callback.from_user.id,
                           text='🤖 Что Вас интересует?',
                           reply_markup=get_product_list_ikb())
    await callback.message.delete()
    await callback.answer()


async def get_form_client(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await state.set_state(ClientRentForm.GET_PRODUCT)
    if callback.data == 'vacuum':
        await bot.send_message(chat_id=callback.from_user.id,
                               text='🤖 Наши моющие пылесосы ⤵⤵⤵',
                               reply_markup=await get_vacuum_list_ikb())
        await callback.message.delete()
        return await callback.answer()
    if callback.data == 'steam':
        await bot.send_message(chat_id=callback.from_user.id,
                               text='🤖 Наши пароочистители ⤵⤵⤵',
                               reply_markup=await get_steam_list_ikb())
        await callback.message.delete()
        return await callback.answer()
    if callback.data == 'dry':
        await bot.send_message(chat_id=callback.from_user.id,
                               text='🤖 Наши фены ⤵⤵⤵',
                               reply_markup=await get_dry_list_ikb())
        await callback.message.delete()
        return await callback.answer()


async def get_product_name_state(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await state.update_data(product=callback.data)

    await bot.send_message(chat_id=callback.from_user.id,
                           text=f'✅ Ближайшие свободные даты:\n{show_free_dates(callback.data)}')  # show free dates from google sheet

    await bot.send_message(chat_id=callback.from_user.id,
                           text='🗓 Выберете дату доставки ⤵⤵⤵',
                           reply_markup=await SimpleCalendar().start_calendar())
    await state.set_state(ClientRentForm.GET_DATE)
    await callback.message.delete()
    await callback.answer()


async def process_simple_calendar(callback: CallbackQuery, callback_data: dict, state: FSMContext, bot: Bot):
    """Aiogram calendar process"""

    context_data = await state.get_data()
    product = context_data.get('product')

    selected, date = await SimpleCalendar().process_selection(callback, callback_data)
    if selected:
        date = date.date()
        now = datetime.date.today()
        if date < now:
            await callback.message.answer(text='❗ Вы выбрали неверную дату\n\n🗓 Выберете дату доставки ⤵⤵⤵',
                                          reply_markup=await SimpleCalendar().start_calendar())
            await callback.message.delete()
            await callback.answer()
            return
        elif get_is_free_date(product, date.strftime("%d/%m/%Y")):
            await callback.message.answer(text='❗ Эта дата уже занята\n\n🗓 Выберете дату доставки ⤵⤵⤵',
                                          reply_markup=await SimpleCalendar().start_calendar())

            await callback.message.delete()
            await callback.answer()
            return

        await state.update_data(date=f'{date.strftime("%d/%m/%Y")}')
        try:
            await callback.message.delete()
        except:
            pass
        await callback.message.answer(text=f'🗓 Вы выбрали дату: <b>{date.strftime("%d/%m/%Y")}</b>')
        await callback.message.answer(f'❓ Куда привезти? Отправьте адрес ⤵⤵⤵',
                                      reply_markup=get_cancel_button_ikb())
        await state.set_state(ClientRentForm.GET_ADDRESS)

    await callback.answer()


async def get_address(message: Message, bot: Bot, state: FSMContext):
    await message.answer(text=f'🏠 Вы указали адрес: <b>{message.text}</b>')
    await message.answer(text=f'📱 Отправьте номер телефона ⤵⤵⤵',
                         reply_markup=get_cancel_button_ikb())
    await state.update_data(address=message.text)
    await state.set_state(ClientRentForm.GET_PHONE)
    await message.delete()
    try:
        await bot.delete_message(chat_id=message.from_user.id,
                                 message_id=message.message_id - 1)
    except:
        pass


async def get_phone(message: Message, bot: Bot, state: FSMContext):
    """Google sheet process"""
    context_data = await state.get_data()
    product = context_data.get('product')
    date = context_data.get('date')
    address = context_data.get('address')
    message_text = (f'🎉 {message.from_user.first_name}, заказ принят 🎉\n'
                    f'Мы свяжемся с вами в ближайшее время, чтобы подтвердить заявку.\n\n'
                    f'Товар: {product}\n'
                    f'Дата: {date}\n'
                    f'Адрес: {address}\n'
                    f'Телефон: {message.text}')
    if product == 'KARCHER PUZZI 10/1':
        open_and_update_vacuums_sheet(product=product,
                                      date=date,
                                      all_info=f'{message.from_user.id}\n'
                                               f'{message.from_user.first_name}\n'
                                               f'{address}\n'
                                               f'{message.text}')  # open and update vacuums worksheet_by_title
    else:
        open_and_update_sheet(product=product,
                              date=date,
                              dialog_id=message.from_user.id,
                              name=message.from_user.first_name,
                              address=address,
                              phone=message.text)  # open and update worksheet_by_title
    await bot.send_message(chat_id=message.from_user.id,
                           text=message_text,
                           reply_markup=get_main_menu_button())
    for admin in [settings.bots.admin_id]:
    # for admin in [settings.bots.admin_id, settings.bots.admin2_id]:
        await bot.send_message(chat_id=admin,
                               text=message_text,
                               reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton
                                                                                   (text=message.from_user.first_name,
                                                                                    url=f'tg://user?id={message.from_user.id}')]]))
    for i in range(10):
        try:
            await bot.delete_message(chat_id=message.from_user.id,
                                     message_id=message.message_id - i)
        except:
            continue

    await state.clear()

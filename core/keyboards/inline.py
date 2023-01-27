from aiogram.utils.keyboard import InlineKeyboardBuilder
from core.utils.sqlite_db import sql_read


def get_main_menu_ikb():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='🗓 АРЕНДА - забронировать онлайн', callback_data='rent')
    keyboard_builder.button(text='❓ Часто задаваемые вопросы', callback_data='faq')
    keyboard_builder.button(text='🤔 Получить консультацию', url='https://t.me/Aleksei_Pavlovich_Please')
    keyboard_builder.button(text='🤖 Наше оборудование', callback_data='our_product')
    keyboard_builder.button(text='😇 О нас', callback_data='about_us')
    keyboard_builder.adjust(1, 1, 1, 1, 1)
    return keyboard_builder.as_markup()


def start_checkout_ikb():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='🗓 Начать оформление заказа', callback_data='checkout')
    keyboard_builder.button(text='🧰 Основное меню', callback_data='main_menu')
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def get_main_menu_button():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='🧰 Основное меню', callback_data='main_menu')
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def get_product_list_ikb():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='♻ Пылесосы', callback_data='vacuum')
    keyboard_builder.button(text='♻ Пароочистители', callback_data='steam')
    keyboard_builder.button(text='♻ Фены для сушки мебели', callback_data='dry')
    keyboard_builder.button(text='🧰 Основное меню', callback_data='main_menu')
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


async def get_vacuum_list_ikb():
    """Buttons with the names of vacuum cleaners are formed from the list of products in the database """
    keyboard_builder = InlineKeyboardBuilder()
    product_list = await sql_read()
    for ind, vacuum in enumerate(product_list):
        if 'пыл' in vacuum[0].lower():
            button_name = " ".join(vacuum[0].split()[1:])
            keyboard_builder.button(text=f'♻ {button_name}',
                                    callback_data=button_name)
    keyboard_builder.button(text='🚫 Отменить оформление заказа', callback_data='cancel_checkout')
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


async def get_steam_list_ikb():
    """Buttons with the names of steam cleaners are formed from the list of products in the database """
    keyboard_builder = InlineKeyboardBuilder()
    product_list = await sql_read()
    for ind, steam in enumerate(product_list):
        if 'пар' in steam[0].lower():
            button_name = " ".join(steam[0].split()[1:])
            keyboard_builder.button(text=f'♻ {button_name}',
                                    callback_data=button_name)
    keyboard_builder.button(text='🚫 Отменить оформление заказа', callback_data='cancel_checkout')
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


async def get_dry_list_ikb():
    """Buttons with the names of dryers are formed from the list of products in the database """
    keyboard_builder = InlineKeyboardBuilder()
    product_list = await sql_read()
    for ind, dry in enumerate(product_list):
        if 'фен' in dry[0].lower():
            button_name = " ".join(dry[0].split()[1:])
            keyboard_builder.button(text=f'♻ {button_name}',
                                    callback_data=button_name)
    keyboard_builder.button(text='🚫 Отменить оформление заказа', callback_data='cancel_checkout')
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def get_choose_time_ikb():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='🌝 Утром', callback_data='Утром')
    keyboard_builder.button(text='🌚 Вечером', callback_data='Вечером')
    keyboard_builder.button(text='🚫 Отменить оформление заказа', callback_data='cancel_checkout')
    keyboard_builder.adjust(2)
    return keyboard_builder.as_markup()


def get_about_us_ikb():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='📱 Наш Instagram', url='https://www.instagram.com/cleanarend/')
    keyboard_builder.button(text='📱 Отзывы на Авито', url='https://www.avito.ru/user/bb10a4fd86632d694ddfa0e63c137ccb/profile?id=1831955239&src=item&page_from=from_item_card&iid=1831955239')
    keyboard_builder.button(text='🧰 Основное меню', callback_data='main_menu')
    keyboard_builder.adjust(2)
    return keyboard_builder.as_markup()


def get_cancel_button_ikb():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='🚫 Отменить оформление заказа', callback_data='cancel_checkout')
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()

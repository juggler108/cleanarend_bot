import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, Text

from core.filters.iscontact import IsTrueContact
from core.handlers import basic
from core.handlers.contact import get_true_contact, get_fake_contact
from core.settings import settings
from core.utils.commands import set_commands, set_admin_commands, set_admin2_commands
from core.handlers import form
from core.utils.statesform import StepsForm, ClientRentForm
from core.utils.sqlite_db import db_start
from core.handlers.admin import delete_item, del_callback_run
from core.aiogram3_calendar.simple_calendar import SimpleCalendarCallback as simple_cal_callback

import logging


async def start_bot(bot: Bot):
    await set_commands(bot)
    await set_admin_commands(bot)
    await set_admin2_commands(bot)
    await db_start()
    await bot.send_message(chat_id=settings.bots.admin_id, text='Бот запущен!')


async def stop_bot(bot: Bot):
    await bot.send_message(chat_id=settings.bots.admin_id, text='Бот остановлен!')


async def start():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] - %(name)s - "
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")

    bot = Bot(token=settings.bots.bot_token, parse_mode='HTML')
    dp = Dispatcher()

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    """Client handlers"""
    dp.callback_query.register(basic.get_main_menu, Text(text='main_menu'))
    dp.callback_query.register(form.get_start_checkout, Text(text='rent'))
    dp.callback_query.register(basic.get_our_product, Text(text='our_product'))
    dp.callback_query.register(basic.get_about_us_menu, Text(text='about_us'))
    dp.callback_query.register(basic.get_faq, Text(text='faq'))
    dp.callback_query.register(form.cmd_cancel_checkout, Text(text='cancel_checkout', ignore_case=True))
    dp.callback_query.register(form.get_our_prod_call, Text(text='checkout'))
    dp.callback_query.register(form.get_form_client, lambda x: x.data in 'vacuumsteamdry')
    dp.callback_query.register(form.get_product_name_state, ClientRentForm.GET_PRODUCT)
    dp.callback_query.register(form.process_simple_calendar, simple_cal_callback.filter())
    # dp.callback_query.register(form.get_choose_time, ClientRentForm.GET_TIME)
    dp.message.register(form.get_address, ClientRentForm.GET_ADDRESS)
    # dp.message.register(get_true_contact, F.contact, IsTrueContact())
    # dp.message.register(get_fake_contact, F.contact)
    dp.message.register(form.get_phone, ClientRentForm.GET_PHONE)


    """Admin handlers"""
    dp.message.register(form.get_form, Command(commands='upload'))
    dp.message.register(delete_item, Command(commands='delete'))
    dp.callback_query.register(del_callback_run, lambda x: x.data and x.data.startswith('del '))
    dp.message.register(basic.get_users_list, Command(commands='users'))
    dp.message.register(form.cmd_cancel, Text(text='Отменить', ignore_case=True))
    dp.message.register(form.get_name, StepsForm.GET_NAME)
    dp.message.register(form.get_photo, StepsForm.GET_PHOTO)
    dp.message.register(form.get_price, StepsForm.GET_PRICE)
    dp.message.register(form.get_description, StepsForm.GET_DESCRIPTION)

    dp.message.register(basic.get_start, Command(commands=['start', 'run']))
    dp.message.register(basic.get_help, Command(commands='help'))

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start())

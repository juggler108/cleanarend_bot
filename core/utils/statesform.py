from aiogram.fsm.state import StatesGroup, State


class StepsForm(StatesGroup):
    GET_NAME = State()
    GET_PHOTO = State()
    GET_PRICE = State()
    GET_DESCRIPTION = State()


class ClientRentForm(StatesGroup):
    GET_PRODUCT = State()
    GET_DATE = State()
    GET_TIME = State()
    GET_ADDRESS = State()
    GET_PHONE = State()


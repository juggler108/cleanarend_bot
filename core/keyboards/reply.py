from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonPollType
from aiogram.utils.keyboard import ReplyKeyboardBuilder


reply_cancel_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отменить')]],
                                            resize_keyboard=True,
                                            one_time_keyboard=False,
                                            input_field_placeholder='Кнопка "Отменить" отменит загрузку товара',
                                            selective=True)


reply_location_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='🌎 Отправить геолокацию')]],
                                              resize_keyboard=True,
                                              one_time_keyboard=True,
                                              input_field_placeholder='Или напишите адрес сюда...',
                                              request_location=True)

reply_phone_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='📱 Отправить номер телефона')]],
                                           resize_keyboard=True,
                                           one_time_keyboard=True,
                                           input_field_placeholder='Или напишите номер сюда...',
                                           request_contact=True)

from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeChat
from core.settings import settings


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Начало работы',
        )
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())


async def set_admin_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Начало работы',
        ),
        BotCommand(
            command='upload',
            description='Загрузить новый товар'
        ),
        BotCommand(
            command='delete',
            description='Удалить товар'
        ),
        BotCommand(
            command='users',
            description='Показать список юзеров'
        )
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeChat(chat_id=settings.bots.admin_id))


async def set_admin2_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Начало работы',
        ),
        BotCommand(
            command='upload',
            description='Загрузить новый товар'
        ),
        BotCommand(
            command='delete',
            description='Удалить товар'
        )
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeChat(chat_id=settings.bots.admin2_id))



from aiogram.types import BotCommand, BotCommandScopeDefault

async def set_commands(bot):
    commands = [
        BotCommand(
            command='start',
            description='Информация о пользователе'
        ),
        BotCommand(
            command='help',
            description='Позвать Нихао'
        ),
        BotCommand(
            command='settings',
            description='Настройки'
        )
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())
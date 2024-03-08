import logging
from settings import nihao, bot
from handlers import Start
from handlers.Authentification import Auth
from handlers.DistCourse import DsCourse
from UserInterface import BotCommands
from DB import Database
logging.basicConfig(level=logging.INFO)

Start.register_handlers_start(nihao)
Auth.register_handlers_sComm(nihao)
DsCourse.register_handlers_cComm(nihao)

async def main():
    await BotCommands.set_commands(bot)
    await Database.create_database()
    await nihao.start_polling(bot)

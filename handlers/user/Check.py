import os

from aiogram import types
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from handlers.user.UserData import UserData


class Zaglushka:
    database_path = os.path.join('DB', 'sqlite', 'user_data.db')
    async_engine = create_async_engine(f'sqlite+aiosqlite:///{database_path}', echo=True)
    async_session = sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

async def check(message: types.Message):
    result = await UserData(message)
    if result is not False:  # Проверяем, что результат не пустой и содержит два значения
        login = result[0]
        password = result[1]
        return True
    else:
        return False









import os
from aiogram import types
import aiohttp
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from DB.Database import UniverAPI
from handlers.user.UserData import UserData


class Zaglushka:
    database_path = os.path.join('DB', 'sqlite', 'user_data.db')
    async_engine = create_async_engine(f'sqlite+aiosqlite:///{database_path}', echo=True)
    async_session = sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


async def Authorization(user_id):
    async with Zaglushka.async_session() as session:
        user = select(UniverAPI).where(UniverAPI.telegram_id == user_id)
        existing_user = await session.execute(user)
        user_object = existing_user.scalar()

        if user_object:  # Если пользователь существует
            # Пытаемся взять данные из таблицы
            aspxauth_cookie = user_object.ASPXAUTH
            sessionid_cookie = user_object.ASPNET_SessionId
            return{
                '.ASPXAUTH': aspxauth_cookie,
                'ASP.NET_SessionId': sessionid_cookie
            }
        else:
            return False
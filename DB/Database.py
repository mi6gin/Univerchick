import os
import hashlib

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

def encrypt_password(password):
    # Простой XOR шифр
    key = 0  # Пример ключа
    encrypted_password = "".join(chr(ord(char) ^ key) for char in password)
    return encrypted_password

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(String)
    password_hash = Column(String)
    telegram_id = Column(String)

class UniverAPI(Base):
    __tablename__ = 'sessions'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(String)
    ASPXAUTH = Column(String)
    ASPNET_SessionId = Column(String)
async def create_database():
    database_path = os.path.join('DB', 'sqlite', 'user_data.db')
    async_engine = create_async_engine(f'sqlite+aiosqlite:///{database_path}', echo=True)

    # Создание таблиц
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Создание асинхронной сессии
    async_session = sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session() as session:
        password = "ХУЙ.ВГОВНЕ"

        # Шифруем пароль
        encrypted_password = encrypt_password(password)

        user = User(login="ПИДОРАС.ЕБАНЫЙ", password_hash=str(encrypted_password), telegram_id="ТВОЮДОЧКУЕБУТЧЕРНОМАЗЫЕ")

        session.add_all([user])
        await session.commit()

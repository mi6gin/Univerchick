import os
from aiogram import types
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from DB.Database import User

class Zaglushka:
    database_path = os.path.join('DB', 'sqlite', 'user_data.db')
    async_engine = create_async_engine(f'sqlite+aiosqlite:///{database_path}', echo=True)
    async_session = sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

# Функция для расшифровки пароля
def decrypt_password(encrypted_password):
    # Простой XOR шифр с тем же ключом
    key = 0
    decrypted_password = "".join(chr(ord(char) ^ key) for char in encrypted_password)
    return decrypted_password

# Измененная функция для расшифровки пароля и возвращения логина и пароля
async def UserData(message: types.Message):
    user_id = message.from_user.id
    async with Zaglushka.async_session() as session:
        telega_user = select(User).where(User.telegram_id == user_id)
        existing_user = await session.execute(telega_user)
        user_object = existing_user.scalar()

        if user_object:
            # Расшифровываем пароль
            encrypted_password = user_object.password_hash
            decrypted_password = decrypt_password(encrypted_password)
            login = user_object.login
            password = decrypted_password
            return login, password, user_id
        else:
            return False  # Если пользователя не найдено, возвращаем None для логина и пароля

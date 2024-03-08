import re
from aiogram import Dispatcher, types
from aiogram.client.session import aiohttp
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from sqlalchemy import select

from DB.Database import User, encrypt_password, UniverAPI
from handlers.Start import FSM, start
from handlers.user import Check


async def process_callback_autorisation(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(FSM.Auth)
    data = await state.get_data()
    message_to_delete = data.get('message_to_delete')
    await message_to_delete.delete()
    message_to_delete = await callback.message.answer(
        "Прошу следовать инструкциям!\nВведите свое ФИО и индивидуальный код абитуриента\nОтправьте по примеру:\n\nВладимир Ильич Ленин\n1917rev01uti0nye@R")
    await state.update_data(message_to_delete=message_to_delete)
    await state.set_state(FSM.Finish)

async def process_callback_deautorisation(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(FSM.Deauth)
    data = await state.get_data()
    message_to_delete = data.get('message_to_delete')
    await message_to_delete.delete()
    await callback.message.answer(
        "Вы действительно хотите выйти из аккаунта?\nда/нет")
    await state.set_state(FSM.End)

async def Deauth(message: types.Message, state: FSMContext):
    telegram_user_id = message.from_user.id
    text = message.text
    async with Check.Zaglushka.async_session() as session:
        query = select(User).where(User.telegram_id == telegram_user_id)
        existing_user = await session.execute(query)
        existing_user = existing_user.scalar()

        query_alt = select(UniverAPI).where(UniverAPI.telegram_id == telegram_user_id)
        existing_api = await session.execute(query_alt)
        existing_api = existing_api.scalar()

        if existing_user:
            if text.lower() == 'да' or 'Да':
                await message.answer(
                    "Вы вышли из аккаунта")
                await session.delete(existing_user)  # Удаляем строку из базы данных
                await session.commit()

                await session.delete(existing_api)  # Удаляем строку из базы данных
                await session.commit()
            else:
                await message.answer(
                    "Действие отменено")
        else:
            await message.answer(
                "Ок")




async def Authorization2(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text
    match = re.match(r'^(.+)\n(.+)$', text, re.DOTALL)
    if match:
        full_name = match.group(1).strip()
        password = match.group(2).strip()
        encrypted_password = encrypt_password(password)  # Шифруем пароль
        # Создаем новый экземпляр пользователя
        async with Check.Zaglushka.async_session() as session:
            async with aiohttp.ClientSession() as http_session:
                async with http_session.get(
                        f'https://univerapi.kstu.kz/?login={full_name}&password={password}') as response:
                    cookies = response.cookies
                    aspxauth_cookie = cookies.get('.ASPXAUTH')
                    sessionid_cookie = cookies.get('ASP.NET_SessionId')
                    if aspxauth_cookie is not None and sessionid_cookie is not None:
                        cookie_values = {
                            '.ASPXAUTH': aspxauth_cookie.value,
                            'ASP.NET_SessionId': sessionid_cookie.value
                        }

                        new_user1 = UniverAPI(
                            telegram_id=user_id,
                            ASPXAUTH=cookie_values['.ASPXAUTH'],
                            ASPNET_SessionId=cookie_values['ASP.NET_SessionId']
                        )
                        new_user2 = User(login=full_name,
                                        password_hash=encrypted_password,
                                        telegram_id = user_id)
                        session.add(new_user1)
                        await session.commit()
                        session.add(new_user2)
                        await session.commit()
                        await start(message, state)
                    else:
                        return False
def register_handlers_sComm(nihao: Dispatcher):
    nihao.message.register(Authorization2, StateFilter(FSM.Finish))
    nihao.message.register(Deauth, StateFilter(FSM.End))
    nihao.callback_query.register(process_callback_autorisation, lambda c: c.data == 'sing in')
    nihao.callback_query.register(process_callback_deautorisation, lambda c: c.data == 'sing out')
import requests
from aiogram.client.session import aiohttp
from aiogram.fsm.context import FSMContext
from univer20 import Umkd_review, Umkd_id, Umkd_list_of_files, Umkd_download_file, Umkd_list
from handlers.DistCourse import DsCourse
from aiogram import types, Bot
import urllib.parse
from handlers.Authentification import Keyboard

async def umkd(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    await state.set_state(DsCourse.FSM.Jornal)
    data = await state.get_data()
    message_to_delete = data.get('message_to_delete')
    await message_to_delete.delete()
    umkd = await Umkd_review.Umkd(callback.message, user_id)
    if umkd is not False:
        message_to_delete = await callback.message.answer(
            text=f'УМКД по дисциплинам:',
            reply_markup=await Keyboard.get_keyboard_umkd(callback)
        )
        await state.update_data(message_to_delete=message_to_delete)

async def button_pressed_umkd(callback: types.CallbackQuery, state: FSMContext):
    umkd_number = int(callback.data.split(':')[1])
    user_id = callback.from_user.id
    umkd = await Umkd_review.Umkd(callback.message, user_id)
    discipline_name = umkd[umkd_number - 1]
    id = await Umkd_id.Umkd_id(callback.message, user_id, discipline_name)
    data = await state.get_data()
    message_to_delete = data.get('message_to_delete')
    await message_to_delete.delete()

    sp_umkd = await Umkd_list.Umkd_download(callback.message, id, user_id)
    if sp_umkd[0] == 'нет данных':
        message_to_delete = await callback.message.answer(
            text=f'Нет данных',
            )
        await state.update_data(message_to_delete=message_to_delete)
    else:
        if id is not False:
            message_to_delete = await callback.message.answer(
                text=f'Выберите преподавателя:',
                reply_markup=await Keyboard.get_keyboard_umkd_teacher(callback, id, user_id)
            )
            await state.update_data(message_to_delete=message_to_delete)


async def button_pressed_umkd_num2(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    teacher_id = callback.data.split(':')[1]
    teacher_number = teacher_id[0]  # Получаем первый символ
    id = teacher_id[1:]
    await Umkd_list_of_files.Umkd_list_of_files(callback.message, user_id, teacher_number, id)
    data = await state.get_data()
    message_to_delete = data.get('message_to_delete')
    await message_to_delete.delete()
    if id is not False:
        message_to_delete = await callback.message.answer(
            text=f'Выберите файл:',
            reply_markup=await Keyboard.get_keyboard_umkd_review_file(callback, teacher_number, id)
        )
        await state.update_data(message_to_delete=message_to_delete)


async def button_pressed_umkd_download(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    data_parts = callback.data.split(":")[1].split("z")
    id = int(data_parts[0])
    num, index = map(int, data_parts[1].split("v"))
    await Umkd_download_file.Umkd_download(callback.message, user_id, id, num, state)






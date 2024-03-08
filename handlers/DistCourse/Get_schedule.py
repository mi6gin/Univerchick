from aiogram import Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from univer20 import Schedule, Jornal
from handlers.Authentification import Keyboard
from handlers.Start import FSM
from aiogram.fsm.state import StatesGroup, State
from aiogram import Bot, Dispatcher, types
from handlers.DistCourse import DsCourse


async def schedule(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    await state.set_state(DsCourse.FSM.Schedule)
    data = await state.get_data()
    message_to_delete = data.get('message_to_delete')
    await message_to_delete.delete()
    message_to_delete = await callback.message.answer(
        text=f'Какое расписание вас интересует?',
        reply_markup=Keyboard.get_keyboard_grafics()
    )
    await state.update_data(message_to_delete=message_to_delete)

async def schedule_znml(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    data = await state.get_data()
    message_to_delete = data.get('message_to_delete')
    await message_to_delete.delete()
    schedule = await Schedule.Schedule(callback.message, user_id)
    if schedule is not False:
        formatted_schedule = convert_schedule(schedule)
        await callback.message.answer(
            text=formatted_schedule
        )
async def schedule_chsl(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    data = await state.get_data()
    message_to_delete = data.get('message_to_delete')
    await message_to_delete.delete()
    schedule = await Schedule.Schedule(callback.message, user_id)
    if schedule is not False:
        formatted_schedule = convert_schedule_alt(schedule)
        await callback.message.answer(
            text=formatted_schedule
        )

def convert_day_name(short_day_name):
    days_dict = {
        "ПН": "Понедельник",
        "ВТ": "Вторник",
        "СР": "Среда",
        "ЧТ": "Четверг",
        "ПТ": "Пятница",
        "СБ": "Суббота"
    }
    return days_dict.get(short_day_name, short_day_name)

def convert_schedule(schedule):
    formatted_schedule = "Расписание занятий:\n\n"
    for day, pairs in schedule.items():
        full_day_name = convert_day_name(day)
        formatted_schedule += f"{full_day_name}:\n"
        if pairs:  # Проверяем, есть ли пары для данного дня
            for pair, details in pairs.items():
                if details['denominator'] != "Числитель":  # Проверяем, не идет ли пара по числителю
                    formatted_schedule += f"- {details['time']}: {pair} ({details['type']})\n"
                    formatted_schedule += f"  Преподаватель: {details['instructor']}\n"
                    formatted_schedule += f"  Аудитория: {details['location']}\n"
                    formatted_schedule += "\n"  # Добавляем пустую строку после каждой пары
        else:
            formatted_schedule += "- Нет пар\n\n"  # Выводим "Нет пар" если для данного дня пары отсутствуют
    return formatted_schedule

def convert_schedule_alt(schedule):
    formatted_schedule = "Расписание занятий:\n\n"
    for day, pairs in schedule.items():
        full_day_name = convert_day_name(day)
        formatted_schedule += f"{full_day_name}:\n"
        if pairs:  # Проверяем, есть ли пары для данного дня
            for pair, details in pairs.items():
                if details['denominator'] != "знаменатель":  # Проверяем, не идет ли пара по числителю
                    formatted_schedule += f"- {details['time']}: {pair} ({details['type']})\n"
                    formatted_schedule += f"  Преподаватель: {details['instructor']}\n"
                    formatted_schedule += f"  Аудитория: {details['location']}\n"
                    formatted_schedule += "\n"  # Добавляем пустую строку после каждой пары
        else:
            formatted_schedule += "- Нет пар\n\n"  # Выводим "Нет пар" если для данного дня пары отсутствуют
    return formatted_schedule
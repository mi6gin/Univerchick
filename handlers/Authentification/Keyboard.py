from aiogram import types
from univer20 import Umkd_review, Umkd_list, Umkd_list_of_files
def get_keyboard_auth():
    buttons = [
        [
            types.InlineKeyboardButton(text="Авторизоваться", callback_data="sing in"),
        ],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
def get_keyboard_deauth():
    buttons = [
        [
            types.InlineKeyboardButton(text="Дистанционные курсы", callback_data="dscourse"),
            types.InlineKeyboardButton(text="Выйти из аккаунта", callback_data="sing out"),
        ],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def get_keyboard_distant():
    buttons = [
        [
            types.InlineKeyboardButton(text="Расписание", callback_data="grafics"),
            types.InlineKeyboardButton(text="Журнал посещений и успеваемости", callback_data="jornal"),
            types.InlineKeyboardButton(text="УМКД", callback_data="umkd"),
        ],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def get_keyboard_grafics():
    buttons = [
        [
            types.InlineKeyboardButton(text="Знаменатель", callback_data="znml"),
            types.InlineKeyboardButton(text="Числитель", callback_data="chsl"),
        ],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def get_keyboard_umkd(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    umkd = await Umkd_review.Umkd(callback.message, user_id)
    buttons = []
    for item in umkd:
        button = types.InlineKeyboardButton(text=f'{item}', callback_data=f'umkd:{str(umkd.index(item) + 1)}')
        buttons.append([button])  # Обратите внимание на двойные скобки здесь
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

async def get_keyboard_umkd_teacher(callback: types.CallbackQuery, id, user_id):
    umkd = await Umkd_list.Umkd_download(callback.message, id, user_id)
    buttons = []
    for item in umkd:
        button = types.InlineKeyboardButton(text=f'{item}', callback_data=f'umkdp:{str(umkd.index(item) + 1) + str(id)}')

        buttons.append([button])  # Обратите внимание на двойные скобки здесь
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

async def get_keyboard_umkd_review_file(callback: types.CallbackQuery, teacher_number, id):
    user_id = callback.from_user.id
    umkd = await Umkd_list_of_files.Umkd_list_of_files(callback.message, user_id, teacher_number, id)
    buttons = []
    for item in umkd:
        button = types.InlineKeyboardButton(text=f"{item['name']}", callback_data=f"umkds:{str(item['id'])}z{str(id)}v{str(umkd.index(item) + 1)}")
        buttons.append([button])
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
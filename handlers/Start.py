from aiogram import Dispatcher, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from handlers.user import Check
from univer20 import Username
from handlers.Authentification import Keyboard
class FSM(StatesGroup):
    Start = State()
    Auth = State()
    End = State()
    Finish = State()
    Deauth = State()

async def start(message: types.Message, state: FSMContext):
    await state.set_state(FSM.Start)
    data = await state.get_data()
    message_to_delete = data.get('message_to_delete')
    if message_to_delete:
        await message_to_delete.delete()
    user_id = message.from_user.id
    first = await Check.check(message)
    if first is not False:
        result = await Username.Username(message, user_id)
        if "name" in result:
            message_to_delete = await message.answer(
                text=f'Добро пожаловать {result["name"]} в систему КарТУ имени А.Сагинова "Бала үйрен!"\n\nФИО: {result["name"]}\nКурс: {result["course"]}\nФакультет: {result["faculty"]}',
                reply_markup=Keyboard.get_keyboard_deauth())
            await state.update_data(message_to_delete=message_to_delete)

    else:
        await state.set_state(FSM.Start)
        message_to_delete = await message.reply(
            text="Приветствую тебя в боте университета🎓\nЯ здесь, чтобы помочь тебе получить всю необходимую информацию о расписании, экзаменах, заданиях и многом другом.\nДля начала работы, пожалуйста, авторизуйся, чтобы получить доступ ко всем функциям бота. Это позволит тебе настроить персональные предпочтения и использовать все возможности нашего университетского бота.\n🔐 Авторизация проста! Просто нажми кнопку Авторизоваться ниже и следуй указаниям. Помни, что без регистрации ты не сможешь воспользоваться функционалом бота."
            , reply_markup=Keyboard.get_keyboard_auth()
        )
        await state.update_data(message_to_delete=message_to_delete)

def register_handlers_start(nihao: Dispatcher):
    nihao.message.register(start, Command('start'))
    nihao.message.register(start, StateFilter(FSM.Start))
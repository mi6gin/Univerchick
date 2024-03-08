from aiogram import Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from univer20 import Schedule, Jornal
from handlers.Authentification import Keyboard
from handlers.Start import FSM
from aiogram.fsm.state import StatesGroup, State
from aiogram import Bot, Dispatcher, types
from handlers.DistCourse import Get_schedule, Get_jornal, Get_umkd
class FSM(StatesGroup):
    DistCour = State()
    Schedule = State()
    Jornal = State()

async def dist_course(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(FSM.DistCour)
    data = await state.get_data()
    message_to_delete = data.get('message_to_delete')
    await message_to_delete.delete()
    message_to_delete = await callback.message.answer(
        text=f'Дистанционные курсы',
        reply_markup=Keyboard.get_keyboard_distant()
    )
    await state.update_data(message_to_delete=message_to_delete)

def register_handlers_cComm(nihao: Dispatcher):
    nihao.callback_query.register(dist_course, lambda c: c.data == 'dscourse')
    nihao.callback_query.register(Get_schedule.schedule, lambda c: c.data == 'grafics')
    nihao.callback_query.register(Get_schedule.schedule_znml, lambda c: c.data == 'znml')
    nihao.callback_query.register(Get_schedule.schedule_chsl, lambda c: c.data == 'chsl')
    nihao.callback_query.register(Get_jornal.jornal, lambda c: c.data == 'jornal')
    nihao.callback_query.register(Get_umkd.umkd, lambda c: c.data == 'umkd')
    nihao.callback_query.register(Get_umkd.button_pressed_umkd, lambda c: c.data.startswith('umkd:'))
    nihao.callback_query.register(Get_umkd.button_pressed_umkd_num2, lambda c: c.data.startswith('umkdp:'))
    nihao.callback_query.register(Get_umkd.button_pressed_umkd_download, lambda c: c.data.startswith('umkds:'))

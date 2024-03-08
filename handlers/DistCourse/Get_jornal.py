
from aiogram.fsm.context import FSMContext
from univer20 import Jornal
from handlers.DistCourse import DsCourse
from aiogram import types
from aiogram.enums import ParseMode

async def jornal(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    await state.set_state(DsCourse.FSM.Jornal)
    data = await state.get_data()
    message_to_delete = data.get('message_to_delete')
    await message_to_delete.delete()
    jornal = await Jornal.Jornal(callback.message, user_id)
    if jornal is not False:
        formatted_text = "<b>Журнал посещений и успеваемости:</b>\n"
        formatted_text += "\n".join(
            [f"<i>{subject}:</i>\n<b>RK1: {scores['RK1']}, RK2: {scores['RK2']}</b>" for subject, scores in
             list(jornal.items())[2:]])
        await callback.message.answer(text=formatted_text, parse_mode=ParseMode.HTML)
from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from states import CorrectionProcess

router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer("Привіт! Надішліть текст для перевірки.")
    await state.set_state(CorrectionProcess.WAITING_FOR_TEXT)
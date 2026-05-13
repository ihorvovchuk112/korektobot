from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from states import CorrectionProcess

router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer("Привіт! Надішліть текст для перевірки.")
    await state.set_state(CorrectionProcess.WAITING_FOR_TEXT)
    
@router.message(Command("help"))
async def cmd_help(message: types.Message):
    help_text = (
        "🤖 <b>Довідка по боту:</b>\n\n"
        "КоректоБот використовує ШІ для перевірки текстів у різних режимах:\n\n"
        "🔹 <b>Орфографічна перевірка:</b> Тільки орфографія та одруки. Не чіпає лексику.\n"
        "🔸 <b>Лінгвістичний аналіз:</b> Граматика, відмінки, правильні прийменники та інше.\n"
        "💡 <b>Стилістична адаптація:</b> Перефразування, усунення русизмів, кальок та суржику.\n"
        "✅ <b>Глибока корекція:</b> Повний аналіз (орфографія + граматика + стиль).\n\n"
        "<b>Команди:</b>\n"
        "/start - Почати спочатку\n"
        "/help - Показати це повідомлення\n"
        "/cancel - Скасувати поточну перевірку"
    )
    await message.answer(help_text, parse_mode="HTML")

@router.message(Command("cancel"))
@router.message(F.text.casefold() == "скасувати")
async def cmd_cancel(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return await message.answer("Наразі немає активного процесу для скасування.")
    
    await state.clear() # Очищуємо дані та стани
    await message.answer("Дію скасовано. Можете надіслати новий текст для перевірки.")
    await state.set_state(CorrectionProcess.WAITING_FOR_TEXT)
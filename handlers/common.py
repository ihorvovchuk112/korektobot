from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from states import CorrectionProcess
from keyboards import get_main_reply_keyboard

router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    
    welcome_text = (
        "👋 <b>Вітаю! Я — КоректоБот, твій персональний помічник з аналізу будь яких текстів.</b>\n\n"
        "Я допоможу позбутися помилок та зробити твій текст досконалим. ✨\n\n"
        
        "❓ <b>Що я вмію:</b>\n\n"
        "🔹 <b>Орфографія</b> — виправляю тільки одруки та помилки в словах.\n"
        "🔸 <b>Граматика</b> — стежу за відмінками, узгодженням та чергуванням.\n"
        "💡 <b>Стилістика</b> — прибираю русизми, кальки та тавтологію.\n"
        "✅ <b>Повна вичитка</b> — роблю все вищеперераховане одразу.\n\n"
        
        "🚀 <b>Як ми будемо працювати?</b>\n\n"
        "1️⃣ Надішліть мені будь-який текст.\n"
        "2️⃣ Оберіть режим перевірки, який вам потрібен.\n"
        "3️⃣ Отримайте результат із наочними виправленнями.\n\n"
        
        "<i>Просто надішліть свій текст нижче, і почнемо!</i> 👇"
    )

    await message.answer(
        welcome_text, 
        parse_mode="HTML", 
        reply_markup=get_main_reply_keyboard() # Виводимо кнопку Довідка
    )
    await state.set_state(CorrectionProcess.WAITING_FOR_TEXT)
    
@router.message(Command("help"))
@router.message(F.text == "❓ Допомога")
async def cmd_help(message: types.Message):
    help_text = (
        "🤖 <b>Довідка:</b>\n\n"
        "❓ <b>Що я вмію:</b>\n\n"
        "🔹 <b>Орфографія</b> — виправляю тільки одруки та помилки в словах.\n"
        "🔸 <b>Граматика</b> — стежу за відмінками, узгодженням та чергуванням.\n"
        "💡 <b>Стилістика</b> — прибираю русизми, кальки та тавтологію.\n"
        "✅ <b>Повна вичитка</b> — роблю все вищеперераховане одразу.\n\n\n"
        "<b>Команди:</b>\n\n"
        "/start — Почати спочатку\n"
        "/help — Показати це повідомлення\n"
        "/cancel — Скасувати поточну перевірку\n\n\n"
        "🚀 <b>Як ми будемо працювати?</b>\n\n"
        "1️⃣ Надішліть мені будь-який текст.\n"
        "2️⃣ Оберіть режим перевірки, який вам потрібен.\n"
        "3️⃣ Отримайте результат із наочними виправленнями.\n\n"
        
        "<i>Просто надішліть свій текст нижче, і почнемо!</i> 👇"
        
    )
    await message.answer(help_text, parse_mode="HTML")

@router.message(Command("cancel"))
@router.message(F.text == "❌ Скасувати")
@router.message(F.text.casefold() == "скасувати")
async def cmd_cancel(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return await message.answer("❗ Наразі немає активного процесу для скасування.")
    
    await state.clear()
    await message.answer("⚡ Дію скасовано. Можете надіслати новий текст для перевірки.", reply_markup=get_main_reply_keyboard())
    await state.set_state(CorrectionProcess.WAITING_FOR_TEXT)
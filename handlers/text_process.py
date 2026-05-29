import html
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramAPIError
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter
from states import CorrectionProcess
from keyboards import get_modes_keyboard, get_result_keyboard, get_inline_cancel_keyboard
import logging
from services.gemini_api import process_text_with_gemini

router = Router()

logger = logging.getLogger(__name__)

@router.message(StateFilter(None, CorrectionProcess.WAITING_FOR_TEXT), F.text)
async def handle_user_text(message: types.Message, state: FSMContext):
    await state.update_data(original_text=message.text)
    logger.info(f"User {message.from_user.id} submitted text. Length: {len(message.text)} chars.")
    await message.answer(
        "✅ Оберіть режим корекції:", 
        reply_markup=get_modes_keyboard()
    )
    await state.set_state(CorrectionProcess.CHOOSING_MODE)

@router.message(StateFilter(None, CorrectionProcess.WAITING_FOR_TEXT), ~F.text)
async def handle_non_text_input(message: types.Message):
    logger.info(f"User {message.from_user.id} submitted non-text-input.")
    await message.answer("❗ На жаль, я підтримую лише текст. Спробуйте надіслати текстове повідомлення.")

@router.callback_query(CorrectionProcess.CHOOSING_MODE, F.data.startswith("mode_"))
async def handle_mode_selection(callback_query: types.CallbackQuery, state: FSMContext):
    selected_mode = callback_query.data
    user_data = await state.get_data()
    original_text = user_data.get("original_text", "")

    await callback_query.answer()
    await state.set_state(CorrectionProcess.PROCESSING)
    
    try:
        await callback_query.message.edit_text(
            "⏳ Зачекайте, аналізую текст...", 
            reply_markup=get_inline_cancel_keyboard()
        )
        
        logger.info(f"Gemini to user {callback_query.from_user.id}, mode: {selected_mode}")

        raw_response = await process_text_with_gemini(original_text, selected_mode)
        
        if await state.get_state() != CorrectionProcess.PROCESSING:
            return

        if "|||" in raw_response:
            parts = raw_response.split("|||")
            clean_text = parts[0].strip()
            display_text = parts[1].strip()
        else:
            clean_text = raw_response
            display_text = raw_response

        await state.update_data(clean_text=clean_text, display_text=display_text)

        try:
            await callback_query.message.delete()
        except Exception:
            pass

        result_msg = f"✅ <b>Аналіз завершено!</b>\n\n{display_text}"

        await callback_query.message.answer(
            result_msg, 
            parse_mode=ParseMode.HTML,
            reply_markup=get_result_keyboard(clean_text=clean_text, view="formatted")
        )
        
        await state.set_state(CorrectionProcess.WAITING_FOR_TEXT)
        logger.info(f"Request is handled.")

    except TelegramAPIError as tg_err:
        logger.error(f"Telegram Error: {tg_err}")
        try:
            await callback_query.message.delete()
        except Exception:
            pass
        await callback_query.message.answer(
            "❌ <b>Помилка форматування.</b>\n\nTelegram не зміг відобразити. Спробуйте надіслати текст ще раз або розбийте його на менші частини.",
            parse_mode=ParseMode.HTML
        )
        await state.set_state(CorrectionProcess.WAITING_FOR_TEXT)

    except Exception as e:
        logger.error(f"System Error: {e}")
        try:
            await callback_query.message.delete()
        except Exception:
            pass
        await callback_query.message.answer(
            "⚠️ <b>Серверна помилка.</b>\n\nНа жаль, сервери тимчасово недоступні або відмовили в обробці цього тексту. Спробуйте пізніше.",
            parse_mode=ParseMode.HTML
        )
        await state.set_state(CorrectionProcess.WAITING_FOR_TEXT)

@router.callback_query(F.data == "view_clean")
async def show_clean_text(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    clean_text = data.get("clean_text", "Текст не знайдено.")
    
    safe_clean = html.escape(clean_text)
    msg = f"📋 <b>Натисніть на текст нижче, щоб скопіювати:</b>\n\n<code>{safe_clean}</code>"
    
    await callback_query.message.edit_text(
        msg, 
        parse_mode=ParseMode.HTML, 
        reply_markup=get_result_keyboard(view="clean")
    )

@router.callback_query(F.data == "view_formatted")
async def show_formatted_text(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    display_text = data.get("display_text", "Текст не знайдено.")
    
    msg = f"✅ <b>Аналіз завершено!</b>\n\n{display_text}"
    
    await callback_query.message.edit_text(
        msg, 
        parse_mode=ParseMode.HTML, 
        reply_markup=get_result_keyboard(view="formatted")
    )

@router.callback_query(F.data == "restart_process")
async def restart_correction(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await state.set_state(CorrectionProcess.WAITING_FOR_TEXT)
    await callback_query.message.answer("Надішліть новий текст для перевірки.")

@router.callback_query(F.data == "cancel_action")
async def cancel_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback_query.answer("Дію скасовано")
    try:
        await callback_query.message.delete()
    except Exception:
        pass
    await callback_query.message.answer("❌ Обробку скасовано. Надішліть новий текст для перевірки коли будете готові.")
    await state.set_state(CorrectionProcess.WAITING_FOR_TEXT)
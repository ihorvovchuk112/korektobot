from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CopyTextButton

def get_modes_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Швидка перевірка", callback_data="mode_ortho")],
            [InlineKeyboardButton(text="Лінгвістичний аналіз", callback_data="mode_grammar")],
            [InlineKeyboardButton(text="Стилістична адаптація", callback_data="mode_style")],
            [InlineKeyboardButton(text="Глибока корекція", callback_data="mode_full")]
        ]
    )

def get_result_keyboard(clean_text: str = "", view: str = "formatted"):
    keyboard = []
    
    if view == "formatted":
        # Перевіряємо довжину тексту для нативної кнопки
        if clean_text and len(clean_text) <= 256:
            keyboard.append([InlineKeyboardButton(
                text="📋 Скопіювати текст", 
                copy_text=CopyTextButton(text=clean_text)
            )])
        else:
            # Якщо текст довгий, даємо кнопку-перемикач
            keyboard.append([InlineKeyboardButton(
                text="👁 Показати чистий текст", 
                callback_data="view_clean"
            )])
    elif view == "clean":
        # Кнопка для повернення до розмітки помилок
        keyboard.append([InlineKeyboardButton(
            text="🔙 Показати виправлення", 
            callback_data="view_formatted"
        )])
        
    # Загальна кнопка для перезапуску завжди внизу
    keyboard.append([InlineKeyboardButton(
        text="🔄 Перевірити інший текст", 
        callback_data="restart_process"
    )])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
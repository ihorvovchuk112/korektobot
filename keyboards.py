from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CopyTextButton, ReplyKeyboardMarkup, KeyboardButton

def get_modes_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Орфографічна перевірка", callback_data="mode_ortho")],
            [InlineKeyboardButton(text="Лінгвістичний аналіз", callback_data="mode_grammar")],
            [InlineKeyboardButton(text="Стилістична адаптація", callback_data="mode_style")],
            [InlineKeyboardButton(text="Глибока корекція", callback_data="mode_full")],
            [InlineKeyboardButton(text="❌ Скасувати", callback_data="cancel_action")]
        ]
    )

def get_inline_cancel_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="❌ Скасувати", callback_data="cancel_action")]
        ]
    )

def get_main_reply_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❓ Допомога")]],
        resize_keyboard=True
    )



def get_result_keyboard(clean_text: str = "", view: str = "formatted"):
    keyboard = []
    
    if view == "formatted":
        if clean_text and len(clean_text) <= 256:
            keyboard.append([InlineKeyboardButton(
                text="📋 Скопіювати текст", 
                copy_text=CopyTextButton(text=clean_text)
            )])
        else:
            keyboard.append([InlineKeyboardButton(
                text="👁 Показати чистий текст", 
                callback_data="view_clean"
            )])
    elif view == "clean":
        keyboard.append([InlineKeyboardButton(
            text="🔙 Показати виправлення", 
            callback_data="view_formatted"
        )])
        
    keyboard.append([InlineKeyboardButton(
        text="🔄 Перевірити інший текст", 
        callback_data="restart_process"
    )])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
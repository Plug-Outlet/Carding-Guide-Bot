from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_confirmation_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Yes", callback_data="confirm_yes"),
                InlineKeyboardButton(text="❌ No", callback_data="confirm_no")
            ]
        ]
    )
    return keyboard
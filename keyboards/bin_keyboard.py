from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_bin_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔍 Check BIN", callback_data="check_bin")],
            [InlineKeyboardButton(text="📊 BIN Info", callback_data="bin_info")],
            [InlineKeyboardButton(text="📚 BIN Database", callback_data="bin_database")],
            [InlineKeyboardButton(text="🔙 Back", callback_data="back_to_main")]
        ]
    )
    return keyboard

def get_bin_result_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Save BIN", callback_data="save_bin")],
            [InlineKeyboardButton(text="🔄 Check Another", callback_data="check_another_bin")],
            [InlineKeyboardButton(text="🔙 Back", callback_data="back_to_bin_menu")]
        ]
    )
    return keyboard
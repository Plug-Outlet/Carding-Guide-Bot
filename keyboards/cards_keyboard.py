from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_cards_menu_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="💳 Check Card", callback_data="check_card"),
                InlineKeyboardButton(text="🏦 Bank Check", callback_data="bank_check")
            ],
            [
                InlineKeyboardButton(text="🔢 BIN Checking", callback_data="bin_check"),
                InlineKeyboardButton(text="💰 IVR Balance Check", callback_data="balance_check")
            ],
            [
                InlineKeyboardButton(text="📊 Card Stats", callback_data="card_stats"),
                InlineKeyboardButton(text="🔙 Back", callback_data="back_to_main")
            ]
        ]
    )
    return keyboard

def get_card_checker_menu_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="1️⃣", callback_data="check_format_1"),
            InlineKeyboardButton(text="2️⃣", callback_data="check_format_2"),
            InlineKeyboardButton(text="3️⃣", callback_data="check_format_3"),
        ],
        [
            InlineKeyboardButton(text="📜 History", callback_data="view_history"),
            InlineKeyboardButton(text="🔙 Back", callback_data="back_to_main"),
        ]
    ])
    return keyboard


def get_card_result_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Save Card", callback_data="save_card")],
            [InlineKeyboardButton(text="🔄 Check Another", callback_data="check_another_card")],
            [InlineKeyboardButton(text="🔙 Back", callback_data="back_to_cards_menu")]
        ]
    )
    return keyboard

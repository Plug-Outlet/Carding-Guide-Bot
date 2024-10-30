from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from utils.admin_utils import is_admin



def get_main_user_keyboard(user_id: int) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(text="🔍 Checker Menu", callback_data="checker_menu"),
            InlineKeyboardButton(text="🏦 BIN Check", callback_data="bin_check")
        ],
        [
            InlineKeyboardButton(text="📚 Guides", callback_data="guides"),
            InlineKeyboardButton(text="💡 Help", callback_data="help")
        ],
        [
            InlineKeyboardButton(text="👤 Profile", callback_data="profile"),
            InlineKeyboardButton(text="🔄 Refresh", callback_data="refresh_menu")
        ],
        [
            InlineKeyboardButton(text="🎟️ Ticket Menu", callback_data="ticket_menu")  # Added Ticket Menu option
        ]
    ]
    
    if is_admin(user_id):
        keyboard.append([InlineKeyboardButton(text="🔐 Admin Panel", callback_data="admin_panel")])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_checker_menu_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💳 CC Checker", callback_data="cc_check")],
            [InlineKeyboardButton(text="🏛 Bank Checker", callback_data="bank_check")],
            [InlineKeyboardButton(text="🔙 Back to Main", callback_data="back_to_main")]
        ]
    )
    return keyboard


def get_ticket_management_keyboard():
    """
    Creates a keyboard for ticket management options.
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🆕 Create New Ticket", callback_data="create_ticket"),
                InlineKeyboardButton(text="📜 View My Tickets", callback_data="view_tickets")
            ],
            [
                InlineKeyboardButton(text="🔄 Update Ticket Status", callback_data="update_ticket_status"),
                InlineKeyboardButton(text="❓ FAQ", callback_data="ticket_faq")
            ],
            [
                InlineKeyboardButton(text="🔙 Back to Admin Menu", callback_data="back_to_admin")
            ]
        ]
    )
    return keyboard



def get_profile_membership_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="⬆️ Upgrade Membership", callback_data="upgrade_membership"),
                InlineKeyboardButton(text="⚙️ Change Settings", callback_data="change_settings")
            ],
            [
                InlineKeyboardButton(text="📊 View Transaction History", callback_data="transaction_history")
            ],
            [
                InlineKeyboardButton(text="🔙 Back to Main Menu", callback_data="back_to_main")
            ]
        ]
    )
    return keyboard
    
    
def get_profile_membership_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="⬆️ Upgrade Membership", callback_data="upgrade_membership"),
                InlineKeyboardButton(text="⚙️ Change Settings", callback_data="change_settings")
            ],
            [
                InlineKeyboardButton(text="📊 View Transaction History", callback_data="transaction_history")
            ],
            [
                InlineKeyboardButton(text="🔙 Back to Main Menu", callback_data="back_to_main")
            ]
        ]
    )
    return keyboard

def get_pagination_keyboard(current_page: int, total_pages: int) -> InlineKeyboardMarkup:
    """
    Creates a pagination keyboard with Next, Previous, and Exit buttons.
    
    :param current_page: The current page number (0-indexed).
    :param total_pages: The total number of pages.
    :return: An InlineKeyboardMarkup object with pagination buttons.
    """
    keyboard = []
    
    # Previous button
    if current_page > 0:
        keyboard.append(InlineKeyboardButton(text="◀️ Previous Page", callback_data=f"prev_page_{current_page}"))
    
    # Current page indicator
    page_indicator = f"Page {current_page + 1} of {total_pages}"
    
    # Exit button
    keyboard.append(InlineKeyboardButton(text=page_indicator, callback_data='exit_pages'))
    
    # Next button
    if current_page < total_pages - 1:
        keyboard.append(InlineKeyboardButton(text="▶️ Next Page", callback_data=f"next_page_{current_page}"))
    
    return InlineKeyboardMarkup(inline_keyboard=[keyboard])
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.database import db






def get_guide_management_keyboard():
    """
    Creates a keyboard for guide management options.
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📝 Create New Guide", callback_data="admin_create_guide"),
                InlineKeyboardButton(text="✏️ Edit Existing Guide", callback_data="admin_edit_guide")
            ],
            [
                InlineKeyboardButton(text="🗑 Delete Guide", callback_data="admin_delete_guide"),
                InlineKeyboardButton(text="📋 List All Guides", callback_data="list_guides")
            ],
            [
                InlineKeyboardButton(text="🔙 Back to Admin Menu", callback_data="back_to_admin")
            ]
        ]
    )
    return keyboard

def get_guide_format_keyboard():
    """
    Creates a keyboard for selecting the format of a guide.
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📄 Plain Text", callback_data="format_plain"),
                InlineKeyboardButton(text="🔗 Markdown", callback_data="format_markdown")
            ],
            [
                InlineKeyboardButton(text="🌐 HTML", callback_data="format_html"),
                InlineKeyboardButton(text="🖼 Image + Caption", callback_data="format_image")
            ],
            [
                InlineKeyboardButton(text="🔙 Cancel", callback_data="cancel_guide_creation")
            ]
        ]
    )
    return keyboard

def get_submission_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Submit", callback_data="submit_guide"),
                InlineKeyboardButton(text="✏️ Edit", callback_data="edit_guide"),
                InlineKeyboardButton(text="❌ Cancel", callback_data="cancel_guide_creation")
            ]
        ]
    )
    return keyboard


def get_admin_keyboard():
    """
    Creates the main admin keyboard with buttons arranged in rows of two.
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="👥 User Management", callback_data="manage_users"),
                InlineKeyboardButton(text="📢 Broadcast", callback_data="admin_broadcast")
            ],
            [
                InlineKeyboardButton(text="📚 Guide Management", callback_data="manage_guides"),
                InlineKeyboardButton(text="⚙️ Bot Settings", callback_data="bot_settings")
            ],
            [
                InlineKeyboardButton(text="📊 Statistics", callback_data="view_stats"),
                InlineKeyboardButton(text="🎟 Tickets", callback_data="view_tickets")
            ],
            [
                InlineKeyboardButton(text="🔙 Exit Admin Mode", callback_data="exit_admin")
            ]
        ]
    )
    return keyboard

def get_user_management_keyboard():
    """
    Creates a keyboard for user management options.
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="👤 View Users", callback_data="view_users"),
                InlineKeyboardButton(text="🔍 Search User", callback_data="search_user")
            ],
            [
                InlineKeyboardButton(text="📈 Promote User", callback_data="promote_user"),
                InlineKeyboardButton(text="🚫 Remove User", callback_data="remove_user")
            ],
            [
                InlineKeyboardButton(text="📊 User Statistics", callback_data="user_statistics"),
                InlineKeyboardButton(text="🔙 Back to Admin Menu", callback_data="back_to_admin")
            ]
        ]
    )
    return keyboard

def get_broadcast_keyboard():
    """
    Creates a keyboard for broadcasting messages.
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📢 Broadcast to All Users", callback_data="broadcast_all"),
                InlineKeyboardButton(text="📬 Broadcast to Premium Users", callback_data="broadcast_premium")
            ],
            [
                InlineKeyboardButton(text="✉️ Send Message to Specific User", callback_data="send_message_to_user"),
                InlineKeyboardButton(text="📊 View Broadcast Statistics", callback_data="broadcast_statistics")
            ],
            [
                InlineKeyboardButton(text="🔙 Back to Admin Menu", callback_data="back_to_admin")
            ]
        ]
    )
    return keyboard


def get_ad_slots_keyboard():
    """
    Creates a keyboard with 6 advertisement slots arranged in rows of two.
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🎯 Ad Slot 1", callback_data="ad_slot_1"),
                InlineKeyboardButton(text="🎯 Ad Slot 2", callback_data="ad_slot_2")
            ],
            [
                InlineKeyboardButton(text="🎯 Ad Slot 3", callback_data="ad_slot_3"),
                InlineKeyboardButton(text="🎯 Ad Slot 4", callback_data="ad_slot_4")
            ],
            [
                InlineKeyboardButton(text="🎯 Ad Slot 5", callback_data="ad_slot_5"),
                InlineKeyboardButton(text="🎯 Ad Slot 6", callback_data="ad_slot_6")
            ],
            [
                InlineKeyboardButton(text="📊 Ad Statistics", callback_data="ad_statistics"),
                InlineKeyboardButton(text="🔙 Back to Main Menu", callback_data="back_to_main")
            ]
        ]
    )










def get_bot_settings_keyboard():
    """
    Creates a keyboard for bot settings, including the startup message toggle.
    """
    startup_message_status = "✅" if db.get_startup_message_status() else "❌"
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f"Send Startup Message {startup_message_status}", callback_data="toggle_startup_message")
            ],
            [
                InlineKeyboardButton(text="🔙 Back to Admin Menu", callback_data="back_to_admin")
            ]
        ]
    )
    return keyboard



def get_guide_submission_keyboard():
    """
    Creates a keyboard for submitting various types of information.
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🔗 Submit URL", callback_data="submit_url"),
                InlineKeyboardButton(text="💳 Submit Payment", callback_data="submit_payment")
            ],
            [
                InlineKeyboardButton(text="✅/❌ Submit AVS", callback_data="submit_avs"),
                InlineKeyboardButton(text="✍️ Submit Description", callback_data="submit_description")
            ],
            [
                InlineKeyboardButton(text="✍️ Publish Guide", callback_data="admin_publish_guide_description")
            ],
        ]
    )
    return keyboard
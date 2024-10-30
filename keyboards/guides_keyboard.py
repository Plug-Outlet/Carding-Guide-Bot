from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.database import db, Database




def get_guides_main_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📦 Guide by Types", callback_data="guide_types"),
                InlineKeyboardButton(text="🛒 Guides by Methods", callback_data="guide_methods")
            ],
            [
                InlineKeyboardButton(text="🎯 Guides by Targets", callback_data="guide_targets"),
                InlineKeyboardButton(text="🏷️ Guides by Categories", callback_data="guide_categories")
            ],
            [
                InlineKeyboardButton(text="❓ FAQ", callback_data="guide_main_faq"),
                InlineKeyboardButton(text="🔙 Back", callback_data="back_to_main")
            ]
        ]
    )
    return keyboard

def get_guide_methods_menu_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🔰 Email Access Targets", callback_data="guide_methods_email_access"),
                InlineKeyboardButton(text="➡️ Direct Access Targets", callback_data="guide_methods_direct_access")
            ],
            [
                InlineKeyboardButton(text="💳 PM On File Targets", callback_data="guide_methods_pmof"),
                InlineKeyboardButton(text="👨‍🏭 Net-30 Sites", callback_data="guide_methods_net30")
            ],
            [
                InlineKeyboardButton(text="🏠 AVS Enforced Sites", callback_data="guide_methods_avs"),
                InlineKeyboardButton(text="🏦 An/RN Accepted", callback_data="guide_methods_an_rn")
            ],
            [
                InlineKeyboardButton(text="🫥 2D", callback_data="guide_methods_2d"),
                InlineKeyboardButton(text="💸 3D", callback_data="guide_methods_3d")
            ],
            [
                InlineKeyboardButton(text="🏦 Bank Specific Guides", callback_data="guide_methods_banks")
            ],
            [
                InlineKeyboardButton(text="❓ FAQ", callback_data="guide_methods_menu_faq"),
                InlineKeyboardButton(text="🔙 Back to Guide - Methods", callback_data="guide_methods_back_to_main")
            ]
        ]
    )
    return keyboard

def get_guide_ordering_types_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🔄 Standard", callback_data="guide_types_standard"),
                InlineKeyboardButton(text="🚀 Rush", callback_data="guide_types_rush")
            ],
            [
                InlineKeyboardButton(text="📦 Bulk", callback_data="guide_types_bulk"),
                InlineKeyboardButton(text="🎨 Custom", callback_data="guide_types_custom")
            ],
            [
                InlineKeyboardButton(text="🔁 Recurring", callback_data="guide_types_recurring")
            ],
            [
                InlineKeyboardButton(text="❓ FAQ", callback_data="guide_types_faq"),
                InlineKeyboardButton(text="🔙 Back to Guides", callback_data="back_to_guides_main")
            ]
        ]
    )
    return keyboard

def get_guide_ordering_methods_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="💻 Online", callback_data="guide_online"),
                InlineKeyboardButton(text="📞 Phone", callback_data="guide_phone")
            ],
            [
                InlineKeyboardButton(text="🏬 In-Store", callback_data="guide_in-store"),
                InlineKeyboardButton(text="✉️ Mail", callback_data="guide_mail")
            ],
            [
                InlineKeyboardButton(text="📱 Mobile", callback_data="guide_mobile")
            ],
            [
                InlineKeyboardButton(text="❓ FAQ", callback_data="guide_ordering_faq"),
                InlineKeyboardButton(text="🔙 Back", callback_data="back_to_main")
            ]
        ]
    )
    return keyboard

def get_guide_ordering_categories_keyboard():
    # Fetch guide counts for each category from the database
    food_count = db.get_guide_count_by_category("Food & Groceries")
    clothing_count = db.get_guide_count_by_category("Clothing & Fashion")
    electronics_count = db.get_guide_count_by_category("Electronics")
    books_count = db.get_guide_count_by_category("Books & Media")
    home_count = db.get_guide_count_by_category("Home & Garden")
    beauty_count = db.get_guide_count_by_category("Beauty & Personal Care")
    toys_count = db.get_guide_count_by_category("Toys & Games")
    sports_count = db.get_guide_count_by_category("Sports & Fitness")
    printing_count = db.get_guide_count_by_category("3D Printing")
    tools_count = db.get_guide_count_by_category("Tools & Home Improvement")
    automotive_count = db.get_guide_count_by_category("Automotive")
    health_count = db.get_guide_count_by_category("Health & Wellness")
    pets_count = db.get_guide_count_by_category("Pet Supplies")
    baby_count = db.get_guide_count_by_category("Baby & Kids")
    arts_count = db.get_guide_count_by_category("Arts & Crafts")
    music_count = db.get_guide_count_by_category("Musical Instruments")
    travel_count = db.get_guide_count_by_category("Travel & Luggage")
    gifts_count = db.get_guide_count_by_category("Gifts & Special Occasions")

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f"🍔 Food & Groceries ({food_count})", callback_data="guide_food"),
                InlineKeyboardButton(text=f"👚 Clothing & Fashion ({clothing_count})", callback_data="guide_clothing"),
                InlineKeyboardButton(text=f"🖥️ Electronics ({electronics_count})", callback_data="guide_electronics")
            ],
            [
                InlineKeyboardButton(text=f"📚 Books & Media ({books_count})", callback_data="guide_books"),
                InlineKeyboardButton(text=f"🏠 Home & Garden ({home_count})", callback_data="guide_home"),
                InlineKeyboardButton(text=f"💄 Beauty & Personal Care ({beauty_count})", callback_data="guide_beauty")
            ],
            [
                InlineKeyboardButton(text=f"🎮 Toys & Games ({toys_count})", callback_data="guide_toys"),
                InlineKeyboardButton(text=f"🏋️ Sports & Fitness ({sports_count})", callback_data="guide_sports"),
                InlineKeyboardButton(text=f"🖨️ 3D Printing ({printing_count})", callback_data="guide_3d_printing")
            ],
            [
                InlineKeyboardButton(text=f"🛠️ Tools & Home Improvement ({tools_count})", callback_data="guide_tools"),
                InlineKeyboardButton(text=f"🚗 Automotive ({automotive_count})", callback_data="guide_automotive"),
                InlineKeyboardButton(text=f"💊 Health & Wellness ({health_count})", callback_data="guide_health")
            ],
            [
                InlineKeyboardButton(text=f"🐶 Pet Supplies ({pets_count})", callback_data="guide_pets"),
                InlineKeyboardButton(text=f"👶 Baby & Kids ({baby_count})", callback_data="guide_baby"),
                InlineKeyboardButton(text=f"🎨 Arts & Crafts ({arts_count})", callback_data="guide_arts")
            ],
            [
                InlineKeyboardButton(text=f"🎵 Musical Instruments ({music_count})", callback_data="guide_music"),
                InlineKeyboardButton(text=f"🧳 Travel & Luggage ({travel_count})", callback_data="guide_travel"),
                InlineKeyboardButton(text=f"🎁 Gifts & Special Occasions ({gifts_count})", callback_data="guide_gifts")
            ],
            [
                InlineKeyboardButton(text="❓ FAQ", callback_data="guide_category_faq"),
                InlineKeyboardButton(text="🔙 Back", callback_data="back_to_main")
            ]
        ]
    )
    return keyboard

def guide_veiwing_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="👀 Open Details", callback_data="submit_url"),
                InlineKeyboardButton(text="⭐ Read Feedback", callback_data="submit_payment")
            ],
            [
                InlineKeyboardButton(text="🔒 Leave Raiting", callback_data="submit_security"),
                InlineKeyboardButton(text="🗂️ Leave Feedback", callback_data="submit_misc")
            ],
            [
                InlineKeyboardButton(text="⏰ Submit Complaint", callback_data="submit_delivery_time"),
                InlineKeyboardButton(text="❌ Cancel", callback_data="cancel_submission")
            ]
        ]
    )
    return keyboard

def get_guide_navigation_keyboard(guide_id, total_pages, current_page):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="◀️ Previous", callback_data=f"guide_{guide_id}_prev_{current_page}"),
                InlineKeyboardButton(text=f"{current_page}/{total_pages}", callback_data="current_page"),
                InlineKeyboardButton(text="Next ▶️", callback_data=f"guide_{guide_id}_next_{current_page}")
            ],
            [InlineKeyboardButton(text="🔙 Back to Guides", callback_data="back_to_guides")]
        ]
    )
    return keyboard
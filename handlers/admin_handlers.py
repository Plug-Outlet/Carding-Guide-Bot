from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram.enums import ChatType

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import ADMIN_USER_IDS, ADMIN_USERNAMES
from utils.admin_utils import is_admin
from keyboards.user_keyboard import get_main_user_keyboard
from keyboards.guides_keyboard import *
from handlers.guide_handlers import *
from aiogram.utils.markdown import hlink
from aiogram import Dispatcher
from handlers.ticket_handlers import *
from aiogram.filters.callback_data import CallbackData
from utils.states import StorageFunctions
from filters.admin_filter import IsAdmin  # Make sure you have this custom filter



from keyboards.admin_keyboard import (
    get_guide_management_keyboard,
    get_guide_format_keyboard,
    get_admin_keyboard,
    get_submission_keyboard,
    get_user_management_keyboard,
    get_guide_submission_keyboard,
    get_bot_settings_keyboard
)
from utils.database import db, Database
import logging

router = Router()
logger = logging.getLogger(__name__)

class Form(StatesGroup):
    waiting_for_url = State()
    waiting_for_payment = State()
    waiting_for_delivery_time = State()
    waiting_for_avs = State()
    waiting_for_misc_info = State()

class AdminStates(StatesGroup):
    waiting_for_broadcast = State()
    waiting_for_ban_user_id = State()
    waiting_for_upgrade_user_id = State()
    waiting_for_guide_url = State()
    waiting_for_payment_method = State()
    waiting_for_delivery_time = State()
    waiting_for_avs_details = State()
    waiting_for_misc_info = State()
    
@router.callback_query(F.data == "admin_panel")
async def admin_panel(callback: CallbackQuery):
    user_id = callback.from_user.id
    username = callback.from_user.username
    if is_admin(user_id, username):
        try:
            # Admin panel logic here
            total_users = db.get_user_count()
            recent_users = db.get_recent_active_users(limit=3)
            new_users = db.get_recent_registered_users(limit=3)
            membership_stats = db.get_membership_stats()
            
            # Get additional statistics
            guide_count = db.get_guide_count()
            
            # Prepare the statistics message
            stats_message = f"""
📊 <b>Admin Panel - Bot Statistics</b>

👥 <b>User Statistics:</b>
• Total Users: {total_users}
• New Users (last 7 days): {db.get_new_user_count(days=7)}

🏅 <b>Membership Levels:</b>
{format_membership_stats(membership_stats)}

📚 <b>Guides:</b>
• Total Guides: {guide_count}

👤 <b>Recent Active Users:</b>
{format_user_list(recent_users, "active")}

🆕 <b>Recently Registered Users:</b>
{format_user_list(new_users, "registered")}
"""
            await callback.message.edit_text(stats_message, reply_markup=get_admin_keyboard(), parse_mode="HTML")
        except Exception as e:
            logger.error(f"Error in admin panel: {e}")
            await callback.answer("An error occurred while fetching admin statistics.", show_alert=True)
    else:
        await callback.answer("You don't have permission to access the admin panel.", show_alert=True)

def format_membership_stats(stats):
    return "\n".join([f"• {level}: {count}" for level, count in stats.items()])

def format_user_list(users, user_type):
    if not users:
        return f"No recent {user_type} users."
    
    user_list = []
    for user in users:
        user_id, username, timestamp, membership_level = user
        profile_link = hlink(username or "Unknown", f"tg://user?id={user_id}")
        user_info = f"""• {profile_link}
    • User ID: {user_id}
    • Membership: {membership_level}
    • {'Last active' if user_type == 'active' else 'Registered'}: {timestamp}"""
        user_list.append(user_info)
    
    return "\n\n".join(user_list)

@router.callback_query(F.data.startswith("admin_"))
async def process_admin_callback(callback: CallbackQuery, state: FSMContext, dispatcher: Dispatcher = None):
    action = callback.data.split("_")[1]
    try:
        if action == "stats":
            stats = await db.get_bot_statistics()
            await callback.message.edit_text(f"Bot Statistics:\n\n{stats}", reply_markup=get_admin_keyboard())
        elif action == "broadcast":
            await state.set_state(AdminStates.waiting_for_broadcast)
            await callback.message.edit_text("Please enter the message you want to broadcast:")
        elif action == "settings":
            await callback.message.edit_text("Bot settings:", reply_markup=get_bot_settings_keyboard())
        await callback.answer()
    except Exception as e:
        logger.error(f"Error in admin callback: {e}")
        await callback.answer("An error occurred. Please try again.")

@router.message(AdminStates.waiting_for_broadcast)
async def process_broadcast(message: Message, state: FSMContext):
    await state.update_data(broadcast_message=message.text)
    await message.reply("Are you sure you want to send this broadcast?", 
                        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                            [InlineKeyboardButton(text="Yes", callback_data="confirm_broadcast"),
                             InlineKeyboardButton(text="No", callback_data="cancel_broadcast")]
                        ]))
    await state.set_state(AdminStates.confirming_broadcast)

@router.callback_query(F.data == "confirm_broadcast")
async def confirm_broadcast(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    broadcast_message = data.get('broadcast_message')
    success = await db.send_broadcast(broadcast_message)
    if success:
        await callback.message.edit_text("Broadcast sent successfully!")
    else:
        await callback.message.edit_text("Failed to send broadcast. Please try again.")
    await state.clear()

@router.callback_query(F.data == "cancel_broadcast")
async def cancel_broadcast(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Broadcast cancelled.")
    await state.clear()

async def send_broadcast(message: str, bot: Bot):
    users = await db.get_all_users()  # Implement this method to get all user IDs
    
    total_users = len(users)
    successful = 0
    failed = 0
    
    for user_id in users:
        try:
            await bot.send_message(
                user_id, 
                message, 
                reply_markup=get_broadcast_keyboard()
            )
            successful += 1
        except exceptions.TelegramAPIError:
            failed += 1
        
        # Update the admin about the progress every 10 messages
        if (successful + failed) % 10 == 0:
            await update_admin_on_progress(successful, failed, total_users)
    
    # Final update to admin
    await update_admin_on_progress(successful, failed, total_users, is_final=True)
    
    return successful, failed

# Usage in a handler
@router.message(Command("ads"))
async def show_ad_slots(message: types.Message):
    await message.answer("📢 Advertisement Slots:", reply_markup=get_ad_slots_keyboard())

# Handling button clicks
@router.callback_query(lambda c: c.data.startswith("ad_slot_"))
async def process_ad_slot(callback_query: types.CallbackQuery):
    slot_number = callback_query.data.split("_")[-1]
    await callback_query.answer(f"You selected Ad Slot {slot_number}")
    # Here you can add logic to manage the selected ad slot

@router.callback_query(lambda c: c.data == "ad_statistics")
async def show_ad_statistics(callback_query: types.CallbackQuery):
    await callback_query.answer("Showing Ad Statistics")
    # Implement logic to display ad statistics













async def update_admin_on_progress(successful, failed, total, is_final=False):
    admin_id = ADMIN_CHAT_IDS  # Replace with your admin's user ID
    status = "completed" if is_final else "in progress"
    message = f"Broadcast {status}:\n"
    message += f"Successful: {successful}\n"
    message += f"Failed: {failed}\n"
    message += f"Remaining: {total - (successful + failed)}"
    
    await bot.send_message(admin_id, message)















class UserSendMessageCD(CallbackData, prefix="user_send_message"):
    user_id: str

@router.callback_query(F.data == "admin_menu")
async def show_admin_menu(callback: CallbackQuery):
    await callback.message.edit_text("Welcome to the Admin Menu. Please select an option:", reply_markup=get_admin_keyboard())

@router.callback_query(F.data == "manage_guides")
async def manage_guides(callback: CallbackQuery):
    await callback.message.edit_text("Guide Management. Choose an action:", reply_markup=get_guide_management_keyboard())

@router.callback_query(F.data == "admin_create_guide")
async def create_guide(callback: CallbackQuery):
    await callback.message.edit_text("Select the format for your new guide:", reply_markup=get_guide_format_keyboard())

@router.callback_query(F.data.startswith("format_"))
async def set_guide_format(callback: CallbackQuery, state: FSMContext):
    format_type = callback.data.split("_")[1]
    await state.update_data(guide_format=format_type)
    await callback.message.edit_text(f"You've selected {format_type} format. Please enter your guide content:")
    await state.set_state(StorageFunctions.waiting_for_guide_content)

@router.message(StorageFunctions.waiting_for_guide_content)
async def receive_guide_content(message: Message, state: FSMContext):
    await state.update_data(guide_content=message.text)
    await message.answer("Guide content received. What would you like to do next?", reply_markup=get_submission_keyboard())

@router.callback_query(F.data == "submit_guide")
async def submit_guide(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    # Here you would typically save the guide to your database
    await callback.message.edit_text("Guide submitted successfully!", reply_markup=get_guide_management_keyboard())
    await state.clear()

@router.callback_query(F.data == "admin_broadcast")
async def broadcast_menu(callback: CallbackQuery):
    await callback.message.edit_text("Broadcast Menu. Choose an option:", reply_markup=get_broadcast_keyboard())


@router.callback_query(F.data == "bot_status")
async def bot_status(callback_query: CallbackQuery):
    current_bot_status = get_current_bot_status()
    await callback_query.message.edit_text(
        f"Current status of the bot: {current_bot_status}",
        reply_markup=BOT_STATUS_MARKUP()
    )

@router.callback_query(F.data == "set_bot_status_online")
async def set_bot_status_online(callback_query: CallbackQuery):
    await update_settings(status="True")
    await bot_status(callback_query)

@router.callback_query(F.data == "set_bot_status_offline")
async def set_bot_status_offline(callback_query: CallbackQuery):
    await update_settings(status="False")
    await bot_status(callback_query)

@router.callback_query(F.data == "refresh_bot_status")
async def refresh_bot_status(callback_query: CallbackQuery):
    await bot_status(callback_query)

@router.callback_query(F.data == "find_user_profile")
async def find_user_profile(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text(
        "Enter user ID (e.g., 123456789) or username (e.g., @example):",
        reply_markup=GO_BACK_TO_INLINE_ADMIN()
    )
    await state.set_state(StorageFunctions.here_search_profile)

@router.callback_query(F.data == "make_advertisement")
async def make_advertisement(callback_query: CallbackQuery, state: FSMContext):
    all_users_count = get_all_users_count()
    data = await state.get_data()
    txt = data.get('advertisement_text', 'No text provided')
    await callback_query.message.edit_text(
        f"Send advertisement to {all_users_count} users?\n\n«{txt}»",
        reply_markup=get_send_advertisement_only_text()
    )
    await state.set_state(StorageFunctions.approve_only_text)

@router.callback_query(F.data == "saot_yes_send_ad_photo_and_text", StorageFunctions.approve_only_text)
async def sends_ad_only_text(call: CallbackQuery, state: FSMContext):
    users_getted, users_failed = await send_advertisement(state)
    await call.message.edit_text(
        f"Advertisement sent:\n\n"
        f"✅ Received by: {users_getted} users\n"
        f"❌ Failed to receive: {users_failed} users",
        reply_markup=CLOSE_BTN()
    )
    await state.clear()

@router.callback_query(F.data == "advertisement_photo_and_text")
async def advertisement_photo_and_text(callback_query: CallbackQuery, state: FSMContext):
    all_users_count = get_all_users_count()
    data = await state.get_data()
    txt = data.get('advertisement_text', 'No text provided')
    await callback_query.message.edit_text(
        f"Send advertisement with photo to {all_users_count} users?\n\n«{txt}»",
        reply_markup=get_send_advertisement_photo_and_text()
    )
    await state.set_state(StorageFunctions.approve)

@router.message(F.chat.type == ChatType.PRIVATE, IsAdmin())
async def get_data_for_search_profile(message: Message, state: FSMContext):
    get_user_data = message.text.strip()
    get_user_id = None

    if get_user_data.isdigit():
        get_user_id = get_userx(user_id=get_user_data)
    elif get_user_data.startswith('@'):
        get_user_id = get_userx(user_login=get_user_data[1:].lower())

    if get_user_id:
        await message.delete()
        user_profile = await search_user_profile(get_user_id[1])
        await message.answer(user_profile, reply_markup=await search_profile_func(get_user_id[1]))
        await state.clear()
    else:
        await message.delete()
        await message.answer(
            f"User with ID/username '{get_user_data}' was not found.\n"
            "Please enter a valid user ID (e.g., 123456789) or username (e.g., @example):",
            reply_markup=CLOSE_BTN()
        )

@router.callback_query(UserSendMessageCD.filter())
async def send_user_to_message(call: CallbackQuery, callback_data: UserSendMessageCD, state: FSMContext):
    await state.update_data(here_cache_user_id=callback_data.user_id)
    await call.message.delete()
    await call.message.answer(
        "Enter the message you want to send to the user:",
        reply_markup=CLOSE_BTN()
    )
    await state.set_state(StorageFunctions.here_send_message)















@router.callback_query(F.data == "admin_manage_guides")
async def admin_manage_guides(callback: CallbackQuery):
    # Fetch the number of guides for each category
    email_access_guides = db.get_guide_count_by_category("Email Access")
    direct_access_guides = db.get_guide_count_by_category("Direct Access")
    pm_on_file_guides = db.get_guide_count_by_category("PM On File")
    net30_guides = db.get_guide_count_by_category("Net-30")
    avs_enforced_guides = db.get_guide_count_by_category("AVS Enforced")
    an_rn_guides = db.get_guide_count_by_category("AN/RN Accepted")
    two_d_guides = db.get_guide_count_by_category("2D")
    three_d_guides = db.get_guide_count_by_category("3D")
    bank_specific_guides = db.get_guide_count_by_category("Bank Specific")

    message_text = f"""
📚 Guide Management Panel

🔰 Email Access Targets ({email_access_guides})
➡️ Direct Access Targets ({direct_access_guides})
💳 PM On File Targets ({pm_on_file_guides})
👨‍🏭 Net-30 Sites ({net30_guides})
🏠 AVS Enforced Sites ({avs_enforced_guides})
🏦 An/RN Accepted ({an_rn_guides})
🫥 2D ({two_d_guides})
💸 3D ({three_d_guides})
🏦 Bank Specific Guides ({bank_specific_guides})

What would you like to do with the guides?
"""
    await callback.message.edit_text(message_text, reply_markup=get_guide_management_keyboard())

@router.callback_query(F.data == "admin_create_guide")
async def admin_create_guide(callback: CallbackQuery):
    try:
        # Fetch guide counts for each category from the database
        categories = [
            "Food & Groceries", "Clothing & Fashion", "Electronics", 
            "Books & Media", "Home & Garden", "Beauty & Personal Care",
            "Toys & Games", "Sports & Fitness", "3D Printing", 
            "Tools & Home Improvement", "Automotive", "Health & Wellness",
            "Pet Supplies", "Baby & Kids", "Arts & Crafts", 
            "Musical Instruments", "Travel & Luggage", 
            "Gifts & Special Occasions"
        ]
        
        counts = [db.get_guide_count_by_category(category) for category in categories]
        
        # Create a message with categories and their respective counts
        message_text = "\n".join(
            [f"{emoji} {category} ({count})" for emoji, category, count in zip(
                ["🍔", "👚", "🖥️", "📚", "🏠", "💄", 
                 "🎮", "🏋️", "🖨️", "🛠️", "🚗", 
                 "💊", "🐶", "👶", "🎨", "🎵", 
                 "🧳", "🎁"], categories, counts)]
        )
        
        await callback.message.edit_text(f"📚 Select a category to create a new guide:\n\n{message_text}", reply_markup=get_ordering_categories_keyboard())
    except Exception as e:
        logger.error(f"Error in creating guide: {e}")
        await callback.answer("An error occurred while fetching categories. Please try again.", show_alert=True)


@router.callback_query(F.data.startswith("guide_submission_"))
async def admin_guide_handle_selected_category(callback: CallbackQuery, state: FSMContext):
    category_selected = callback.data.split("_")[1]
    
    confirmation_message = await callback.message.edit_text(
        f"You have chosen to create:"
        "Guide for: <b>{category_selected.replace('_', ' ').title()}</b>.\n\n"

        "URL: [To be filled]\n"
        "Payment Used: [To be filled]\n"
        "Delivery Time: [To be filled]\n"
        "AVS: [To be filled]\n"
        "Misc Info: [To be filled]\n"
        "\nPlease choose an option for submission:",
        parse_mode="HTML"
    )
    
    await state.update_data(category=category_selected, original_message_id=confirmation_message.message_id)
    await callback.message.answer("Pick an Option for Submission:", reply_markup=get_guide_submission_keyboard())

@router.callback_query(F.data.in_(["submit_url", "submit_payment", "submit_avs", "submit_description"]))
async def handle_submit(callback: CallbackQuery, state: FSMContext):
    field_map = {
        "submit_url": ("waiting_for_url", "Please enter the URL for the guide:"),
        "submit_payment": ("waiting_for_payment", "Please enter the payment method used:"),
        "submit_avs": ("waiting_for_avs", "Please enter the AVS (Address Verification System) information:"),
        "submit_description": ("waiting_for_description", "Please enter a description or any miscellaneous information:")
    }
    state_to_set, prompt = field_map[callback.data]
    await state.set_state(state_to_set)
    await callback.message.answer(prompt)

@router.message(lambda message: message.text)
async def handle_user_input(message: Message, state: FSMContext):
    current_state = await state.get_state()
    data = await state.get_data()
    
    field_map = {
        "waiting_for_url": "url",
        "waiting_for_payment": "payment",
        "waiting_for_avs": "avs",
        "waiting_for_description": "description"
    }
    
    if current_state in field_map:
        data[field_map[current_state]] = message.text
    
    await state.update_data(data)
    
    all_fields = ["url", "payment", "avs", "description"]
    all_filled = all(data.get(field) for field in all_fields)
    
    updated_text = (
        f"Guide for: <b>{data.get('category', 'Unknown').replace('_', ' ').title()}</b>\n\n"
        f"URL: {data.get('url', '[To be filled]')}\n"
        f"Payment Used: {data.get('payment', '[To be filled]')}\n"
        f"AVS: {data.get('avs', '[To be filled]')}\n"
        f"Misc Info: {data.get('description', '[To be filled]')}\n\n"
        "What would you like to submit next?"
    )
    
    try:
        await message.bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=data.get('original_message_id'),
            text=updated_text,
            reply_markup=get_guide_submission_keyboard(all_filled),
            parse_mode="HTML"
        )
    except Exception as e:
        print(f"Error editing message: {e}")
        # You might want to send a new message here if editing fails
    
    await state.set_state(None)

@router.callback_query(F.data == "admin_publish_guide")
async def admin_finish_guide(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    # Here you would typically save the guide data to your database
    await callback.message.answer("Guide has been saved successfully!")
    await state.clear()


@router.callback_query(F.data == "bot_settings")
async def bot_settings(callback: CallbackQuery):
    await callback.message.edit_text("Bot Settings. Choose an option:", reply_markup=get_bot_settings_keyboard())

@router.callback_query(F.data == "toggle_startup_message")
async def toggle_startup_message(callback: CallbackQuery):
    try:
        current_status = await db.get_startup_message_status()
        new_status = not current_status
        success = await db.set_startup_message_status(new_status)
        if success:
            await callback.message.edit_reply_markup(reply_markup=get_bot_settings_keyboard())
            await callback.answer(f"Startup message {'enabled' if new_status else 'disabled'}.")
        else:
            await callback.answer("Failed to change setting. Please try again.")
    except Exception as e:
        logger.error(f"Error toggling startup message: {e}")
        await callback.answer("An error occurred. Please try again.")

@router.callback_query(F.data == "ban_user")
async def ban_user_menu(callback: CallbackQuery, state: FSMContext):
    message_text = "🚫 Ban User\n\nEnter the user ID to ban:"
    await callback.message.edit_text(message_text)
    await state.set_state(AdminStates.waiting_for_ban_user_id)

@router.message(AdminStates.waiting_for_ban_user_id)
async def process_ban_user(message: Message, state: FSMContext):
    try:
        user_id = int(message.text)
        success = await db.ban_user(user_id)
        if success:
            await message.reply(f"User {user_id} has been banned.")
        else:
            await message.reply("Failed to ban user. Please check the user ID and try again.")
    except ValueError:
        await message.reply("Invalid user ID. Please enter a valid number.")
    except Exception as e:
        logger.error(f"Error banning user: {e}")
        await message.reply("An error occurred while banning the user.")
    finally:
        await state.clear()
        await message.answer("Admin Menu:", reply_markup=get_admin_keyboard())

@router.callback_query(F.data == "upgrade_membership")
async def upgrade_membership_menu(callback: CallbackQuery, state: FSMContext):
    message_text = "⬆️ Upgrade Membership\n\nEnter the user ID to upgrade membership:"
    await callback.message.edit_text(message_text)
    await state.set_state(AdminStates.waiting_for_upgrade_user_id)

@router.message(AdminStates.waiting_for_upgrade_user_id)
async def process_upgrade_membership(message: Message, state: FSMContext):
    try:
        user_id = int(message.text)
        success = await db.upgrade_user_membership(user_id)
        if success:
            await message.reply(f"User {user_id} membership has been upgraded.")
        else:
            await message.reply("Failed to upgrade membership. Please check the user ID and try again.")
    except ValueError:
        await message.reply("Invalid user ID. Please enter a valid number.")
    except Exception as e:
        logger.error(f"Error upgrading membership: {e}")
        await message.reply("An error occurred while upgrading the membership.")
    finally:
        await state.clear()
        await message.answer("Admin Menu:", reply_markup=get_admin_keyboard())

@router.callback_query(F.data == "update_ticket_status")
async def handle_update_ticket_status(callback: CallbackQuery):
    await callback.message.answer("Please enter the Ticket ID you want to update:")
    await state.set_state(GuideStates.waiting_for_ticket_id)  # Assuming you have this state defined

@router.callback_query(F.data == "manage_users")
async def manage_users(callback: CallbackQuery):
    keyboard = get_user_management_keyboard()
    await callback.message.answer("User Management Options:", reply_markup=keyboard)

@router.callback_query(F.data == "admin_broadcast")
async def admin_broadcast(callback: CallbackQuery):
    keyboard = get_broadcast_keyboard()
    await callback.message.answer("Broadcast Options:", reply_markup=keyboard)


@router.callback_query(F.data == "back_to_admin")
async def back_to_admin(callback: CallbackQuery):
    await callback.message.edit_text("Admin Panel:", reply_markup=get_admin_keyboard())
    
    
    
@router.callback_query(F.data == 'view_all_tickets')
async def view_all_tickets(callback_query: types.CallbackQuery):
    # Here you would typically fetch all tickets from your database
    # all_tickets = db_manager.get_all_tickets()

    # Mock response for demonstration
    all_tickets = ["Ticket 1: Issue with login - Status: open", 
                   "Ticket 2: Payment problem - Status: resolved"]

    if not all_tickets:
        await callback_query.answer("No tickets available.")
        return

    response = "All Tickets:\n" + "\n".join(all_tickets)
    
    await callback_query.answer()
    await callback_query.message.edit_text(response)

@router.callback_query(F.data == 'update_ticket_status')
async def update_ticket_status(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_text("Please provide the ticket ID and new status (e.g., '1 resolved'):")
    await TicketStates.WAITING_FOR_STATUS_UPDATE.set()  # Set state to wait for status update

@router.message(F.state == TicketStates.WAITING_FOR_STATUS_UPDATE)
async def process_status_update(message: types.Message, state: FSMContext):
    try:
        ticket_id, new_status = message.text.split()  # Expecting input like "1 resolved"
        
        # Here you would typically update the ticket status in your database
        # db_manager.update_ticket_status(ticket_id=int(ticket_id), new_status=new_status)

        await message.answer(f"Ticket ID {ticket_id} updated successfully to '{new_status}'.")
        
    except ValueError:
        await message.answer("Invalid format. Please use 'ticket_id new_status'.")
    
    await state.finish()  # Reset state

@router.callback_query(F.data == 'delete_ticket')
async def delete_ticket(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_text("Please provide the ticket ID to delete:")
    
@router.message(F.text.isdigit() & F.state('*'))  # Handle number inputs globally
async def process_delete_ticket(message: types.Message, state: FSMContext):
    ticket_id = int(message.text)

    # Here you would typically delete the ticket from your database
    # db_manager.delete_ticket(ticket_id=ticket_id)

    await message.answer(f"Ticket ID {ticket_id} deleted successfully.")

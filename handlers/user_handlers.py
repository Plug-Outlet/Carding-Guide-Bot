from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
import logging
from utils.database import db
from config import ADMIN_USER_IDS  # Add this to your config.py file
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
import html
from keyboards.user_keyboard import get_pagination_keyboard
from config import help_pages

router = Router()
# Start with page 0
current_page = 0

class TicketStates:
    WAITING_FOR_TICKET_DETAILS = "waiting_for_ticket_details"
    WAITING_FOR_STATUS_UPDATE = "waiting_for_status_update"





@router.message(Command("profile"))
async def show_profile(message: Message):
    user_id = message.from_user.id
    user_data = db.get_user(user_id)
    
    if user_data:
        user_id, username, membership_level, first_seen, last_active = user_data
        
        # Determine membership emoji
        membership_emoji = "🌟" if membership_level.lower() == "premium" else "👤"
        
        profile_text = (
            f"<b>👤 User Profile:</b>\n\n"
            f"🆔 <b>ID:</b> <code>{user_id}</code>\n"
            f"👤 <b>Username:</b> <code>{username}</code>\n"
            f"{membership_emoji} <b>Membership:</b> <code>{membership_level}</code>\n"
            f"🕒 <b>First seen:</b> <code>{first_seen}</code>\n"
            f"🔄 <b>Last active:</b> <code>{last_active}</code>"
        )
        await message.reply(profile_text, parse_mode="HTML")
    else:
        await message.reply("❌ User profile not found.")

@router.message(Command("upgrade"))
async def upgrade_membership(message: Message, state: FSMContext):
    # This is a placeholder for membership upgrade logic
    # You would typically implement payment processing here
    user_id = message.from_user.id
    
    # For demonstration, we'll just upgrade the user to 'premium'
    db.cur.execute("UPDATE users SET membership_level = 'premium' WHERE user_id = ?", (user_id,))
    db.conn.commit()
    
    await message.reply("Congratulations! Your membership has been upgraded to premium.")

@router.message(Command("help"))
async def show_help(message: Message):
    help_text = (
        "🤖 Bot Commands:\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/profile - View your user profile\n"
        "/upgrade - Upgrade your membership\n"
        "🔍 Checker Menu - Access the checker menu\n"
        "🏦 BIN Check - Check a BIN number"
    )
    await message.reply(help_text)



############### Admin Notices ###################
async def notify_admin(bot: Bot, user_id: int, username: str, timestamp: str):
    # Create a link to the user's profile
    user_link = f'<a href="tg://user?id={user_id}">{html.escape(username)}</a>'
    
    admin_message = (
        f"🆕 <b>New User Registered!</b>\n\n"
        f"👤 <b>User:</b> {user_link}\n"
        f"🆔 <b>User ID:</b> <code>{user_id}</code>\n"
        f"🕒 <b>Joined:</b> <code>{html.escape(timestamp)}</code>\n"
        f"🎫 <b>Membership:</b> <i>guest</i>"
    )
    
    # Create inline keyboard
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="👋 Greet User", callback_data=f"greet_user:{user_id}"),
            InlineKeyboardButton(text="🚫 Ban User", callback_data=f"ban_user:{user_id}")
        ],
        [InlineKeyboardButton(text="❌ Cancel", callback_data="cancel")]
    ])
    
    try:
        await bot.send_message(ADMIN_USER_IDS, admin_message, parse_mode=ParseMode.HTML, reply_markup=keyboard)
        logging.info(f"Admin notification sent for new user {user_id}")
    except Exception as e:
        logging.error(f"Failed to send admin notification: {e}")









    
@router.message()
async def log_user(message: Message, bot: Bot):
    user_id = message.from_user.id
    username = message.from_user.username or "Unknown"
    
    try:
        is_new_user, timestamp = db.register_user(user_id, username)
        db.update_user_activity(user_id)
        
        if is_new_user:
            logging.info(f"New user registered: User ID: {user_id}, Username: {username}")
            await notify_admin(bot, user_id, username, timestamp)
        else:
            logging.info(f"Message from existing User ID: {user_id}, Username: {username}")
    except Exception as e:
        logging.error(f"Error in log_user: {e}")

@router.callback_query(F.data.startswith("greet_user:"))
async def greet_user(callback_query: CallbackQuery):
    user_id = int(callback_query.data.split(":")[1])
    await callback_query.bot.send_message(user_id, "Welcome to our bot! We're glad to have you here.")
    await callback_query.answer("User greeted successfully!")

@router.callback_query(F.data.startswith("ban_user:"))
async def ban_user(callback_query: CallbackQuery):
    user_id = int(callback_query.data.split(":")[1])
    # Implement your ban logic here
    await callback_query.answer("User banned successfully!")

@router.callback_query(F.data == "cancel")
async def cancel_action(callback_query: CallbackQuery):
    await callback_query.answer("Action cancelled.")
    await callback_query.bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)



__all__ = ["router", "notify_admin"]


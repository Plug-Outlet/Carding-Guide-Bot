import asyncio
import logging
from typing import Any, Dict
from aiogram import Bot, Dispatcher, F, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery, BotCommand
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import BOT_TOKEN, ADMIN_USER_IDS
from utils.database import Database
from keyboards.user_keyboard import get_main_user_keyboard
from utils.states import BotStates
from handlers.ticket_handlers import *
from handlers.bin_handlers import *
from handlers.admin_handlers import *
from handlers.user_managment_handler import *
from handlers.membership_handler import *

from keyboards.ticket_keyboard import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

db = Database('bot_database.db')

bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

storage = MemoryStorage()
dp = Dispatcher(storage=storage)

router = Router()

async def send_startup_message(bot: Bot):
    if not db.get_startup_message_status():
        logger.info("Startup message is disabled. Skipping...")
        return

    user_count = db.get_user_count()
    premium_count = db.get_premium_user_count()
    guide_count = db.get_guide_count()

    users = db.get_all_users()
    for user in users:
        user_id = user['user_id']
        user_data = db.get_user(user_id)
        
        if user_data:
            _, username, membership_level, first_seen, last_active = user_data
            
            # Determine membership emoji
            membership_emoji = "🌟" if membership_level.lower() == "premium" else "👤"

            startup_message = f"""
🎉 <b>Carding Empire Bot is Online!</b> 🎉

📊 <b>Current Stats:</b>
• <b>Total Users</b>: <code>{user_count}</code>
• <b>Premium Members</b>: <code>{premium_count}</code>
• <b>Available Guides</b>: <code>{guide_count}</code>

👤 <b>Your Profile:</b>
{membership_emoji} <b>Membership:</b> <code>{membership_level}</code>
🕒 <b>First seen:</b> <code>{first_seen}</code>
🔄 <b>Last active:</b> <code>{last_active}</code>

Welcome back, <b>{username}</b>! Choose an option below to get started:
"""

            keyboard = get_main_user_keyboard(user_id)

            try:
                await bot.send_message(
                    chat_id=user_id, 
                    text=startup_message, 
                    reply_markup=keyboard,
                    parse_mode="HTML"
                )
                await asyncio.sleep(0.05)  # Small delay to avoid hitting rate limits
            except Exception as e:
                logger.error(f"Failed to send startup message to user {user_id}: {e}")
        else:
            logger.error(f"User data not found for user_id: {user_id}")

async def on_startup(dispatcher: Dispatcher, bot: Bot):
    logger.info("Bot is starting up...")
    
    # Set bot commands
    await bot.set_my_commands([
        BotCommand(command="start", description="Start the bot"),
        BotCommand(command="help", description="Get help"),
        BotCommand(command="menu", description="Show main menu"),
        BotCommand(command="admin", description="Admin panel (for admins only)")
    ])

    # Send startup message to all users
    await send_startup_message(bot)

    logger.info("Startup complete.")
# - Developed by https://t.me/Doomsday_X_Productions @ https://github.com/Plug-Outlet/Carding-Guide-Bot/discussions
async def on_shutdown(dispatcher: Dispatcher, bot: Bot):
    logger.info("Bot is shutting down...")
    await bot.session.close()
    db.close()

async def main() -> None:
    # Import routers
    from handlers.main_menu import router as main_menu_router
    from handlers.user_handlers import router as user_router
    from handlers.admin_handlers import router as admin_router
    from handlers.bin_handlers import router as bin_router
    from handlers.cards_handlers import router as cards_router
    from handlers.guide_handlers import router as guide_router
    from handlers.membership_handler import router as membership_router
    from handlers.ticket_handlers import router as ticket_router
    # Include routers
    dp.include_router(main_menu_router)
    dp.include_router(user_router)
    dp.include_router(admin_router)
    dp.include_router(bin_router)
    dp.include_router(cards_router)
    dp.include_router(guide_router)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.include_router(membership_router)
    dp.include_router(ticket_router)

    try:
        logger.info("Starting bot...")
        await dp.start_polling(bot)
    finally:
        logger.info("Bot has stopped.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped!")
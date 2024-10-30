import logging
from aiogram import Bot, Dispatcher, F, Router
import aiohttp
import asyncio
import os
from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from collections import Counter
import requests
import logging
from aiogram.exceptions import TelegramUnauthorizedError
from utils.database import Database  # Ensure you have your Database utility imported
from keyboards.admin_keyboard import *
# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Assuming you have a database instance
db = Database('bot_database.db')  # Replace with your actual database path



router = Router()
@router.message(Command("view_users"))
async def handle_view_users(message: Message):
    await view_users(message)


async def view_users(message: Message):
    """
    Retrieves and displays a list of all users in the database.
    """
    try:
        users = db.get_all_users()  # Assuming this method retrieves all user records
        if not users:
            await message.reply("❌ No users found.")
            return
        
        user_list = "\n".join([f"🆔 {user['user_id']} - {user['username']}" for user in users])
        await message.reply(f"👥 List of Users:\n{user_list}")
    except Exception as e:
        logger.error(f"Error retrieving users: {e}")
        await message.reply("❌ An error occurred while retrieving the user list.")

async def search_user(message: Message):
    """
    Prompts the admin to enter a username or user ID to search for.
    """
    await message.reply("🔍 Please enter the username or user ID of the user you want to search for:")

async def promote_user(callback_query: CallbackQuery):
    """
    Promotes a user to a higher membership level.
    """
    try:
        user_id = int(callback_query.data.split(":")[1])  # Extract user ID from callback data
        db.promote_user(user_id)  # Assuming this method updates the user's membership level
        await callback_query.answer("✅ User promoted successfully!")
    except Exception as e:
        logger.error(f"Error promoting user {user_id}: {e}")
        await callback_query.answer("❌ An error occurred while promoting the user.")

async def remove_user(callback_query: CallbackQuery):
    """
    Removes a user from the database.
    """
    try:
        user_id = int(callback_query.data.split(":")[1])  # Extract user ID from callback data
        db.remove_user(user_id)  # Assuming this method deletes the user record from the database
        await callback_query.answer("🚫 User removed successfully!")
    except Exception as e:
        logger.error(f"Error removing user {user_id}: {e}")
        await callback_query.answer("❌ An error occurred while removing the user.")

async def user_statistics(message: Message):
    """
    Displays statistics about users, such as total count, premium members, etc.
    """
    try:
        total_users = db.get_user_count()  # Assuming this method returns the total number of users
        premium_users = db.get_premium_user_count()  # Assuming this method returns the count of premium users

        stats_message = (
            f"📊 <b>User Statistics:</b>\n"
            f"• Total Users: <code>{total_users}</code>\n"
            f"• Premium Members: <code>{premium_users}</code>"
        )
        
        await message.reply(stats_message, parse_mode="HTML")
    except Exception as e:
        logger.error(f"Error retrieving user statistics: {e}")
        await message.reply("❌ An error occurred while retrieving statistics.")
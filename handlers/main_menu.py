# handlers/main_menu.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hcode
import aiosqlite
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hcode
import os
from datetime import datetime
import logging
from aiogram.filters import Command
from utils.database import db, Database
from utils.admin_utils import is_admin
from .bin_handlers import router as bin_router
from keyboards.guides_keyboard import *
from keyboards.user_keyboard import get_main_user_keyboard, get_profile_membership_keyboard, get_pagination_keyboard
from keyboards.cards_keyboard import get_cards_menu_keyboard, get_card_checker_menu_keyboard, get_card_result_keyboard
from keyboards.ticket_keyboard import *
from aiogram.fsm.context import FSMContext
from aiogram import types
from utils.admin_utils import is_admin
from utils.states import BankCheckStates
import asyncio
import sqlite3
from config import help_pages




current_directory = os.getcwd()
router = Router()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
current_page = 0
current_dir = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(current_directory, "data", "database.db")



@router.message(Command("start", "menu"))
async def send_welcome(message: Message):
    user_id = message.from_user.id  # Retrieve user ID from the message
    user_count = db.get_user_count()
    premium_count = db.get_premium_user_count()
    guide_count = db.get_guide_count()
    user_is_admin = is_admin(user_id)  # Use the imported is_admin function

    welcome_text = f"""
Welcome to the main menu!

Here are some key features:
• <b>💳 Card Checking</b>: Validate and get info on credit cards
• <b>🏦 BIN Lookup</b>: Get details on Bank Identification Numbers
• <b>📚 Guides</b>: Access helpful guides on various topics
• <b>👤 User Profile</b>: Check your status and membership

To navigate, use the command buttons or the inline keyboards that appear with messages.

📊 Current Stats:
• <b>Total Users</b>: <code>{user_count}</code>
• <b>Premium Members</b>: <code>{premium_count}</code>
• <b>Available Guides</b>: <code>{guide_count}</code>

If you have any questions, feel free to ask! Enjoy using the bot. 😊
"""

    keyboard = get_main_user_keyboard(user_id)  # Pass user_id here
    
    if user_is_admin:
        admin_button = InlineKeyboardButton(text="🔐 Admin Menu", callback_data="admin_menu")
        keyboard.inline_keyboard.append([admin_button])

    await message.reply(welcome_text, reply_markup=keyboard)

@router.callback_query(lambda c: c.data == "admin_menu")
async def admin_menu(callback_query: CallbackQuery):
    if not is_admin(callback_query.from_user.id):
        await callback_query.answer("You don't have permission to access the admin menu.", show_alert=True)
        return

    admin_welcome_text = """
Welcome to the Admin Menu!

Here you can manage various aspects of the bot:
• 👥 User Management
• 📢 Broadcast messages
• 📚 Guide Management
• ⚙️ Bot Settings
• 📊 View Statistics

Use the buttons below to navigate through admin functions.
"""
    await callback_query.message.edit_text(admin_welcome_text, reply_markup=get_admin_keyboard())

@router.callback_query(F.data == "checker_menu")
async def checker_menu(callback_query: CallbackQuery):
    await callback_query.answer("Opening Checker Menu...")
    
    # Pause for 1 second
    await asyncio.sleep(1)
    
    checker_menu_text = """
🔍 Checker Menu

Here are the available card checking functions:

💳 <b>Check Card:</b> Validate information about a specific credit card.
🏦 <b>Bank Check:</b> Get detailed information about a card's issuing bank.
🔢 <b>BIN Check:</b> Retrieve information based on the Bank Identification Number.
💰 <b>Balance Check:</b> Check the balance of a card (Note: This may be limited due to security reasons).
📊 <b>Card Stats:</b> View statistics about card checks performed.

Please select a function from the menu below:
"""
    
    await callback_query.message.edit_text(
        text=checker_menu_text,
        reply_markup=get_cards_menu_keyboard()
    )

# Add handlers for each checker menu option
@router.callback_query(F.data == "check_card")
async def check_card_start(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer("Opening Card Check...")
    
    # Pause for 1 second
    await asyncio.sleep(1)
    
    greeting_text = """
💳 <b>Card Check</b>

Welcome to the Card Check feature! Here you can validate and get information about credit cards.

Please select a format to enter the card information:

1️⃣ <code>CC|MM|YY|CVV</code>
2️⃣ <code>CC|M|YYYY|CVV</code>
3️⃣ <code>CC|MM|YYYY|CVV</code>

Where:
• CC: Card number (13-19 digits)
• MM: Month (01-12)
• YY: Year (last two digits)
• YYYY: Full year
• CVV: Card Verification Value (3-4 digits)

Select a format or choose an option below:
"""

    await callback_query.message.edit_text(
        text=greeting_text,
        reply_markup=get_card_checker_menu_keyboard(),
        parse_mode="HTML"
    )


    
@router.callback_query(F.data == "balance_check")
async def balance_check(callback_query: CallbackQuery):
    await callback_query.answer("Opening IVR Balance Check...")
    
    await asyncio.sleep(1)
    
    balance_check_text = """
💰 <b>IVR Balance Check</b>

Welcome to the IVR Balance Check feature! 
IVR stands for Interactive Voice Response, a technology that allows a computer to interact with humans through voice and DTMF tones input via keypad.

How does it work?

1️⃣ <b>Card Entry:</b> You'll enter the full card number, just like you would on a phone keypad during a real IVR call.

2️⃣ <b>Card Verification:</b> Our system will simulate checking the card details and provide information about the bank, card type, and card level.

3️⃣ <b>Additional Verification:</b> To mimic real-world security measures, we'll ask for one of three verification methods:
   • Last Four of SSN
   • ZIP Code
   • ATM PIN

4️⃣ <b>Balance Simulation:</b> After verification, we'll display a simulated balance, available credit, and recent transaction.

This process mirrors actual IVR systems used by banks, allowing you to understand the flow of information and security checks involved in balance inquiries.

⚠️ <b>Important Notice:</b>
This feature is for educational purposes only. It simulates the IVR experience but does not connect to any real financial systems or provide actual account information.

Ready to start? Enter the card number to begin the simulation:
"""

    await callback_query.message.edit_text(
        text=balance_check_text,
        parse_mode="HTML"
    )
    
    # Set the state to wait for card number input
    await state.set_state("waiting_for_card_number")

@router.callback_query(F.data == "card_stats")
async def card_stats(callback_query: CallbackQuery):
    await callback_query.answer("Opening Card Stats...")
    
    await asyncio.sleep(1)
    
    card_stats_text = """
📊 <b>Card Stats</b>

Welcome to the Card Stats feature! Here's an overview of your card checking activity:

🔢 Total checks: <code>42</code>
✅ Valid cards: <code>38</code>
❌ Invalid cards: <code>4</code>
🏆 Success rate: <code>90.48%</code>

Top card types checked:
1. 💳 Visa: <code>45%</code>
2. 💳 Mastercard: <code>30%</code>
3. 💳 American Express: <code>15%</code>
4. 💳 Others: <code>10%</code>

Want to improve your stats? Check out our guides for tips on card checking best practices!
"""

    await callback_query.message.edit_text(
        text=card_stats_text,
        parse_mode="HTML"
    )

@router.callback_query(F.data == "back_to_main")
async def back_to_main_menu(callback_query: CallbackQuery):
    await callback_query.answer("Returning to main menu...")

    user_id = callback_query.from_user.id  # Get the user ID from the callback query

    await asyncio.sleep(1)
    
    main_menu_text = """
🏠 <b>Main Menu</b>

Welcome back to the main menu! What would you like to do?

💳 <b>Check Card:</b> Validate and get info on credit cards  
🏦 <b>Bank Check:</b> Get details on card issuers  
💰 <b>Balance Check:</b> New IVR AutoCalling Balance Checking  
📊 <b>Card Stats:</b> View your card checking statistics  
📚 <b>Guides:</b> Access helpful tutorials and tips  
❓ <b>Help:</b> Get assistance with using the bot  
👤 <b>Profile:</b> View and manage your account  

Select an option to get started!
"""

    await callback_query.message.edit_text(
        text=main_menu_text,
        reply_markup=get_main_user_keyboard(user_id),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "guides")
async def guides(callback_query: CallbackQuery):
    await callback_query.answer("Opening Guides...")
    
    await asyncio.sleep(1)
    
    guides_text = """
             📚 <b>Guides</b>

                Welcome to the Heart and Main purpose of this bot.
            Detailed, Comprehensive - Step-by-Step Ordering Guides
                        With 100% Sure Deliveries!!
               Inside of this function you can discover various
                     types of guides broken down as such:
            ------------------------ ------------------------
                 We have a total of:
            {Number of guide_types}: Various Types
            {Number of guide_catagories}: Various Catagories
            {Number of guide_targets}: Various Targets
            {Number of types}: Various Methods
            
                        A Grand Total of:
                    {Total Number of Guides}
                    
                    Most Recent Submission:
                {Catagory Type} - On {Submission Date} 


                                Total Feedback:
                {Number of Still Working Rates} Users with Postive Responses
                {Number of Compaints} Users Reported Not Working/Failed
            ------------------------- ------------------------

"""

    await callback_query.message.edit_text(
        text=guides_text,
        reply_markup=get_guides_main_keyboard(),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "back_to_guides_menu")
async def back_to_guides_menu(callback: CallbackQuery):
    await callback.answer("Returning to Guides Menu...")
    try:
        await callback.message.edit_text(
            "Welcome to the Guides Menu",
            reply_markup=get_guides_main_keyboard()
        )
    except TelegramBadRequest as e:
        if "message is not modified" in str(e).lower():
            pass  # Ignore this error as the message content didn't change
        else:
            print(f"TelegramBadRequest in back_to_guides_menu: {e}")
    except Exception as e:
        print(f"Error in back_to_guides_menu function: {e}")
        await callback.message.answer("An error occurred. Please try again later.")


@router.callback_query(F.data == "help")
async def help_command(callback_query: CallbackQuery):
    global current_page
    await callback_query.answer("Opening Help...")
    
    await asyncio.sleep(1)
    
    help_text = help_pages[current_page]
    
    # Create navigation buttons
    keyboard = types.InlineKeyboardMarkup()
    
    if current_page > 0:
        keyboard.add(types.InlineKeyboardButton("⏮️ Previous", callback_data="help_previous"))
    
    if current_page < len(help_pages) - 1:
        keyboard.add(types.InlineKeyboardButton("⏭️ Next", callback_data="help_next"))
    
    await callback_query.message.edit_text(
        text=help_text,
        parse_mode="HTML",
        reply_markup=keyboard
    )


@router.callback_query(F.data == "help_next")
async def help_next(callback_query: CallbackQuery):
    global current_page
    if current_page < len(help_pages) - 1:
        current_page += 1
        await help_command(callback_query)

@router.callback_query(F.data == "help_previous")
async def help_previous(callback_query: CallbackQuery):
    global current_page
    if current_page > 0:
        current_page -= 1
        await help_command(callback_query)

@router.callback_query(F.data == "profile")
async def get_user_profile(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    db = Database()  # This should create or get the existing instance

    try:
        # Check if the users table exists
        if not db.table_exists('users'):
            db.create_users_table()
            logger.warning("Users table did not exist and was created.")

        # Fetch user data
        db.cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        user = db.cur.fetchone()

        if not user:

            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            db.cur.execute("""
                INSERT INTO users (user_id, username, membership_level, first_seen, last_active) 
                VALUES (?, ?, 'guest', ?, ?)
            """, (user_id, callback_query.from_user.username, current_time, current_time))
            db.conn.commit()
            db.cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            user = db.cur.fetchone()

        # Update last_active
        db.cur.execute("UPDATE users SET last_active = ? WHERE user_id = ?", 
                       (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user_id))
        db.conn.commit()

        # Format user data
        user_id, username, membership_level, first_seen, last_active = user

        user_profile_text = f"""
👤 <b>User Profile</b>

Here's your current profile information:

🆔 <b>User ID:</b> {hcode(str(user_id))}
👤 <b>Username:</b> {hcode(username or 'Not set')}
🌟 <b>Membership Level:</b> {hcode(membership_level)}
📅 <b>First Seen:</b> {hcode(first_seen[:10])}
🕒 <b>Last Active:</b> {hcode(last_active[:10])}

Use the buttons below to manage your profile and membership:
"""
        # Get the profile membership keyboard
        keyboard = get_profile_membership_keyboard()

        await callback_query.message.edit_text(
            text=user_profile_text,
            reply_markup=keyboard,
            parse_mode="HTML"
        )

    except Exception as e:
        error_message = f"Unexpected error in get_user_profile: {str(e)}"
        logger.error(error_message)
        await callback_query.answer("An unexpected error occurred. Please try again later.")

@router.message(Command("profile"))
async def show_profile(message: types.Message):
    user_id = message.from_user.id
    profile_text = await get_user_profile(user_id)
    await message.answer(profile_text, parse_mode="HTML")

@router.callback_query(F.data == "profile")
async def profile_callback(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    profile_text = await get_user_profile(user_id)
    await callback_query.message.edit_text(profile_text, parse_mode="HTML")
    await callback_query.answer()



@router.callback_query(F.data == "ticket_menu")
async def ticket_menu(callback: CallbackQuery, state: FSMContext):
    try:
        # Get the ticket keyboard
        keyboard = get_ticket_keyboard()
        
        # Edit the message with the new text and keyboard
        await callback.message.edit_text(
            "🎫 Ticket Management Menu\n\n"
            "Here you can manage all ticket-related operations:\n"
            "• Create new tickets\n"
            "• View existing tickets\n"
            "• Close resolved tickets\n"
            "• Reopen closed tickets if needed\n\n"
            "Please select an option:",
            reply_markup=keyboard
        )
        
        # Answer the callback query to remove the loading indicator
        await callback.answer()
        
    except Exception as e:
        logger.error(f"Error in ticket_menu handler: {e}")
        await callback.answer("An error occurred. Please try again.")

@router.callback_query(F.data == "create_ticket")
async def create_ticket(callback: CallbackQuery, state: FSMContext):
    try:
        # Get the create ticket options keyboard
        keyboard = create_ticket_options_keyboard()
        
        # Edit the message with the new text and keyboard
        await callback.message.edit_text(
            "📝 Create a New Ticket\n\n"
            "Please select the type of inquiry for your ticket:",
            reply_markup=keyboard
        )
        
        # Answer the callback query to remove the loading indicator
        await callback.answer()
        
    except Exception as e:
        logger.error(f"Error in create_ticket handler: {e}")
        await callback.answer("An error occurred. Please try again.")

@router.callback_query(F.data == "back_to_ticket_menu")
async def back_to_ticket_menu(callback: CallbackQuery, state: FSMContext):
    await ticket_menu(callback, state)






# Make sure to export the router
__all__ = ["router"]
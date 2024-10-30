from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.markdown import hcode
from utils.database import Database
from datetime import datetime, timedelta
import logging
from utils.admin_utils import is_admin

router = Router()
logger = logging.getLogger(__name__)

# Define membership levels and their durations
MEMBERSHIP_LEVELS = {
    'basic': {'duration': 30, 'price': 10},
    'premium': {'duration': 90, 'price': 25},
    'vip': {'duration': 180, 'price': 50}
}

class MembershipStates(StatesGroup):
    choosing_level = State()
    confirming_upgrade = State()

@router.callback_query(F.data == "view_membership_info")
async def view_membership_info(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    db = Database()

    try:
        db.cur.execute("SELECT membership_level, membership_expiry FROM users WHERE user_id = ?", (user_id,))
        user = db.cur.fetchone()

        if not user:
            await callback_query.answer("User not found. Please try again.")
            return

        membership_level, membership_expiry = user

        # Calculate days remaining if expiry date exists
        days_remaining = "N/A"
        if membership_expiry:
            expiry_date = datetime.strptime(membership_expiry, "%Y-%m-%d %H:%M:%S")
            days_remaining = (expiry_date - datetime.now()).days

        membership_info_text = f"""
📊 <b>Membership Information</b>

🌟 <b>Current Level:</b> {hcode(membership_level)}
📅 <b>Expiry Date:</b> {hcode(membership_expiry[:10] if membership_expiry else 'N/A')}
⏳ <b>Days Remaining:</b> {hcode(str(days_remaining))}

To upgrade your membership or for more options, use the buttons below.
"""

        # Get the profile membership keyboard
        keyboard = get_profile_membership_keyboard()

        await callback_query.message.edit_text(
            text=membership_info_text,
            reply_markup=keyboard,
            parse_mode="HTML"
        )

    except Exception as e:
        error_message = f"Unexpected error in view_membership_info: {str(e)}"
        logger.error(error_message)
        await callback_query.answer("An unexpected error occurred. Please try again later.")



@router.callback_query(F.data == "upgrade_membership")
async def upgrade_membership(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    
    keyboard = [
        [('Basic (30 days) - $10', 'upgrade_basic')],
        [('Premium (90 days) - $25', 'upgrade_premium')],
        [('VIP (180 days) - $50', 'upgrade_vip')],
        [('Cancel', 'cancel_upgrade')]
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    
    await callback_query.message.edit_text(
        "Choose a membership level to upgrade to:",
        reply_markup=markup
    )
    await state.set_state(MembershipStates.choosing_level)

@router.callback_query(F.data.startswith("upgrade_"))
async def confirm_upgrade(callback_query: CallbackQuery, state: FSMContext):
    level = callback_query.data.split('_')[1]
    if level not in MEMBERSHIP_LEVELS:
        await callback_query.answer("Invalid membership level.")
        return

    await state.update_data(chosen_level=level)
    await callback_query.answer()

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [('Confirm', f'confirm_{level}')],
        [('Cancel', 'cancel_upgrade')]
    ])

    await callback_query.message.edit_text(
        f"You've selected {level.capitalize()} membership.\n"
        f"Duration: {MEMBERSHIP_LEVELS[level]['duration']} days\n"
        f"Price: ${MEMBERSHIP_LEVELS[level]['price']}\n\n"
        "Do you want to confirm this upgrade?",
        reply_markup=markup
    )
    await state.set_state(MembershipStates.confirming_upgrade)

@router.callback_query(F.data.startswith("confirm_"))
async def process_upgrade(callback_query: CallbackQuery, state: FSMContext):
    level = callback_query.data.split('_')[1]
    user_id = callback_query.from_user.id
    db = Database()

    try:
        # Update user's membership in the database
        current_time = datetime.now()
        expiry_date = current_time + timedelta(days=MEMBERSHIP_LEVELS[level]['duration'])
        
        db.cur.execute("""
            UPDATE users 
            SET membership_level = ?, membership_expiry = ?
            WHERE user_id = ?
        """, (level, expiry_date.strftime("%Y-%m-%d %H:%M:%S"), user_id))
        db.conn.commit()

        await callback_query.message.edit_text(
            f"Congratulations! Your membership has been upgraded to {level.capitalize()}.\n"
            f"Your new membership will expire on {expiry_date.strftime('%Y-%m-%d')}."
        )
    except Exception as e:
        logger.error(f"Error upgrading membership: {e}")
        await callback_query.message.edit_text(
            "An error occurred while processing your upgrade. Please try again later."
        )

    await state.clear()

@router.callback_query(F.data == "cancel_upgrade")
async def cancel_upgrade(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer("Upgrade cancelled.")
    await callback_query.message.edit_text("Membership upgrade has been cancelled.")
    await state.clear()

# Admin commands

@router.message(Command("set_membership"))
async def set_membership(message: Message):
    # Check if the user is an admin (you need to implement this check)
    if not is_admin(message.from_user.id):
        await message.reply("You don't have permission to use this command.")
        return

    # Parse the command arguments
    args = message.text.split()[1:]
    if len(args) != 3:
        await message.reply("Usage: /set_membership <user_id> <level> <duration_days>")
        return

    user_id, level, duration = args
    db = Database()

    try:
        # Update user's membership in the database
        expiry_date = datetime.now() + timedelta(days=int(duration))
        db.cur.execute("""
            UPDATE users 
            SET membership_level = ?, membership_expiry = ?
            WHERE user_id = ?
        """, (level, expiry_date.strftime("%Y-%m-%d %H:%M:%S"), int(user_id)))
        db.conn.commit()

        await message.reply(f"Membership for user {user_id} has been set to {level} until {expiry_date.strftime('%Y-%m-%d')}.")
    except Exception as e:
        logger.error(f"Error setting membership: {e}")
        await message.reply("An error occurred while setting the membership.")
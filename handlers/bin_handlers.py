import aiohttp
import asyncio
import os
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from collections import Counter

# Create a router instance
router = Router()

# Define states using StatesGroup for better structure
class BankCheckStates(StatesGroup):
    waiting_for_bin = State()

# Initialize data structures for BIN statistics
most_checked_bins = Counter()
recent_bins = []

@router.callback_query(F.data == "bin_check")
async def bank_check(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer("Opening BIN Check Function...")

    await asyncio.sleep(1)

    bank_check_text = """
🏦 <b>BIN Check</b>

Welcome to the BIN Check feature! Here you can get detailed information about a card's issuing bank.

To use this feature:
1️⃣ Enter the first 6-8 digits of the card number (BIN)
2️⃣ We'll provide you with information such as:
   • Bank name and location
   • Card type (Credit, Debit, Prepaid)
   • Card brand (Visa, Mastercard, etc.)

<i>Please note: This feature is for informational purposes only and does not guarantee card validity.</i>

You can check multiple BINs by separating them with commas or semicolons.

Enter the BIN(s) now:
"""

    # Create an inline keyboard with a Back button
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Back", callback_data="back_to_main")]
        ]
    )

    await callback_query.message.edit_text(
        text=bank_check_text,
        parse_mode="HTML",
        reply_markup=keyboard  # Add the keyboard here
    )

    await state.set_state(BankCheckStates.waiting_for_bin)

@router.message(BankCheckStates.waiting_for_bin)
async def process_bin(message: Message, state: FSMContext):
    bin_numbers = message.text.split(',')  # Split input by commas
    
    response = "BIN Check Results:\n\n"
    
    async with aiohttp.ClientSession() as session:
        for bin_number in bin_numbers:
            bin_number = bin_number.strip()  # Remove any leading/trailing whitespace
            
            if bin_number.isdigit() and 6 <= len(bin_number) <= 8:
                url = "https://bin-ip-checker.p.rapidapi.com/"
                headers = {
                    'x-rapidapi-key': os.getenv('RAPIDAPI_KEY'),  # Ensure your RapidAPI key is set as an environment variable
                    'x-rapidapi-host': "bin-ip-checker.p.rapidapi.com",
                    'Content-Type': "application/json"
                }
                payload = {"bin": bin_number, "ip": "8.8.8.8"}  # Using IP address 8.8.8.8

                try:
                    async with session.post(url, json=payload, headers=headers) as response_api:
                        if response_api.status == 200:
                            data = await response_api.json()
                            if data.get("result") == 1:
                                response += (
                                    f"BIN: {bin_number}\n"
                                    f"Bank: {data.get('bank', 'N/A')}\n"
                                    f"Card Type: {data.get('type', 'N/A')}\n"
                                    f"Card Brand: {data.get('brand', 'N/A')}\n\n"
                                )
                                update_bin_stats(bin_number)  # Update statistics for the checked BIN
                            else:
                                response += f"No information found for BIN: {bin_number}\n\n"
                        else:
                            response += f"Error checking BIN: {bin_number} (HTTP Status: {response_api.status})\n\n"
                except Exception as e:
                    response += f"Exception occurred while checking BIN {bin_number}: {str(e)}\n\n"
            else:
                response += f"Invalid BIN: {bin_number}\n\n"

    await message.reply(response)
    
    # Reset the state after processing the message
    await state.clear()

def update_bin_stats(bin):
    most_checked_bins[bin] += 1
    if bin in recent_bins:
        recent_bins.remove(bin)
    recent_bins.append(bin)
    if len(recent_bins) > 20:  # Keep only the last 20 recent BINs
        recent_bins.pop(0)

def get_bin_stats():
    top_bins = most_checked_bins.most_common(5)
    top_bins_text = "\n".join([f"   • {bin}: {count} checks" for bin, count in top_bins])
    recent_bins_text = "\n".join([f"   • {bin}" for bin in reversed(recent_bins[-5:])])
    
    return f"""
📊 <b>Most Checked BINs:</b>
{top_bins_text}

🕒 <b>Recent BINs:</b>
{recent_bins_text}
"""

# Function to include BIN stats in the initial bank check message
async def bank_check_with_stats(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer("Opening Bank Check...")
    
    await asyncio.sleep(1)
    
    bank_check_text = f"""
🏦 <b>Bank Check</b>

Welcome to the Bank Check feature! Here you can get detailed information about a card's issuing bank.

To use this feature:
1️⃣ Enter the first 6-8 digits of the card number (BIN)
2️⃣ We'll provide you with information such as:
   • Bank name and location
   • Card type (Credit, Debit, Prepaid)
   • Card brand (Visa, Mastercard, etc.)

<i>Please note: This feature is for informational purposes only and does not guarantee card validity.</i>

{get_bin_stats()}

You can check multiple BINs by separating them with commas or semicolons.

Enter the BIN(s) now:
"""

    await callback_query.message.edit_text(
        text=bank_check_text,
        parse_mode="HTML"
    )
    
    await state.set_state(BankCheckStates.waiting_for_bin)
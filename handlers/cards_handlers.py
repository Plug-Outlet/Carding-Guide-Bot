from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.cards_keyboard import *
from aiogram.filters import Command, CommandStart
from handlers.main_menu import *

router = Router()

class CardCheckStates(StatesGroup):
    waiting_for_card_info = State()

@router.callback_query(F.data == "check_card")
async def check_card_start(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    
    greeting_text = """
💳 <b>Card Check</b>

Welcome to the Card Check feature! Here you can validate and get information about credit cards.

Please enter the card information in one of the following formats:

1️⃣ <code>CC|MM|YY|CVV</code>
2️⃣ <code>CC|M|YYYY|CVV</code>
3️⃣ <code>CC|MM|YYYY|CVV</code>

Where:
• CC: Card number (13-19 digits)
• MM: Month (01-12)
• YY: Year (last two digits)
• YYYY: Full year
• CVV: Card Verification Value (3-4 digits)

For example:
<code>4111111111111111|05|25|123</code>
<code>4111111111111111|5|2025|123</code>
<code>4111111111111111|05|2025|123</code>

Please enter your card information now:
"""

    await callback_query.message.edit_text(
        text=checker_menu_text,
        reply_markup=get_card_checker_menu_keyboard(),
        parse_mode="HTML"
    )

@router.message(CardCheckStates.waiting_for_card_info)
async def process_card_info(message: Message, state: FSMContext):
    card_info = message.text.strip()
    
    # Here you would typically validate the input format and process the card information
    # For this example, we'll just acknowledge receipt of the information
    
    response_text = f"""
Received card information: <code>{card_info}</code>

Processing... (This is where you'd implement the actual card checking logic)

To check another card, use the /check_card command.
To return to the main menu, use /menu.
"""
    
    await message.answer(response_text, parse_mode="HTML")
    await state.clear()

@router.callback_query(F.data.startswith("check_format_"))
async def process_format_selection(callback_query: CallbackQuery, state: FSMContext):
    format_number = callback_query.data.split("_")[-1]
    formats = {
        "1": "CC|MM|YY|CVV",
        "2": "CC|M|YYYY|CVV",
        "3": "CC|MM|YYYY|CVV"
    }
    selected_format = formats[format_number]
    
    await state.update_data(selected_format=selected_format)
    
    response_text = f"""
Please now paste your data in the requested format of:
<code>{selected_format}</code>

         Membership Tiers and Limits:
<pre>
┌────────┬────┬────┬─────┐
│ Access │Rows│ 24h│Total│
├────────┼────┼────┼─────┤
│👤 Guest│  5 │  1 │   5 │
│🔹 Basic│ 10 │  5 │  50 │
│🔸 Adv  │ 25 │  7 │ 175 │
│💎 Elite│ 50 │ 10 │ 500 │
└────────┴────┴────┴─────┘
</pre>
Enter your card information now:
"""

    await callback_query.message.edit_text(
        text=response_text,
        parse_mode="HTML"
    )
    await state.set_state(CardCheckStates.waiting_for_card_info)

@router.message(CardCheckStates.waiting_for_card_info)
async def process_card_info(message: Message, state: FSMContext):
    card_info = message.text.strip()
    state_data = await state.get_data()
    selected_format = state_data.get('selected_format')
    
    # Here you would typically validate the input format and process the card information
    # For this example, we'll just acknowledge receipt of the information
    
    response_text = f"""
Received card information in format: <code>{selected_format}</code>

Data received:
<code>{card_info}</code>

Processing... (This is where you'd implement the actual card checking logic)

To check more cards, use the /check_card command.
To return to the main menu, use /menu.
"""
    
    await message.answer(response_text, parse_mode="HTML")
    await state.clear()


@router.message(CardCheckStates.waiting_for_card_info)
async def process_card_info(message: Message, state: FSMContext):
    card_info = message.text.strip()
    state_data = await state.get_data()
    selected_format = state_data.get('selected_format')
    
    # Here you would typically validate the input format and process the card information
    # For this example, we'll just acknowledge receipt of the information
    
    response_text = f"""
Received card information in format: <code>{selected_format}</code>

Data received:
<code>{card_info}</code>

Processing... (This is where you'd implement the actual card checking logic)

To check more cards, use the /check_card command.
To return to the main menu, use /menu.
"""
    
    await message.answer(response_text, parse_mode="HTML")
    await state.clear()

@router.callback_query(F.data == "view_history")
async def view_history(callback_query: CallbackQuery):
    await callback_query.answer("Opening your history...")
    # Implement logic to show user's history

@router.callback_query(F.data == "back_to_main")
async def back_to_main(callback_query: CallbackQuery):
    from handlers.main_menu import send_welcome
    await callback_query.message.edit_text("Returning to main menu...")
    await send_welcome(callback_query.message)

from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.states import BotStates
from utils.helper import format_timestamp, validate_card_number, mask_card_number
from keyboards.cards_keyboard import get_cards_menu_keyboard, get_card_result_keyboard

async def show_checker_menu(message: types.Message):
    checker_message = """
╭══•:|★✧♡💝♡✧★|: ══╮
   🔍 *Choose a Checker Option* 🔍
╰══•:|★✧♡💝♡✧★|:  ══╯

Choose a checker to validate card information:

• *X Checker*: Our standard CC checker. Verifies card validity and provides details about status and issuing bank.

• *Stripe Checker*: Uses Stripe's API to validate cards without charging. Provides insights on card validity and potential issues.

• *BIN Checker*: Analyzes the Bank Identification Number (first 6 digits) for card issuer, type, and country information.

• *BIN Lookup*: Similar to BIN Checker, but often provides more detailed issuer and card characteristic information.

• *VBV Checker*: Verifies if a card is enrolled in Verified by Visa (VBV) or similar 3D Secure programs.

Select an option to proceed with your check. Remember to use these responsibly and in compliance with applicable laws.

*Created by:* @ Me Bitch
    """

    await message.answer(checker_message, reply_markup=get_cards_menu_keyboard(), parse_mode="Markdown")

async def process_checker_callback(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == 'back_to_main':
        await callback_query.message.answer("Returning to main menu.", reply_markup=get_main_keyboard())
    else:
        await process_checker(callback_query.message, callback_query.data, state)

async def process_checker(message: types.Message, checker_type: str, state: FSMContext):
    await message.answer(f"*{checker_type} Selected*\n\nPlease enter the card details in the format:\n`XXXXXXXXXXXXXXXX|MM|YY|CVV`\n\nFor example: `4111111111111111|12|25|123`", parse_mode="Markdown")
    await state.set_state(BotStates.BIN_CHECK)

async def handle_card_input(message: types.Message, state: FSMContext):
    # Parse and validate card input
    card_info = parse_card_info(message.text)
    if not card_info:
        await message.answer("Invalid card format. Please try again.")
        return

    if not validate_card_number(card_info['card_number']):
        await message.answer("Invalid card number. Please check and try again.")
        return

    # Process the card (this is where you'd implement your actual checking logic)
    result = await check_card(card_info)

    # Display result
    masked_number = mask_card_number(card_info['card_number'])
    result_message = f"Card: {masked_number}\nResult: {result}"
    await message.answer(result_message, reply_markup=get_card_result_keyboard())

    # Clear the state
    await state.clear()

async def check_card(card_info):
    # Implement your card checking logic here
    # This is just a placeholder
    return "Card is valid (This is a placeholder result)"

# Helper function to parse card info
def parse_card_info(card_string):
    parts = card_string.split("|")
    if len(parts) != 4:
        return None
    
    card_number, month, year, cvv = parts
    if not (card_number.isdigit() and month.isdigit() and year.isdigit() and cvv.isdigit()):
        return None
    
    return {
        "card_number": card_number,
        "expiry_month": month,
        "expiry_year": year,
        "cvv": cvv
    }

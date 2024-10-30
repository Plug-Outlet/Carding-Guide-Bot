from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.ticket_keyboard import get_ticket_keyboard, create_ticket_options_keyboard
from utils.ticket_utils import generate_ticket_id, save_ticket, notify_admin
from keyboards.ticket_keyboard import *
from aiogram import types



router = Router()

class TicketStates(StatesGroup):
    WAITING_FOR_MESSAGE = State()
    CONFIRMING_SUBMISSION = State()
    WAITING_FOR_STATUS_UPDATE = State()





@router.callback_query(F.data.startswith("ticket_"))
async def handle_ticket_inquiry(callback: CallbackQuery, state: FSMContext):
    inquiry_type = callback.data.split("_")[1]
    await state.update_data(inquiry_type=inquiry_type)
    
    await callback.message.edit_text(
        f"You've selected {inquiry_type.replace('_', ' ').title()} Inquiry.\n"
        "Please provide details for your inquiry:",
        reply_markup=None
    )
    await state.set_state(TicketStates.WAITING_FOR_MESSAGE)

@router.message(TicketStates.WAITING_FOR_MESSAGE)
async def process_ticket_message(message: Message, state: FSMContext):
    user_message = message.text
    await state.update_data(user_message=user_message)
    
    data = await state.get_data()
    inquiry_type = data['inquiry_type']
    ticket_id = generate_ticket_id()
    
    await message.answer(
        f"Please review your {inquiry_type.replace('_', ' ').title()} Inquiry:\n\n"
        f"Ticket ID: {ticket_id}\n"
        f"Message: {user_message}\n\n"
        "Is this correct?",
        reply_markup=get_confirm_keyboard()
    )
    await state.update_data(ticket_id=ticket_id)
    await state.set_state(TicketStates.CONFIRMING_SUBMISSION)

@router.callback_query(TicketStates.CONFIRMING_SUBMISSION, F.data == "confirm")
async def submit_ticket(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    ticket_id = data['ticket_id']
    inquiry_type = data['inquiry_type']
    user_message = data['user_message']
    
    # Save the ticket to the database
    await save_ticket(callback.from_user.id, ticket_id, inquiry_type, user_message)
    
    # Notify admin
    await notify_admin(ticket_id, inquiry_type, user_message)
    
    await callback.message.edit_text(
        f"Your ticket (ID: {ticket_id}) has been submitted successfully.\n"
        "An admin will review it shortly.",
        reply_markup=get_ticket_keyboard()
    )
    await state.clear()

@router.callback_query(TicketStates.CONFIRMING_SUBMISSION, F.data == "cancel")
async def cancel_submission(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Ticket submission cancelled. What would you like to do?",
        reply_markup=get_ticket_keyboard()
    )
    await state.clear()

@router.callback_query(F.data == "back_to_ticket_menu")
async def back_to_ticket_menu(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "🎫 Ticket Management Menu\n\n"
        "Here you can manage all ticket-related operations:\n"
        "• Create new tickets\n"
        "• View existing tickets\n"
        "• Close resolved tickets\n"
        "• Reopen closed tickets if needed\n\n"
        "Please select an option:",
        reply_markup=get_ticket_keyboard()
    )
    await state.clear()
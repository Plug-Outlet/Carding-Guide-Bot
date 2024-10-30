from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import List, Dict
from utils.database import Database
from keyboards.guides_keyboard import *
from typing import List, Dict
import re

router = Router()
db = Database()

class GuideStates(StatesGroup):
    WAITING_FOR_TITLE = State()
    WAITING_FOR_CONTENT = State()
    WAITING_FOR_FORMAT = State()
    WAITING_FOR_CATEGORY = State()
    WAITING_FOR_TYPE = State()
    WAITING_FOR_TARGET = State()
    WAITING_FOR_URL = State()

# Helper functions for keyboards
def get_guide_category_keyboard():
    categories = db.get_guide_categories()
    builder = InlineKeyboardBuilder()
    for category in categories:
        builder.button(text=category, callback_data=f"guide_category:{category}")
    builder.adjust(2)  # 2 buttons per row
    return builder.as_markup()

def get_guide_stats_keyboard():
    stats = db.get_guide_stats_by_category()
    builder = InlineKeyboardBuilder()
    for stat in stats:
        builder.button(
            text=f"{stat['category']} ({stat['count']})",
            callback_data=f"guide_category:{stat['category']}"
        )
    builder.adjust(2)  # 2 buttons per row
    return builder.as_markup()

# Command handlers
@router.message(Command("guides"))
async def show_guide_menu(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="View Guide Categories", callback_data="view_categories")],
        [InlineKeyboardButton(text="Create New Guide", callback_data="create_guide")],
        [InlineKeyboardButton(text="Search Guides", callback_data="search_guides")]
    ])
    await message.answer("Guide Menu:", reply_markup=keyboard)


@router.callback_query(F.data == "guide_categories")
async def show_guide_categories(callback: CallbackQuery):
    categories = db.get_guide_categories()  # Implement this method in your Database class
    builder = InlineKeyboardBuilder()
    for category in categories:
        builder.button(text=category, callback_data=f"category:{category}")
    builder.button(text="🔙 Back", callback_data="back_to_guides_main")
    builder.adjust(2)  # 2 buttons per row
    await callback.message.edit_text("Select a guide category:", reply_markup=builder.as_markup())
    await callback.answer()

@router.callback_query(F.data == "guide_methods")
async def show_guide_methods(callback: CallbackQuery):
    categories = db.get_guide_categories()  # Implement this method in your Database class
    builder = InlineKeyboardBuilder()
    for category in categories:
        builder.button(text=category, callback_data=f"category:{category}")
    builder.button(text="🔙 Back", callback_data="back_to_guides_main")
    builder.adjust(2)  # 2 buttons per row
    await callback.message.edit_text("Select a guide category:", reply_markup=builder.as_markup())
    await callback.answer()

@router.callback_query(F.data == "guide_targets")
async def show_guide_targets(callback: CallbackQuery):
    categories = db.get_guide_categories()  # Implement this method in your Database class
    builder = InlineKeyboardBuilder()
    for category in categories:
        builder.button(text=category, callback_data=f"category:{category}")
    builder.button(text="🔙 Back", callback_data="back_to_guides_main")
    builder.adjust(2)  # 2 buttons per row
    await callback.message.edit_text("Select a guide category:", reply_markup=builder.as_markup())
    await callback.answer()

@router.callback_query(F.data == "guide_types")
async def show_guide_types(callback: CallbackQuery):
    keyboard = get_guide_ordering_types_keyboard()  # Call the function to get the keyboard
    
    message_text = (
        "📚 Guide to Order Types:\n\n"
        "🔄 Standard: Regular orders with standard processing and delivery times.\n\n"
        "🚀 Rush: Expedited orders with priority processing and faster delivery.\n\n"
        "📦 Bulk: Large quantity orders, often with discounted rates.\n\n"
        "🎨 Custom: Tailored orders with specific requirements or modifications.\n\n"
        "🔁 Recurring: Regular, scheduled orders at set intervals.\n\n"
        "Select an order type to learn more or view related guides."
    )
    
    await callback.message.edit_text(message_text, reply_markup=keyboard)
    await callback.answer()







@router.callback_query(F.data == "guide_types_standard")
async def show_guide_types_standard(callback: CallbackQuery):
    keyboard = get_guide_ordering_types_keyboard()  # Call the function to get the keyboard
    
    message_text = (
        "📚 Guide to Order Types:\n\n"
        "🔄 Standard: Regular orders with standard processing and delivery times.\n\n"
        "🚀 Rush: Expedited orders with priority processing and faster delivery.\n\n"
        "📦 Bulk: Large quantity orders, often with discounted rates.\n\n"
        "🎨 Custom: Tailored orders with specific requirements or modifications.\n\n"
        "🔁 Recurring: Regular, scheduled orders at set intervals.\n\n"
        "Select an order type to learn more or view related guides."
    )
    
    await callback.message.edit_text(message_text, reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data == "guide_types_rush")
async def show_guide_types_rush(callback: CallbackQuery):
    keyboard = get_guide_ordering_types_keyboard()  # Call the function to get the keyboard
    
    message_text = (
        "📚 Guide to Order Types:\n\n"
        "🔄 Standard: Regular orders with standard processing and delivery times.\n\n"
        "🚀 Rush: Expedited orders with priority processing and faster delivery.\n\n"
        "📦 Bulk: Large quantity orders, often with discounted rates.\n\n"
        "🎨 Custom: Tailored orders with specific requirements or modifications.\n\n"
        "🔁 Recurring: Regular, scheduled orders at set intervals.\n\n"
        "Select an order type to learn more or view related guides."
    )
    
    await callback.message.edit_text(message_text, reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data == "guide_types_bulk")
async def guide_types_bulk(callback: CallbackQuery):
    keyboard = get_guide_ordering_types_keyboard()  # Call the function to get the keyboard
    
    message_text = (
        "📚 Guide to Order Types:\n\n"
        "🔄 Standard: Regular orders with standard processing and delivery times.\n\n"
        "🚀 Rush: Expedited orders with priority processing and faster delivery.\n\n"
        "📦 Bulk: Large quantity orders, often with discounted rates.\n\n"
        "🎨 Custom: Tailored orders with specific requirements or modifications.\n\n"
        "🔁 Recurring: Regular, scheduled orders at set intervals.\n\n"
        "Select an order type to learn more or view related guides."
    )
    
    await callback.message.edit_text(message_text, reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data == "guide_types_custom")
async def guide_types_custom(callback: CallbackQuery):
    keyboard = get_guide_ordering_types_keyboard()  # Call the function to get the keyboard
    
    message_text = (
        "📚 Guide to Order Types:\n\n"
        "🔄 Standard: Regular orders with standard processing and delivery times.\n\n"
        "🚀 Rush: Expedited orders with priority processing and faster delivery.\n\n"
        "📦 Bulk: Large quantity orders, often with discounted rates.\n\n"
        "🎨 Custom: Tailored orders with specific requirements or modifications.\n\n"
        "🔁 Recurring: Regular, scheduled orders at set intervals.\n\n"
        "Select an order type to learn more or view related guides."
    )
    
    await callback.message.edit_text(message_text, reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data == "guide_types_recurring")
async def guide_types_recurring(callback: CallbackQuery):
    recurring_guides = db.get_guides_by_type("recurring")  # Implement this method in your Database class
    
    message_text = (
        "📚 Guides: Recurring Orders\n\n"
        "Recurring orders are subscription-based or regularly scheduled purchases. "
        "These guides will help you understand and manage recurring orders effectively.\n\n"
    )
    
    if recurring_guides:
        message_text += "Available guides:\n\n"
        for guide in recurring_guides:
            message_text += f"• {guide['title']}\n"
        message_text += "\nSelect a guide to view its details."
    else:
        message_text += "No guides are currently available for recurring orders. Check back later!"

    message_text += (
        "\n\nRemember to rate and provide feedback for each guide you view. "
        "Your input helps us improve our content!"
    )

    # Create a keyboard with buttons for each guide and a back button
    builder = InlineKeyboardBuilder()
    for guide in recurring_guides:
        builder.button(text=guide['title'], callback_data=f"view_guide_{guide['id']}")
    builder.button(text="🔙 Back to Order Types", callback_data="guide_types")
    builder.adjust(1)  # One button per row for better readability
    
    await callback.message.edit_text(message_text, reply_markup=builder.as_markup())
    await callback.answer()


@router.callback_query(F.data == "guide_main_faq")
async def show_guide_faq(callback: CallbackQuery):
    faq_items = db.get_faq_items()  # Implement this method in your Database class
    faq_text = "Frequently Asked Questions:\n\n"
    for item in faq_items:
        faq_text += f"Q: {item['question']}\nA: {item['answer']}\n\n"
    builder = InlineKeyboardBuilder()
    builder.button(text="🔙 Back", callback_data="back_to_guides_main")
    await callback.message.edit_text(faq_text, reply_markup=builder.as_markup())
    await callback.answer()


@router.callback_query(F.data == "back_to_guides_main")
async def back_to_guides_main(callback: CallbackQuery):
    await callback.message.edit_text("Guides Menu", reply_markup=get_guides_main_keyboard())
    await callback.answer()

# Handlers for specific guide selections
@router.callback_query(F.data.startswith(("type:", "method:", "target:", "category:")))
async def show_guides_for_selection(callback: CallbackQuery):
    selection_type, selection_value = callback.data.split(":")
    guides = db.get_guides_by_selection(selection_type, selection_value)  # Implement this method
    
    if not guides:
        await callback.answer("No guides found for this selection.")
        return

    text = f"Guides for {selection_type} '{selection_value}':\n\n"
    for guide in guides:
        text += f"• {guide['title']} - /view_guide_{guide['id']}\n"

    builder = InlineKeyboardBuilder()
    builder.button(text="🔙 Back", callback_data=f"guide_{selection_type}s")
    await callback.message.edit_text(text, reply_markup=builder.as_markup())
    await callback.answer()



@router.message(Command(commands=["view_guide_"], magic=F.text.regexp(r"^/view_guide_(\d+)")))
async def view_guide(message: Message, match: re.Match):
    guide_id = int(match.group(1))
    guide = db.get_guide(guide_id)
    if guide:
        response = f"Title: {guide['title']}\n"
        response += f"Category: {guide['category']}\n"
        response += f"Format: {guide['format']}\n"
        response += f"Type: {guide['type']}\n"
        response += f"Target: {guide['target']}\n"
        response += f"URL: {guide['url']}\n\n"
        response += f"Content:\n{guide['content']}"
        await message.answer(response)
    else:
        await message.answer("Guide not found.")

# Create guide process
@router.callback_query(F.data == "create_guide")
async def start_create_guide(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Let's create a new guide. First, what's the title of your guide?")
    await state.set_state(GuideStates.WAITING_FOR_TITLE)
    await callback.answer()

@router.message(GuideStates.WAITING_FOR_TITLE)
async def process_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer("Great! Now, what's the content of your guide?")
    await state.set_state(GuideStates.WAITING_FOR_CONTENT)

@router.message(GuideStates.WAITING_FOR_CONTENT)
async def process_content(message: Message, state: FSMContext):
    await state.update_data(content=message.text)
    await message.answer("What's the format of your guide? (e.g., text, video, pdf)")
    await state.set_state(GuideStates.WAITING_FOR_FORMAT)

@router.message(GuideStates.WAITING_FOR_FORMAT)
async def process_format(message: Message, state: FSMContext):
    await state.update_data(format=message.text)
    await message.answer("What category does this guide belong to?")
    await state.set_state(GuideStates.WAITING_FOR_CATEGORY)

@router.message(GuideStates.WAITING_FOR_CATEGORY)
async def process_category(message: Message, state: FSMContext):
    await state.update_data(category=message.text)
    await message.answer("What type of guide is this? (e.g., Tutorial, How-to, Reference)")
    await state.set_state(GuideStates.WAITING_FOR_TYPE)

@router.message(GuideStates.WAITING_FOR_TYPE)
async def process_type(message: Message, state: FSMContext):
    await state.update_data(type=message.text)
    await message.answer("Who is the target audience for this guide?")
    await state.set_state(GuideStates.WAITING_FOR_TARGET)

@router.message(GuideStates.WAITING_FOR_TARGET)
async def process_target(message: Message, state: FSMContext):
    await state.update_data(target=message.text)
    await message.answer("Finally, what's the URL for this guide? (If applicable)")
    await state.set_state(GuideStates.WAITING_FOR_URL)

@router.message(GuideStates.WAITING_FOR_URL)
async def process_url(message: Message, state: FSMContext):
    await state.update_data(url=message.text)
    guide_data = await state.get_data()
    
    new_guide_id = db.create_guide(
        title=guide_data['title'],
        content=guide_data['content'],
        format=guide_data['format'],
        category=guide_data['category'],
        guide_type=guide_data['type'],
        target=guide_data['target'],
        url=guide_data['url']
    )
    
    await message.answer(f"Guide created successfully! Guide ID: {new_guide_id}")
    await state.clear()

# Search guides
@router.callback_query(F.data == "search_guides")
async def search_guides(callback: CallbackQuery):
    await callback.message.answer("Please enter a search term for the guides:")
    await callback.answer()

@router.message(F.text)
async def process_search(message: Message):
    search_term = message.text
    guides = db.search_guides(search_term)  # You'll need to implement this method in your Database class
    
    if guides:
        response = "Search results:\n\n"
        for guide in guides:
            response += f"• {guide['title']} - /view_guide_{guide['id']}\n"
    else:
        response = "No guides found matching your search term."
    
    await message.answer(response)

# Don't forget to include this router in your main bot file
# from guide_handlers import router as guide_router
# dp.include_router(guide_router)
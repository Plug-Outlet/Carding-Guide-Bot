from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

class BotStates(StatesGroup):
    MAIN = State()
    BIN_CHECK = State()
    # Add other states as needed

class BankCheckStates(StatesGroup):
    waiting_for_bin = State()


class AdminStates(StatesGroup):
    WAITING_FOR_GUIDE_CONTENT = State()
    APPROVE_ONLY_TEXT = State()
    HERE_SEARCH_PROFILE = State()
    HERE_SEND_MESSAGE = State()
    here_search_profile = State()
    
class StorageFunctions(StatesGroup):
    waiting_for_guide_content = State()
    approve_only_text = State()
    def __init__(self, state: FSMContext):
        self.state = state

    async def set_state(self, state: State):
        """Set the current state."""
        await self.state.set_state(state)

    async def get_state(self):
        """Get the current state."""
        return await self.state.get_state()

    async def clear_state(self):
        """Clear the current state."""
        await self.state.clear()

    async def update_data(self, **kwargs):
        """Update state data."""
        await self.state.update_data(**kwargs)

    async def get_data(self):
        """Get all state data."""
        return await self.state.get_data()

    async def get_data_item(self, key: str, default=None):
        """Get a specific item from state data."""
        data = await self.get_data()
        return data.get(key, default)

    async def set_data_item(self, key: str, value):
        """Set a specific item in state data."""
        await self.update_data(**{key: value})

    async def remove_data_item(self, key: str):
        """Remove a specific item from state data."""
        data = await self.get_data()
        if key in data:
            del data[key]
            await self.state.set_data(data)

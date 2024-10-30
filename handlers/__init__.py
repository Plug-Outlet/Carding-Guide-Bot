# handlers/__init__.py

from .main_menu import router as main_menu_router
from .user_handlers import router as user_router
from .admin_handlers import router as admin_router
from .bin_handlers import router as bin_router
from .cards_handlers import router as cards_router
from .guide_handlers import router as guides_router

__all__ = [
    'main_menu_router',
    'user_router',
    'admin_router',
    'bin_router',
    'cards_router',
    'guides_router'
]
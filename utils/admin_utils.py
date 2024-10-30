# utils/admin_utils.py
from config import ADMIN_USER_IDS, ADMIN_USERNAMES

def is_admin(user_id: int, username: str = None) -> bool:
    return user_id in ADMIN_USER_IDS or (username and username in ADMIN_USERNAMES)
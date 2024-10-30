import sqlite3
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional



class Database:
    _instance = None

    def __new__(cls, db_file='bot_database.db'):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.conn = sqlite3.connect(db_file)
            cls._instance.cur = cls._instance.conn.cursor()
            cls._instance.initialize_database()
        return cls._instance

    def initialize_database(self):
        self.create_data_table()
        self.create_card_data_table()
        self.create_metadata_table()
        self.create_bins_table()
        self.create_bin_checks_table()
        self.create_users_table()
        self.create_guides_table()  # New table for guides
        self.create_settings_table()
        self.create_tickets_table()  # Create tickets table

        self.conn.commit()

    def create_data_table(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS data
                            (id INTEGER PRIMARY KEY, 
                             content TEXT,
                             timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')

    def create_card_data_table(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS card_data
                            (id INTEGER PRIMARY KEY,
                             card_number TEXT,
                             expiry_date TEXT,
                             cvv TEXT,
                             name TEXT,
                             address TEXT,
                             city TEXT,
                             state TEXT,
                             zip_code TEXT,
                             country TEXT)''')

    def create_metadata_table(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS metadata
                            (key TEXT PRIMARY KEY, value TEXT)''')

    def create_bins_table(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS bins
                            (bin TEXT PRIMARY KEY, 
                             added_count INTEGER DEFAULT 1, 
                             requested_count INTEGER DEFAULT 0, 
                             last_added DATETIME,
                             last_checked DATETIME)''')

    def create_bin_checks_table(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS bin_checks
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                             bin TEXT NOT NULL,
                             check_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

    def create_users_table(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS users
                            (user_id INTEGER PRIMARY KEY,
                            username TEXT,
                            membership_level TEXT DEFAULT 'guest',
                            first_seen DATETIME DEFAULT CURRENT_TIMESTAMP,
                            last_active DATETIME DEFAULT CURRENT_TIMESTAMP,
                            membership_expiry DATETIME)''')

    def create_guides_table(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS guides
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                             title TEXT NOT NULL,
                             content TEXT NOT NULL,
                             format TEXT NOT NULL,
                             category TEXT NOT NULL,
                             type TEXT NOT NULL,
                             target TEXT NOT NULL,
                             url TEXT NOT NULL,
                             guide_type TEXT NOT NULL,
                             created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                             updated_at DATETIME DEFAULT CURRENT_TIMESTAMP)''')

    def request_bin(self, bin_number):
        current_time = datetime.now().isoformat()
        self.cur.execute('''INSERT INTO bin_checks (bin) VALUES (?)''', (bin_number,))
        self.cur.execute('''INSERT OR REPLACE INTO bins (bin, requested_count, last_checked)
                            VALUES (?, 
                                    COALESCE((SELECT requested_count FROM bins WHERE bin = ?) + 1, 1),
                                    ?)''', (bin_number, bin_number, current_time))
        self.conn.commit()

    def create_settings_table(self):
        self.cur.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
        ''')
        self.conn.commit()


    def create_tickets_table(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS tickets (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER NOT NULL,
                            details TEXT NOT NULL,
                            status TEXT DEFAULT 'open',
                            created_at DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        self.conn.commit()

    def create_ticket(self, user_id, details):
        # Logic to create a new ticket in the database
        current_time = datetime.now().isoformat()
        
        self.cur.execute('''
            INSERT INTO tickets (user_id, details, created_at)
            VALUES (?, ?, ?)
        ''', (user_id, details, current_time))
        
        self.conn.commit()
        return self.cur.lastrowid  # Return the ID of the created ticket

    def get_guides_by_type(self, guide_type):
        self.cur.execute('''
            SELECT id, title, content, format, category, guide_type, target, url
            FROM guides
            WHERE guide_type = ?
        ''', (guide_type,))
        guides = [
            {
                "id": row[0],
                "title": row[1],
                "content": row[2],
                "format": row[3],
                "category": row[4],
                "type": row[5],
                "target": row[6],
                "url": row[7]
            }
            for row in self.cur.fetchall()
        ]
        return guides

    def check_guides_table_schema(self):
        self.cur.execute("PRAGMA table_info(guides)")
        columns = self.cur.fetchall()
        for column in columns:
            print(column)







    def get_user_tickets(self, user_id):
        # Logic to fetch all tickets for a specific user
        self.cur.execute("SELECT * FROM tickets WHERE user_id = ?", (user_id,))
        
        return self.cur.fetchall()  # Return all tickets for the user

    def update_ticket_status(self, ticket_id, new_status):
        # Logic to update a specific ticket's status in the database
        self.cur.execute('''
            UPDATE tickets SET status = ? WHERE id = ?
        ''', (new_status, ticket_id))
        
        self.conn.commit()

    def get_guide_count_by_category(self, category):
        self.cur.execute("SELECT COUNT(*) FROM guides WHERE category = ?", (category,))
        return self.cur.fetchone()[0]

    def get_bin_check_count(self, bin_number):
        self.cur.execute("SELECT COUNT(*) FROM bin_checks WHERE bin = ?", (bin_number,))
        return self.cur.fetchone()[0]

    def get_top_bins(self, limit=10):
        self.cur.execute('''SELECT bin, added_count FROM bins 
                            ORDER BY added_count DESC LIMIT ?''', (limit,))
        return self.cur.fetchall()

    def table_exists(self, table_name):
        self.cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        return self.cur.fetchone() is not None

    def register_user(self, user_id, username):
        current_time = datetime.now().isoformat()
        self.cur.execute('''
        INSERT OR IGNORE INTO users (user_id, username, membership_level, first_seen, last_active)
        VALUES (?, ?, 'guest', ?, ?)
        ''', (user_id, username, current_time, current_time))
        
        is_new_user = self.cur.rowcount > 0
        
        self.cur.execute('''
        UPDATE users SET 
            username = ?,
            last_active = ?
        WHERE user_id = ?
        ''', (username, current_time, user_id))
        
        self.conn.commit()
        return is_new_user, current_time

    def get_user_count(self):
        self.cur.execute("SELECT COUNT(*) FROM users")
        return self.cur.fetchone()[0]

    def create_checks_table(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS checks
                            (id INTEGER PRIMARY KEY, 
                            status TEXT,
                            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        self.conn.commit()

    def create_guide(self, title: str, content: str, format: str, category: str, guide_type: str, target: str, url: str) -> int:
        """
        Create a new guide and store it in the database.
        
        Args:
        title (str): The title of the guide
        content (str): The content of the guide
        format (str): The format of the guide (e.g., 'text', 'video', 'pdf')
        category (str): The category of the guide
        guide_type (str): The type of the guide
        target (str): The target audience of the guide
        url (str): The URL of the guide
        
        Returns:
        int: The ID of the newly created guide
        """
        current_time = datetime.now().isoformat()
        self.cur.execute('''
            INSERT INTO guides (title, content, format, category, type, target, url, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (title, content, format, category, guide_type, target, url, current_time, current_time))
        self.conn.commit()
        return self.cur.lastrowid

    def get_all_guides(self) -> List[Dict]:
        """
        Retrieve all guides from the database.
        
        Returns:
        List[Dict]: A list of dictionaries, each containing guide information
        """
        self.cur.execute('''
            SELECT id, title, format, category, type, target, url, created_at, updated_at
            FROM guides
        ''')
        guides = [
            {
                "id": row[0],
                "title": row[1],
                "format": row[2],
                "category": row[3],
                "type": row[4],
                "target": row[5],
                "url": row[6],
                "created_at": row[7],
                "updated_at": row[8]
            }
            for row in self.cur.fetchall()
        ]
        return guides

    def get_guide(self, guide_id: int) -> Optional[Dict]:
        """
        Retrieve a specific guide by its ID.
        
        Args:
        guide_id (int): The ID of the guide to retrieve
        
        Returns:
        Optional[Dict]: A dictionary containing guide information, or None if not found
        """
        self.cur.execute('''
            SELECT id, title, content, format, category, type, target, url, created_at, updated_at
            FROM guides
            WHERE id = ?
        ''', (guide_id,))
        row = self.cur.fetchone()
        if row:
            return {
                "id": row[0],
                "title": row[1],
                "content": row[2],
                "format": row[3],
                "category": row[4],
                "type": row[5],
                "target": row[6],
                "url": row[7],
                "created_at": row[8],
                "updated_at": row[9]
            }
        return None

    def delete_guide(self, guide_id: int) -> bool:
        """
        Delete a guide from the database.
        
        Args:
        guide_id (int): The ID of the guide to delete
        
        Returns:
        bool: True if the guide was successfully deleted, False otherwise
        """
        self.cur.execute('DELETE FROM guides WHERE id = ?', (guide_id,))
        self.conn.commit()
        return self.cur.rowcount > 0

    def get_guide_categories(self) -> List[str]:
        """
        Retrieve all unique guide categories from the database.
        
        Returns:
        List[str]: A list of all unique categories
        """
        self.cur.execute('SELECT DISTINCT category FROM guides')
        return [row[0] for row in self.cur.fetchall()]

    def get_recent_active_users(self, limit=5):
        self.cur.execute("""
            SELECT user_id, username, last_active, membership_level
            FROM users 
            ORDER BY last_active DESC 
            LIMIT ?
        """, (limit,))
        return self.cur.fetchall()
    
    def get_recent_registered_users(self, limit=5):
        self.cur.execute("""
            SELECT user_id, username, first_seen, membership_level
            FROM users 
            ORDER BY first_seen DESC 
            LIMIT ?
        """, (limit,))
        return self.cur.fetchall()

    def get_membership_stats(self):
        self.cur.execute("""
            SELECT membership_level, COUNT(*) 
            FROM users 
            GROUP BY membership_level
        """)
        return dict(self.cur.fetchall())

    def get_new_user_count(self, days=7):
        self.cur.execute("""
            SELECT COUNT(*) 
            FROM users 
            WHERE first_seen >= datetime('now', '-' || ? || ' days')
        """, (days,))
        return self.cur.fetchone()[0]


    def get_total_checks(self):
        self.cur.execute("SELECT COUNT(*) FROM checks")  # Assuming you have a 'checks' table
        return self.cur.fetchone()[0]

    def get_successful_checks(self):
        self.cur.execute("SELECT COUNT(*) FROM checks WHERE status = 'success'")  # Adjust as per your schema
        return self.cur.fetchone()[0]

    def format_user_list(users, user_type):
        if not users:
            return f"No recent {user_type} users."
        
        user_list = []
        for user in users:
            if user_type == "active":
                user_list.append(f"• {user[1]} (ID: {user[0]}) - Last active: {user[2]}")
            else:
                user_list.append(f"• {user[1]} (ID: {user[0]}) - Registered: {user[2]}")
        
        return "\n".join(user_list)

    def get_startup_message_status(self):
        self.create_settings_table()  # Ensure the table exists
        self.cur.execute("SELECT value FROM settings WHERE key = 'send_startup_message'")
        result = self.cur.fetchone()
        if result is None:
            # If the setting doesn't exist, create it with a default value of True
            self.set_startup_message_status(True)
            return True
        return result[0] == 'True'
    
    def set_startup_message_status(self, status: bool):
        self.create_settings_table()  # Ensure the table exists
        self.cur.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
                        ('send_startup_message', str(status)))
        self.conn.commit()

    def get_user(self, user_id):
        self.cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        return self.cur.fetchone()

    def get_premium_user_count(self):
        self.cur.execute("SELECT COUNT(*) FROM users WHERE membership_level = 'premium'")
        return self.cur.fetchone()[0]

    def get_guide_count(self):
        self.cur.execute("SELECT COUNT(*) FROM guides")
        return self.cur.fetchone()[0]

    def get_all_users(self):
        self.cur.execute("SELECT user_id FROM users")
        return [{"user_id": row[0]} for row in self.cur.fetchall()]

    def update_user_activity(self, user_id):
        current_time = datetime.now().isoformat()
        self.cur.execute("UPDATE users SET last_active = ? WHERE user_id = ?", (current_time, user_id))
        self.conn.commit()

    # New methods for guide management
    def create_guide(self, title, content, format, category):
        current_time = datetime.now().isoformat()
        self.cur.execute('''
        INSERT INTO guides (title, content, format, category, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (title, content, format, category, current_time, current_time))
        self.conn.commit()
        return self.cur.lastrowid

    def get_guide(self, guide_id):
        self.cur.execute("SELECT * FROM guides WHERE id = ?", (guide_id,))
        return self.cur.fetchone()

    def update_guide(self, guide_id, title, content, format, category):
        current_time = datetime.now().isoformat()
        self.cur.execute('''
        UPDATE guides SET 
            title = ?, content = ?, format = ?, category = ?, updated_at = ?
        WHERE id = ?
        ''', (title, content, format, category, current_time, guide_id))
        self.conn.commit()

    def delete_guide(self, guide_id):
        self.cur.execute("DELETE FROM guides WHERE id = ?", (guide_id,))
        self.conn.commit()

    def get_all_guides(self):
        self.cur.execute("SELECT id, title, category FROM guides ORDER BY updated_at DESC")
        return self.cur.fetchall()

    def get_guide_categories(self):
        self.cur.execute("SELECT DISTINCT category FROM guides")
        return [row[0] for row in self.cur.fetchall()]

    def ban_user(self, user_id: int) -> bool:
        try:
            self.cur.execute("UPDATE users SET is_banned = TRUE WHERE user_id = ?", (user_id,))
            self.conn.commit()
            return self.cur.rowcount > 0
        except Exception as e:
            print(f"Error banning user: {e}")
            return False

    def upgrade_user_membership(self, user_id: int) -> bool:
        try:
            self.cur.execute("UPDATE users SET membership_level = 'premium' WHERE user_id = ?", (user_id,))
            self.conn.commit()
            return self.cur.rowcount > 0
        except Exception as e:
            print(f"Error upgrading user membership: {e}")
            return False














    def close(self):
        self.conn.close()

# Initialize database
db = Database('bot_database.db')
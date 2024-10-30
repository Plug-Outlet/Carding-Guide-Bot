# Card Checker Bot

## Overview

This Telegram bot, built with aiogram, provides a card checking service for educational purposes. It offers various features including card validation, user support, and an admin interface.

## Project Structure

<code>Cardbot (2)/
├── bot_database.db
├── config.py
├── DoomsdayCardbot.rar
├── main.py
├── Read Me.txt
├── tree.py
├── init.py
├── filters/
│ ├── admin_filter.py
│ └── pycache/
├── handlers/
│ ├── admin_handlers.py
│ ├── bin_handlers.py
│ ├── cards_functions.py
│ ├── cards_handlers.py
│ ├── guide_handlers.py
│ ├── main_menu.py
│ ├── membership_handler.py
│ ├── ticket_handlers.py
│ ├── user_handlers.py
│ ├── user_managment_handler.py
│ ├── init.py
│ └── pycache/
├── keyboards/
│ ├── admin_keyboard.py
│ ├── bin_keyboard.py
│ ├── cards_keyboard.py
│ ├── guides_keyboard.py
│ ├── misc_keyboard.py
│ ├── ticket_keyboard.py
│ ├── user_keyboard.py
│ ├── init.py
│ └── pycache/
├── utils/
│ ├── admin_utils.py
│ ├── database.py
│ ├── helper.py
│ ├── keyboards.py
│ ├── states.py
│ ├── ticket_utils.py
│ ├── init.py
│ └── pycache/
└── pycache/</code>

## Features

- Card checking functionality
- Multi-page help center
- Admin controls
- User data storage
- Privacy protection

![image](https://github.com/user-attachments/assets/28d41d9b-503f-4b3d-9b4b-9e448a92c01c)


![image](https://github.com/user-attachments/assets/ea808ad3-4801-4ef0-8134-cde939fba218)

![image](https://github.com/user-attachments/assets/3aeb581f-1c3a-407a-8e42-6f2545239134)


![image](https://github.com/user-attachments/assets/051f93b7-a0b1-4202-9861-1b52a4eef661)

![image](https://github.com/user-attachments/assets/cc38c9a6-b691-4be0-b183-70af24e3fc0d)






## Installation

1. Clone the repository:
git clone https://github.com/Plug-Outlet/Carding-Guide-Bot/card-checker-bot.git

2. Install the required dependencies:
 pip install aiogram

3. Set up your bot token in `config.py`:
Replace `BOT_TOKEN` in the code with your actual Telegram Bot Token.

4. Configure the database:
Ensure the path in `DATABASE_PATH` points to your desired database location.

## Usage

Run the main bot script:
python main.py



## Configuration (Config.py)
- `BOT_TOKEN`: Your Telegram Bot Token
- `DATABASE_PATH`: Path to the SQLite database
- `ADMIN_USER_IDS`: List of admin user IDs
- `ADMIN_USERNAMES`: List of admin usernames

## Admin Features

Admins have access to special commands and features for managing the bot. Ensure you add the correct admin user IDs and usernames in the configuration.

## Help Center

The bot includes a multi-page help center with frequently asked questions and answers. Users can navigate through these pages for assistance.

## Legal Disclaimer

This bot is for educational purposes only. Users must comply with local laws and regulations when using this service.

## Support

For bug reports or support requests, please contact [Doomsday X Productions](https://t.me/Doomsday_X_Productions) or use the [GitHub Discussions](https://github.com/Plug-Outlet/Carding-Guide-Bot/discussions) feature.

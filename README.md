# Telegram Certificate Bot

Full Telegram bot for generating paid certificates. Features user registration, admin approval, automatic PDF certificate generation, and QR code verification links.

## Setup Instructions

1. **Clone or copy** the source code into a folder.
2. **Install Python 3.9+** on your machine.
3. **Run the following commands** to set up your environment:
   ```bash
   python -m venv venv
   # Windows: venv\Scripts\activate
   # Linux/Mac: source venv/bin/activate
   pip install -r requirements.txt
   ```
4. **Copy the environment template** and update the variables:
   ```bash
   copy .env.example .env
   # Or directly rename .env.example to .env
   ```
   Open `.env` and configure:
   - `BOT_TOKEN`: Your Telegram Bot token from @BotFather
   - `ADMIN_IDS`: Comma-separated list of Admin Telegram User IDs (e.g., 12345,67890)
   - `BOT_USERNAME`: Your bot's unique username (e.g., mysertibot)
   - `CARD_NUMBER`: Payment card number (e.g., 8600 1234 5678 9012)
5. **Run the Bot**:
   ```bash
   python bot.py
   ```

## Admin Management
- Multiple admins can be configured by adding their IDs separated by commas in the `ADMIN_IDS` environment variable.
- To find your Telegram ID, you can use the `@userinfobot`.

## Architecture
- `aiogram` (v3) is used for routing and handling updates.
- SQLite is used for persistent data storage (`users` and `certificates` tables).
- `reportlab` is used to draw elegant PDF certificates from scratch.
- `qrcode` with PIL generates inline QR codes in the PDF that link back to the bot for quick verification.

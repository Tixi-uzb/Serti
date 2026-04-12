import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
ADMIN_IDS = [int(i.strip()) for i in os.getenv("ADMIN_IDS", "").split(",") if i.strip()]
CARD_NUMBER = os.getenv("CARD_NUMBER", "8600 0000 0000 0000")
PRICE = "10,000 UZS"
BOT_USERNAME = os.getenv("BOT_USERNAME", "YourBotUsername")
VERIFICATION_URL = "https://tixi-uzb.github.io/Serti/"



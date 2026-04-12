from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

def get_start_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Boshlash (Start)", callback_data="start_registration")]
    ])

def get_contact_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📱 Telefon raqamni yuborish", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def get_professions_keyboard():
    professions = [
        "Axborot texnologiyalari",
        "Tikuvchilik",
        "Oshpazlik",
        "Kosmetologiya",
        "Elektrik",
        "Sartaroshlik",
        "Buxgalteriya",
        "Mobil ilovalar yaratish",
        "Dasturlash",
        "Payvandlash",
        "Videomontaj",
        "Xorijiy tillar",
        "Moliyaviy savodxonlik"
    ]
    buttons = []
    for prof in professions:
        buttons.append([InlineKeyboardButton(text=prof, callback_data=f"prof_{prof}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_admin_approval_keyboard(user_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Tasdiqlash", callback_data=f"approve_{user_id}"),
         InlineKeyboardButton(text="❌ Rad etish", callback_data=f"reject_{user_id}")]
    ])

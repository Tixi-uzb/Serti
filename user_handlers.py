import database as db
import keyboards
from config import ADMIN_IDS, CARD_NUMBER, PRICE, BOT_USERNAME
from states import Registration

from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, FSInputFile
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
import os

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    text = message.text
    if text and text.startswith('/start verify_'):
        serial_number = text.split('verify_')[1]
        cert = db.get_certificate(serial_number)
        if cert:
            await message.answer(
                f"✅ <b>Hujjat haqiqiydir!</b>\n\n"
                f"🧑‍💼 <b>Ism-sharif:</b> {cert['full_name']}\n"
                f"🎓 <b>Kasb:</b> {cert['profession']}\n"
                f"📅 <b>Sana:</b> {cert['created_at'].split(' ')[0]}\n"
                f"🔢 <b>Seriya raqami:</b> {cert['serial_number']}",
                parse_mode="HTML"
            )
            if cert.get('file_path') and os.path.exists(cert['file_path']):
                cert_file = FSInputFile(cert['file_path'])
                await message.answer_document(document=cert_file)
        else:
            await message.answer("❌ Bunday seriya raqamiga ega sertifikat topilmadi.")
        return

    db.add_user(message.from_user.id, message.from_user.username)
    await message.answer(
        f"Assalomu alaykum, <b>{message.from_user.first_name}</b>!\n\n"
        f"Bu bot orqali siz o'z kasbingiz bo'yicha rasmiy sertifikat olishingiz mumkin.\n\n"
        f"Sertifikat narxi: <b>{PRICE}</b>\n\n"
        f"Jarayonni boshlash uchun quyidagi tugmani bosing.",
        reply_markup=keyboards.get_start_keyboard(),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "start_registration")
async def process_start_registration(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(
        "Iltimos, telefon raqamingizni yuboring:",
        reply_markup=keyboards.get_contact_keyboard()
    )
    await state.set_state(Registration.waiting_for_contact)
    await callback.answer()

@router.message(Registration.waiting_for_contact, F.contact)
async def process_contact(message: Message, state: FSMContext):
    phone = message.contact.phone_number
    db.update_user_info(message.from_user.id, phone=phone)
    
    await message.answer(
        "Rahmat! Endi sertifikat kimning nomiga berilishini xohlasangiz, o'sha insonning **Ism va Familiyasini** kiriting:",
        reply_markup=ReplyKeyboardRemove(),
        parse_mode="Markdown"
    )
    await state.set_state(Registration.waiting_for_name)

@router.message(Registration.waiting_for_name, F.text)
async def process_name(message: Message, state: FSMContext):
    full_name = message.text
    db.update_user_info(message.from_user.id, full_name=full_name)
    
    await message.answer(
        "Iltimos, kasbingizni tanlang:",
        reply_markup=keyboards.get_professions_keyboard()
    )
    await state.set_state(Registration.waiting_for_profession)

@router.callback_query(Registration.waiting_for_profession, F.data.startswith("prof_"))
async def process_profession(callback: CallbackQuery, state: FSMContext):
    profession = callback.data.split("prof_")[1]
    db.update_user_info(callback.from_user.id, profession=profession)
    
    await callback.message.edit_text(
        f"Kasb tanlandi: <b>{profession}</b>\n\n"
        f"To'lov qilish uchun quyidagi karta raqamiga <b>{PRICE}</b> o'tkazing:\n\n"
        f"💳 Karta: <code>{CARD_NUMBER}</code>\n\n"
        f"To'lovni muvaffaqiyatli amalga oshirgandan so'ng, to'lov skrinshotini (rasmini) shu yerga yuboring.",
        parse_mode="HTML"
    )
    await state.set_state(Registration.waiting_for_payment)
    await callback.answer()

@router.message(Registration.waiting_for_payment, F.photo)
async def process_payment_screenshot(message: Message, state: FSMContext, bot: Bot):
    photo_id = message.photo[-1].file_id
    db.update_user_info(message.from_user.id, status='pending_approval')
    
    user = db.get_user(message.from_user.id)
    
    await message.answer(
        "✅ Rahmat! Sizning so'rovingiz adminga yuborildi. "
        "Admin to'lovni tasdiqlagandan so'ng, sertifikat sizga avtomatik tarzda yuboriladi.\n\n💬 Agar qandaydir muammo bo'lsa yoki ma'lumotlarni o'zgartirmoqchi bo'lsangiz, adminga murojaat qilishingiz mumkin: @Zed003"
    )
    await state.clear()
    
    # Send to admins
    for admin_id in ADMIN_IDS:
        try:
            username_str = f"@{user['username']}" if user.get('username') else "Mavjud emas"
            
            await bot.send_photo(
                chat_id=admin_id,
                photo=photo_id,
                caption=(
                    f"🆕 <b>Yangi sertifikat so'rovi!</b>\n\n"
                    f"👤 <b>Sertifikat egasi:</b> {user['full_name']}\n"
                    f"📱 <b>Telefon:</b> {user['phone']}\n"
                    f"🎓 <b>Kasb:</b> {user['profession']}\n"
                    f"🔗 <b>Username:</b> {username_str}\n"
                    f"🆔 <b>ID:</b> {message.from_user.id}"
                ),
                reply_markup=keyboards.get_admin_approval_keyboard(message.from_user.id),
                parse_mode="HTML"
            )
        except Exception as e:
            print(f"Failed to send to admin {admin_id}: {e}")

@router.message(Registration.waiting_for_payment, ~F.photo)
async def process_invalid_payment(message: Message):
    await message.answer("Iltimos, to'lov holati tasdiqlangan skrinshotni (rasmni) yuboring.")

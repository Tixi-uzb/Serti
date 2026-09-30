import datetime
import uuid
import os

from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, FSInputFile, Message

import database as db
import keyboards
from config import ADMIN_IDS, BOT_USERNAME
from certificate_generator import create_certificate

router = Router()

def generate_serial_number():
    return str(uuid.uuid4().hex)[:10].upper()

@router.callback_query(F.data.startswith("approve_"))
async def approve_payment(callback: CallbackQuery, bot: Bot):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("Siz admin emassiz!", show_alert=True)
        return

    user_id = int(callback.data.split("approve_")[1])
    user = db.get_user(user_id)
    
    if not user or user['status'] == 'approved':
        await callback.answer("Foydalanuvchi topilmadi yoki allaqachon tasdiqlangan.", show_alert=True)
        return
        
    db.update_user_info(user_id, status='approved')
    
    # Generate certificate
    serial_number = generate_serial_number()
    tz = datetime.timezone(datetime.timedelta(hours=5))
    date_str = datetime.datetime.now(tz).strftime("%d.%m.%Y")
    
    await callback.message.edit_caption(
        caption=callback.message.caption + "\n\n✅ <b>Tasdiqlandi!</b> Sertifikat yaratilmoqda...",
        parse_mode="HTML",
        reply_markup=None
    )
    
    try:
        cert_path = create_certificate(
            full_name=user['full_name'],
            profession=user['profession'],
            date_str=date_str,
            serial_number=serial_number,
            bot_username=BOT_USERNAME
        )
        
        db.create_certificate_record(user_id, serial_number, user['profession'], cert_path)
        
        # Send to user
        cert_file = FSInputFile(cert_path)
        await bot.send_document(
            chat_id=user_id,
            document=cert_file,
            caption=(
                f"🎉 <b>Tabriklaymiz!</b> Sizning to'lovingiz tasdiqlandi.\n\n"
                f"Sizning sertifikatingiz tayyor!\n\n"
                f"Seriya raqami: {serial_number}"
            ),
            parse_mode="HTML"
        )
        
        await callback.message.edit_caption(
            caption=callback.message.caption.replace("yaratilmoqda...", "Muvaffaqiyatli yuborildi!"),
            parse_mode="HTML",
            reply_markup=None
        )
        
        # PDF faylni o'chirish
        if os.path.exists(cert_path):
            os.remove(cert_path)

        # Foydalanuvchi ma'lumotlarini bazadan o'chirish
        db.delete_user_data(user_id)
            
    except Exception as e:
        print(f"Error generating certificate: {e}")
        await callback.message.answer(f"Xatolik yuz berdi: {e}")

@router.callback_query(F.data.startswith("reject_"))
async def reject_payment(callback: CallbackQuery, bot: Bot):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("Siz admin emassiz!", show_alert=True)
        return

    user_id = int(callback.data.split("reject_")[1])
    user = db.get_user(user_id)
    
    if not user:
        await callback.answer("Foydalanuvchi topilmadi.", show_alert=True)
        return
        
    db.update_user_info(user_id, status='rejected')
    
    await callback.message.edit_caption(
        caption=callback.message.caption + "\n\n❌ <b>Rad etildi!</b>",
        parse_mode="HTML",
        reply_markup=None
    )
    
    await bot.send_message(
        chat_id=user_id,
        text="❌ Kechirasiz, sizning to'lovingiz tasdiqlanmadi. Iltimos, admin bilan bog'laning yoki qaytadan urinib ko'ring."
    )

    # Rad etilgan foydalanuvchi ma'lumotlarini ham o'chirish
    db.delete_user_data(user_id)

import re
from aiogram.filters import Command

@router.message(Command("send"))
async def admin_send_message(message: Message, bot: Bot):
    if message.from_user.id not in ADMIN_IDS:
        return
        
    parts = message.text.split(maxsplit=2)
    if len(parts) < 3:
        await message.answer("Foydalanish: /send <ID> <xabar>\nMasalan: /send 123456789 Salom")
        return
        
    user_id_str = parts[1]
    text = parts[2]
    
    if not user_id_str.isdigit():
        await message.answer("Xato: ID raqam bo'lishi kerak.")
        return
        
    user_id = int(user_id_str)
    try:
        await bot.send_message(
            chat_id=user_id, 
            text=f"👨‍💻 <b>Markaz ma'muriyati:</b>\n\n{text}", 
            parse_mode="HTML"
        )
        await message.answer(f"✅ Xabar {user_id} ga yuborildi.")
    except Exception as e:
        await message.answer(f"❌ Xabar yuborishda xatolik: {e}")

@router.message(F.reply_to_message)
async def reply_to_user(message: Message, bot: Bot):
    if message.from_user.id not in ADMIN_IDS:
        return
        
    original_msg = message.reply_to_message
    text_to_search = original_msg.caption if original_msg.caption else original_msg.text
    
    if not text_to_search:
        return
        
    match = re.search(r"ID:\s*(\d+)", text_to_search)
    if match:
        user_id = int(match.group(1))
        try:
            await bot.send_message(
                chat_id=user_id, 
                text=f"👨‍💻 <b>Markaz ma'muriyati:</b>\n\n{message.text}", 
                parse_mode="HTML"
            )
            await message.answer("✅ Xabaringiz foydalanuvchiga yuborildi.")
        except Exception as e:
            await message.answer(f"❌ Xatolik yuz berdi. Foydalanuvchi botni bloklagan bo'lishi mumkin.\n{e}")

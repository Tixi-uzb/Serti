import os
import io
import qrcode
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.utils import ImageReader
import urllib.parse


def generate_qr_code(serial_number, verification_url_base, full_name, profession, date_str):
    # Construct the verification link with additional data for a static site
    params = {
        'id': serial_number,
        'name': full_name,
        'prof': profession,
        'date': date_str
    }
    query_string = urllib.parse.urlencode(params)
    separator = '?' if '?' not in verification_url_base else '&'
    verify_link = f"{verification_url_base}{separator}{query_string}"



    
    qr = qrcode.QRCode(
        version=1, 
        error_correction=qrcode.constants.ERROR_CORRECT_H, 
        box_size=10, 
        border=4,
    )
    qr.add_data(verify_link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr

def create_certificate(full_name, profession, date_str, serial_number, bot_username):
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'certs')
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"cert_{serial_number}.pdf")
    
    # QR kod uchun havolani generatsiya qilish
    from config import VERIFICATION_URL
    qr_img = generate_qr_code(serial_number, VERIFICATION_URL, full_name, profession, date_str)


    
    c = canvas.Canvas(file_path, pagesize=landscape(A4))
    width, height = landscape(A4)
    
    # Background and Border
    c.setFillColorRGB(1, 1, 1)
    c.rect(0, 0, width, height, fill=1)
    
    # Ornamental Border (Simulated with multiple lines)
    c.setStrokeColorRGB(0.1, 0.3, 0.7) # Professional Blue to match logo
    c.setLineWidth(4)
    c.rect(30, 30, width-60, height-60, fill=0)
    c.setStrokeColorRGB(0.2, 0.6, 0.4) # Professional Green/Sea-green for inner border
    c.setLineWidth(2)
    c.rect(36, 36, width-72, height-72, fill=0)
    
    # Top Logo Image "user_logo.png"
    logo_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'user_logo.png')
    if os.path.exists(logo_path):
        logo_img = ImageReader(logo_path)
        # Position logo centered at the top - Enlarged
        c.drawImage(logo_img, width/2.0 - 250, height - 140, width=500, height=120, mask='auto', preserveAspectRatio=True)
    
    c.setStrokeColorRGB(0.5, 0.5, 0.5)
    c.setLineWidth(1)
    c.line(width/2.0 - 350, height - 155, width/2.0 - 50, height - 155)
    c.line(width/2.0 + 50, height - 155, width/2.0 + 350, height - 155)
    
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(width/2.0 - 200, height - 175, "KASB-HUNARGA O'QITISH MARKAZI")
    c.drawCentredString(width/2.0 + 200, height - 175, "VOCATIONAL TRAINING CENTER")
    
    # Title
    c.setFillColorRGB(0.1, 0.3, 0.7) # Blue to match logo
    c.setFont("Times-Bold", 40)
    c.drawCentredString(width/2.0, height - 230, "SERTIFIKAT")
    
    # Serial
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width/2.0, height - 260, f"QQ № {serial_number}")
    
    # Candidate Name
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width/2.0, height - 310, full_name.upper())
    
    # Uzbek description
    c.setFont("Helvetica", 14)
    c.drawCentredString(width/2.0, height - 350, f"Onlayn kasb-hunar platformasida {date_str} dagi holatga ko'ra 56 soatli")
    
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width/2.0, height - 375, profession)
    
    c.setFont("Helvetica", 14)
    c.drawCentredString(width/2.0, height - 400, "kasbi bo'yicha (tayyorlash, qayta tayyorlash va malakasini oshirish) kursini to'liq tamomladi.")
    
    # Bottom Layout (QR code, Signatures, Reg info)
    qr_reader = ImageReader(qr_img)
    c.drawImage(qr_reader, 60, 60, width=100, height=100)
    
    # QR kod ostiga yozuv qo'shish
    c.setFont("Helvetica", 7)
    c.drawCentredString(110, 50, "Skaner qiling va tekshiring")
    
    # Deleted Director / Director: D. Raximov section
    
    c.drawString(530, 130, "Ro'yxatga olish raqami")

    c.drawString(530, 115, "(Registration number):")
    c.setFont("Helvetica-Bold", 12)
    c.drawString(680, 120, str(serial_number))
    
    c.setFont("Helvetica", 12)
    c.drawString(530, 90, "Ro'yxatga olish sanasi")
    c.drawString(530, 75, "(Registration date):")
    c.setFont("Helvetica-Bold", 12)
    c.drawString(680, 80, str(date_str))
    
    # Note at bottom
    c.setFont("Helvetica-Oblique", 8)
    note = "Izoh: Ushbu sertifikat egallagan bilimlarni mehnat faoliyatida amalga oshirish huquqini beradi."
    c.drawCentredString(width/2.0, 40, note)
    
    c.showPage()
    c.save()
    
    return file_path

import os
import io
import qrcode
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
import urllib.parse

def generate_qr_code(serial_number, verification_url_base, full_name, profession, date_str):
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
        border=1,
    )
    qr.add_data(verify_link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#0f172a", back_color="white")
    
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr

def create_certificate(full_name, profession, date_str, serial_number, bot_username):
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'certs')
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"cert_{serial_number}.pdf")
    
    from config import VERIFICATION_URL
    qr_img = generate_qr_code(serial_number, VERIFICATION_URL, full_name, profession, date_str)
    
    c = canvas.Canvas(file_path, pagesize=landscape(A4))
    width, height = landscape(A4)
    
    # Background
    c.setFillColor(HexColor("#f8fafc"))
    c.rect(0, 0, width, height, fill=1, stroke=0)
    
    # Main Card Base
    margin = 30
    c.setFillColor(HexColor("#ffffff"))
    c.setStrokeColor(HexColor("#e2e8f0"))
    c.setLineWidth(1)
    c.roundRect(margin, margin, width - 2*margin, height - 2*margin, 12, fill=1, stroke=1)
    
    # Inner Gold Border
    inner_margin = margin + 15
    c.setStrokeColor(HexColor("#d4af37"))
    c.setLineWidth(1.2)
    c.rect(inner_margin, inner_margin, width - 2*inner_margin, height - 2*inner_margin, fill=0, stroke=1)
    
    # Gold Corners
    corner_size = 20
    c.setLineWidth(3)
    c.line(inner_margin-2, height-inner_margin-corner_size, inner_margin-2, height-inner_margin+2)
    c.line(inner_margin-2, height-inner_margin+2, inner_margin+corner_size, height-inner_margin+2)
    c.line(width-inner_margin-corner_size, height-inner_margin+2, width-inner_margin+2, height-inner_margin+2)
    c.line(width-inner_margin+2, height-inner_margin+2, width-inner_margin+2, height-inner_margin-corner_size)
    c.line(inner_margin-2, inner_margin+corner_size, inner_margin-2, inner_margin-2)
    c.line(inner_margin-2, inner_margin-2, inner_margin+corner_size, inner_margin-2)
    c.line(width-inner_margin+2, inner_margin+corner_size, width-inner_margin+2, inner_margin-2)
    c.line(width-inner_margin-corner_size, inner_margin-2, width-inner_margin+2, inner_margin-2)
    
    cx = width / 2.0
    
    # Header Title
    c.setFillColor(HexColor("#334155"))
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(cx, height - 90, "KASB-HUNARGA O'QITISH MARKAZI")
    
    # Main Titles
    c.setFillColor(HexColor("#0f172a"))
    c.setFont("Times-Italic", 46)
    c.drawCentredString(cx, height - 150, "Sertifikat")
    
    c.setFillColor(HexColor("#3b82f6"))
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(cx, height - 180, "C E R T I F I C A T E")
    
    # Name
    c.setFillColor(HexColor("#0f172a"))
    c.setFont("Helvetica-Bold", 30)
    c.drawCentredString(cx, height - 250, full_name.upper())
    
    # Name Underline
    c.setStrokeColor(HexColor("#e2e8f0"))
    c.setLineWidth(2)
    name_width = c.stringWidth(full_name.upper(), "Helvetica-Bold", 30)
    c.line(cx - name_width/2 - 20, height - 265, cx + name_width/2 + 20, height - 265)
    
    # Description 1
    c.setFillColor(HexColor("#475569"))
    c.setFont("Helvetica", 16)
    c.drawCentredString(cx, height - 305, "Onlayn kasb-hunar platformasida 56 soatlik")
    
    # Profession Badge
    c.setFont("Helvetica-Bold", 18)
    prof_width = c.stringWidth(profession, "Helvetica-Bold", 18)
    badge_w = prof_width + 40
    badge_h = 40
    badge_x = cx - badge_w/2
    badge_y = height - 360
    
    c.setFillColor(HexColor("#0f172a"))
    c.roundRect(badge_x, badge_y, badge_w, badge_h, 8, fill=1, stroke=0)
    
    c.setFillColor(HexColor("#ffffff"))
    c.drawCentredString(cx, badge_y + 13, profession)
    
    # Description 2
    c.setFillColor(HexColor("#475569"))
    c.setFont("Helvetica", 16)
    c.drawCentredString(cx, height - 395, "yo'nalishi bo'yicha tayyorlov va malaka oshirish kursini muvaffaqiyatli tamomladi.")
    
    # Bottom Layout (QR and Details)
    qr_y = inner_margin + 15
    qr_x = inner_margin + 20
    
    # Dashed Line separator
    c.setStrokeColor(HexColor("#cbd5e1"))
    c.setLineWidth(1)
    c.setDash(4, 4)
    c.line(inner_margin + 20, qr_y + 115, width - inner_margin - 20, qr_y + 115)
    c.setDash()
    
    # QR Code
    qr_reader = ImageReader(qr_img)
    c.drawImage(qr_reader, qr_x, qr_y + 10, width=90, height=90)
    
    # Skaner qiling matni olib tashlandi
    
    
    # Registration Info (Right side)
    c.setFillColor(HexColor("#94a3b8"))
    c.setFont("Helvetica-Bold", 10)
    c.drawRightString(width - inner_margin - 20, qr_y + 70, "SERIYA RAQAMI")
    c.drawRightString(width - inner_margin - 20, qr_y + 30, "BERILGAN SANA")
    
    c.setFillColor(HexColor("#0f172a"))
    c.setFont("Helvetica-Bold", 18)
    c.drawRightString(width - inner_margin - 20, qr_y + 50, f"#{serial_number}")
    c.drawRightString(width - inner_margin - 20, qr_y + 10, date_str)
    
    c.showPage()
    c.save()
    
    return file_path

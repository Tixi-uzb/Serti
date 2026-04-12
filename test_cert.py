import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from certificate_generator import create_certificate
from config import BOT_USERNAME

def test():
    print("Testing certificate generation...")
    full_name = "Test User"
    profession = "Sifat Nazoratchisi"
    date_str = "11.04.2026"
    serial_number = "TEST12345"
    
    try:
        file_path = create_certificate(full_name, profession, date_str, serial_number, BOT_USERNAME)
        print(f"Success! Certificate created at: {file_path}")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    if test():
        print("Verification complete.")
    else:
        sys.exit(1)

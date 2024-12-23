import random
import datetime
from database import get_db_connection

def generate_otp(phone_number):
    otp = random.randint(100000, 999999)
    expiry = datetime.datetime.now() + datetime.timedelta(minutes=5)

    conn = get_db_connection()
    cursor = conn.cursor()

    # Insert or update OTP
    cursor.execute('''
    INSERT INTO users (phone_number, otp, otp_expiry)
    VALUES (?, ?, ?)
    ON CONFLICT(phone_number) DO UPDATE SET otp = excluded.otp, otp_expiry = excluded.otp_expiry
    ''', (phone_number, otp, expiry))
    conn.commit()
    conn.close()

    # Send OTP via SMS (placeholder for Twilio or another service)
    print(f"OTP for {phone_number}: {otp}")

    return {"success": True, "message": "OTP sent successfully"}

def verify_otp(phone_number, otp):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check OTP
    cursor.execute('''
    SELECT otp, otp_expiry FROM users WHERE phone_number = ?
    ''', (phone_number,))
    user = cursor.fetchone()

    if user and user['otp'] == otp and datetime.datetime.now() < datetime.datetime.fromisoformat(user['otp_expiry']):
        return {"success": True, "message": "OTP verified"}
    else:
        return {"success": False, "message": "Invalid or expired OTP"}
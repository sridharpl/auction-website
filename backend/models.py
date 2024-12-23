from database import get_db_connection

class User:
    @staticmethod
    def get_by_phone(phone_number):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE phone_number = ?', (phone_number,))
        user = cursor.fetchone()
        conn.close()
        return user

    @staticmethod
    def save_otp(phone_number, otp, expiry):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO users (phone_number, otp, otp_expiry)
        VALUES (?, ?, ?)
        ON CONFLICT(phone_number) DO UPDATE SET otp = excluded.otp, otp_expiry = excluded.otp_expiry
        ''', (phone_number, otp, expiry))
        conn.commit()
        conn.close()

class Auction:
    @staticmethod
    def get_active():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
        SELECT * FROM auctions
        WHERE start_time <= datetime('now') AND end_time >= datetime('now')
        LIMIT 1
        ''')
        auction = cursor.fetchone()
        conn.close()
        return auction

    @staticmethod
    def get_last_completed():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
        SELECT * FROM auctions
        WHERE end_time < datetime('now')
        ORDER BY end_time DESC
        LIMIT 1
        ''')
        auction = cursor.fetchone()
        conn.close()
        return auction
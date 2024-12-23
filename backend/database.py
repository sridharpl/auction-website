import sqlite3

DB_PATH = 'auction.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        phone_number TEXT UNIQUE NOT NULL,
        otp TEXT,
        otp_expiry DATETIME
    )
    ''')

    # Auctions table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS auctions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        details TEXT NOT NULL,
        total_quantity INTEGER NOT NULL,
        max_quantity INTEGER NOT NULL,
        min_price REAL NOT NULL,
        max_price REAL NOT NULL,
        increment REAL NOT NULL,
        start_time DATETIME NOT NULL,
        end_time DATETIME NOT NULL
    )
    ''')

    # Bids table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bids (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        auction_id INTEGER NOT NULL,
        phone_number TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        price REAL NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (auction_id) REFERENCES auctions(id)
    )
    ''')

    conn.commit()
    conn.close()

# Initialize database on first run
initialize_database()
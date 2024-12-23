import datetime
from database import get_db_connection

def create_auction(data):
    details = data.get('details')
    total_quantity = data.get('total_quantity')
    max_quantity = data.get('max_quantity')
    min_price = data.get('min_price')
    max_price = data.get('max_price')
    increment = data.get('increment')
    start_time = data.get('start_time')
    end_time = data.get('end_time')

    if not all([details, total_quantity, max_quantity, min_price, max_price, increment, start_time, end_time]):
        return {"success": False, "message": "All fields are required"}

    conn = get_db_connection()
    cursor = conn.cursor()

    # Insert auction
    try:
        cursor.execute('''
        INSERT INTO auctions (details, total_quantity, max_quantity, min_price, max_price, increment, start_time, end_time)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (details, total_quantity, max_quantity, min_price, max_price, increment, start_time, end_time))
        conn.commit()
        conn.close()
        return {"success": True, "message": "Auction created successfully"}
    except Exception as e:
        conn.close()
        return {"success": False, "message": str(e)}

def get_bids(auction_id=None):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch bids
    if auction_id:
        cursor.execute('SELECT * FROM bids WHERE auction_id = ? ORDER BY timestamp DESC', (auction_id,))
    else:
        cursor.execute('SELECT * FROM bids ORDER BY timestamp DESC')

    bids = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return {"success": True, "bids": bids}

def visualize_bids(auction_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch bids for visualization
    cursor.execute('SELECT price, COUNT(*) as bid_count FROM bids WHERE auction_id = ? GROUP BY price ORDER BY price DESC', (auction_id,))
    bid_data = [{"price": row["price"], "bid_count": row["bid_count"]} for row in cursor.fetchall()]

    conn.close()
    return {"success": True, "data": bid_data}
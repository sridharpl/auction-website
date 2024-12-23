from database import get_db_connection
import datetime

def get_auction_stats():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch the active auction
    cursor.execute('''
    SELECT * FROM auctions
    WHERE start_time <= ? AND end_time >= ?
    LIMIT 1
    ''', (datetime.datetime.now(), datetime.datetime.now()))
    auction = cursor.fetchone()

    if not auction:
        conn.close()
        return {"success": False, "message": "No active auction"}

    # Fetch auction stats
    auction_id = auction["id"]
    cursor.execute('''
    SELECT MAX(price) as highest_bid, SUM(quantity) as total_bid_quantity
    FROM bids WHERE auction_id = ?
    ''', (auction_id,))
    stats = cursor.fetchone()

    remaining_quantity = auction["total_quantity"] - (stats["total_bid_quantity"] or 0)
    highest_bid = stats["highest_bid"] or 0

    conn.close()
    return {
        "success": True,
        "auction": dict(auction),
        "remaining_quantity": remaining_quantity,
        "highest_bid": highest_bid,
        "time_remaining": (datetime.datetime.fromisoformat(auction["end_time"]) - datetime.datetime.now()).seconds
    }

def submit_bid(quantity, price):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch the active auction
    cursor.execute('''
    SELECT * FROM auctions
    WHERE start_time <= ? AND end_time >= ?
    LIMIT 1
    ''', (datetime.datetime.now(), datetime.datetime.now()))
    auction = cursor.fetchone()

    if not auction:
        conn.close()
        return {"success": False, "message": "No active auction"}

    # Validate bid
    auction_id = auction["id"]
    if not (auction["min_price"] <= price <= auction["max_price"]):
        return {"success": False, "message": f"Price must be between {auction['min_price']} and {auction['max_price']}"}

    if not (0 < quantity <= auction["max_quantity"]):
        return {"success": False, "message": f"Quantity must be between 1 and {auction['max_quantity']}"}

    # Insert bid
    try:
        cursor.execute('''
        INSERT INTO bids (auction_id, phone_number, quantity, price)
        VALUES (?, ?, ?, ?)
        ''', (auction_id, "PLACEHOLDER_PHONE", quantity, price))  # Replace with the logged-in user's phone
        conn.commit()
        conn.close()
        return {"success": True, "message": "Bid submitted successfully"}
    except Exception as e:
        conn.close()
        return {"success": False, "message": str(e)}

def get_results():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch the last completed auction
    cursor.execute('''
    SELECT * FROM auctions
    WHERE end_time < ?
    ORDER BY end_time DESC
    LIMIT 1
    ''', (datetime.datetime.now(),))
    auction = cursor.fetchone()

    if not auction:
        conn.close()
        return {"success": False, "message": "No completed auction"}

    auction_id = auction["id"]

    # Fetch and sort bids
    cursor.execute('''
    SELECT phone_number, quantity, price
    FROM bids WHERE auction_id = ?
    ORDER BY price DESC, quantity DESC
    ''', (auction_id,))
    bids = cursor.fetchall()

    # Calculate results
    remaining_quantity = auction["total_quantity"]
    results = []
    for bid in bids:
        allocation = 0
        if remaining_quantity > 0:
            if remaining_quantity >= bid["quantity"]:
                allocation = bid["quantity"]
            else:
                allocation = remaining_quantity
            remaining_quantity -= allocation

        results.append({
            "phone_number": bid["phone_number"],
            "allocated_quantity": allocation,
            "price": bid["price"],
        })

    conn.close()
    return {"success": True, "results": results}
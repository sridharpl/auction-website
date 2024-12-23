from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.auth import generate_otp, verify_otp
from utils.auction import get_auction_stats, submit_bid, get_results
from utils.admin import create_auction, get_bids, visualize_bids

app = Flask(__name__)
CORS(app)

# Authentication routes
@app.route('/api/send-otp', methods=['POST'])
def send_otp():
    data = request.json
    phone_number = data.get('phone_number')
    if not phone_number:
        return jsonify({"success": False, "message": "Phone number is required"}), 400

    result = generate_otp(phone_number)
    return jsonify(result)

@app.route('/api/verify-otp', methods=['POST'])
def verify():
    data = request.json
    phone_number = data.get('phone_number')
    otp = data.get('otp')
    if not phone_number or not otp:
        return jsonify({"success": False, "message": "Phone number and OTP are required"}), 400

    result = verify_otp(phone_number, otp)
    return jsonify(result)

# Auction routes
@app.route('/api/auction-stats', methods=['GET'])
def auction_stats():
    stats = get_auction_stats()
    return jsonify(stats)

@app.route('/api/submit-bid', methods=['POST'])
def bid():
    data = request.json
    quantity = data.get('quantity')
    price = data.get('price')
    if quantity is None or price is None:
        return jsonify({"success": False, "message": "Quantity and price are required"}), 400

    result = submit_bid(quantity, price)
    return jsonify(result)

@app.route('/api/results', methods=['GET'])
def results():
    results = get_results()
    return jsonify(results)

# Admin routes
@app.route('/api/admin/create-auction', methods=['POST'])
def create():
    data = request.json
    result = create_auction(data)
    return jsonify(result)

@app.route('/api/admin/bids', methods=['GET'])
def bids():
    bids = get_bids()
    return jsonify(bids)

@app.route('/api/admin/visualize', methods=['GET'])
def visualize():
    visualization = visualize_bids()
    return jsonify(visualization)

if __name__ == '__main__':
    app.run(debug=True)
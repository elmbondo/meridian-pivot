from flask import Flask, jsonify

app = Flask(__name__)

# fake warehouse inventory - pretend this is Northstar's real system
inventory = [
    {"sku": "SKU-001", "name": "Blue Hoodie", "qty": 42},
    {"sku": "SKU-002", "name": "White Sneakers", "qty": 0},
    {"sku": "SKU-003", "name": "Black Cap", "qty": 17},
    {"sku": "SKU-004", "name": "Red Jacket", "qty": 8},
]

@app.route("/stock")
def get_stock():
    return jsonify(inventory)

if __name__ == "__main__":
    app.run(port=5001, debug=True)
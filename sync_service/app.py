from flask import Flask, jsonify
import sqlite3
import requests
import threading
import time

app = Flask(__name__)

DB_PATH = "stock.db"
WAREHOUSE_URL = "http://127.0.0.1:5001/stock"
POLL_INTERVAL_SECONDS = 300  # 5 minutes

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS stock (
            sku TEXT PRIMARY KEY,
            name TEXT,
            qty INTEGER,
            last_updated TEXT
        )
    """)
    conn.commit()
    conn.close()

def poll_warehouse():
    while True:
        try:
            response = requests.get(WAREHOUSE_URL, timeout=5)
            items = response.json()

            conn = sqlite3.connect(DB_PATH)
            for item in items:
                conn.execute("""
                    INSERT INTO stock (sku, name, qty, last_updated)
                    VALUES (?, ?, ?, datetime('now'))
                    ON CONFLICT(sku) DO UPDATE SET
                        name=excluded.name,
                        qty=excluded.qty,
                        last_updated=excluded.last_updated
                """, (item["sku"], item["name"], item["qty"]))
            conn.commit()
            conn.close()
            print(f"Polled warehouse, updated {len(items)} items")
        except Exception as e:
            print(f"Poll failed: {e}")

        time.sleep(POLL_INTERVAL_SECONDS)

@app.route("/stock/<sku>")
def get_stock(sku):
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute("SELECT sku, name, qty, last_updated FROM stock WHERE sku = ?", (sku,)).fetchone()
    conn.close()

    if row is None:
        return jsonify({"error": "SKU not found"}), 404

    return jsonify({"sku": row[0], "name": row[1], "qty": row[2], "last_updated": row[3]})

if __name__ == "__main__":
    init_db()
    poller_thread = threading.Thread(target=poll_warehouse, daemon=True)
    poller_thread.start()
    app.run(port=5002, debug=True, use_reloader=False)
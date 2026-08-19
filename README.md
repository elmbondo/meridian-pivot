 Meridian Pivot - Northstar Inventory Sync



Day 3 build for the Meridian Pivot sprint (PLP). Two-service architecture simulating a live inventory sync between Northstar's warehouse system and a support-facing query service.



 Services

\- `warehouse\_api/` - mock warehouse system exposing `/stock`, standing in for Northstar's real inventory system

\- `sync\_service/` - polls the warehouse every 5 minutes, caches results in SQLite, and exposes `/stock/<sku>` for querying current stock



 Running locally

1\. Create and activate a virtual environment, then `pip install flask requests`

2\. In one terminal: `cd warehouse\_api \&\& python app.py` (runs on port 5001)

3\. In another terminal: `cd sync\_service \&\& python app.py` (runs on port 5002)

4\. Query stock: `http://127.0.0.1:5002/stock/<SKU>`


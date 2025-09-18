from flask import Flask, request, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import json

# Load sheet configuration
with open("sheet_config.json") as f:
    config = json.load(f)

# Setup credentials and client
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Open sheet and tab
sheet = client.open(config["sheet_name"]).worksheet(config["sheet_tab"])
columns = config.get("columns", {})

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.json
        print(f"📩 Incoming webhook data: {data}")

        # Validate required fields
        required_fields = [col["source"] for col in columns.values()]
        if not all(field in data for field in required_fields):
            print("❌ Missing required fields.")
            return jsonify({"error": "Missing required fields"}), 400

        # Ensure timestamp exists
        if "timestamp" not in data:
            data["timestamp"] = datetime.now().strftime("%m/%d/%y %H:%M")

        # Normalize signal
        signal = str(data.get("signal", "")).strip().lower()
        if signal not in ["long", "short"]:
            print("❌ Invalid signal format.")
            return jsonify({"error": "Invalid signal value"}), 400
        data["signal"] = signal.capitalize()

        # Clean numeric fields
        for field in ["entry", "stop", "exit"]:
            data[field] = float(str(data[field]).replace("$", "").replace(",", ""))

        # Get next available row in Column A
        values = sheet.col_values(1)
        next_row = len(values) + 1

        # Build row A–F in correct order
        row_data = []
        for col_letter in sorted(columns.keys()):
            key = columns[col_letter]["source"]
            row_data.append(data.get(key, ""))

        # Write into A:F only
        sheet.update(f"A{next_row}:F{next_row}", [row_data])

        print(f"✅ Trade added to row {next_row}: {row_data}")
        return jsonify({"status": "received"}), 200

    except Exception as e:
        print(f"🔥 Error in webhook: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000)





















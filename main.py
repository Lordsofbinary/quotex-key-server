import json
from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import os

app = Flask(__name__)
from valid_keys import VALID_KEYS

USED_KEYS_FILE = "used_keys.json"

# Load used keys
if os.path.exists(USED_KEYS_FILE):
    with open(USED_KEYS_FILE, "r") as f:
        USED_KEYS = set(json.load(f))
else:
    USED_KEYS = set()

@app.route('/verify', methods=['POST'])
def verify_key():
    data = request.json
    key = data.get('key')
    key_data = VALID_KEYS.get(key)

    if not key_data:
        return jsonify({'status': 'error', 'message': '❌ Invalid Key'}), 401

    # ✅ Handle already used keys gracefully
    if key in USED_KEYS:
        return jsonify({
            "status": "success",
            "message": "🔒 Key Already Used",
            "plan": key_data.get("plan", "lifetime"),
            "expires_at": None if key_data.get("plan") == "lifetime"
                          else (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        }), 200

    # Mark key as used
    USED_KEYS.add(key)
    with open(USED_KEYS_FILE, "w") as f:
        json.dump(list(USED_KEYS), f)

    # Generate expiry based on plan
    if key_data["plan"] == "1month":
        expiry_date = datetime.now() + timedelta(days=30)
        return jsonify({
            "status": "success",
            "plan": "1month",
            "expires_at": expiry_date.strftime("%Y-%m-%d")
        }), 200

    elif key_data["plan"] == "lifetime":
        return jsonify({
            "status": "success",
            "plan": "lifetime",
            "expires_at": None
        }), 200

    return jsonify({'status': 'error', 'message': '❌ Unknown Plan'}), 400

@app.route("/", methods=["GET"])
def home():
    return "🔐 Key Server Running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

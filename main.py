from flask import Flask, request, jsonify

app = Flask(__name__)

# Dummy activation keys — you can update them as needed
VALID_KEYS = {"ABC123", "XYZ456", "LOQ2024"}

@app.route("/verify", methods=["POST"])
def verify_key():
    data = request.get_json()
    user_key = data.get("key")
    return jsonify({"valid": user_key in VALID_KEYS})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
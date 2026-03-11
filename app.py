from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route("/")
def home():
    return "Feishu bot running"

@app.route("/feishu", methods=["POST"])
def feishu():
    data = request.json

    # 飞书验证
    if "challenge" in data:
        return jsonify({"challenge": data["challenge"]})

    print("Received:", data)

    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

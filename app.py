from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

APP_ID = os.environ.get("FEISHU_APP_ID")
APP_SECRET = os.environ.get("FEISHU_APP_SECRET")


@app.route("/")
def home():
    return "Feishu bot running"


def get_tenant_access_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    resp = requests.post(url, json={
        "app_id": APP_ID,
        "app_secret": APP_SECRET
    })
    data = resp.json()
    return data["tenant_access_token"]


def send_message(chat_id, text):
    token = get_tenant_access_token()
    url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "receive_id": chat_id,
        "msg_type": "text",
        "content": "{\"text\":\"" + text + "\"}"
    }
    requests.post(url, headers=headers, json=payload)


@app.route("/feishu", methods=["POST"])
def feishu():
    data = request.json

    if "challenge" in data:
        return jsonify({"challenge": data["challenge"]})

    print("Received:", data)

    chat_id = data["event"]["message"]["chat_id"]
    send_message(chat_id, "你好你好你好你好")

    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

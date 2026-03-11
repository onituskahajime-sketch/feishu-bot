from flask import Flask, request, jsonify
import requests

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

    message = data["event"]["message"]["content"]
    chat_id = data["event"]["message"]["chat_id"]

    send_message(chat_id, "我收到了你的消息")

    return jsonify({"status": "ok"})


def send_message(chat_id, text):

    url = "https://open.feishu.cn/open-apis/im/v1/messages"

    headers = {
        "Authorization": "Bearer YOUR_ACCESS_TOKEN",
        "Content-Type": "application/json"
    }

    payload = {
        "receive_id": chat_id,
        "msg_type": "text",
        "content": {
            "text": text
        }
    }

    requests.post(
        url + "?receive_id_type=chat_id",
        headers=headers,
        json=payload
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

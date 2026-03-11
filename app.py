from flask import Flask, request, jsonify
import requests
import os
import json

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

    # 读取用户发的内容
    content = data["event"]["message"]["content"]

    try:
        text = json.loads(content)["text"]
    except:
        text = content

    print("User said:", text)

    # 如果用户说 "日报"
    if "日报" in text:
        records = get_table_records()
        report = build_daily_report(records)
        send_message(chat_id, report)

    else:
        send_message(chat_id, "你好你好你好你好你好")

    return jsonify({"status": "ok"})


def get_table_records():
    token = get_tenant_access_token()

    app_token = "XZ0Tbz2lKakp6Nsy3Suc1Sgnud"
    table_id = "tblHz7TeQBFu8Nl38"

    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    resp = requests.get(url, headers=headers)
    data = resp.json()

    return data["data"]["items"]


def build_daily_report(records):

    projects = {}

    for r in records:
        fields = r["fields"]

        project = fields.get("项目", "未知项目")
        task = fields.get("镜头/任务", "")
        step = fields.get("环节", "")
        person = fields.get("人员", "")
        date = fields.get("预计提交", "")

        line = f"{task}｜{step}｜{person}｜预计{date}"

        if project not in projects:
            projects[project] = []

        projects[project].append(line)

    text = "【动画项目日报】\n\n"

    for p in projects:
        text += f"{p}\n"
        for l in projects[p]:
            text += l + "\n"
        text += "\n"

    return text


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

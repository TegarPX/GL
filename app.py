from flask import Flask, request
import datetime
import os
import requests  # ⬅️ tambah ini

app = Flask(__name__)

LOG_FILE = "logs.txt"
SECRET_KEY = "kaze123"

WEBHOOK_URL = "https://discord.com/api/v10/webhooks/1442080509587886112/BkLaXIlaozElIt6EXyPuCFTM4GlKbLeBf9tLhGvIThXJze22NqURKDi1uZR8fkk0lIwH"

@app.route("/log")
def log():
    key = request.args.get("key")
    if key != SECRET_KEY:
        return "Unauthorized", 403

    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    data = dict(request.args)
    data.pop("key", None)

    log_line = f"[{time}] IP: {ip} | DATA: {data}\n"

    # simpan ke file
    with open(LOG_FILE, "a") as f:
        f.write(log_line)

    # =========================
    # 🔥 DISCORD WEBHOOK
    # =========================
    if data.get("action") == "Growlauncher":
        try:
            payload = {
                "content": f"🚀 **Growlauncher Triggered!**\n"
                           f"IP: {ip}\n"
                           f"Data: {data}\n"
                           f"Time: {time}"
            }
            requests.post(WEBHOOK_URL, json=payload, timeout=5)
        except Exception as e:
            print("Webhook error:", e)

    return "LOGGED"

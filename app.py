from flask import Flask, request
import datetime
import os

app = Flask(__name__)

LOG_FILE = "logs.txt"
SECRET_KEY = "kaze123"  # ganti sesuai keinginan

# =========================
# Endpoint Logger
# =========================
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

    with open(LOG_FILE, "a") as f:
        f.write(log_line)

    return "LOGGED"


# =========================
# Console Viewer
# =========================
@app.route("/")
def index():
    if not os.path.exists(LOG_FILE):
        open(LOG_FILE, "w").close()

    with open(LOG_FILE, "r") as f:
        logs = f.read()

    return f"""
    <html>
    <head>
        <title>Logger Console</title>
        <meta http-equiv="refresh" content="2">
        <style>
            body {{
                background: #0d1117;
                color: #00ff88;
                font-family: monospace;
                padding: 20px;
            }}
        </style>
    </head>
    <body>
        <h2>🖥️ Logger Console</h2>
        <p>Endpoint: /log?key={SECRET_KEY}</p>
        <pre>{logs if logs else "No logs yet..."}</pre>
    </body>
    </html>
    """


# =========================
# Run (Railway Compatible)
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

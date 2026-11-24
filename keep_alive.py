"""
keep_alive.py  -  Flask web server + Auto Ping (Render ko sleep hone se rokta hai)

Env variables:
  PORT            -> Render khud set karta hai
  RENDER_EXTERNAL_URL -> Render khud set karta hai (https://yourapp.onrender.com)
  PING_URL        -> (optional) manually URL dena ho to
  PING_INTERVAL   -> seconds, default 5
"""
import os
import time
import logging
import threading
from datetime import datetime

import requests
from flask import Flask, jsonify

# Flask ke har request ka log band (5 sec ping se logs bhar jaate)
logging.getLogger('werkzeug').setLevel(logging.ERROR)
logger = logging.getLogger("keep_alive")

app = Flask(__name__)

START_TIME = datetime.now()
ping_stats = {"success": 0, "failed": 0, "last_ping": None, "last_status": None}


@app.route('/')
def home():
    return "I'am Atx File Host - Bot is alive ✅"


@app.route('/health')
def health():
    uptime = str(datetime.now() - START_TIME).split('.')[0]
    return jsonify(status="ok", uptime=uptime, ping=ping_stats)


def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port, threaded=True, use_reloader=False)


def _get_ping_url():
    base = os.environ.get("PING_URL") or os.environ.get("RENDER_EXTERNAL_URL")
    if base:
        return base.rstrip('/') + '/health'
    port = int(os.environ.get("PORT", 8080))
    return f"http://127.0.0.1:{port}/health"


def auto_ping():
    interval = max(1, int(os.environ.get("PING_INTERVAL", 5)))
    url = _get_ping_url()
    logger.info(f"Auto-ping started: {url} every {interval}s")
    time.sleep(10)  # server start hone do
    while True:
        try:
            r = requests.get(url, timeout=10)
            ping_stats["success"] += 1
            ping_stats["last_status"] = r.status_code
        except Exception as e:
            ping_stats["failed"] += 1
            ping_stats["last_status"] = str(e)[:80]
        ping_stats["last_ping"] = datetime.now().strftime("%H:%M:%S")
        time.sleep(interval)


def keep_alive():
    threading.Thread(target=run_flask, daemon=True).start()
    threading.Thread(target=auto_ping, daemon=True).start()
    print("Flask Keep-Alive + Auto-Ping (every %ss) started." % os.environ.get("PING_INTERVAL", 5))

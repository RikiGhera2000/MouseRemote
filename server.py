from __future__ import annotations

import json
import socket
from typing import Any

import pyautogui
import qrcode
from flask import Flask, render_template
from flask_sock import Sock


HOST = "0.0.0.0"
PORT = 5000
MAX_DELTA = 300
MAX_SCROLL = 100
SHIFTED_KEYS = {
    "!": ("1", True), "@": ("2", True), "#": ("3", True), "$": ("4", True),
    "%": ("5", True), "^": ("6", True), "&": ("7", True), "*": ("8", True),
    "(": ("9", True), ")": ("0", True), "_": ("-", True), "+": ("=", True),
    "{": ("[", True), "}": ("]", True), "|": ("\\", True), ":": (";", True),
    '"': ("'", True), "<": (",", True), ">": (".", True), "?": ("/", True),
    "~": ("`", True),
}

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
sock = Sock(app)
pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False


@app.after_request
def disable_browser_cache(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


def get_local_ip() -> str:
    """Return the LAN address used to reach the internet, if available."""
    probe = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        probe.connect(("8.8.8.8", 80))
        return probe.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        probe.close()


def bounded_number(value: Any, default: float = 0, limit: float = MAX_DELTA) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return default
    return max(-limit, min(limit, value))


@app.get("/")
def index():
    return render_template("index.html")


@sock.route("/mouse")
def mouse(ws):
    held_buttons: set[str] = set()
    while True:
        raw = ws.receive()
        if raw is None:
            break
        try:
            event = json.loads(raw)
        except (json.JSONDecodeError, TypeError):
            continue
        if not isinstance(event, dict):
            continue

        kind = event.get("type")
        try:
            if kind == "move":
                dx = bounded_number(event.get("dx"))
                dy = bounded_number(event.get("dy"))
                pyautogui.moveRel(dx, dy, duration=0)
            elif kind == "click":
                button = event.get("button", "left")
                if button in ("left", "right", "middle"):
                    pyautogui.click(button=button)
            elif kind == "double":
                pyautogui.doubleClick()
            elif kind == "down":
                button = event.get("button", "left")
                if button in ("left", "right", "middle") and button not in held_buttons:
                    pyautogui.mouseDown(button=button)
                    held_buttons.add(button)
            elif kind == "up":
                button = event.get("button", "left")
                if button in held_buttons:
                    pyautogui.mouseUp(button=button)
                    held_buttons.discard(button)
            elif kind == "scroll":
                amount = bounded_number(event.get("amount"), limit=MAX_SCROLL)
                pyautogui.scroll(int(amount))
            elif kind == "key":
                key = event.get("key")
                shift = bool(event.get("shift"))
                if isinstance(key, str) and key in SHIFTED_KEYS:
                    key, shifted = SHIFTED_KEYS[key]
                    shift = shift or shifted
                if isinstance(key, str) and key in pyautogui.KEYBOARD_KEYS:
                    if shift and key not in ("shift", "ctrl", "alt"):
                        pyautogui.hotkey("shift", key)
                    else:
                        pyautogui.press(key)
        except (OSError, pyautogui.FailSafeException):
            # A desktop-side interruption should not take down the web server.
            continue

    for button in held_buttons:
        try:
            pyautogui.mouseUp(button=button)
        except (OSError, pyautogui.FailSafeException):
            pass


def print_qr(url: str) -> None:
    code = qrcode.QRCode(version=None, box_size=1, border=1)
    code.add_data(url)
    code.make(fit=True)
    code.print_ascii(invert=True)


if __name__ == "__main__":
    url = f"http://{get_local_ip()}:{PORT}"
    print("\n" + "=" * 52)
    print("                 MOUSE REMOTE")
    print("=" * 52)
    print(f"PC:     http://localhost:{PORT}")
    print(f"iPhone: {url}\n")
    print("Scansiona il QR code con l'iPhone:\n")
    print_qr(url)
    print("\nServer attivo. Premi CTRL+C per chiuderlo.\n")
    app.run(host=HOST, port=PORT, debug=False, threaded=True)

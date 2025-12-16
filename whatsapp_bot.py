# whatsapp_bot.py

from whatsapp_api import Client
from whatsapp_engine import handle_message
import json
import os

# -----------------------------
# Load authorized users
# -----------------------------

AUTH_FILE = "authorized_users.json"

def load_authorized_users():
    if os.path.exists(AUTH_FILE):
        with open(AUTH_FILE, "r") as f:
            return json.load(f)
    return {}

AUTHORIZED_USERS = load_authorized_users()

# -----------------------------
# WhatsApp Client
# -----------------------------

client = Client()

@client.on_message
def on_message(message):
    try:
        sender = "+" + message.author.id  # normalize number
        text = message.text.strip()

        print(f"[WA] {sender}: {text}")

        reply = handle_message(sender, text, AUTHORIZED_USERS)

        if reply:
            message.reply(reply)

    except Exception as e:
        print("Error handling message:", e)

# -----------------------------
# START BOT
# -----------------------------

print("📱 Scan QR code to login to WhatsApp...")
client.run()

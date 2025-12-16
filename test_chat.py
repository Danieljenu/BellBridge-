# test_chat.py

from whatsapp_engine import handle_message

AUTHORIZED_USERS = {
    "+911111111111": "principal",
    "+922222222222": "teacher",
    "+933333333333": "developer"
}

number = "+933333333333"

while True:
    msg = input("YOU: ")
    reply = handle_message(number, msg, AUTHORIZED_USERS)
    print("BOT:", reply)
    
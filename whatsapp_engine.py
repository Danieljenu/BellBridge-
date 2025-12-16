# whatsapp_engine.py

from typing import Dict

# -----------------------------
# USER STATES
# -----------------------------

USER_STATE: Dict[str, str] = {}   # number -> state
USER_ROLE: Dict[str, str] = {}    # number -> role

# -----------------------------
# MENUS
# -----------------------------

def main_menu(role: str) -> str:
    if role == "principal":
        return (
            "JOTHI – Smart Bell & Assembly System\n\n"
            "Main Menu:\n"
            "1. Announcement\n"
            "2. About Us\n"
            "0. Exit"
        )

    if role == "teacher":
        return (
            "JOTHI – Smart Bell & Assembly System\n\n"
            "Main Menu:\n"
            "1. Bell Mode\n"
            "2. Assembly\n"
            "3. About Us\n"
            "0. Exit"
        )

    # developer
    return (
        "JOTHI – Smart Bell & Assembly System\n\n"
        "Main Menu:\n"
        "1. Bell Mode\n"
        "2. Assembly\n"
        "3. Announcement\n"
        "4. Settings\n"
        "5. About Us\n"
        "0. Exit"
    )

# -----------------------------
# ENTRY POINT
# -----------------------------

def handle_message(number: str, text: str, authorized_users: dict) -> str:
    text = text.strip()
    # 🔒 AUTH CHECK
    if number not in authorized_users:
        return (
            "❌ Access denied.\n"
            "You are not authorized to use JOTHI system."
        )

    role = authorized_users[number]
    USER_ROLE[number] = role

    # INIT STATE
    if number not in USER_STATE or text.lower() in ("hello", "hi", "/help"):
        USER_STATE[number] = "MAIN"
        return main_menu(role)

    state = USER_STATE[number]

    # -----------------------------
    # MAIN MENU HANDLER
    # -----------------------------
    if state == "MAIN":
        return handle_main_menu(number, text)

    # -----------------------------
    # FALLBACK
    # -----------------------------
    return "❌ Invalid command.\nPlease choose a valid option."


# -----------------------------
# MAIN MENU LOGIC
# -----------------------------

def handle_main_menu(number: str, choice: str) -> str:
    role = USER_ROLE[number]

    if choice == "0":
        USER_STATE[number] = "MAIN"
        return (
            "Exited from JOTHI system.\n"
            "Type 'hello' to start again."
        )

    if role == "principal":
        if choice == "1":
            USER_STATE[number] = "ANNOUNCEMENT"
            return "Announcement mode selected."
        if choice == "2":
            return load_about_us()

    if role == "teacher":
        if choice == "1":
            USER_STATE[number] = "BELL"
            return "Bell mode selected."
        if choice == "2":
            USER_STATE[number] = "ASSEMBLY"
            return "Assembly mode selected."
        if choice == "3":
            return load_about_us()

    if role == "developer":
        if choice == "1":
            USER_STATE[number] = "BELL"
            return "Bell mode selected."
        if choice == "2":
            USER_STATE[number] = "ASSEMBLY"
            return "Assembly mode selected."
        if choice == "3":
            USER_STATE[number] = "ANNOUNCEMENT"
            return "Announcement mode selected."
        if choice == "4":
            USER_STATE[number] = "SETTINGS"
            return "Settings mode selected."
        if choice == "5":
            return load_about_us()

    return "❌ Invalid option.\nPlease select from the menu."

# -----------------------------
# ABOUT US
# -----------------------------

def load_about_us():
    try:
        with open("about_us.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "About Us file not found."

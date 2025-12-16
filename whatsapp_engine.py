# whatsapp_engine.py

from typing import Dict

# -----------------------------
# USER STATE & ROLE
# -----------------------------

USER_STATE: Dict[str, str] = {}   # number -> state
USER_ROLE: Dict[str, str] = {}    # number -> role

# -----------------------------
# MENU TEXTS
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


def bell_menu_text():
    return (
        "BELL MODE:\n"
        "1. Set Today’s Bell Times\n"
        "2. Use Saved Schedule\n"
        "3. Edit Schedule\n"
        "4. Create Schedule\n"
        "5. Delete Schedule\n"
        "0. Back"
    )


def assembly_menu_text():
    return (
        "ASSEMBLY MODE:\n"
        "1. Prayer\n"
        "2. Birthday Song\n"
        "3. National Anthem\n"
        "4. Extra Audio 1\n"
        "5. Extra Audio 2\n"
        "6. Ring Bell (5 sec)\n"
        "0. Back"
    )


def announcement_menu_text():
    return (
        "ANNOUNCEMENT MODE:\n"
        "1. Robert (Male)\n"
        "2. Zara (Female)\n"
        "3. Orion (Deep)\n"
        "0. Back"
    )


def settings_menu_text():
    return (
        "SETTINGS:\n"
        "1. Change National Anthem\n"
        "2. Change Assembly Bell\n"
        "3. Set Extra Audio 1\n"
        "4. Set Extra Audio 2\n"
        "5. Change Prayer/Birthday Files\n"
        "6. Manage Authorized Users\n"
        "0. Back"
    )

# -----------------------------
# ENTRY POINT
# -----------------------------

def handle_message(number: str, text: str, authorized_users: dict) -> str:
    text = text.strip()

    # 🔒 Authorization
    if number not in authorized_users:
        return "❌ Access denied.\nYou are not authorized."

    role = authorized_users[number]
    USER_ROLE[number] = role

    # Init
    if number not in USER_STATE or text.lower() in ("hello", "hi", "/help"):
        USER_STATE[number] = "MAIN"
        return main_menu(role)

    state = USER_STATE[number]

    # Route by state
    if state == "MAIN":
        return handle_main_menu(number, text)

    if state == "BELL":
        return handle_bell_menu(number, text)

    if state == "ASSEMBLY":
        return handle_assembly_menu(number, text)

    if state == "ANNOUNCEMENT":
        return handle_announcement_menu(number, text)

    if state == "SETTINGS":
        return handle_settings_menu(number, text)

    return "❌ Invalid command."

# -----------------------------
# MAIN MENU HANDLER
# -----------------------------

def handle_main_menu(number: str, choice: str) -> str:
    role = USER_ROLE[number]

    if choice == "0":
        USER_STATE[number] = "MAIN"
        return "Exited.\nType 'hello' to start again."

    if role == "principal":
        if choice == "1":
            USER_STATE[number] = "ANNOUNCEMENT"
            return announcement_menu_text()
        if choice == "2":
            return load_about_us()

    if role == "teacher":
        if choice == "1":
            USER_STATE[number] = "BELL"
            return bell_menu_text()
        if choice == "2":
            USER_STATE[number] = "ASSEMBLY"
            return assembly_menu_text()
        if choice == "3":
            return load_about_us()

    if role == "developer":
        if choice == "1":
            USER_STATE[number] = "BELL"
            return bell_menu_text()
        if choice == "2":
            USER_STATE[number] = "ASSEMBLY"
            return assembly_menu_text()
        if choice == "3":
            USER_STATE[number] = "ANNOUNCEMENT"
            return announcement_menu_text()
        if choice == "4":
            USER_STATE[number] = "SETTINGS"
            return settings_menu_text()
        if choice == "5":
            return load_about_us()

    return "❌ Invalid option.\nChoose again."

# -----------------------------
# SUB-MENU HANDLERS (BASIC)
# -----------------------------

def handle_bell_menu(number, choice):
    if choice == "0":
        USER_STATE[number] = "MAIN"
        return main_menu(USER_ROLE[number])

    return "⏳ Bell action recorded.\n(Execution will be connected later)\n\n" + bell_menu_text()


def handle_assembly_menu(number, choice):
    if choice == "0":
        USER_STATE[number] = "MAIN"
        return main_menu(USER_ROLE[number])

    return "▶ Assembly action triggered.\n\n" + assembly_menu_text()


def handle_announcement_menu(number, choice):
    if choice == "0":
        USER_STATE[number] = "MAIN"
        return main_menu(USER_ROLE[number])

    return "🔊 Announcement voice selected.\n\n" + announcement_menu_text()


def handle_settings_menu(number, choice):
    if choice == "0":
        USER_STATE[number] = "MAIN"
        return main_menu(USER_ROLE[number])

    return "⚙ Settings updated.\n\n" + settings_menu_text()

# -----------------------------
# ABOUT US
# -----------------------------

def load_about_us():
    try:
        with open("about_us.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "About Us file not found."

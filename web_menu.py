from main import parse_time_to_24h, format_time_tuple


from flask import Flask, request, redirect, url_for, render_template_string
import threading

from main import (
    ringBell,
    ring_assembly_bell,
    play_audio_blocking,
    BELL_SCHEDULES,
    get_today_assembly_config,
    NATIONAL_ANTHEM_FILE,
    ASSEMBLY_BELL_FILE,
    EXTRA1_FILE,
    EXTRA2_FILE,
    speak_robert,
    speak_zara,
    speak_orion
)

app = Flask(__name__)

# -------------------------------------------------
# GLOBAL STATUS (USED BY WEB + FUTURE WHATSAPP)
# -------------------------------------------------
SYSTEM_STATUS = {
    "mode": "IDLE",
    "message": "System idle"
}

def set_status(mode, msg):
    SYSTEM_STATUS["mode"] = mode
    SYSTEM_STATUS["message"] = msg

# -------------------------------------------------
#help us read about us info from a file
# -------------------------------------------------

def load_about_us():
    try:
        with open("about_us.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "About Us file (about_us.txt) not found."

# -------------------------------------------------
# HTML TEMPLATE
# -------------------------------------------------
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>JOTHI – Smart Bell System</title>
</head>
<body>
    <h1>JOTHI – Smart Bell & Assembly System</h1>

    <p><b>Status:</b> {{ status.mode }} — {{ status.message }}</p>
    <hr>

    <h2>Main Menu</h2>
    <form action="/bell-menu"><button>🔔 Bell Mode</button></form>
    <form action="/assembly-menu"><button>📢 Assembly</button></form>
    <form action="/announcement"><button>🗣 Announcement</button></form>
    <form action="/settings"><button>⚙ Settings</button></form>
    <form action="/about"><button>ℹ About Us</button></form>

    {% if menu == "bell" %}
        <hr>
        <h2>Bell Mode</h2>

        {% for name, times in schedules.items() %}
            <form action="/start-schedule/{{ name }}">
                <button>▶ {{ name }} ({{ ", ".join(times) }})</button>
            </form>
        {% endfor %}

        <h3>Today Only</h3>
        <form method="post" action="/start-today">
            <input name="times" placeholder="09:00,10:30,12:00" required>
            <button>▶ Start Today Schedule</button>
        </form>

        <form action="/"><button>⬅ Back</button></form>
    {% endif %}

    {% if menu == "assembly" %}
        <hr>
        <h2>Assembly</h2>
        <form action="/assembly/prayer"><button>🙏 Prayer</button></form>
        <form action="/assembly/birthday"><button>🎂 Birthday</button></form>
        <form action="/assembly/anthem"><button>🇮🇳 Anthem</button></form>
        <form action="/assembly/bell"><button>🔔 Bell (5 sec)</button></form>
        <form action="/"><button>⬅ Back</button></form>
    {% endif %}

    {% if menu == "announce" %}
        <hr>
        <h2>Announcement</h2>
        <form method="post" action="/announce">
            <input name="text" placeholder="Type announcement" required>
            <select name="voice">
                <option value="robert">Robert (Formal)</option>
                <option value="zara">Zara (Energetic)</option>
                <option value="orion">Orion (Deep)</option>
            </select>
            <button>Speak</button>
        </form>
        <form action="/"><button>⬅ Back</button></form>
    {% endif %}

    {% if menu == "settings" %}
        <hr>
        <h2>Settings</h2>
        <form method="post" action="/settings/update">
            National Anthem:
            <input name="anthem" placeholder="{{ anthem }}"><br><br>
            Assembly Bell:
            <input name="bell" placeholder="{{ bell }}"><br><br>
            Extra Audio 1:
            <input name="extra1" placeholder="{{ extra1 }}"><br><br>
            Extra Audio 2:
            <input name="extra2" placeholder="{{ extra2 }}"><br><br>
            <button>Save Settings</button>
        </form>
        <form action="/"><button>⬅ Back</button></form>
    {% endif %}

{% if menu == "about" %}
    <hr>
    <h2>About Us</h2>
    <pre>{{ about_text }}</pre>
    <form action="/"><button>⬅ Back</button></form>
{% endif %}
</body>
</html>
"""

# -------------------------------------------------
# ROUTES
# -------------------------------------------------

@app.route("/")
def home():
    return render_template_string(HTML, menu=None, status=SYSTEM_STATUS)

@app.route("/bell-menu")
def bell_menu():
    return render_template_string(
        HTML,
        menu="bell",
        schedules=BELL_SCHEDULES,
        status=SYSTEM_STATUS
    )

@app.route("/start-schedule/<name>")
def start_schedule(name):
    schedule = BELL_SCHEDULES.get(name)
    if schedule:
        set_status("BELL", f"Running {name} ({', '.join(schedule)})")
        threading.Thread(target=ringBell, args=(schedule,)).start()
    return redirect(url_for("bell_menu"))

@app.route("/start-today", methods=["POST"])
def start_today():
    times = request.form.get("times", "")
    raw_times = [t.strip() for t in times.split(",") if t.strip()]
    schedule = []

    for t in raw_times:
        try:
            canonical = parse_time_to_24h(t)   # "7" -> "07:00"
            schedule.append(canonical)
        except Exception:
            pass  # ignore invalid entries

    if schedule:
        set_status("BELL", f"Running today-only schedule ({', '.join(schedule)})")
        threading.Thread(
            target=ringBell,
            args=(schedule,),
            kwargs={"today_only": True}
        ).start()
    return redirect(url_for("bell_menu"))

@app.route("/assembly-menu")
def assembly_menu():
    set_status("ASSEMBLY", "Assembly control active")
    return render_template_string(HTML, menu="assembly", status=SYSTEM_STATUS)

@app.route("/assembly/prayer")
def prayer():
    _, _, cfg = get_today_assembly_config()
    threading.Thread(target=play_audio_blocking, args=(cfg["prayer"],)).start()
    set_status("ASSEMBLY", "Playing prayer")
    return redirect(url_for("assembly_menu"))

@app.route("/assembly/birthday")
def birthday():
    _, _, cfg = get_today_assembly_config()
    threading.Thread(target=play_audio_blocking, args=(cfg["birthday"],)).start()
    set_status("ASSEMBLY", "Playing birthday song")
    return redirect(url_for("assembly_menu"))

@app.route("/assembly/anthem")
def anthem():
    threading.Thread(target=play_audio_blocking, args=(NATIONAL_ANTHEM_FILE,)).start()
    set_status("ASSEMBLY", "Playing national anthem")
    return redirect(url_for("assembly_menu"))

@app.route("/assembly/bell")
def assembly_bell():
    threading.Thread(target=ring_assembly_bell, args=(5,)).start()
    set_status("ASSEMBLY", "Assembly bell ringing")
    return redirect(url_for("assembly_menu"))

@app.route("/announcement")
def announcement():
    set_status("ANNOUNCEMENT", "Waiting for announcement")
    return render_template_string(HTML, menu="announce", status=SYSTEM_STATUS)

@app.route("/announce", methods=["POST"])
def announce():
    text = request.form.get("text")
    voice = request.form.get("voice")

    if text:
        if voice == "zara":
            threading.Thread(target=speak_zara, args=(text,)).start()
            set_status("ANNOUNCEMENT", "Announcement by Zara")
        elif voice == "orion":
            threading.Thread(target=speak_orion, args=(text,)).start()
            set_status("ANNOUNCEMENT", "Announcement by Orion")
        else:
            threading.Thread(target=speak_robert, args=(text,)).start()
            set_status("ANNOUNCEMENT", "Announcement by Robert")
    return redirect(url_for("announcement"))

@app.route("/settings")
def settings():
    return render_template_string(
        HTML,
        menu="settings",
        status=SYSTEM_STATUS,
        anthem=NATIONAL_ANTHEM_FILE,
        bell=ASSEMBLY_BELL_FILE,
        extra1=EXTRA1_FILE or "",
        extra2=EXTRA2_FILE or ""
    )

@app.route("/settings/update", methods=["POST"])
def update_settings():
    global NATIONAL_ANTHEM_FILE, ASSEMBLY_BELL_FILE, EXTRA1_FILE, EXTRA2_FILE

    if request.form.get("anthem"):
        NATIONAL_ANTHEM_FILE = request.form.get("anthem")
    if request.form.get("bell"):
        ASSEMBLY_BELL_FILE = request.form.get("bell")
    if request.form.get("extra1"):
        EXTRA1_FILE = request.form.get("extra1")
    if request.form.get("extra2"):
        EXTRA2_FILE = request.form.get("extra2")

    set_status("SETTINGS", "Settings updated")
    return redirect(url_for("settings"))

@app.route("/about")
def about():
    about_text = load_about_us()
    return render_template_string(
        HTML,
        menu="about",
        status=SYSTEM_STATUS,
        about_text=about_text
    )

# -------------------------------------------------
# RUN
# -------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)

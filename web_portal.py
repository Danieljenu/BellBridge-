from flask import Flask, render_template_string
import threading

# IMPORT FUNCTIONS FROM YOUR EXISTING FILE
# ⚠️ change filename if needed
from main import ring_assembly_bell, play_audio_blocking

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>School Bell Control</title>
</head>
<body>
    <h1>School Bell – Web Control</h1>

    <form action="/bell">
        <button>🔔 Ring Bell (5 sec)</button>
    </form>

    <form action="/anthem">
        <button>🇮🇳 Play National Anthem</button>
    </form>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/bell")
def bell():
    threading.Thread(target=ring_assembly_bell, args=(5,)).start()
    return "<p>Bell rung. <a href='/'>Back</a></p>"

@app.route("/anthem")
def anthem():
    threading.Thread(
        target=play_audio_blocking,
        args=("national_anthem.mp3",)
    ).start()
    return "<p>Anthem playing. <a href='/'>Back</a></p>"

if __name__ == "__main__":
    app.run(debug=True)

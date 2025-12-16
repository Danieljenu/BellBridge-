# whatsapp_connector.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

driver = None
connected = False

def connect_whatsapp():
    global driver, connected

    if driver is not None:
        return True

    options = webdriver.ChromeOptions()
    options.add_argument("--user-data-dir=./wa_session")  # keeps login

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    driver.get("https://web.whatsapp.com")
    print("📱 WhatsApp Web opened.")

    # Wait for QR scan or existing login
    for _ in range(60):
        time.sleep(2)
        try:
            driver.find_element(By.ID, "pane-side")
            connected = True
            print("✅ WhatsApp Connected")
            return True
        except:
            print("⌛ Waiting for QR scan...")

    print("❌ QR not scanned in time.")
    return False


def is_connected():
    return connected


def read_latest_messages():
    """
    VERY BASIC message reader (for demo).
    Reads visible chat messages.
    """
    if not connected:
        return []

    messages = []
    try:
        msg_elements = driver.find_elements(By.CSS_SELECTOR, "span.selectable-text")
        for el in msg_elements[-5:]:
            messages.append(el.text)
    except:
        pass

    return messages

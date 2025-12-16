# whatsapp_bot.py

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from whatsapp_engine import handle_message

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time


def start_whatsapp():
    chrome_options = Options()

    # IMPORTANT FLAGS (fix crash)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("--remote-debugging-port=9222")

    # Use a FRESH Chrome profile (avoid crashes)
    chrome_options.add_argument("--user-data-dir=./chrome_profile")

    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(
        service=service,
        options=chrome_options
    )

    driver.get("https://web.whatsapp.com")
    print("📱 Waiting for QR / WhatsApp login...")

    # Wait until WhatsApp loads
    while True:
        try:
            driver.find_element("id", "pane-side")
            print("✅ WhatsApp Connected")
            break
        except:
            time.sleep(2)

    return driver



def listen_messages(driver):
    last_message = ""

    while True:
        try:
            chats = driver.find_elements(By.CSS_SELECTOR, "div.copyable-text")
            if not chats:
                time.sleep(1)
                continue

            chat = chats[-1]
            text = chat.text

            if text != last_message:
                last_message = text

                sender = chat.get_attribute("data-pre-plain-text")
                if sender:
                    sender = sender.split("] ")[1].replace(":", "")

                print(f"📩 {sender}: {text}")

                reply = handle_message(sender, text)
                if reply:
                    send_message(driver, reply)

        except Exception as e:
            print("Error:", e)

        time.sleep(2)


def send_message(driver, message):
    try:
        box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
        box.send_keys(message)
        box.send_keys(Keys.ENTER)
        print("📤 Sent:", message)
    except Exception as e:
        print("Send failed:", e)


if __name__ == "__main__":
    driver = start_whatsapp()
    listen_messages(driver)

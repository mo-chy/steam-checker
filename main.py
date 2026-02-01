import requests
import random
import string
import time
import threading
import os
from colorama import Fore, Style, init
from flask import Flask

init(autoreset=True)

ASCII = f"""{Fore.RED}
███████╗████████╗███████╗ █████╗ ███╗   ███╗
██╔════╝╚══██╔══╝██╔════╝██╔══██╗████╗ ████║
███████╗   ██║   █████╗  ███████║██╔████╔██║
╚════██║   ██║   ██╔══╝  ██╔══██║██║╚██╔╝██║
███████║   ██║   ███████╗██║  ██║██║ ╚═╝ ██║
╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝
{Style.RESET_ALL}"""

print(ASCII)

# Read webhook from environment variable (set in Render dashboard)
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

HEADERS = {"User-Agent": "Mozilla/5.0"}

def send_webhook(username):
    if not WEBHOOK_URL:
        return
    try:
        requests.post(WEBHOOK_URL, json={"content": f"`{username}`"})
    except:
        print(Fore.RED + "❌ Webhook failed")

def check_username(username):
    url = f"https://steamcommunity.com/id/{username}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        return "The specified profile could not be found" in r.text
    except:
        return False

# Generate 3-character combos
chars = string.ascii_lowercase + "_-"
all_combos = [''.join([a,b,c]) for a in chars for b in chars for c in chars for d in chars]
random.shuffle(all_combos)

def username_loop():
    print(Fore.CYAN + f"Starting random 3-character username checks... Total combos: {len(all_combos)}\nCTRL+C to stop...\n")
    while True:
        for username in all_combos:
            available = check_username(username)
            if available:
                print(Fore.GREEN + f"[+] {username}")
                send_webhook(username)
            else:
                print(Fore.RED + f"[-] {username}")
            time.sleep(0.5)

# Flask server to keep Render alive
app = Flask(__name__)

@app.route("/")
def home():
    return "Steam Username Checker Running 24/7!"

if __name__ == "__main__":
    t = threading.Thread(target=username_loop, daemon=True)
    t.start()
    app.run(host="0.0.0.0", port=10000)

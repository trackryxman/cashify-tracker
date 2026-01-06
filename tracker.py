import requests
from bs4 import BeautifulSoup
import sys
import os

URLS = [
    "https://www.cashify.in/buy/search?plid=35",
    "https://www.cashify.in/buy-refurbished-laptops"
]

KEYWORD = "Gaming Series","TUF","Nitro"
STATE_FILE = "state.txt"

headers = {"User-Agent": "Mozilla/5.0"}

found_now = False

for url in URLS:
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    text = soup.get_text().lower()

    if KEYWORD in text:
        found_now = True

# read previous state
previous = "none"
if os.path.exists(STATE_FILE):
    with open(STATE_FILE, "r") as f:
        previous = f.read().strip()

# logic
if found_now and previous != "found":
    with open(STATE_FILE, "w") as f:
        f.write("found")
    print("NEW Gaming Series detected")
    sys.exit(1)   # send email ONCE

if not found_now:
    with open(STATE_FILE, "w") as f:
        f.write("none")

print("No new Gaming Series")

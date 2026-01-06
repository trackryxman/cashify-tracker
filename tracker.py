import requests
from bs4 import BeautifulSoup
import json
import sys
import os

URLS = [
    "https://www.cashify.in/buy/search?plid=35",
    "https://www.cashify.in/buy-refurbished-laptops"
]

STATE_FILE = "products.json"
headers = {"User-Agent": "Mozilla/5.0"}

current_products = set()

for url in URLS:
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    cards = soup.find_all("a", href=True)

    for card in cards:
        text = card.get_text(" ", strip=True).lower()

        # skip out of stock
        if "out of stock" in text:
            continue

        # must be gaming series
        if "Gaming Series" in text:
            link = "https://www.cashify.in" + card["href"]
            current_products.add(text + "|" + link)

# load previous state
old_products = set()
if os.path.exists(STATE_FILE):
    with open(STATE_FILE, "r") as f:
        old_products = set(json.load(f))

# find new ones
new_products = current_products - old_products

# save current state
with open(STATE_FILE, "w") as f:
    json.dump(list(current_products), f)

if new_products:
    print("NEW GAMING LAPTOP ADDED:")
    for p in new_products:
        print(p)
    sys.exit(1)  # email alert

print("No new in-stock gaming laptop")

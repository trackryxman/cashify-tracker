import requests
from bs4 import BeautifulSoup
import json
import os

URLS = [
    "https://www.cashify.in/buy/search?plid=35",
    "https://www.cashify.in/buy-refurbished-laptops"
]

KEYWORDS = ["Gaming Series", "TUF", "Nitro"]
STATE_FILE = "products.json"

headers = {
    "User-Agent": "Mozilla/5.0"
}

current_products = set()

for url in URLS:
    r = requests.get(url, headers=headers, timeout=20)
    soup = BeautifulSoup(r.text, "html.parser")

    for a in soup.find_all("a", href=True):
        text = a.get_text(" ", strip=True)

        # must match keyword
        if not any(k in text for k in KEYWORDS):
            continue

        # skip out of stock
        if "out of stock" in text.lower():
            continue

        link = "https://www.cashify.in" + a["href"]
        current_products.add(text + " | " + link)

# load previous state
old_products = set()
if os.path.exists(STATE_FILE):
    with open(STATE_FILE, "r")

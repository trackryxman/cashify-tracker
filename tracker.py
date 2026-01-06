import requests
from bs4 import BeautifulSoup
import json
import os

GAMING_URL = "https://www.cashify.in/buy-refurbished-laptops/gaming"
HIGH_PERF_URL = "https://www.cashify.in/buy-refurbished-laptops/high-performance"

HP_KEYWORDS = ["Nitro", "TUF", "Omen", "Predator"]
STATE_FILE = "products.json"

headers = {
    "User-Agent": "Mozilla/5.0"
}

current_products = set()

def collect_products(url, keywords=None):
    r = requests.get(url, headers=headers, timeout=20)
    soup = BeautifulSoup(r.text, "html.parser")

    for a in soup.find_all("a", href=True):
        text = a.get_text(" ", strip=True)

        # skip out of stock
        if "out of stock" in text.lower():
            continue

        # keyword filter (only for high performance page)
        if keywords:
            if not any(k in text for k in keywords):
                continue

        link = "https://www.cashify.in" + a["href"]
        current_products.add(text + " | " + link)


# collect from both pages
collect_products(GAMING_URL)
collect_products(HIGH_PERF_URL, HP_KEYWORDS)

# load old state
old_products = set()
if os.path.exists(STATE_FILE):
    with open(STATE_FILE, "r") as f:
        old_products = set(json.load(f))

# find new products
new_products = current_products - old_products

# save current state
with open(STATE_FILE, "w") as f:
    json.dump(list(current_products), f)

# create alert file if new products found
if new_products:
    with open("alert.txt", "w") as f:
        for p in new_products:
            f.write(p + "\n")

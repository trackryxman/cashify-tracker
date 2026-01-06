import requests
from bs4 import BeautifulSoup
import json
import os

GAMING_URL = "https://www.cashify.in/buy-refurbished-laptops/gaming"
HIGH_PERF_URL = "https://www.cashify.in/buy-refurbished-laptops/high-performance"

HP_KEYWORDS = ["Nitro", "TUF", "Omen", "Predator"]
STATE_FILE = "products.json"

headers = {"User-Agent": "Mozilla/5.0"}

current = {}

def process_page(url, keywords=None):
    r = requests.get(url, headers=headers, timeout=20)
    soup = BeautifulSoup(r.text, "html.parser")

    for a in soup.find_all("a", href=True):
        name = a.get_text(" ", strip=True)
        link = "https://www.cashify.in" + a["href"]

        if keywords and not any(k in name for k in keywords):
            continue

        in_stock = "out of stock" not in name.lower()
        current[name] = {
            "link": link,
            "in_stock": in_stock
        }

# collect products
process_page(GAMING_URL)
process_page(HIGH_PERF_URL, HP_KEYWORDS)

# load old state
old = {}
if os.path.exists(STATE_FILE):
    with open(STATE_FILE, "r") as f:
        old = json.load(f)

alerts = []

for name, data in current.items():
    if name not in old and data["in_stock"]:
        alerts.append("NEW: " + name + " | " + data["link"])
    elif name in old:
        if not old[name]["in_stock"] and data["in_stock"]:
            alerts.append("RESTOCK: " + name + " | " + data["link"])

# save current state
with open(STATE_FILE, "w") as f:
    json.dump(current, f)

# create alert file
if alerts:
    with open("alert.txt", "w") as f:
        for a in alerts:
            f.write(a + "\n")

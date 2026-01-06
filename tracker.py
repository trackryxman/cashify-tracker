import requests
from bs4 import BeautifulSoup
import json
import os

URLS = [
    "https://www.cashify.in/buy/search?plid=35",
    "https://www.cashify.in/buy-refurbished-laptops"
]

STATE_FILE = "products.json"
headers = {"User-Agent": "Mozilla/5.0"}

current = set()

for url in URLS:
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    for a in soup.find_all("a", href=True):
        text = a.get_text(" ", strip=True).lower()

        if "gaming series" not in text:
            continue
        if "out of stock" in text:
            continue

        link = "https://www.cashify.in" + a["href"]
        current.add(text + " | " + link)

old = set()
if os.path.exists(STATE_FILE):
    with open(STATE_FILE, "r") as f:
        old = set(json.load(f))

new_items = current - old

with open(STATE_FILE, "w") as f:
    json.dump(list(current), f)

if new_items:
    print("NEW ITEMS FOUND:")
    for i in new_items:
        print(i)
    # signal new item without failing
    with open("new.txt", "w") as f:
        f.write("\n".join(new_items))
else:
    print("No new gaming laptop")

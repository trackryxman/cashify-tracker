import requests
from bs4 import BeautifulSoup
import sys

URLS = [
    "https://www.cashify.in/buy/search?plid=35",
    "https://www.cashify.in/buy-refurbished-laptops"
]

KEYWORDS = ["Gaming Series", "ROG", "predator", "omen", "legion", "TUF","Nitro"]

headers = {
    "User-Agent": "Mozilla/5.0"
}

for url in URLS:
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text().lower()

    for word in KEYWORDS:
        if word in text:
            print("GAMING LAPTOP FOUND:", word, "URL:", url)
            sys.exit(1)   # email alert

print("No gaming laptop found")

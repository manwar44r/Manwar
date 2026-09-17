import requests
from bs4 import BeautifulSoup
import json

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "en-IN,en;q=0.9"
}

# Aapka Amazon Associate tag
AMAZON_TAG = "manwar-21"

all_deals = []

search_queries = [
    ("Korean+Jewelry+under+299", "Amazon"),
    ("Aesthetic+Room+Decor+under+499", "Amazon"),
    ("Trendy+Accessories+under+399", "Amazon")
]

for query, store in search_queries:
    try:
        url = f"https://www.amazon.in/s?k={query}"
        r = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.content, "html.parser")
        items = soup.find_all("div", {"data-component-type": "s-search-result"})

        for item in items[:4]:
            try:
                title = item.h2.text.strip()
                price_str = item.find("span", "a-price-whole").text.replace(",", "").replace(".", "").strip()
                price = int(price_str)

                if price <= 10000:
                    raw_link = "https://www.amazon.in" + item.h2.a["href"].split("?")[0]
                    aff_link = f"{raw_link}?tag={AMAZON_TAG}"
                    img = item.find("img", "s-image")["src"]

                    all_deals.append({
                        "title": title[:55] + "...",
                        "price": price,
                        "cut_price": int(price * 1.5),
                        "image": img,
                        "link": aff_link,
                        "store": store
                    })
            except Exception:
                continue
    except Exception as e:
        print(f"Error: {e}")

# Fallback Starter Deals agar live scraping block ho
if len(all_deals) == 0:
    all_deals = [
        {
            "title": "Aesthetic Pearl Layered Choker Necklace",
            "price": 199,
            "cut_price": 599,
            "image": "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=400",
            "link": f"https://www.amazon.in/?tag={AMAZON_TAG}",
            "store": "Meesho"
        },
        {
            "title": "Mini USB Desktop Ambient Lamp & Humidifier",
            "price": 399,
            "cut_price": 999,
            "image": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400",
            "link": f"https://www.amazon.in/?tag={AMAZON_TAG}",
            "store": "Amazon"
        },
        {
            "title": "Retro Aesthetic Oval Sunglasses for Youth",
            "price": 249,
            "cut_price": 699,
            "image": "https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=400",
            "link": f"https://www.amazon.in/?tag={AMAZON_TAG}",
            "store": "Flipkart"
        }
    ]

with open("products.json", "w", encoding="utf-8") as f:
    json.dump(all_deals, f, ensure_ascii=False, indent=2)

print(f"Updated products.json with {len(all_deals)} items.")

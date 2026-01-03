from bs4 import BeautifulSoup
import csv
from datetime import date

# 1. Load local HTML snapshot
with open("data/amazon_snapshot.html", "r", encoding="utf-8") as file:
    html = file.read()

soup = BeautifulSoup(html, "html.parser")

# 2. Price extraction (snapshot is stable)
price_tag = soup.find("span", class_="a-offscreen")

if not price_tag:
    price_tag = soup.find("span", class_="a-price-whole")

if not price_tag:
    for span in soup.find_all("span"):
        text = span.text.strip()
        if "₹" in text:
            cleaned = text.replace("₹", "").replace(",", "").replace(".", "")
            if cleaned.isdigit():
                price_tag = span
                break

if not price_tag:
    print("Price not found in snapshot")
    exit()

raw_price = price_tag.text.strip()

# 3. Clean price
clean_price = raw_price.replace("₹", "").replace(",", "").split(".")[0]
clean_price = int(clean_price)

# 4. Save to CSV
today = date.today()

with open("data/price_data.csv", "a", newline="") as file:
    writer = csv.writer(file)
    writer.writerow([today, clean_price])

print("Saved from snapshot:", today, clean_price)

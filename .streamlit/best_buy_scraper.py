import os
import requests
from bs4 import BeautifulSoup

# Send a request to Best Buy's website and parse the HTML response
response = requests.get("https://www.bestbuy.com/")
soup = BeautifulSoup(response.text, "html.parser")

# Extract the name, price, and description of each item
items = soup.find_all("div", class_="sku-item")
for item in items:
    name = item.find("h4", class_="sku-header").text.strip()
    price = item.find("div", class_="priceView-hero-price priceView-customer-price").text.strip()
    description = item.find("p", class_="sku-description").text.strip()

    # Create a folder for the device and paginate the comments into it
    device_folder = name.replace("/", "_")
    if not os.path.exists(device_folder):
        os.makedirs(device_folder)

    # Save the scraped data to a file in the device folder
    with open(os.path.join(device_folder, "data.txt"), "w") as file:
        file.write(f"Name: {name}\n")
        file.write(f"Price: {price}\n")
        file.write(f"Description: {description}\n")
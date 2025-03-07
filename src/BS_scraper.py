import requests
from bs4 import BeautifulSoup

# Set the target URL (Replace with a real D.R. Horton listing page)
url = "https://www.drhorton.com/[REPLACE-WITH-ALLOWED-URL]"

# Set headers to mimic a real browser to avoid bot detection
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Send request to the website
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all home listings (Modify the class based on the actual website structure)
    listings = soup.find_all("div", class_="home-listing")  # Example, update based on real HTML structure

    for listing in listings:
        # Extract home price (modify based on real class names)
        price = listing.find("span", class_="price").text.strip() if listing.find("span", class_="price") else "N/A"
        address = listing.find("span", class_="address").text.strip() if listing.find("span", class_="address") else "N/A"

        print(f"🏡 {address} - {price}")

else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")

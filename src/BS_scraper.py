import requests
from bs4 import BeautifulSoup
import csv

# Set the target URL (Replace with a real D.R. Horton listing page)
url = "https://www.drhorton.com/texas/austin"

# Set headers to mimic a real browser to avoid bot detection
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Send request to the website
response = requests.get(url, headers=headers)

# Open a CSV file to save results
csv_filename = "drhorton_homes.csv"
with open(csv_filename, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    
    # Write the header row
    writer.writerow(["Title", "Address", "Community Status", "Square Footage", "Stats", "Link"])

# Check if the request was successful
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all home listings (Modify the class based on the actual website structure)
    listings = soup.find_all("div", class_="coveo-list-layout CoveoResult")  # Example, update based on real HTML structure

    for listing in listings:
        # Extract House URL
            link_tag = listing.find("a", class_="CoveoResultLink")
            house_url = "https://www.drhorton.com" + link_tag["href"] if link_tag else "N/A"

            # Extract House Title
            title_tag = listing.find("div", class_="title CoveoResultTitle")
            house_title = title_tag.find("h2").text.strip() if title_tag else "N/A"

            # Extract Community Status
            status_tag = listing.find("div", class_="home-info__community-status")
            community_status = status_tag.find("span").text.strip() if status_tag else "N/A"

            # Extract Address
            address_tag = listing.find("div", class_="home-info__address")
            address = address_tag.text.strip() if address_tag else "N/A"

            # Extract Square Footage
            sqft_tag = listing.find("div", class_="home-info__square-foot")
            square_footage = sqft_tag.text.strip() if sqft_tag else "N/A"

            # Extract Home Stats (Bedrooms, Bathrooms, Garage, etc.)
            stats_tag = listing.find("div", class_="home-info__stats")
            home_stats = stats_tag.text.strip().replace("\n", " | ") if stats_tag else "N/A"

            # Write data to CSV
            writer.writerow([house_title, address, community_status, square_footage, home_stats, house_url])

            # Print data to terminal
            print(f"🏡 {house_title} - {address}")
            print(f"🔗 Link: {house_url}")
            print(f"📍 Status: {community_status}")
            print(f"📏 Square Footage: {square_footage}")
            print(f"🛏 Stats: {home_stats}")
            print("-" * 60)

else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")

import requests
from bs4 import BeautifulSoup
import csv
import time
import random

# Set the actual listings page URL (Replace with a real page)
url = "https://www.drhorton.com/texas/austin"

# List of user agents to rotate
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
]

# Function to make requests with retry logic
def fetch_page(url, max_retries=5):
    for attempt in range(max_retries):
        headers = {"User-Agent": random.choice(USER_AGENTS)}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response
        elif response.status_code == 429:  # Too many requests
            wait_time = 2 ** attempt  # Exponential backoff
            print(f"⚠ Received 429 Too Many Requests. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
        else:
            print(f"❌ Failed to retrieve the page. Status code: {response.status_code}")
            return None
    return None  # Return None if all retries fail

# Fetch the page with retry mechanism
response = fetch_page(url)

if response is None:
    print("❌ Could not retrieve the webpage after multiple attempts.")
    exit()

# Parse the HTML
soup = BeautifulSoup(response.text, "html.parser")

# Print the raw HTML of the page for debugging
print(soup.prettify())

# Open a CSV file to save results
csv_filename = "drhorton_homes.csv"
with open(csv_filename, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    
    # Write the header row
    writer.writerow(["Title", "Address", "Community Status", "Square Footage", "Stats", "Link"])

    # Find all house listings (Top-Level Container)
    listings = soup.find_all("div", class_="coveo-list-layout CoveoResult")

    # Debugging: Check if listings were found
    print(f"Found {len(listings)} listings")
    if not listings:
        print("⚠ No listings found. Check the class name in soup.find_all().")

    for listing in listings:
        # Add a delay between requests
        time.sleep(random.uniform(1, 3))

        # Extract House URL
        link_tag = listing.find("a", class_="CoveoResultLink")
        house_url = "https://www.drhorton.com" + link_tag["href"] if link_tag else "N/A"

        # Find home-info__community inside listing
        community_info = listing.find("div", class_="home-info__community")
        if not community_info:
            print("⚠ Skipping a listing: home-info__community not found")
            continue  

        # Now find info-frame inside home-info__community
        info_frame = community_info.find("div", class_="info-frame")
        if not info_frame:
            print("⚠ Skipping a listing: info-frame not found")
            continue  

        # Extract House Title
        title_tag = info_frame.find("div", class_="title CoveoResultTitle")
        house_title = title_tag.find("h2").text.strip() if title_tag else "N/A"

        # Extract Community Status
        status_tag = info_frame.find("div", class_="home-info__community-status")
        community_status = status_tag.find("span").text.strip() if status_tag else "N/A"

        # Extract Address
        address_tag = info_frame.find("div", class_="home-info__address")
        address = address_tag.text.strip() if address_tag else "N/A"

        # Extract Square Footage
        sqft_tag = info_frame.find("div", class_="home-info__square-foot")
        square_footage = sqft_tag.text.strip() if sqft_tag else "N/A"

        # Extract Home Stats (Bedrooms, Bathrooms, Garage, etc.)
        stats_tag = info_frame.find("div", class_="home-info__stats")
        home_stats = stats_tag.text.strip().replace("\n", " | ") if stats_tag else "N/A"

        # Write data to CSV
        writer.writerow([house_title, address, community_status, square_footage, home_stats, house_url])

        # Print data to terminal for debugging
        print(f"🏡 {house_title} - {address}")
        print(f"🔗 Link: {house_url}")
        print(f"📍 Status: {community_status}")
        print(f"📏 Square Footage: {square_footage}")
        print(f"🛏 Stats: {home_stats}")
        print("-" * 60)

print(f"✅ Data saved to {csv_filename}")

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
# import ace_tools as tools
import time


service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.get("https://www.drhorton.com//texas")

#get webpage title
print(driver.title)

# #find search bar element
# search = driver.find_element(By.NAME,"lctm")
# search.send_keys("Austin")

time.sleep(5)

try:
#    listings_container = driver.find_element(By.CLASS_NAME, "coveo-list-layout CoveoResult")
    listings_container = driver.find_element(By.XPATH, "//div[contains(@class, 'coveo-list-layout CoveoResult')]")
    print("Found the listings container:", listings_container)
except Exception as e:
    print("Listings container not found:", e)
# search.send_keys(Keys.RETURN)

# Print the HTML contents of the container
# print("=== LISTINGS CONTAINER HTML ===")
# print(listings_container.get_attribute("outerHTML"))

# extract all listings on the page as list "listings"

try:
    listings = driver.find_elements(By.XPATH, "//div[contains(@class, 'coveo-list-layout CoveoResult')]")
    print("listings extraction successful")
except Exception as e:
    print("listings extraction failed big time: ", e)

# initialized house elements storage list
houses = []

# start iterating through listings using variable house to extract individual elements
for house in listings:
    try:
        # Extract Page Link
        page_link = house.find_element(By.XPATH, ".//a").get_attribute("href")

        # Extract Title
        title = house.find_element(By.XPATH, ".//div[contains(@class, 'title CoveoResultTitle')]/h2").text

        # Extract Community Status
        status = house.find_element(By.XPATH, ".//div[contains(@class, 'home-info__community-status')]//span[2]").text

        # Extract Location
        location = house.find_element(By.XPATH, ".//div[contains(@class, 'home-info__address')]").text.strip()

        # Extract Call for Info (Price)
        try:
            call_info = house.find_element(By.XPATH, ".//div[contains(@class, 'home-info__callforinfo')]").text
        except:
            call_info = "N/A"

        # Append to list
        houses.append({
            "Title": title,
            "Status": status,
            "Location": location,
            "Price/Info": call_info,
            "Page Link": page_link
        })
    except Exception as e:
        print("Error extracting house details:", e)

# create dataframe
df = pd.DataFrame(houses)

# display extracted data
# tools.display_dataframe_to_user(name="House Listings", dataframe=df)
print(df)

time.sleep(5)

# Prevent the script from exiting immediately
input("Press Enter to close the browser...")
driver.quit()


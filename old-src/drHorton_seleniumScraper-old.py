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

        # Extract Community Status
        status = house.find_element(By.XPATH, ".//div[contains(@class, 'home-info__community-status')]//span[2]").text

        # Extract Title
        title = house.find_element(By.XPATH, ".//div[contains(@class, 'title CoveoResultTitle')]/h2").text

        # Extract Location
        location = house.find_element(By.XPATH, ".//div[contains(@class, 'home-info__address')]").text.strip()

        # # Extract Call for Info - if info present then this will go to except
        # try:
        #     info = house.find_element(By.XPATH, ".//div[contains(@class, 'home-info__callforinfo')]").text
        # except:
        #     info = "Present"

        #     # Extract Price 
        #     price = house.find_element(By.XPATH, ".//div[contains(@class, 'home-info__from')]").text

            # # Extract home stats
            # stats_div = house.find_element(By.XPATH, ".//div[contains(@class, 'home-info__stats')]")

            # # Extract text content from the div
            # stats_text = stats_div.text.strip()
            # print("Full Stats Text:", stats_text)  # Debugging: Print raw text content

        #     # Extract individual values
        #     try:
        #         beds = stats_div.find_element(By.XPATH, ".//text()[1]").strip()
        #         baths = stats_div.find_element(By.XPATH, ".//text()[3]").strip()
        #         garages = stats_div.find_element(By.XPATH, ".//text()[5]").strip()
        #         stories = stats_div.find_element(By.XPATH, ".//text()[7]").strip()
        #     except:
        #         beds, baths, garages, stories = "N/A", "N/A", "N/A", "N/A"

        #     print(f"Beds: {beds}, Baths: {baths}, Garages: {garages}, Stories: {stories}")

        try:
            info = house.find_element(By.XPATH, ".//div[contains(@class, 'home-info__callforinfo')]").text
        except:
            info = "True"
        

        if (info == "Call for Information"):
            continue

        try:
            # Extract Price 
            price = house.find_element(By.XPATH, ".//div[contains(@class, 'home-info__from')]").text
        except:
            continue

        try:
            # Extract Stats
            stats = house.find_element(By.XPATH, ".//div[contains(@class, 'home-info__stats')]")
        except:
            continue

        try:    
            # Extract text from stats
            stats_text = stats.text.strip()
            print("Full Stats Text:", stats_text)  # Debugging: Print raw text content
        except:
            continue

        try:
            beds = stats.find_element(By.XPATH, ".//text()[1]").strip()
        except:
            beds = "N/A"

        try:
            baths = stats.find_element(By.XPATH, ".//text()[3]").strip()
        except:
            baths = "N/A"

        try:
            garages = stats.find_element(By.XPATH, ".//text()[5]").strip()
        except:
            garages = "N/A"        

        try:
            stories = stats.find_element(By.XPATH, ".//text()[7]").strip()
        except:
            stories = "N/A"
        
        print(f"Beds: {beds}, Baths: {baths}, Garages: {garages}, Stories: {stories}")

        try:


        
        



        # Append to list
        houses.append({
            "Title": title,
            "Status": status,
            "Location": location,
            "Info": info,



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


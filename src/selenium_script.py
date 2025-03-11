from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Set up WebDriver (Update path to chromedriver if necessary)
service = Service("chromedriver")
driver = webdriver.Chrome(service=service, options=chrome_options)

# D.R. Horton website URL
driver.get("https://www.drhorton.com/")
time.sleep(3)  # Allow time for page to load

# Search for homes in a specific location
search_box = driver.find_element(By.NAME, "search-field")  # Update selector if needed
search_box.send_keys("Texas")  # Example search
search_box.send_keys(Keys.RETURN)
time.sleep(5)

# Extract home details
properties = []
home_cards = driver.find_elements(By.CLASS_NAME, "property-card")  # Update selector

for home in home_cards:
    try:
        title = home.find_element(By.CLASS_NAME, "property-title").text
        price = home.find_element(By.CLASS_NAME, "property-price").text
        address = home.find_element(By.CLASS_NAME, "property-address").text
        properties.append({"Title": title, "Price": price, "Address": address})
    except Exception as e:
        print(f"Error extracting property: {e}")
        continue

# Save results to CSV
if properties:
    df = pd.DataFrame(properties)
    df.to_csv("drhorton_home_prices.csv", index=False)
    print("Data saved to drhorton_home_prices.csv")
else:
    print("No listings found.")

# Close WebDriver
driver.quit()

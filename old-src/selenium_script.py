from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (Remove this if you want to see the browser)
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# ✅ Set up WebDriver (Make sure chromedriver.exe path is correct)
chrome_driver_path = r"..\chromedriver.exe"
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# ✅ Open D.R. Horton website
driver.get("https://www.drhorton.com/")
time.sleep(3)  # Allow time for page to load

# ✅ Search for homes in Austin     
try:
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "search-site"))  # Updated to use correct ID
    )
    search_box.send_keys("Austin")
    search_box.send_keys(Keys.RETURN)
    time.sleep(5)  # Allow search results to load
except Exception as e:
    print(f"Search box not found or interaction failed: {e}")
    driver.quit()
    exit()

# ✅ Extract home details
properties = []
home_cards = driver.find_elements(By.CLASS_NAME, "property-card")  # Update selector if needed

for home in home_cards:
    try:
        title = home.find_element(By.CLASS_NAME, "property-title").text
        price = home.find_element(By.CLASS_NAME, "property-price").text
        address = home.find_element(By.CLASS_NAME, "property-address").text
        properties.append({"Title": title, "Price": price, "Address": address})
    except Exception as e:
        print(f"Error extracting property: {e}")
        continue

# ✅ Save results to CSV
if properties:
    df = pd.DataFrame(properties)
    df.to_csv("drhorton_home_prices.csv", index=False)
    print("Data saved to drhorton_home_prices.csv")
else:
    print("No listings found.")

# ✅ Close WebDriver
driver.quit()

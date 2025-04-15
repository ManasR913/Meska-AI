from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import re
import undetected_chromedriver as uc


# ---------------------------------------------------
# vvv old chrome driver vvv
# service = Service(ChromeDriverManager().install())
# driver = webdriver.Chrome(service=service)
# ---------------------------------------------------

driver = uc.Chrome()

# get dr horton page

driver.get("https://www.drhorton.com//texas")

# explicit wait for links to show up
try:
    link_elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'home-info__available-homes')]/object/a"))
    )
    print(f"✅ Link found: {len(link_elements)} total links on this page...")

    # we want to extract the links themselves into a separate list make a new list called linksAH
    available_home_links = [element.get_attribute("href") for element in link_elements]
except: 
    print(f"Links not found")



for link in available_home_links:
    driver.get(link)
    
    try:
        # Wait for community-secondary-info section to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "community-secondary-info"))
        )
    except:
        print("nothing found here")
        time.sleep()
    
    link_address = driver.find_element(By.XPATH, "//a[@id='directions']").text.strip()

    print(link_address)

    # parse this string into city, state, zipcode omit model home address for now

    # Define a regex pattern for "Street Address, City, State ZIP"
    pattern = r"^(.*?),\s*([\w\s]+),\s*([A-Z]{2})\s*(\d{5})$"

    # Apply regex
    match = re.match(pattern, link_address)

    if match:
        modelHomeAddress = match.group(1)  # Extract model home address
        city = match.group(2)  # Extract city
        state = match.group(3)  # Extract state
        zip_code = match.group(4)  # Extract ZIP code
    else:
        print("Address format not recognized")

    try:
        available_homes_section = driver.find_element(By.ID, "available-homes")
    except:
        print("available_homes_section not found")
    
    try:
        toggle_items = available_homes_section.find_elements(By.CLASS_NAME, "toggle-item")
        print(f"✅ Found {len(toggle_items)} toggle-item containers")
    except:
        print("could not create toggle-items list")
try:
    next_button = driver.find_element(By.XPATH, "//button[contains(@class, 'pagination__button') and @data-page-id]")
    driver.execute_script("arguments[0].click();", next_button)  # Click next button
    print("🔄 Moving to next page...")
    time.sleep(3)  # Wait for new page to load
except:
    print("🚫 No more pages found. Exiting loop.")
     

time.sleep(5)

# Prevent the script from exiting immediately
input("Press Enter to close the browser...")
driver.quit()


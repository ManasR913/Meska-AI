from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# import pandas as pd
# import ace_tools as tools
import time


service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

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

#get webpage title
print(driver.title)

print(link_elements[0])

# we want to extract the links themselves into a separate list make a new list called linksAH



time.sleep(5)

# Prevent the script from exiting immediately
input("Press Enter to close the browser...")
driver.quit()


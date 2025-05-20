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

# initialize driver (undetected chrome driver)

driver = uc.Chrome()

# get dr horton page

driver.get("https://www.drhorton.com//texas")

all_links = []

prev_page_number = None

while True:
    try:
        # Close cookie popup
        try:
            cookie_button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'onetrust-close-btn-handler')]"))
            )
            cookie_button.click()
            print("✅ Closed cookie banner")
            time.sleep(1)
        except:
            pass

        # Wait for and collect links
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//div[contains(@class, 'home-info__available-homes')]/object/a")
            )
        )
        link_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'home-info__available-homes')]/object/a")
        page_links = [el.get_attribute("href") for el in link_elements if el.get_attribute("href")]
        all_links.extend(page_links)
        print(f"✅ Found {len(page_links)} links on this page")

        # Read current page number
        current_page_elem = driver.find_element(By.XPATH, "//button[contains(@class, 'pagination__button') and contains(@class, 'active')]")
        current_page = current_page_elem.text.strip()
        print(f"📄 Currently on page {current_page}")

        # Click next button
        next_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'pagination__button--next-previous')]"))
        )
        next_button.click()
        time.sleep(2)

        # Wait until page number changes
        WebDriverWait(driver, 5).until(
            lambda d: d.find_element(By.XPATH, "//button[contains(@class, 'pagination__button') and contains(@class, 'active')]").text.strip() != current_page
        )

    except Exception as e:
        print("❌ Pagination ended or failed:", e)
        break

# Remove duplicates
all_links = list(set(all_links))
print(f"🔗 Total unique links collected: {len(all_links)}")
input("Press Enter to close the browser...")
driver.quit()


# # ----------------------------------------------------------------------------

# # iterating through the collected links (not right now)

# for link in available_home_links:
#     driver.get(link)
    
#     try:
#         # Wait for community-secondary-info section to load
#         WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.CLASS_NAME, "community-secondary-info"))
#         )
#     except:
#         print("nothing found here")
#         time.sleep()
    
#     link_address = driver.find_element(By.XPATH, "//a[@id='directions']").text.strip()

#     print(link_address)

#     # parse this string into city, state, zipcode omit model home address for now

#     # Define a regex pattern for "Street Address, City, State ZIP"
#     pattern = r"^(.*?),\s*([\w\s]+),\s*([A-Z]{2})\s*(\d{5})$"

#     # Apply regex
#     match = re.match(pattern, link_address)

#     if match:
#         modelHomeAddress = match.group(1)  # Extract model home address
#         city = match.group(2)  # Extract city
#         state = match.group(3)  # Extract state
#         zip_code = match.group(4)  # Extract ZIP code
#     else:
#         print("Address format not recognized")

#     try:
#         available_homes_section = driver.find_element(By.ID, "available-homes")
#     except:
#         print("available_homes_section not found")
    
#     try:
#         toggle_items = available_homes_section.find_elements(By.CLASS_NAME, "toggle-item")
#         print(f"✅ Found {len(toggle_items)} toggle-item containers")
#     except:
#         print("could not create toggle-items list")
# try:
#     next_button = driver.find_element(By.XPATH, "//button[contains(@class, 'pagination__button') and @data-page-id]")
#     driver.execute_script("arguments[0].click();", next_button)  # Click next button
#     print("🔄 Moving to next page...")
#     time.sleep(3)  # Wait for new page to load
# except:
#     print("🚫 No more pages found. Exiting loop.")
     

# time.sleep(5)

# Prevent the script from exiting immediately
input("Press Enter to close the browser...")
driver.quit()


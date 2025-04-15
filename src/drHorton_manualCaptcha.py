from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import time
import re

# ==== Setup options for stealth ====
options = uc.ChromeOptions()
options.add_argument("--window-size=960,1080")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")

# ==== Launch driver ====
driver = uc.Chrome(options=options)
driver.set_window_size(960, 1080)
driver.set_window_position(0, 0)

# ==== Visit website ====
driver.get("https://www.drhorton.com//texas")
time.sleep(2)  # slight delay after load

# Scroll to bottom to mimic human
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(2)

# Human-like cursor movement
from selenium.webdriver import ActionChains
ActionChains(driver).move_by_offset(100, 100).perform()
time.sleep(1)

# ==== Extract links ====
try:
    link_elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'home-info__available-homes')]/object/a"))
    )
    print(f"✅ Link found: {len(link_elements)} total links on this page...")
    available_home_links = [element.get_attribute("href") for element in link_elements]
except Exception as e:
    print("Links not found:", e)
    available_home_links = []

# ==== Loop through links ====
for link in available_home_links:
    driver.get(link)
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "community-secondary-info"))
        )
    except:
        print("nothing found here")
        continue

    try:
        link_address = driver.find_element(By.XPATH, "//a[@id='directions']").text.strip()
        print(link_address)
    except:
        print("❌ Couldn't find directions text.")
        continue

    pattern = r"^(.*?),\s*([\w\s]+),\s*([A-Z]{2})\s*(\d{5})$"
    match = re.match(pattern, link_address)
    if match:
        modelHomeAddress = match.group(1)
        city = match.group(2)
        state = match.group(3)
        zip_code = match.group(4)
        print(f"🏠 Parsed Address: {city}, {state}, {zip_code}")
    else:
        print("⚠️ Address format not recognized")

    try:
        available_homes_section = driver.find_element(By.ID, "available-homes")
    except:
        print("❌ available_homes_section not found")
        continue

    try:
        toggle_items = available_homes_section.find_elements(By.CLASS_NAME, "toggle-item")
        print(f"✅ Found {len(toggle_items)} toggle-item containers")
    except:
        print("⚠️ Could not create toggle-items list")

# ==== Try next page ====
try:
    next_button = driver.find_element(By.XPATH, "//button[contains(@class, 'pagination__button') and @data-page-id]")
    driver.execute_script("arguments[0].click();", next_button)
    print("🔄 Moving to next page...")
    time.sleep(3)
except:
    print("🚫 No more pages found. Exiting loop.")

# ==== Keep window open ====
input("Press Enter to close the browser...")
driver.quit()
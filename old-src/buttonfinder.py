from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import time

# Step 1: Launch undetected Chrome
driver = uc.Chrome()

# Step 2: Go to DR Horton Texas listings page
driver.get("https://www.drhorton.com//texas")

# Step 3: Give the page some time to load dynamic content
time.sleep(3)

# === DEBUGGING: List all button elements ===
buttons = driver.find_elements(By.TAG_NAME, "button")
for i, btn in enumerate(buttons):
    print(f"[{i}] Text: '{btn.text.strip()}' | Class: {btn.get_attribute('class')}")



# # Step 4: Find all <a> elements on the page
# all_a_tags = driver.find_elements(By.TAG_NAME, "a")

# # Step 5: Print each one's visible text and href
# print(f"🔍 Found {len(all_a_tags)} <a> elements. Displaying non-empty ones:\n")

# for i, a in enumerate(all_a_tags):
#     text = a.text.strip()
#     href = a.get_attribute("href")
#     if text or href:
#         print(f"[{i}] Text: '{text}' | HREF: {href}")

# Optional: Close browser when done
driver.quit()

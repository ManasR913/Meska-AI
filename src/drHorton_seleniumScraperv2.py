from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time


def get_driver():
    chrome_options = webdriver.ChromeOptions()

    # Use Guest Mode (avoids "Profile 2" errors)
    chrome_options.add_argument("--guest")

    # Prevent Selenium from closing immediately
    chrome_options.add_experimental_option("detach", True)

    # Initialize WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    return driver

# Start the driver with the 'Profile 1' directory
driver = get_driver()
driver.get("https://www.drhorton.com/texas")

# Function to detect Captcha by looking for known elements
def is_captcha_present(driver):
    try:
        # Check if the page has a Captcha iframe or a "I'm not a robot" element
        captcha_iframe = driver.find_element(By.CSS_SELECTOR, "iframe[src*='recaptcha']")
        if captcha_iframe:
            print("✅ Captcha Detected")
            return True
    except:
        pass
    try:
        # Check for another common Captcha element
        captcha_text = driver.find_element(By.XPATH, "//*[contains(text(), 'I’m not a robot')]")
        if captcha_text:
            print("✅ Captcha Detected")
            return True
    except:
        pass
    
    return False


driver = get_driver()

# Open the website
driver.get("https://www.drhorton.com/texas")

# Try browsing until Captcha is detected
while True:
    # Check for Captcha
    if is_captcha_present(driver):
        print("❌ Captcha detected. Switching profile...")

        # Switch to a different profile
        driver.quit()  # Quit the current browser session
        profile = "Profile 2"  # Switch to another profile
        driver = get_driver(profile)  # Launch a new driver with the new profile

        # Open the page again with the new profile
        driver.get("https://www.drhorton.com/texas")
        
    # Here you can put other code to interact with the page as needed
    # For example, navigating through links, extracting data, etc.
    
    time.sleep(5)  # Simulate a delay for a while (or interact with the page)

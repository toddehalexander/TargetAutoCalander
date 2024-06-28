from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import random
import getpass
import os

def wait_for_element(driver, by, value, timeout=30):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )

# Prompt user for credentials
username = input("Enter your MyTime Target username: ")
password = getpass.getpass("Enter your MyTime Target password: ")

# Set up Chrome options to use your default profile
chrome_options = Options()
chrome_options.add_argument("user-data-dir=" + os.path.expanduser('~') + "/Library/Application Support/Google/Chrome")
chrome_options.add_argument("profile-directory=Default")
chrome_options.add_experimental_option("detach", True)  # This will keep the browser open

# Initialize the WebDriver with the options
driver = webdriver.Chrome(options=chrome_options)

try:
    # Navigate to the MyTime Target login page
    driver.get("https://mytime.target.com/")

    # Wait for the page to load completely
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    # Check if we're already logged in
    if "login" in driver.current_url.lower():
        # We need to log in
        # Wait for the username field to be visible and interactable
        username_field = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.ID, "loginID"))
        )

        # Enter the username
        username_field.clear()  # Clear any pre-filled text
        for char in username:
            username_field.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3))

        # Wait for and enter the password
        password_field = wait_for_element(driver, By.ID, "password")
        password_field.clear()
        for char in password:
            password_field.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3))

        # Wait for the login button to be clickable
        login_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.ID, "submit-button"))
        )

        # Click the login button
        login_button.click()

        # Wait for a page change or a specific element on the next page
        WebDriverWait(driver, 30).until(
            EC.url_changes(driver.current_url)
        )

    print("Login successful or already logged in!")

except TimeoutException:
    print("Timed out waiting for page to load or element to be found")
except Exception as e:
    print(f"An error occurred: {e}")

# The browser will remain open, so you can manually close it when you're done
print("Script completed. You can manually close the browser when you're finished.")
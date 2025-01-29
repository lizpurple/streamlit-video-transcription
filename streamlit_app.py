import os
import time
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- Step 1: Install the latest Chrome version (should be 132) ---
os.system("wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb")
os.system("dpkg -i google-chrome-stable_current_amd64.deb")
os.system("apt-get -f install")  # Fix missing dependencies

# --- Step 2: Define Chrome binary path (after installation) ---
chrome_path = "/usr/bin/google-chrome"

# --- Step 3: Set up Chrome options ---
options = Options()
options.binary_location = chrome_path  # Force WebDriver to use newly installed Chrome
options.add_argument("--disable-gpu")
options.add_argument("--headless")  # Keep headless mode
options.add_argument("--no-sandbox")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.6834.159 Safari/537.36")  # Updated User-Agent
options.add_argument("accept-language=en-US,en;q=0.9")
options.add_argument("--lang=en-US,en")
options.add_argument("accept-encoding=gzip, deflate, br")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("start-maximized")
options.add_argument("--window-size=1920,1080")
options.add_argument("enable-automation")
options.add_argument("--incognito")
options.add_argument("--remote-debugging-port=9222")
options.add_argument("--disable-blink-features")
options.add_argument("--disable-blink-features=AutomationControlled")

# --- Step 4: Function to get Selenium WebDriver instance ---
@st.cache_resource
def get_driver():
    chrome_driver_path = ChromeDriverManager().install()  # Get ChromeDriver matching Chrome 132
    return webdriver.Chrome(service=Service(chrome_driver_path), options=options)

# --- Step 5: Create WebDriver instance ---
driver = get_driver()

# --- Step 6: Print ChromeDriver and browser versions ---
st.write(f"Browser Version: {driver.capabilities['browserVersion']}")
st.write(f"ChromeDriver Version: {driver.capabilities['chrome']['chromedriverVersion']}")

# --- Step 7: Load the webpage ---
driver.get("https://www.jw.org")

# --- Step 8: Wait for page load ---
time.sleep(10)

# --- Step 9: Display page source in Streamlit ---
st.code(driver.page_source)

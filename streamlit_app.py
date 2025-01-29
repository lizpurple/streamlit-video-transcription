import os
import time
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- Step 1: Detect the installed Chrome binary path ---
chrome_path = "/usr/bin/google-chrome"  # Default path in Streamlit Cloud

# --- Step 2: Set up Chrome options ---
options = Options()
options.binary_location = chrome_path  # Use pre-installed Chrome
options.add_argument("--disable-gpu")
options.add_argument("--headless=new")  # Alternative headless mode
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("start-maximized")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-blink-features=AutomationControlled")

# Updated User-Agent (match Google Colab)
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.6834.159 Safari/537.36")

# --- Step 3: Function to get Selenium WebDriver instance ---
@st.cache_resource
def get_driver():
    chrome_driver_path = ChromeDriverManager().install()  # Get matching ChromeDriver
    return webdriver.Chrome(service=Service(chrome_driver_path), options=options)

# --- Step 4: Create WebDriver instance ---
driver = get_driver()

# --- Step 5: Print Chrome and WebDriver versions ---
st.write(f"Browser Version: {driver.capabilities['browserVersion']}")
st.write(f"ChromeDriver Version: {driver.capabilities['chrome']['chromedriverVersion']}")

# --- Step 6: Load the webpage ---
driver.get("https://www.jw.org")

# --- Step 7: Wait for page load ---
time.sleep(10)

# --- Step 8: Display page source in Streamlit ---
st.code(driver.page_source)

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
import streamlit as st
import time

# Set up Chrome options
options = Options()
options.add_argument("--disable-gpu")
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
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

# Function to get a Selenium WebDriver instance
@st.cache_resource
def get_driver():
    return webdriver.Chrome(
        service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()),
        options=options,
    )

# Create a WebDriver instance
driver = get_driver()

# Print ChromeDriver and browser versions
st.write(f"Browser Version: {driver.capabilities['browserVersion']}")
st.write(f"ChromeDriver Version: {driver.capabilities['chrome']['chromedriverVersion']}")
# Load the webpage
driver.get("https://www.jw.org")

# Wait for the page to load
time.sleep(10)

# Display the page source in Streamlit
st.code(driver.page_source)

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
import streamlit as st

@st.cache_resource
def get_driver():
    # Set up Chrome options
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    # Use webdriver_manager to install Chromium and ChromeDriver
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()),
        options=options,
    )
    return driver

# Initialize the driver
driver = get_driver()

# Test with example.com
st.write("Navigating to example.com...")
driver.get("https://example.com")
st.write("Example.com Page Source:")
st.code(driver.page_source)

# Try navigating to jw.org
st.write("Navigating to jw.org...")
try:
    driver.get("https://www.jw.org")
    st.write("Navigation to jw.org succeeded!")
except Exception as e:
    st.write(f"Navigation failed: {e}")

# Debugging: Print browser and driver versions
st.write(f"Browser Version: {driver.capabilities['browserVersion']}")
st.write(f"ChromeDriver Version: {driver.capabilities['chrome']['chromedriverVersion']}")

# Debugging: Take a screenshot
driver.save_screenshot('screenshot.png')
st.image('screenshot.png')

# Display page source
st.write("JW.org Page Source:")
st.code(driver.page_source)

# Close the driver
driver.quit()

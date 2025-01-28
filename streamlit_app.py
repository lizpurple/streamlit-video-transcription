from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
import time
import streamlit as st

@st.cache_resource
def get_driver():
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    options.add_argument("accept-language=en-US,en;q=0.9")
    options.add_argument("accept-encoding=gzip, deflate, br")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("start-maximized")
    options.add_argument("enable-automation")
    options.add_argument("--incognito")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()),
        options=options,
    )
    return driver

driver = get_driver()

# Test with a simpler website first
driver.get("https://example.com")
time.sleep(5)
st.write("Example.com Page Source:")
st.code(driver.page_source)

# Now try jw.org
driver.get("https://www.jw.org")
time.sleep(10)

# Debugging: Print browser and driver versions
st.write(f"Browser Version: {driver.capabilities['browserVersion']}")
st.write(f"ChromeDriver Version: {driver.capabilities['chrome']['chromedriverVersion']}")

# Debugging: Take a screenshot
driver.save_screenshot('screenshot.png')
st.image('screenshot.png')

# Debugging: Print browser logs
logs = driver.get_log('browser')
st.write("Browser Logs:")
for log in logs:
    st.write(log)

# Display page source
st.write("JW.org Page Source:")
st.code(driver.page_source)

# Close the driver
driver.quit()

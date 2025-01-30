import streamlit as st
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options

def get_page_content(url):
    options = Options()
    options.add_argument("--headless=new")  # Keep it headless
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")  # Helps avoid detection
    options.add_argument("--window-size=375,812")  # Mimic mobile device
    options.add_argument("user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/537.36")

    driver = uc.Chrome(options=options)  # Use undetected Chrome
    driver.get(url)

    page_source = driver.page_source
    driver.quit()
    
    return page_source

st.title("Selenium with Undetected Chrome on Streamlit Cloud")
st.write("Navigating to jw.org...")

jw_content = get_page_content("https://www.jw.org")
if jw_content:
    st.write("Navigation to jw.org succeeded!")
    st.code(jw_content)
else:
    st.write("Failed to fetch content.")

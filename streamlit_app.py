import logging
import time
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from chromedriver_autoinstaller import install

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_page_html(page_url):
    try:
        # Set up Chrome options for headless browsing
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

        # Install the correct version of ChromeDriver
        install()

        # Start WebDriver
        logging.info("Starting WebDriver...")
        service = Service()  # chromedriver_autoinstaller ensures the path is correct
        driver = webdriver.Chrome(service=service, options=chrome_options)

        logging.info(f"Opening page: {page_url}")
        driver.get(page_url)
        time.sleep(5)  # Allow time for JavaScript to load the page

        # Extract the page HTML
        page_html = driver.page_source
        logging.info("Page HTML extracted successfully.")

        # Close the browser after extracting the page HTML
        driver.quit()

        return page_html

    except Exception as e:
        logging.error(f"Error extracting page HTML: {e}")
        return None

# Streamlit UI
st.title('Extract Page HTML')
page_url = st.text_input('Enter the URL of the page to extract HTML:')

if st.button("Extract HTML"):
    if page_url:
        logging.info("Extract button clicked.")
        page_html = extract_page_html(page_url)
        if page_html:
            st.text_area("Page HTML", page_html, height=300)
        else:
            st.error("Failed to extract the HTML from the page.")
    else:
        st.warning("Please enter a valid URL.")

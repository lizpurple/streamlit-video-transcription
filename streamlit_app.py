import streamlit as st
from playwright.sync_api import sync_playwright
import os

# Install Playwright browsers (only needed once)
os.system("playwright install chromium")

# Function to get page content using Playwright
def get_page_content(url):
    with sync_playwright() as p:
        # Launch Chromium in headless mode
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Navigate to the URL
        page.goto(url)

        # Wait for the page to load (adjust the timeout as needed)
        page.wait_for_load_state("networkidle")

        # Take a screenshot for debugging
        page.screenshot(path="screenshot.png")

        # Get the page content
        content = page.content()

        # Close the browser
        browser.close()

        return content

# Streamlit app
st.title("Playwright on Streamlit Cloud")

# Test with example.com
st.write("Navigating to example.com...")
example_content = get_page_content("https://example.com")
st.write("Example.com Page Source:")
st.code(example_content)

# Display the screenshot
st.write("Screenshot of example.com:")
st.image("screenshot.png")

# Try navigating to jw.org
st.write("Navigating to jw.org...")
try:
    jw_content = get_page_content("https://www.jw.org")
    st.write("Navigation to jw.org succeeded!")
    st.write("JW.org Page Source:")
    st.code(jw_content)

    # Display the screenshot
    st.write("Screenshot of jw.org:")
    st.image("screenshot.png")
except Exception as e:
    st.write(f"Navigation failed: {e}")

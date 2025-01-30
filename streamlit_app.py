import streamlit as st
from playwright.sync_api import sync_playwright
import os
import time

# Install Playwright browsers (only needed once)
os.system("playwright install chromium")

# Function to get page content using Playwright
def get_page_content(url):
    with sync_playwright() as p:
        # Launch Chromium with stealth options
        browser = p.chromium.launch(headless=False)  # Try non-headless first
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080},
        )
        page = context.new_page()

        # Add realistic delays to mimic human behavior
        page.wait_for_timeout(2000)  # Wait 2 seconds before navigating

        # Navigate to the URL
        try:
            page.goto(url, wait_until="networkidle", timeout=60000)  # Increase timeout
        except Exception as e:
            st.write(f"Navigation failed: {e}")
            return None

        # Add another delay to mimic human reading time
        page.wait_for_timeout(3000)

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
if example_content:
    st.write("Example.com Page Source:")
    st.code(example_content)
    st.write("Screenshot of example.com:")
    st.image("screenshot.png")

# Try navigating to jw.org
st.write("Navigating to jw.org...")
jw_content = get_page_content("https://www.jw.org")
if jw_content:
    st.write("Navigation to jw.org succeeded!")
    st.write("JW.org Page Source:")
    st.code(jw_content)
    st.write("Screenshot of jw.org:")
    st.image("screenshot.png")

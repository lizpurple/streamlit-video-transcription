import streamlit as st
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
import os

# Install Playwright browsers (only needed once)
os.system("playwright install chromium")

# Function to get page content using Playwright with stealth
def get_page_content(url):
    with sync_playwright() as p:
        # Launch Chromium with stealth options
        browser = p.chromium.launch(
            headless=True,  # Run in headless mode
            args=["--remote-debugging-port=9222"],  # Enable remote debugging
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",  # Set a realistic user-agent
            viewport={"width": 1920, "height": 1080},  # Set a large viewport
            extra_http_headers={
                "Accept-Language": "en-US,en;q=0.9",  # Set accept-language header
                "Accept-Encoding": "gzip, deflate, br",  # Set accept-encoding header
            },
        )
        page = context.new_page()

        # Apply stealth plugin to make the browser less detectable
        stealth_sync(page)

        # Navigate to the URL
        try:
            page.goto(url, wait_until="networkidle", timeout=60000)  # Wait for the page to load
        except Exception as e:
            st.write(f"Navigation failed: {e}")
            return None

        # Take a screenshot for debugging
        page.screenshot(path="screenshot.png")

        # Get the page content
        content = page.content()

        # Close the browser
        browser.close()

        return content

# Streamlit app
st.title("Playwright with Stealth on Streamlit Cloud")

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

import streamlit as st
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
import os

# Function to get page content using Playwright with stealth
def get_page_content(url):
    with sync_playwright() as p:
        # Try using the latest Chrome version
        browser = p.chromium.launch(
            channel="chrome",  # Use latest Chrome version
            headless=True,
            args=[
                "--disable-gpu",
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--start-maximized",
                "--enable-automation"
            ]
        )
        context = browser.new_context(
            # Try a mobile user-agent to bypass detection
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/537.36",
            viewport={"width": 375, "height": 812},  # iPhone viewport
            extra_http_headers={
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate, br"
            }
        )
        page = context.new_page()

        # Apply stealth plugin to make browser less detectable
        stealth_sync(page)

        # Navigate to the URL
        try:
            page.goto(url, wait_until="networkidle", timeout=60000)  # Wait for full load
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

# Try navigating to jw.org
st.write("Navigating to jw.org...")
jw_content = get_page_content("https://www.jw.org")
if jw_content:
    st.write("Navigation to jw.org succeeded!")
    st.write("JW.org Page Source:")
    st.code(jw_content)
    st.write("Screenshot of jw.org:")
    st.image("screenshot.png")

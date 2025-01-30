import streamlit as st
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
import shutil

# Install Chromium manually if not found
if not shutil.which("chromium"):
    import subprocess
    subprocess.run(["playwright", "install", "chromium"], check=True)

# Function to get page content using Playwright
def get_page_content(url):
    with sync_playwright() as p:
        # Use the installed Chromium
        browser = p.chromium.launch(
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
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/537.36",
            viewport={"width": 375, "height": 812},
            extra_http_headers={
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate, br"
            }
        )
        page = context.new_page()
        stealth_sync(page)

        try:
            page.goto(url, wait_until="networkidle", timeout=60000)
        except Exception as e:
            st.write(f"Navigation failed: {e}")
            return None

        content = page.content()
        browser.close()
        return content

# Streamlit app
st.title("Playwright with Stealth on Streamlit Cloud")
st.write("Navigating to jw.org...")

jw_content = get_page_content("https://www.jw.org")
if jw_content:
    st.write("Navigation to jw.org succeeded!")
    st.code(jw_content)

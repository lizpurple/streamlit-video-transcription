import ffmpeg
import re
import os
import streamlit as st
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from chromedriver_py import binary_path
from st_copy_to_clipboard import st_copy_to_clipboard
import time
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_chromium():
    # Install or update ChromeDriver to match the Chromium version
    logging.info("Installing or updating ChromeDriver...")
    chromedriver_autoinstaller.install()

# Function to extract video URL using Selenium
def extract_video_url(page_url):
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("start-maximized")

        # Start WebDriver
        logging.info("Starting WebDriver...")
        service = Service()  # chromedriver_autoinstaller ensures the path is correct
        driver = webdriver.Chrome(service=service, options=chrome_options)

        logging.info(f"Opening page: {page_url}")
        driver.get(page_url)
        time.sleep(10)  # Allow time for JavaScript to load

        # Debug: Log page source
        logging.debug("Page source loaded:")
        logging.debug(driver.page_source)

        # Debug: Check if the button exists
        logging.info("Looking for buttons with the selector 'a.secondaryButton'...")
        buttons = driver.find_elements(By.CSS_SELECTOR, 'a.secondaryButton')
        logging.debug(f"Found {len(buttons)} buttons with the selector.")

        # Extract video URL if the button exists
        if buttons:
            video_url = buttons[0].get_attribute("href")
            logging.info(f"Extracted video URL: {video_url}")
        else:
            video_url = None
            logging.warning("No buttons found with the selector 'a.secondaryButton'.")

        driver.quit()
        return video_url

    except Exception as e:
        logging.error(f"Error extracting video URL: {e}")
        return None

# Function to process video URL with FFmpeg
def process_video_url(video_url):
    try:
        # Download the subtitles using ffmpeg
        output_path = '/tmp/sub.srt'
        logging.info(f"Processing video URL with FFmpeg: {video_url}")
        ffmpeg.input(video_url).output(output_path, vn=None, **{'scodec': 'srt'}).overwrite_output().run()

        # Check if the subtitle file exists
        if os.path.exists(output_path):
            logging.info("Subtitle file downloaded successfully.")
            with open(output_path, 'r') as input_file:
                srt = input_file.read()

            # Process the SRT content
            logging.info("Processing subtitle content...")
            srt = re.sub(r'<.+?>', '', srt)
            srt = re.sub(r'{.+?}', '', srt)
            srt = re.sub(r'^\d+\n\d+:\d+:\d+,\d+ --> \d+:\d+:\d+,\d+\n', '', srt, flags=re.M)
            srt = re.sub('\n', ' ', srt)
            srt = re.sub(r' ‏', ' ', srt)
            srt = re.sub(r'  ', ' ', srt)
            srt = re.sub(r'\. ', '.\n\n', srt)
            srt = re.sub(r'\? ', '?\n\n', srt)
            srt = re.sub(r'\.” ', '.”\n\n', srt)
            srt = re.sub('  ', ' ', srt)
            srt = re.sub(r'\.\n\n\.\n\n\.\n\n', '. . . ', srt)
            srt = re.sub(r'\.\n\n\.\n\n\.”', '. . .”', srt)
            srt = re.sub(r'\.\n\.\n\.\n', '. . . ', srt)

            # Display the cleaned subtitle text
            st.session_state.srt_text = srt
            st.text_area("Vídeo transcrito com sucesso!", srt, height=300)
            st_copy_to_clipboard(st.session_state.srt_text)

        else:
            logging.warning("Subtitle file not found.")
            st.error("Este vídeo não possui um arquivo de legendas.")

    except Exception as e:
        logging.error(f"Error processing video URL: {e}")
        st.error(f"Ocorreu um erro: {e}")

# Streamlit UI
st.title('Transcrição de Vídeos')
page_url = st.text_input('Cole o link da página do vídeo aqui:')

if st.button("Extrair e Transcrever"):
    if page_url:
        logging.info("Extract and transcribe button clicked.")
        video_url = extract_video_url(page_url)
        if video_url:
            process_video_url(video_url)
        else:
            st.warning("Não foi possível extrair o URL do vídeo.")
    else:
        logging.warning("No URL entered by user.")
        st.warning("Por favor, insira o link da página.")

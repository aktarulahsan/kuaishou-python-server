from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import requests
import time
import uuid

app = FastAPI()
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def resolve_redirect_url(short_url: str) -> str:
    response = requests.get(short_url, allow_redirects=True)
    return response.url

def get_real_video_url(page_url: str) -> str:
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920x1080')
    chrome_options.add_argument('--user-agent=Mozilla/5.0')

    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(page_url)
        time.sleep(8)  # give time for video to load

        # Check for <video> tag first
        video_elements = driver.find_elements("tag name", "video")
        for video in video_elements:
            video_url = video.get_attribute("src")
            if video_url and video_url.startswith("http"):
                return video_url

        # Fallback: check <script> tag content
        page_source = driver.page_source
        import re
        matches = re.findall(r'https://[^"]+\.mp4', page_source)
        if matches:
            return matches[0]

        raise HTTPException(status_code=404, detail="Video URL not found.")

    finally:
        driver.quit()

@app.get("/download/")
def download_video(share_url: str):
    try:
        resolved_url = resolve_redirect_url(share_url)
    except Exception:
        raise HTTPException(status_code=400, detail="Could not resolve shared link")

    video_url = get_real_video_url(resolved_url)
    filename = f"{uuid.uuid4().hex}.mp4"
    filepath = os.path.join(DOWNLOAD_DIR, filename)

    with requests.get(video_url, stream=True) as r:
        r.raise_for_status()
        with open(filepath, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    return FileResponse(path=filepath, filename=filename, media_type='video/mp4')
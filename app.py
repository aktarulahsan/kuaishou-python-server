import time
import logging
import uuid
import os
import requests
from fastapi import FastAPI, HTTPException, Query, UploadFile
from fastapi.responses import JSONResponse
from bs4 import BeautifulSoup
import re
from pydantic import BaseModel
import subprocess
# from fastapi import UploadFile
from tempfile import gettempdir

# //
DOWNLOAD_DIR = os.path.join(os.getcwd(), "downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
# //

app = FastAPI()
logging.basicConfig(level=logging.INFO)

# Shared session for faster repeated requests
session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0"})

# Precompiled regex
mp4_regex = re.compile(r'https://[^"]+\.mp4')
playaddr_regex = re.compile(r'"playAddr":"([^"]+)"')

def sanitize_url(raw_url: str) -> str:
    sanitized = raw_url.strip().split(" ")[0]
    logging.info(f"Sanitized URL: {sanitized}")
    return sanitized

from fastapi.staticfiles import StaticFiles

app.mount("/downloads", StaticFiles(directory=DOWNLOAD_DIR), name="downloads")

def resolve_redirect_url(short_url: str, retries=3, timeout=5) -> str:
    for attempt in range(retries):
        try:
            logging.info(f"Resolving short URL (attempt {attempt+1}): {short_url}")
            response = session.get(short_url, allow_redirects=True, timeout=timeout)
            logging.info(f"Resolved to: {response.url}")
            return response.url
        except requests.exceptions.Timeout:
            logging.warning(f"Timeout resolving URL on attempt {attempt+1}, retrying...")
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            break
    raise HTTPException(status_code=400, detail="Could not resolve shared link")

def get_real_video_url(page_url: str) -> str:
    try:
        logging.info(f"Fetching page for video URL extraction: {page_url}")
        response = session.get(page_url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Failed to fetch page: {e}")
        raise HTTPException(status_code=400, detail="Failed to fetch video page")

    soup = BeautifulSoup(response.text, "html.parser")

    video_tags = soup.find_all("video")
    for video in video_tags:
        src = video.get("src")
        if src and src.startswith("http"):
            logging.info(f"Found video URL in <video> tag: {src}")
            return src

    mp4_urls = mp4_regex.findall(response.text)
    if mp4_urls:
        logging.info(f"Found video URL in page content: {mp4_urls[0]}")
        return mp4_urls[0]

    scripts = soup.find_all("script")
    for script in scripts:
        if script.string and "playAddr" in script.string:
            match = playaddr_regex.search(script.string)
            if match:
                video_url = match.group(1).replace('\\u0026', '&').replace('\\', '')
                logging.info(f"Found video URL in script tag JSON: {video_url}")
                return video_url

    raise HTTPException(status_code=404, detail="Video URL not found")

@app.get("/orginal2/")
def download_video(share_url: str = Query(..., description="Kuaishou share URL")):
    logging.info(f"Received share URL: {share_url}")
    start_time = time.time()

    sanitized_url = sanitize_url(share_url)
    resolved_url = resolve_redirect_url(sanitized_url)
    video_url = get_real_video_url(resolved_url)

    total_time = time.time() - start_time
    logging.info(f"Resolved video URL: {video_url}")
    logging.info(f"Total request time: {total_time:.2f}s")

    return JSONResponse(content={"downloadUrl": video_url})

class ShareURLRequest(BaseModel):
    url: str
@app.post("/orginal")
def download_video(request: ShareURLRequest):
    logging.info(f"Received share URL: {request.url}")
    start_time = time.time()

    sanitized_url = sanitize_url(request.url)
    resolved_url = resolve_redirect_url(sanitized_url)
    video_url = get_real_video_url(resolved_url)

    total_time = time.time() - start_time
    logging.info(f"Resolved video URL: {video_url}")
    logging.info(f"Total request time: {total_time:.2f}s")

    return JSONResponse(content={"downloadUrl": video_url})
    
    
@app.get("/hello")   
def hello():
	return {"message": "Wellcome server is running"}


@app.get("/welcome")   
def welcome():
	return {"message": "Wellcome server is running"}
    
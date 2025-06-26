# from fastapi import FastAPI, HTTPException
# from fastapi.responses import FileResponse
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# import os
# import requests
# import time
# import uuid

# app = FastAPI()
# DOWNLOAD_DIR = "downloads"
# os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# def resolve_redirect_url(short_url: str) -> str:
#     response = requests.get(short_url, allow_redirects=True)
#     return response.url

# def get_real_video_url(page_url: str) -> str:
#     chrome_options = Options()
#     chrome_options.add_argument('--headless')
#     chrome_options.add_argument('--no-sandbox')
#     chrome_options.add_argument('--disable-dev-shm-usage')
#     chrome_options.add_argument('--disable-gpu')
#     chrome_options.add_argument('--window-size=1920x1080')
#     chrome_options.add_argument('--user-agent=Mozilla/5.0')

#     driver = webdriver.Chrome(options=chrome_options)

#     try:
#         driver.get(page_url)
#         time.sleep(8)  # give time for video to load

#         # Check for <video> tag first
#         video_elements = driver.find_elements("tag name", "video")
#         for video in video_elements:
#             video_url = video.get_attribute("src")
#             if video_url and video_url.startswith("http"):
#                 return video_url

#         # Fallback: check <script> tag content
#         page_source = driver.page_source
#         import re
#         matches = re.findall(r'https://[^"]+\.mp4', page_source)
#         if matches:
#             return matches[0]

#         raise HTTPException(status_code=404, detail="Video URL not found.")

#     finally:
#         driver.quit()

# @app.get("/download/")
# def download_video(share_url: str):
#     try:
#         resolved_url = resolve_redirect_url(share_url)
#     except Exception:
#         raise HTTPException(status_code=400, detail="Could not resolve shared link")

#     video_url = get_real_video_url(resolved_url)
#     filename = f"{uuid.uuid4().hex}.mp4"
#     filepath = os.path.join(DOWNLOAD_DIR, filename)

#     with requests.get(video_url, stream=True) as r:
#         r.raise_for_status()
#         with open(filepath, 'wb') as f:
#             for chunk in r.iter_content(chunk_size=8192):
#                 f.write(chunk)

#     return FileResponse(path=filepath, filename=filename, media_type='video/mp4')

# //////////

# import time
# from fastapi import FastAPI, HTTPException
# from fastapi.responses import FileResponse
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import os
# import requests
# import uuid
# import logging

# app = FastAPI()
# DOWNLOAD_DIR = "downloads"
# os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# # Logging setup
# logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# def resolve_redirect_url(short_url: str) -> str:
#     logging.info(f"Resolving short URL: {short_url}")
#     attempts = 3
#     for attempt in range(attempts):
#         try:
#             response = requests.get(short_url, allow_redirects=True, timeout=30, headers={
#                 "User-Agent": "Mozilla/5.0"
#             })
#             logging.info(f"Resolved to: {response.url}")
#             return response.url
#         except requests.exceptions.RequestException as e:
#             logging.warning(f"Attempt {attempt + 1} failed: {e}")
#             time.sleep(2)

#     logging.error("All attempts to resolve URL failed.")
#     raise Exception("Could not resolve shared link")

# def get_real_video_url(page_url: str) -> str:
#     logging.info(f"Opening page: {page_url}")
#     chrome_options = Options()
#     chrome_options.add_argument('--headless')
#     chrome_options.add_argument('--no-sandbox')
#     chrome_options.add_argument('--disable-dev-shm-usage')
#     chrome_options.add_argument('--disable-gpu')
#     chrome_options.add_argument('--window-size=1920x1080')
#     chrome_options.add_argument('--user-agent=Mozilla/5.0')

#     driver = webdriver.Chrome(options=chrome_options)

#     try:
#         driver.get(page_url)
#         logging.info("Page loaded. Waiting for video elements...")
#         time.sleep(8)

#         video_elements = driver.find_elements("tag name", "video")
#         logging.info(f"Found {len(video_elements)} <video> tags")
#         for video in video_elements:
#             src = video.get_attribute("src")
#             logging.info(f"Found video src: {src}")
#             if src and src.startswith("http"):
#                 return src

#         # Fallback: try finding .mp4 URL in page source
#         page_source = driver.page_source
#         import re
#         matches = re.findall(r'https://[^"]+\.mp4', page_source)
#         logging.info(f"Found {len(matches)} .mp4 matches in page source")
#         if matches:
#             return matches[0]

#         raise HTTPException(status_code=404, detail="Video URL not found.")

#     finally:
#         driver.quit()

# @app.get("/download/")
# def download_video(share_url: str):
#     logging.info(f"Received share URL: {share_url}")

#     try:
#         resolved_url = resolve_redirect_url(share_url)
#     except Exception as e:
#         logging.error(f"URL resolution failed: {e}")
#         raise HTTPException(status_code=400, detail="Could not resolve shared link")

#     video_url = get_real_video_url(resolved_url)
#     filename = f"{uuid.uuid4().hex}.mp4"
#     filepath = os.path.join(DOWNLOAD_DIR, filename)

#     logging.info(f"Starting download: {video_url}")
#     with requests.get(video_url, stream=True, timeout=15) as r:
#         r.raise_for_status()
#         with open(filepath, 'wb') as f:
#             for chunk in r.iter_content(chunk_size=1024 * 1024):  # 1MB chunks
#                 if chunk:
#                     f.write(chunk)
#         logging.info(f"Download complete: {filepath}")

#     return FileResponse(path=filepath, filename=filename, media_type='video/mp4')


# /////////////


# import time
# import os
# import uuid
# import logging
# import requests
# from fastapi import FastAPI, HTTPException
# from fastapi.responses import FileResponse
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# app = FastAPI()
# DOWNLOAD_DIR = "downloads"
# os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# # Logging setup
# logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# def resolve_redirect_url(short_url: str) -> str:
#     logging.info(f"Resolving short URL: {short_url}")
#     attempts = 3
#     for attempt in range(attempts):
#         try:
#             start = time.perf_counter()
#             response = requests.get(short_url, allow_redirects=True, timeout=30, headers={
#                 "User-Agent": "Mozilla/5.0"
#             })
#             elapsed = time.perf_counter() - start
#             logging.info(f"Resolved to: {response.url} (took {elapsed:.2f}s)")
#             return response.url
#         except requests.exceptions.RequestException as e:
#             logging.warning(f"Attempt {attempt + 1} failed: {e}")
#             time.sleep(2)

#     logging.error("All attempts to resolve URL failed.")
#     raise Exception("Could not resolve shared link")

# def get_real_video_url(page_url: str) -> str:
#     logging.info(f"Opening page: {page_url}")
#     start = time.perf_counter()

#     chrome_options = Options()
#     chrome_options.add_argument('--headless')
#     chrome_options.add_argument('--no-sandbox')
#     chrome_options.add_argument('--disable-dev-shm-usage')
#     chrome_options.add_argument('--disable-gpu')
#     chrome_options.add_argument('--window-size=1920x1080')
#     chrome_options.add_argument('--user-agent=Mozilla/5.0')

#     driver = webdriver.Chrome(options=chrome_options)
#     try:
#         driver.get(page_url)

#         # Wait dynamically for <video> tag to appear
#         try:
#             WebDriverWait(driver, 12).until(EC.presence_of_element_located((By.TAG_NAME, "video")))
#         except:
#             logging.warning("Video tag not found quickly, fallback to page scan")

#         video_elements = driver.find_elements(By.TAG_NAME, "video")
#         logging.info(f"Found {len(video_elements)} <video> tags")
#         for video in video_elements:
#             src = video.get_attribute("src")
#             if src and src.startswith("http"):
#                 logging.info(f"Video src found: {src}")
#                 return src

#         # Fallback to regex extraction
#         page_source = driver.page_source
#         import re
#         matches = re.findall(r'https://[^"]+\.mp4', page_source)
#         logging.info(f"Found {len(matches)} .mp4 matches in page source")
#         if matches:
#             return matches[0]

#         raise HTTPException(status_code=404, detail="Video URL not found.")
#     finally:
#         driver.quit()
#         elapsed = time.perf_counter() - start
#         logging.info(f"Selenium execution took {elapsed:.2f}s")

# @app.get("/download/")
# def download_video(share_url: str):
#     logging.info(f"Received share URL: {share_url}")
#     total_start = time.perf_counter()

#     try:
#         resolved_url = resolve_redirect_url(share_url)
#     except Exception as e:
#         logging.error(f"URL resolution failed: {e}")
#         raise HTTPException(status_code=400, detail="Could not resolve shared link")

#     video_url = get_real_video_url(resolved_url)

#     filename = f"{uuid.uuid4().hex}.mp4"
#     filepath = os.path.join(DOWNLOAD_DIR, filename)

#     logging.info(f"Starting download: {video_url}")
#     start_download = time.perf_counter()
#     with requests.get(video_url, stream=True, timeout=15) as r:
#         r.raise_for_status()
#         with open(filepath, 'wb') as f:
#             for chunk in r.iter_content(chunk_size=1024 * 1024):  # 1MB chunks
#                 if chunk:
#                     f.write(chunk)
#     elapsed_download = time.perf_counter() - start_download
#     logging.info(f"Download complete: {filepath} (took {elapsed_download:.2f}s)")

#     total_elapsed = time.perf_counter() - total_start
#     logging.info(f"Total request time: {total_elapsed:.2f}s")

#     return FileResponse(path=filepath, filename=filename, media_type='video/mp4')




# //////////


# import time
# import logging
# import requests
# from fastapi import FastAPI, HTTPException
# from fastapi.responses import StreamingResponse
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# app = FastAPI()

# # Logging setup
# logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


# def resolve_redirect_url(short_url: str) -> str:
#     logging.info(f"Resolving short URL: {short_url}")
#     attempts = 3
#     for attempt in range(attempts):
#         try:
#             start = time.perf_counter()
#             response = requests.get(short_url, allow_redirects=True, timeout=15, headers={
#                 "User-Agent": "Mozilla/5.0"
#             })
#             elapsed = time.perf_counter() - start
#             logging.info(f"Resolved to: {response.url} (took {elapsed:.2f}s)")
#             return response.url
#         except requests.exceptions.RequestException as e:
#             logging.warning(f"Attempt {attempt + 1} failed: {e}")
#             time.sleep(1)

#     raise HTTPException(status_code=400, detail="Could not resolve shared link")


# def get_real_video_url(page_url: str) -> str:
#     logging.info(f"Opening page: {page_url}")
#     start = time.perf_counter()

#     chrome_options = Options()
#     chrome_options.add_argument('--headless')
#     chrome_options.add_argument('--no-sandbox')
#     chrome_options.add_argument('--disable-dev-shm-usage')
#     chrome_options.add_argument('--disable-gpu')
#     chrome_options.add_argument('--window-size=1920x1080')
#     chrome_options.add_argument('--user-agent=Mozilla/5.0')

#     driver = webdriver.Chrome(options=chrome_options)
#     try:
#         driver.get(page_url)

#         try:
#             WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "video")))
#         except:
#             logging.warning("Video tag not found quickly, fallback to page scan")

#         video_elements = driver.find_elements(By.TAG_NAME, "video")
#         for video in video_elements:
#             src = video.get_attribute("src")
#             if src and src.startswith("http"):
#                 logging.info(f"Found video URL: {src}")
#                 return src

#         import re
#         matches = re.findall(r'https://[^"]+\.mp4', driver.page_source)
#         if matches:
#             logging.info(f"Fallback found video URL: {matches[0]}")
#             return matches[0]

#         raise HTTPException(status_code=404, detail="Video URL not found.")

#     finally:
#         driver.quit()
#         logging.info(f"Selenium finished in {time.perf_counter() - start:.2f}s")


# @app.get("/download/")
# def download_video(share_url: str):
#     total_start = time.perf_counter()
#     logging.info(f"Received share URL: {share_url}")

#     resolved_url = resolve_redirect_url(share_url)
#     video_url = get_real_video_url(resolved_url)

#     logging.info(f"Streaming video from: {video_url}")
#     try:
#         r = requests.get(video_url, stream=True, timeout=15)
#         r.raise_for_status()
#     except Exception as e:
#         logging.error(f"Failed to stream video: {e}")
#         raise HTTPException(status_code=500, detail="Failed to stream video")

#     total_elapsed = time.perf_counter() - total_start
#     logging.info(f"Total request time: {total_elapsed:.2f}s")

#     return StreamingResponse(r.iter_content(chunk_size=1024 * 1024),
#                              media_type="video/mp4",
#                              headers={"Content-Disposition": f'attachment; filename="video.mp4"'})



# import time
# import uuid
# import os
# import logging
# import requests
# from fastapi import FastAPI, HTTPException
# from fastapi.responses import JSONResponse, StreamingResponse
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options

# app = FastAPI()

# # Logging setup
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s - %(levelname)s - %(message)s"
# )

# def resolve_redirect_url(short_url: str) -> str:
#     logging.info(f"Resolving short URL: {short_url}")
#     start = time.time()
#     try:
#         response = requests.get(short_url, allow_redirects=True, timeout=30, headers={
#             "User-Agent": "Mozilla/5.0"
#         })
#         resolved = response.url
#         elapsed = time.time() - start
#         logging.info(f"Resolved to: {resolved} (took {elapsed:.2f}s)")
#         return resolved
#     except requests.exceptions.RequestException as e:
#         logging.error(f"Failed to resolve URL: {e}")
#         raise HTTPException(status_code=400, detail="Could not resolve shared link")

# def get_real_video_url(page_url: str) -> str:
#     logging.info(f"Opening page: {page_url}")
#     chrome_options = Options()
#     chrome_options.add_argument('--headless')
#     chrome_options.add_argument('--no-sandbox')
#     chrome_options.add_argument('--disable-dev-shm-usage')
#     chrome_options.add_argument('--disable-gpu')
#     chrome_options.add_argument('--window-size=1920x1080')
#     chrome_options.add_argument('--user-agent=Mozilla/5.0')

#     driver = webdriver.Chrome(options=chrome_options)

#     try:
#         start = time.time()
#         driver.get(page_url)
#         time.sleep(5)

#         video_elements = driver.find_elements("tag name", "video")
#         for video in video_elements:
#             src = video.get_attribute("src")
#             if src and src.startswith("http"):
#                 logging.info(f"Found video tag src: {src}")
#                 logging.info(f"Selenium finished in {time.time() - start:.2f}s")
#                 return src

#         # Fallback: Find .mp4 in page source
#         import re
#         matches = re.findall(r'https://[^"]+\.mp4', driver.page_source)
#         if matches:
#             logging.info(f"Fallback found video URL: {matches[0]}")
#             logging.info(f"Selenium finished in {time.time() - start:.2f}s")
#             return matches[0]

#         raise HTTPException(status_code=404, detail="Video URL not found.")

#     finally:
#         driver.quit()
# @app.get("/download/")
# def download_video(share_url: str):
#     logging.info(f"Received share URL: {share_url}")
#     start = time.time()

#     resolved_url = resolve_redirect_url(share_url)
#     video_url = get_real_video_url(resolved_url)

#     logging.info(f"Resolved and extracted video URL: {video_url}")
#     logging.info(f"Total request time: {time.time() - start:.2f}s")

#     return JSONResponse(content={"downloadUrl": video_url})

# import time
# import logging
# import re
# import requests
# from urllib.parse import unquote
# from fastapi import FastAPI, HTTPException
# from fastapi.responses import JSONResponse
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options

# app = FastAPI()

# # Logging setup
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s - %(levelname)s - %(message)s"
# )

# def sanitize_url(raw_url: str) -> str:
#     """Extract only the first valid HTTP/HTTPS URL from the input."""
#     decoded = unquote(raw_url)
#     match = re.search(r"https?://[^\s\"']+", decoded)
#     if not match:
#         logging.error("No valid URL found in input")
#         raise HTTPException(status_code=400, detail="No valid URL found in input")
#     return match.group(0)

# def resolve_redirect_url(short_url: str) -> str:
#     logging.info(f"Resolving short URL: {short_url}")
#     start = time.time()
#     try:
#         response = requests.get(short_url, allow_redirects=True, timeout=10, headers={
#             "User-Agent": "Mozilla/5.0"
#         })
#         resolved = response.url
#         elapsed = time.time() - start
#         logging.info(f"Resolved to: {resolved} (took {elapsed:.2f}s)")
#         return resolved
#     except requests.exceptions.RequestException as e:
#         logging.error(f"Failed to resolve URL: {e}")
#         raise HTTPException(status_code=400, detail="Could not resolve shared link")

# def get_real_video_url(page_url: str) -> str:
#     logging.info(f"Opening page: {page_url}")
#     chrome_options = Options()
#     chrome_options.add_argument('--headless')
#     chrome_options.add_argument('--no-sandbox')
#     chrome_options.add_argument('--disable-dev-shm-usage')
#     chrome_options.add_argument('--disable-gpu')
#     chrome_options.add_argument('--window-size=1920x1080')
#     chrome_options.add_argument('--user-agent=Mozilla/5.0')

#     driver = webdriver.Chrome(options=chrome_options)

#     try:
#         start = time.time()
#         driver.get(page_url)
#         time.sleep(2.5)  # optimized from 5s to 2.5s

#         video_elements = driver.find_elements("tag name", "video")
#         for video in video_elements:
#             src = video.get_attribute("src")
#             if src and src.startswith("http"):
#                 logging.info(f"Found video tag src: {src}")
#                 logging.info(f"Selenium finished in {time.time() - start:.2f}s")
#                 return src

#         # Fallback: Look for .mp4 URLs
#         matches = re.findall(r'https://[^"]+\.mp4', driver.page_source)
#         if matches:
#             logging.info(f"Fallback found video URL: {matches[0]}")
#             logging.info(f"Selenium finished in {time.time() - start:.2f}s")
#             return matches[0]

#         raise HTTPException(status_code=404, detail="Video URL not found.")
#     finally:
#         driver.quit()

# @app.get("/download/")
# def download_video(share_url: str):
#     logging.info(f"Received raw share URL: {share_url}")
#     start = time.time()

#     sanitized_url = sanitize_url(share_url)
#     logging.info(f"Sanitized URL: {sanitized_url}")

#     resolved_url = resolve_redirect_url(sanitized_url)
#     video_url = get_real_video_url(resolved_url)

#     logging.info(f"Resolved and extracted video URL: {video_url}")
#     logging.info(f"Total request time: {time.time() - start:.2f}s")

#     return JSONResponse(content={"downloadUrl": video_url})




# import time
# import logging
# import requests
# from fastapi import FastAPI, HTTPException, Query
# from fastapi.responses import JSONResponse
# from bs4 import BeautifulSoup

# app = FastAPI()

# logging.basicConfig(level=logging.INFO)

# def sanitize_url(raw_url: str) -> str:
#     """
#     Extract only the base short URL part before any space or query params.
#     Example: "https://v.kuaishou.com/2CIW3U2 some text" => "https://v.kuaishou.com/2CIW3U2"
#     """
#     sanitized = raw_url.strip().split(" ")[0]
#     logging.info(f"Sanitized URL: {sanitized}")
#     return sanitized

# def resolve_redirect_url(short_url: str, retries=3, timeout=10) -> str:
#     """
#     Follow redirects to get the final URL. Retry if timeout occurs.
#     """
#     headers = {"User-Agent": "Mozilla/5.0"}
#     for attempt in range(retries):
#         try:
#             logging.info(f"Resolving short URL (attempt {attempt+1}): {short_url}")
#             response = requests.get(short_url, allow_redirects=True, timeout=timeout, headers=headers)
#             logging.info(f"Resolved to: {response.url}")
#             return response.url
#         except requests.exceptions.Timeout:
#             logging.warning(f"Timeout resolving URL on attempt {attempt+1}, retrying...")
#         except requests.exceptions.RequestException as e:
#             logging.error(f"Request failed: {e}")
#             break
#     raise HTTPException(status_code=400, detail="Could not resolve shared link")

# def get_real_video_url(page_url: str) -> str:
#     """
#     Fetch page and extract video URL using requests + BeautifulSoup (no Selenium).
#     This method is faster.
#     """
#     headers = {"User-Agent": "Mozilla/5.0"}
#     try:
#         logging.info(f"Fetching page for video URL extraction: {page_url}")
#         response = requests.get(page_url, headers=headers, timeout=10)
#         response.raise_for_status()
#     except requests.RequestException as e:
#         logging.error(f"Failed to fetch page: {e}")
#         raise HTTPException(status_code=400, detail="Failed to fetch video page")

#     soup = BeautifulSoup(response.text, "html.parser")

#     # Strategy 1: Look for <video> tags (unlikely in HTML response, but keep it)
#     video_tags = soup.find_all("video")
#     for video in video_tags:
#         src = video.get("src")
#         if src and src.startswith("http"):
#             logging.info(f"Found video URL in <video> tag: {src}")
#             return src

#     # Strategy 2: Search for .mp4 URLs in script or page text
#     import re
#     mp4_urls = re.findall(r'https://[^"]+\.mp4', response.text)
#     if mp4_urls:
#         logging.info(f"Found video URL in page content: {mp4_urls[0]}")
#         return mp4_urls[0]

#     # Strategy 3: Sometimes the video URL is embedded in JSON in <script> tags
#     scripts = soup.find_all("script")
#     for script in scripts:
#         if script.string and "playAddr" in script.string:
#             match = re.search(r'"playAddr":"([^"]+)"', script.string)
#             if match:
#                 video_url = match.group(1).replace('\\u0026', '&').replace('\\', '')
#                 logging.info(f"Found video URL in script tag JSON: {video_url}")
#                 return video_url

#     raise HTTPException(status_code=404, detail="Video URL not found")

# @app.get("/download/")
# def download_video(share_url: str = Query(..., description="Kuaishou share URL")):
#     logging.info(f"Received share URL: {share_url}")
#     start_time = time.time()

#     sanitized_url = sanitize_url(share_url)
#     resolved_url = resolve_redirect_url(sanitized_url)
#     video_url = get_real_video_url(resolved_url)

#     total_time = time.time() - start_time
#     logging.info(f"Resolved video URL: {video_url}")
#     logging.info(f"Total request time: {total_time:.2f}s")

#     return JSONResponse(content={"downloadUrl": video_url})

###############################


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



class EnhancedRequest(BaseModel):
    url: str
    resolution: str  # e.g., "640x360"
    fps: int   



DOWNLOAD_DIR = os.path.join(os.getcwd(), "downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
from playwright.sync_api import sync_playwright
class EnhancedRequest(BaseModel):
    url: str
    resolution: str  # e.g., '1280x720', '1920x1080', '3840x2160'
    fps: int         # e.g., 30 or 60

def resolve_url_with_playwright(url: str) -> str:
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False, args=["--start-maximized"])
            # page.set_user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36")
            page = browser.new_page()
            page.goto(url, timeout=15000)
            resolved = page.url
            browser.close()
            logging.info(f"Resolved final URL: {resolved}")
            return resolved
    except Exception as e:
        logging.error(f"Playwright resolution failed: {e}")
        raise HTTPException(status_code=502, detail="URL resolution failed")

def download_video_with_ytdlp(url: str, output_path: str):
    try:
        cmd = [
            "yt-dlp", "-f", "best", "-o", output_path, url
        ]
        subprocess.run(cmd, check=True)
        logging.info("Video downloaded using yt-dlp")
    except subprocess.CalledProcessError as e:
        logging.error(f"yt-dlp failed: {e}")
        raise HTTPException(status_code=500, detail="Video download failed")

@app.post("/enhanced")
def enhance_video(request: EnhancedRequest):
    logging.info(f"Enhancing video from URL: {request.url} to {request.resolution} @ {request.fps}fps")
    start_time = time.time()

    # Step 1: Resolve short URL
    resolved_url = resolve_url_with_playwright(request.url)

    # Step 2: Prepare paths
    video_id = str(uuid.uuid4())
    raw_path = os.path.join(DOWNLOAD_DIR, f"{video_id}_raw.%(ext)s")
    input_path = os.path.join(DOWNLOAD_DIR, f"{video_id}_raw.mp4")
    output_path = os.path.join(DOWNLOAD_DIR, f"{video_id}_enhanced.mp4")

    # Step 3: Download the video
    download_video_with_ytdlp(resolved_url, raw_path)

    # Sometimes yt-dlp outputs different extensions, find the real file
    actual_input = None
    for f in os.listdir(DOWNLOAD_DIR):
        if f.startswith(f"{video_id}_raw") and f.endswith(".mp4"):
            actual_input = os.path.join(DOWNLOAD_DIR, f)
            break
    if not actual_input:
        raise HTTPException(status_code=500, detail="Downloaded video not found")

    # Step 4: Transcode using ffmpeg
    try:
        logging.info(f"Transcoding video to {request.resolution} @ {request.fps}fps")
        cmd = [
            "ffmpeg", "-i", actual_input,
            "-vf", f"scale={request.resolution}",
            "-r", str(request.fps),
            "-y",
            output_path
        ]
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"FFmpeg failed: {e}")
        raise HTTPException(status_code=500, detail="Video processing failed")

    total_time = time.time() - start_time
    logging.info(f"Video processed in {total_time:.2f} seconds. Saved at: {output_path}")

    return JSONResponse(content={
        "downloadUrl": f"/downloads/{os.path.basename(output_path)}",
        "processingTime": f"{total_time:.2f}s"
    })
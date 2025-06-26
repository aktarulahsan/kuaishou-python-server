from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
from pathlib import Path
import re
import os
import uuid
import subprocess
import shutil
import logging
from typing import Optional
from playwright.async_api import async_playwright

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class KuaiShouDownloader:
    @staticmethod
    async def get_video_url(short_url: str) -> Optional[str]:
        """Extract video URL with enhanced Playwright setup"""
        try:
            async with async_playwright() as p:
                # Launch browser with more natural settings
                browser = await p.chromium.launch(
                    headless=False,  # Try with visible browser first
                    timeout=30000,
                    args=[
                        '--disable-blink-features=AutomationControlled',
                        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                    ]
                )
                
                context = await browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                    locale="en-US",
                    viewport={"width": 1920, "height": 1080},
                    java_script_enabled=True
                )
                
                # Block unnecessary resources
                await context.route("**/*.{png,jpg,jpeg,svg,gif,webp}", lambda route: route.abort())
                
                page = await context.new_page()
                
                try:
                    # Navigate with longer timeout and wait for network idle
                    await page.goto(
                        short_url,
                        timeout=45000,
                        wait_until="networkidle"
                    )
                    
                    # Wait for video element to appear
                    try:
                        await page.wait_for_selector('video', timeout=15000)
                    except:
                        # If video not found, try to find alternative sources
                        content = await page.content()
                        if 'video' in content:
                            # Try alternative extraction methods
                            video_url = await KuaiShouDownloader.extract_from_page_content(content)
                            if video_url:
                                return video_url
                        raise
                    
                    # Get video element
                    video_element = await page.query_selector('video')
                    if video_element:
                        video_url = await video_element.get_attribute('src')
                        if not video_url:
                            # Try to get source from child source elements
                            source_element = await video_element.query_selector('source')
                            if source_element:
                                video_url = await source_element.get_attribute('src')
                        
                        if video_url:
                            # Ensure URL is absolute
                            if video_url.startswith('//'):
                                video_url = f'https:{video_url}'
                            elif video_url.startswith('/'):
                                video_url = f'https://www.kuaishou.com{video_url}'
                            
                            return video_url
                    
                    # Fallback to content analysis
                    content = await page.content()
                    return await KuaiShouDownloader.extract_from_page_content(content)
                
                finally:
                    await browser.close()
                
        except Exception as e:
            logger.error(f"Playwright error: {str(e)}")
            return None

    @staticmethod
    async def extract_from_page_content(content: str) -> Optional[str]:
        """Alternative extraction from page content"""
        try:
            patterns = [
                r'"srcNoMark":"([^"]+)"',
                r'"playUrl":"([^"]+)"',
                r'video-src="([^"]+)"',
                r'src="(https?://[^"]+\.mp4)"'
            ]
            
            for pattern in patterns:
                match = re.search(pattern, content)
                if match:
                    url = match.group(1)
                    # Clean up URL
                    url = url.replace('\\u002F', '/')
                    if not url.startswith('http'):
                        if url.startswith('//'):
                            url = f'https:{url}'
                        else:
                            url = f'https://{url}'
                    return url
            return None
        except Exception as e:
            logger.error(f"Content extraction failed: {str(e)}")
            return None

    @staticmethod
    def download_video(url: str, save_path: Path) -> bool:
        """Enhanced download with retries"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://www.kuaishou.com/',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Range': 'bytes=0-'
        }
        
        for attempt in range(3):
            try:
                with requests.get(url, stream=True, headers=headers, timeout=30) as r:
                    r.raise_for_status()
                    with open(save_path, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                return True
            except Exception as e:
                logger.warning(f"Download attempt {attempt + 1} failed: {str(e)}")
                if attempt == 2:
                    return False
                continue

    @staticmethod
    def process_video(input_path: Path, output_path: Path, resolution: str, fps: str) -> bool:
        """Process video with FFmpeg"""
        try:
            cmd = [
                'ffmpeg',
                '-i', str(input_path),
                '-vf', f'scale={resolution},fps={fps}',
                '-c:v', 'libx264',
                '-preset', 'fast',
                '-crf', '18',
                '-movflags', 'faststart',
                '-y',
                str(output_path)
            ]
            subprocess.run(cmd, check=True, capture_output=True, timeout=300)
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"FFmpeg error: {e.stderr.decode()}")
            return False
        except Exception as e:
            logger.error(f"Processing error: {str(e)}")
            return False

@app.get("/enhanced")
async def enhance_video(
    url: str = Query(..., description="KuaiShou video URL"),
    resolution: str = Query("3840x2160", description="Output resolution"),
    fps: str = Query("60", description="Output FPS")
):
    try:
        # Validate URL
        if not url.startswith('https://v.kuaishou.com/'):
            raise HTTPException(400, detail="Only KuaiShou short links are supported")
        
        # Step 1: Extract video URL
        video_url = await KuaiShouDownloader.get_video_url(url)
        if not video_url:
            raise HTTPException(400, detail="Failed to extract video URL. This might be due to: "
                                          "1) Invalid or private video "
                                          "2) KuaiShou updated their page structure "
                                          "3) Regional restrictions")
        
        logger.info(f"Extracted video URL: {video_url}")
        
        # Step 2: Setup working directory
        work_dir = Path(f"temp/{uuid.uuid4()}")
        work_dir.mkdir(parents=True, exist_ok=True)
        original_path = work_dir / "original.mp4"
        processed_path = work_dir / "processed.mp4"
        
        # Step 3: Download video
        if not KuaiShouDownloader.download_video(video_url, original_path):
            raise HTTPException(400, detail="Failed to download video file. The video might be unavailable or protected")
        
        # Step 4: Process video
        if not KuaiShouDownloader.process_video(original_path, processed_path, resolution, fps):
            raise HTTPException(400, detail="Video processing failed. Invalid video format or corrupted download")
        
        # Step 5: Return the processed video
        return FileResponse(
            processed_path,
            media_type='video/mp4',
            filename=f'enhanced_{resolution}_{fps}fps.mp4',
            background=BackgroundTask(lambda: shutil.rmtree(work_dir, ignore_errors=True))
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(500, detail="Internal server error")
    finally:
        if 'work_dir' in locals() and work_dir.exists():
            shutil.rmtree(work_dir, ignore_errors=True)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000, log_level="info")
import time
import os
import requests
import re
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright

OUTPUT_DIR = r"c:\Users\HP Victus 15\Downloads\BRWAX_site_v1_pudim\BRWAX_site_v1_pudim\site_creator\assets\extracted_pdf_images"
SITE_URL = "https://brwax.my.canva.site/"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def download_image(url, name):
    name = re.sub(r'[\\/*?:"<>|]', "", name)
    name = name.strip()
    if not name:
        return
        
    ext = os.path.splitext(urlparse(url).path)[1]
    if not ext:
        ext = ".jpg"
        
    filename = f"{name}{ext}"
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    # Simple check to avoid redownloading, though maybe we want to overwrite
    try:
        resp = requests.get(url, stream=True)
        if resp.status_code == 200:
            with open(filepath, 'wb') as f:
                for chunk in resp.iter_content(1024):
                    f.write(chunk)
            print(f"Downloaded: {filename}")
        else:
            print(f"Failed to download {filename} (HTTP {resp.status_code})")
    except Exception as e:
        print(f"Error downloading {filename}: {e}")

def run():
    print("Starting Playwright...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(SITE_URL, wait_until="networkidle")
        
        # Scroll to bottom slowly to trigger lazy loading
        print("Scrolling page to load all images...")
        last_height = page.evaluate("document.body.scrollHeight")
        while True:
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(2)
            new_height = page.evaluate("document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            
        # Give a moment for remaining requests
        time.sleep(5)
        
        # Extract image data
        # Canva often uses divs with background-image or img tags. Let's find img tags first
        # and try to extract 'alt' texts or nearby text nodes for the title.
        print("Extracting images...")
        images = page.locator("img").all()
        downloaded = set()
        count = 1
        
        for img in images:
            src = img.get_attribute("src")
            if not src or "data:image" in src:
                continue
                
            # If Canva delivers scaled images, try to get the highest res. Usually src resolves to the max requested.
            # Canva urls look like: https://m.media-amazon.com... or internal. Removing query params might get original.
            # Let's clean the query param or keep it if needed. For now just fetch what's in src.
            # Canva srcs sometimes have ?width=xxx. If so, drop the query to get full res if possible.
            # But let's just get what we have first.
            
            alt = img.get_attribute("alt")
            
            name_to_use = ""
            if alt and alt.strip() and len(alt.strip()) < 100:
                name_to_use = alt.strip()
            else:
                # Canva text elements are often absolute positioned over or near images.
                # Let's just use generic numbering if we can't find a name, but user explicitly asked to "nomeadas"
                # If alt exists, usually it's the named layer in Canva!
                name_to_use = f"scraped_img_{count}"
                
            if src not in downloaded:
                download_image(src, name_to_use)
                downloaded.add(src)
                count += 1
                
        browser.close()
        print(f"Total images found and processed: {len(downloaded)}")

if __name__ == "__main__":
    run()

import time
import os
import requests
import re
from playwright.sync_api import sync_playwright

OUTPUT_DIR = r"c:\Users\HP Victus 15\Downloads\BRWAX_site_v1_pudim\BRWAX_site_v1_pudim\site_creator\assets\extracted_pdf_images"

def slugify(text):
    text = re.sub(r'[\\/*?:"<>|\n\r]+', ' ', text).strip()
    # take first ~100 characters max
    return text[:100].strip()

def run():
    print("Starting Playwright slider extraction...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://brwax.my.canva.site/", wait_until="networkidle")
        
        current_page = 1
        downloaded_images = set()

        while True:
            time.sleep(3)
            # Find the title on the current view.
            # Canva texts are complex. We use innerText of specific typography blocks
            title_text = page.evaluate('''() => {
                let text = "";
                Array.from(document.querySelectorAll('p._28USrA')).forEach(e => {
                    text += " " + e.innerText;
                });
                return text;
            }''')
            
            clean_name = slugify(title_text)
            if not clean_name:
                clean_name = f"Slide_{current_page}"
                
            # Then get all imgs
            imgs = page.evaluate('''() => {
                let t = [];
                document.querySelectorAll('img').forEach(i => {
                    // Check if it's within the viewport roughly
                    let rect = i.getBoundingClientRect();
                    if(rect.right > 0 && rect.left < window.innerWidth) {
                        t.push(i.src);
                    }
                });
                return t;
            }''')
            
            idx = 1
            for img_url in imgs:
                if not img_url or "data:image" in img_url or ".svg" in img_url or "favicon" in img_url: 
                    continue
                    
                if img_url not in downloaded_images:
                    downloaded_images.add(img_url)
                    filename = f"{clean_name}_{idx}.jpg"
                    filepath = os.path.join(OUTPUT_DIR, filename)
                    
                    print(f"Downloading {filename}")
                    try:
                        r = requests.get(img_url, stream=True)
                        if r.status_code == 200:
                            with open(filepath, 'wb') as f:
                                for chunk in r.iter_content(1024):
                                    f.write(chunk)
                    except Exception as e:
                        print(f"Error downloading {img_url}: {e}")
                    idx += 1
            
            # Click next
            next_btn = page.query_selector('button[aria-label="Próxima página (Direita)"]')
            if not next_btn:
                print("No next button found.")
                break
                
            if next_btn.get_attribute('aria-disabled') == 'true':
                print("End of slideshow reached.")
                break
                
            next_btn.click()
            current_page += 1
            
        browser.close()
        print(f"Extracted {len(downloaded_images)} images.")

if __name__ == "__main__":
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    run()

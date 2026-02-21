import time
import os
import requests
import re
import json
from playwright.sync_api import sync_playwright

OUTPUT_DIR = r"c:\Users\HP Victus 15\Downloads\BRWAX_site_v1_pudim\BRWAX_site_v1_pudim\site_creator\assets\extracted_pdf_images"
MANIFEST = r"c:\Users\HP Victus 15\Downloads\BRWAX_site_v1_pudim\BRWAX_site_v1_pudim\site_creator\assets\projects_manifest.json"

with open(MANIFEST, 'r', encoding='utf-8') as f:
    manifest_data = json.load(f)

# Hard-coded known mappings for speed and accuracy
KNOWN_HINTS = {
    'converse': 'CONVERSE ALL STORIES ARE TRUE',
    'all stories are true': 'CONVERSE ALL STORIES ARE TRUE',
    'city forest': 'CONVERSE CITY FOREST',
    'anitta': 'ANITTA - GLOBAL CITIZEN FESTIVAL',
    'disney': 'DISNEY - ALIEN EARTH',
    'alien earth': 'DISNEY - ALIEN EARTH',
    'ballantine': 'BALLANTINES - MOXXI',
    'moxxi': 'BALLANTINES - MOXXI',
    'cabelinho': 'SHOW CABELINHO LISBOA',
    'djonga': 'DJONGA - INOCENTE CAMPANHA',
    'daki': 'DAKI - UM ANO SEM PERRENGUES',
    'perrengue': 'DAKI - UM ANO SEM PERRENGUES',
    'vibra': 'FILME - VIBRA',
    'nubank': 'NUBANK - PAPO DE PATROA',
    'patroa': 'NUBANK - PAPO DE PATROA',
    'iza': 'IZA - THE TOWN',
    'jack daniel': 'JACK DANIELS - MARCELO D2',
    'marcelo d2': 'JACK DANIELS - MARCELO D2',
    'ludmilla': 'LUDMILLA VERANO SHOW',
    'mario bros': 'MARIO BROS LOLLAPALOOZA',
    'ambev': 'AMBEV - 25 ANOS',
    'meta': 'META AFROPUNK',
    'afropunk': 'META AFROPUNK',
    'youtube': 'YOUTUBE SHORTS BRASIL',
    'shorts': 'YOUTUBE SHORTS BRASIL',
    'versus': 'MIXTAPE VERSUS - TROPKILLAZ',
    'mixtape': 'MIXTAPE VERSUS - TROPKILLAZ',
    'tropkillaz': 'MIXTAPE VERSUS - TROPKILLAZ',
    'spotify': 'SPOTIFY - TOP BRASIL',
    'top brasil': 'SPOTIFY - TOP BRASIL',
    'caetano': 'TURNÊ CAETANO E BETHANIA',
    'bethania': 'TURNÊ CAETANO E BETHANIA'
}

def match_project_title(text):
    text_lower = text.lower()
    
    # First: Check known hints specifically
    for hint, project_name in KNOWN_HINTS.items():
        if hint in text_lower:
            return project_name
            
    # Second: Check if part of the text directly matches the title array
    best_match = None
    best_score = 0
    words_in_text = set(re.findall(r'\b\w+\b', text_lower))
    
    for p in manifest_data:
        title = p['title']
        clean_title = re.sub(r'[^a-z0-9\s]', ' ', title.lower()).strip()
        title_words = set(re.findall(r'\b\w+\b', clean_title))
        
        intersection = words_in_text.intersection(title_words)
        score = len(intersection) / float(max(len(title_words), 1))
        
        if score > best_score:
            best_score = score
            best_match = title
            
    if best_score >= 0.3:
        return best_match
        
    return None

def run():
    print("Starting Playwright slider extraction...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://brwax.my.canva.site/", wait_until="networkidle")
        
        # Accept cookies if the dialog exists to prevent blocking viewport
        try:
            btn = page.query_selector('button:has-text("Aceitar")')
            if btn: btn.click()
        except:
            pass

        current_page = 1
        downloaded_images = set()
        
        # State: last identified project title
        current_project_title = "BRWAX - INITIAL"
        project_image_counts = {}

        while True:
            time.sleep(2.5) # Time for animations to finish loading
            
            # Fetch texts only within the VERY viewport center.
            # Canva places slide wrappers, let's grab texts within the viewport.
            texts_in_viewport = page.evaluate('''() => {
                let texts = [];
                // Look for header/paragraph texts
                document.querySelectorAll('p, h1, h2, h3, span').forEach(el => {
                    let rect = el.getBoundingClientRect();
                    // Check if it is primarily in the active center area [left > 0 && right < window.innerWidth]
                    // Canva often stretches things.
                    let isVisible = (rect.width > 0 && rect.height > 0) &&
                                    (window.getComputedStyle(el).opacity !== '0') && 
                                    (rect.left >= -50 && rect.right <= window.innerWidth + 50);
                                    
                    if (isVisible && el.innerText.trim().length > 3) {
                        texts.push(el.innerText);
                    }
                });
                return texts.join(' ');
            }''')
            
            # Try to match a strong project title from viewport text
            matched_title = match_project_title(texts_in_viewport)
            if matched_title:
                current_project_title = matched_title
                print(f"[Slide {current_page}] Title DETECTED: {current_project_title}")
            else:
                print(f"[Slide {current_page}] No clear title, carrying over: {current_project_title}")
                
            # Now download all images currently in the viewport
            imgs = page.evaluate('''() => {
                let t = [];
                document.querySelectorAll('img').forEach(i => {
                    let rect = i.getBoundingClientRect();
                    if(rect.width > 20 && rect.height > 20 && rect.left > -100 && rect.right < window.innerWidth + 100) {
                        t.push(i.src);
                    }
                });
                return t;
            }''')
            
            for img_url in imgs:
                if not img_url or "data:image" in img_url or ".svg" in img_url or "favicon" in img_url: 
                    continue
                    
                if img_url not in downloaded_images:
                    downloaded_images.add(img_url)
                    
                    # Update counter
                    if current_project_title not in project_image_counts:
                        project_image_counts[current_project_title] = 0
                    project_image_counts[current_project_title] += 1
                    
                    idx = project_image_counts[current_project_title]
                    
                    filename = f"{current_project_title} - {idx}.jpg"
                    # Remove unsafe chars for windows files
                    filename = re.sub(r'[\\/*?:"<>|]', '-', filename)
                    filepath = os.path.join(OUTPUT_DIR, filename)
                    
                    print(f" -> Downloading {filename}")
                    try:
                        r = requests.get(img_url, stream=True)
                        if r.status_code == 200:
                            with open(filepath, 'wb') as f:
                                for chunk in r.iter_content(1024):
                                    f.write(chunk)
                    except Exception as e:
                        print(f"Error downloading {img_url}: {e}")
            
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
        print(f"Extracted {len(downloaded_images)} clean named images.")

if __name__ == "__main__":
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    run()

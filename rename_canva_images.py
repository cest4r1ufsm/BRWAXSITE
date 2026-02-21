import os
import re
import json
import difflib
import shutil

OUTPUT_DIR = r"c:\Users\HP Victus 15\Downloads\BRWAX_site_v1_pudim\BRWAX_site_v1_pudim\site_creator\assets\extracted_pdf_images"
MANIFEST = r"c:\Users\HP Victus 15\Downloads\BRWAX_site_v1_pudim\BRWAX_site_v1_pudim\site_creator\assets\projects_manifest.json"

if not os.path.exists(MANIFEST):
    print("No manifest found!")
    exit(1)

with open(MANIFEST, 'r', encoding='utf-8') as f:
    manifest_data = json.load(f)

projects = [p['title'] for p in manifest_data]

def get_best_match(filename):
    # The filename usually starts with the actual slide title.
    # We grab the first 30 chars approx to match.
    prefix = filename[:40].lower()
    prefix = re.sub(r'[^a-z0-9\s]', ' ', prefix).strip()
    
    # Simple keyword mappings based on the user's manual matches we know about
    if 'converse' in prefix and 'city' in prefix: return "CONVERSE CITY FOREST"
    if 'converse' in prefix and 'story' in prefix: return "CONVERSE ALL STORIES ARE TRUE"
    if 'converse' in prefix and 'stories' in prefix: return "CONVERSE ALL STORIES ARE TRUE"
    if 'anitta' in prefix: return "ANITTA - GLOBAL CITIZEN FESTIVAL"
    if 'disney' in prefix or 'alien' in prefix: return "DISNEY - ALIEN EARTH"
    if 'ballantines' in prefix or 'moxxi' in prefix: return "BALLANTINES - MOXXI"
    if 'cabelinho' in prefix: return "SHOW CABELINHO LISBOA"
    if 'djonga' in prefix: return "DJONGA - INOCENTE CAMPANHA"
    if 'daki' in prefix: return "DAKI - UM ANO SEM PERRENGUES"
    if 'vibra' in prefix: return "FILME - VIBRA"
    if 'nubank' in prefix or 'patroa' in prefix: return "NUBANK - PAPO DE PATROA"
    if 'iza' in prefix: return "IZA - THE TOWN"
    if 'jack daniel' in prefix or 'marcelo' in prefix: return "JACK DANIELS - MARCELO D2"
    if 'ludmilla' in prefix: return "LUDMILLA VERANO SHOW"
    if 'mario' in prefix or 'lollapalooza' in prefix: return "MARIO BROS LOLLAPALOOZA"
    if 'ambev' in prefix: return "AMBEV - 25 ANOS"
    if 'meta' in prefix or 'afropunk' in prefix: return "META AFROPUNK"
    if 'youtube' in prefix or 'shorts' in prefix: return "YOUTUBE SHORTS BRASIL"
    if 'versus' in prefix or 'mixtape' in prefix or 'tropkillaz' in prefix: return "MIXTAPE VERSUS - TROPKILLAZ"
    if 'spotify' in prefix: return "SPOTIFY - TOP BRASIL"
    if 'caetano' in prefix or 'bethania' in prefix: return "TURNÊ CAETANO E BETHANIA"
    
    # Add a fuzzy match fallback
    best = None
    best_score = 0
    for title in projects:
        clean_title = re.sub(r'[^a-z0-9\s]', ' ', title.lower()).strip()
        
        # Word overlap
        words_prefix = set(prefix.split())
        words_title = set(clean_title.split())
        intersection = words_prefix.intersection(words_title)
        
        score = len(intersection) / float(max(len(words_title), 1))
        if score > best_score:
            best_score = score
            best = title
            
    if best_score > 0.3:
         return best
         
    return "UNKNOWN"

def rename_files():
    files = [f for f in os.listdir(OUTPUT_DIR) if f.lower().endswith(('.jpg', '.png', '.webp'))]
    
    # We will rename files into a temporary list and then actually rename them to avoid overwriting issues
    project_counts = {}
    rename_plan = []
    
    for filename in files:
        if filename.startswith("scraped_img"): 
            continue # ignore dummy files
            
        # extract original index or generate one
        match = re.search(r'_(\d+)\.[a-zA-Z]+$', filename)
        orig_index = match.group(1) if match else "1"
        ext = filename.split('.')[-1].lower()
        
        best_title = get_best_match(filename)
        
        if best_title not in project_counts:
            project_counts[best_title] = 1
        else:
            project_counts[best_title] += 1
            
        new_filename = f"{best_title} - {project_counts[best_title]}.{ext}"
        # Make safe for Windows
        new_filename = re.sub(r'[\\/*?:"<>|]', '-', new_filename)
        
        old_path = os.path.join(OUTPUT_DIR, filename)
        new_path = os.path.join(OUTPUT_DIR, new_filename)
        
        rename_plan.append((old_path, new_path, filename, new_filename))

    for old, new, orig, new_nm in rename_plan:
        if old != new:
             print(f"Renaming: {orig[:30]}... -> {new_nm}")
             try:
                 shutil.move(old, new)
             except Exception as e:
                 print(f"Error renaming {old}: {e}")

if __name__ == "__main__":
    rename_files()
    print("\nDONE!")

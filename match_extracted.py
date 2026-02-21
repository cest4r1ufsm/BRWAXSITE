import os
from PIL import Image
import numpy as np

EXTRACTED_DIR = r"c:\Users\HP Victus 15\Downloads\BRWAX_site_v1_pudim\BRWAX_site_v1_pudim\site_creator\assets\extracted_pdf_images"
PROJECTS_DIR = r"c:\Users\HP Victus 15\Downloads\BRWAX_site_v1_pudim\BRWAX_site_v1_pudim\site_creator\assets\projects"

def get_hash(image_path, hash_size=8):
    try:
        with Image.open(image_path) as img:
            img = img.convert('L').resize((hash_size + 1, hash_size), Image.Resampling.LANCZOS)
            pixels = np.array(img.getdata(), dtype=float).reshape((hash_size, hash_size + 1))
            diff = pixels[:, 1:] > pixels[:, :-1]
            return diff
    except Exception as e:
        return None

def main():
    # 1. Gather all "named" images from the projects folder
    named_hashes = []
    for root, dirs, files in os.walk(PROJECTS_DIR):
        for file in files:
            if not file.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')): continue
            # Avoid overly generic names if possible, but let's assume all here are properly named
            if file.startswith("1") or len(file) < 5: 
                continue # Skip numbered dummy ones like "104.jpg" if any
            
            full_path = os.path.join(root, file)
            h = get_hash(full_path)
            if h is not None:
                named_hashes.append({'name': file, 'hash': h, 'path': full_path})
                
    print(f"Loaded {len(named_hashes)} properly named images from projects.")
    
    # 2. Compare and rename the files in extracted_pdf_images
    renamed_count = 0
    extracted_files = [f for f in os.listdir(EXTRACTED_DIR) if f.startswith("image_p") and f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
    print(f"Found {len(extracted_files)} files in extracted_pdf_images to process.")
    
    for ext_file in extracted_files:
        ext_path = os.path.join(EXTRACTED_DIR, ext_file)
        ext_hash = get_hash(ext_path)
        if ext_hash is None: continue
        
        best_match = None
        best_diff = float('inf')
        
        for named in named_hashes:
            diff = np.count_nonzero(ext_hash != named['hash'])
            if diff < best_diff:
                best_diff = diff
                best_match = named
                
        # If the difference is very small (e.g. max 5 bits out of 64), it's the same image
        if best_match and best_diff <= 5:
            # Found a match, let's rename it!
            name_base, name_ext = os.path.splitext(best_match['name'])
            ext_file_ext = os.path.splitext(ext_file)[1]
            
            # Formulate the new name. Might need to append an index if it already exists
            new_name = name_base + ext_file_ext
            new_path = os.path.join(EXTRACTED_DIR, new_name)
            
            idx = 1
            while os.path.exists(new_path) and new_name != ext_file:
                new_name = f"{name_base}_{idx}{ext_file_ext}"
                new_path = os.path.join(EXTRACTED_DIR, new_name)
                idx += 1
                
            if new_path != ext_path:
                os.rename(ext_path, new_path)
                print(f"MATCH: {ext_file} -> {new_name} (diff: {best_diff})")
                renamed_count += 1
                
    print(f"Total files renamed: {renamed_count}")

if __name__ == '__main__':
    main()

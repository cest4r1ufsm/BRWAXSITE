import os
import cv2
import numpy as np

EXTRACTED_DIR = r"c:\Users\HP Victus 15\Downloads\BRWAX_site_v1_pudim\BRWAX_site_v1_pudim\site_creator\assets\extracted_pdf_images"
PROJECTS_DIR = r"c:\Users\HP Victus 15\Downloads\BRWAX_site_v1_pudim\BRWAX_site_v1_pudim\site_creator\assets\projects"

def get_descriptors(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None: return None, None
    orb = cv2.ORB_create(nfeatures=1500)
    keypoints, descriptors = orb.detectAndCompute(img, None)
    return keypoints, descriptors

def main():
    named_data = []
    
    # Precompute descriptors for named images in projects
    print("Precomputing descriptors for target site images...")
    for root, dirs, files in os.walk(PROJECTS_DIR):
        for file in files:
            if not file.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')): continue
            if len(file) < 5 or file.startswith("1"): continue # Skip generic
            
            # Avoid processing re-named versions of the same file heavily, but for thoroughness we load them
            path = os.path.join(root, file)
            kp, desc = get_descriptors(path)
            if desc is not None and len(desc) > 10:
                named_data.append({'name': file, 'desc': desc, 'path': path})
                
    print(f"Loaded descriptors for {len(named_data)} named images.")
    
    # Process extracted images that still have the default naming
    extracted_files = [f for f in os.listdir(EXTRACTED_DIR) if f.startswith("image_p") and f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
    print(f"Found {len(extracted_files)} unmatched extracted images to process.")
    
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    renamed_count = 0
    
    for ext_file in extracted_files:
        ext_path = os.path.join(EXTRACTED_DIR, ext_file)
        kp, ext_desc = get_descriptors(ext_path)
        if ext_desc is None or len(ext_desc) < 10: continue
        
        best_match = None
        best_score = 0
        
        for named in named_data:
            matches = bf.match(ext_desc, named['desc'])
            # Good matches are those with distance < 50
            good_matches = [m for m in matches if m.distance < 50]
            if len(good_matches) > best_score:
                best_score = len(good_matches)
                best_match = named
                
        # If we have a significant number of good matches (e.g. > 15), consider it a match
        if best_match and best_score > 15:
            name_base, name_ext = os.path.splitext(best_match['name'])
            ext_file_ext = os.path.splitext(ext_file)[1]
            
            new_name = name_base + ext_file_ext
            new_path = os.path.join(EXTRACTED_DIR, new_name)
            
            idx = 1
            while os.path.exists(new_path) and new_name != ext_file:
                new_name = f"{name_base}_{idx}{ext_file_ext}"
                new_path = os.path.join(EXTRACTED_DIR, new_name)
                idx += 1
                
            if new_path != ext_path:
                os.rename(ext_path, new_path)
                print(f"MATCH: {ext_file} -> {new_name} (Matches: {best_score})")
                renamed_count += 1

    print(f"Total structured matches renamed: {renamed_count}")

if __name__ == '__main__':
    main()

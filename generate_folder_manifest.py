import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECTS_ROOT = os.path.join(BASE_DIR, "assets", "extracted_pdf_images")

manifest = []

for folder_name in sorted(os.listdir(PROJECTS_ROOT)):
    proj_path = os.path.join(PROJECTS_ROOT, folder_name)
    if not os.path.isdir(proj_path): continue
    
    # In extracted_pdf_images, images are directly in the project folder
    imgs = sorted([f for f in os.listdir(proj_path) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif'))])
        
    # Read description from the old projects folder if it exists, to preserve context
    desc = ""
    old_desc_path = os.path.join(BASE_DIR, "assets", "projects", folder_name, "descritivo.txt")
    if os.path.exists(old_desc_path):
        with open(old_desc_path, 'r', encoding='utf-8') as f:
            desc = f.read().strip()
            
    manifest.append({
        "folder": folder_name,
        "title": folder_name.replace("_", " ").upper(),
        "description": desc,
        "web_images": imgs,
        "mobile_images": imgs
    })

# Save manifest to root of assets so the JS app can read it
output_path = os.path.join(BASE_DIR, "assets", "projects_manifest.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=4, ensure_ascii=False)
    
print(f"Generated generic projects manifest with {len(manifest)} folders.")

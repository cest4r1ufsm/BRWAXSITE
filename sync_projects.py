import os
import json
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
PROJECTS_ROOT = os.path.join(ASSETS_DIR, "projects")

WEB_DEST = os.path.join(ASSETS_DIR, "grid_web")
MOBILE_DEST = os.path.join(ASSETS_DIR, "grid_mobile")

# Clear existing images in web and mobile destinations
for dest in [WEB_DEST, MOBILE_DEST]:
    if not os.path.exists(dest):
        os.makedirs(dest)
    for f in os.listdir(dest):
        if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif', '.mp4')):
            os.remove(os.path.join(dest, f))

manifest = []
all_web_images = []
all_mobile_images = []

for folder_name in os.listdir(PROJECTS_ROOT):
    proj_path = os.path.join(PROJECTS_ROOT, folder_name)
    if not os.path.isdir(proj_path): continue
    
    # Read description if exists
    desc = ""
    desc_path = os.path.join(proj_path, "descritivo.txt")
    if os.path.exists(desc_path):
        with open(desc_path, 'r', encoding='utf-8') as f:
            desc = f.read().strip()
            
    # Read title (from manifest or fallback to folder name)
    title = folder_name.replace("_", " ").upper()
    
    web_src = os.path.join(proj_path, "web")
    mobile_src = os.path.join(proj_path, "mobile")
    
    web_imgs = []
    mob_imgs = []
    
    # Copy web images
    if os.path.exists(web_src):
        for img in os.listdir(web_src):
            if img.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif', '.mp4')):
                shutil.copy2(os.path.join(web_src, img), os.path.join(WEB_DEST, img))
                web_imgs.append(img)
                all_web_images.append(img)
                
    # Copy mobile images
    if os.path.exists(mobile_src):
        for img in os.listdir(mobile_src):
            if img.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif', '.mp4')):
                shutil.copy2(os.path.join(mobile_src, img), os.path.join(MOBILE_DEST, img))
                mob_imgs.append(img)
                all_mobile_images.append(img)
                
    # If no specific mobile images, fallback to web
    if not mob_imgs and web_imgs:
        mob_imgs = web_imgs.copy()
        for img in web_imgs:
            shutil.copy2(os.path.join(WEB_DEST, img), os.path.join(MOBILE_DEST, img))
            all_mobile_images.append(img)
            
    # Add to manifest
    if web_imgs or mob_imgs:
        entry = {
            "id": folder_name,
            "title": title,
            "year": "2024",
            "services": "VISUAL CONTENT",
            "description": desc,
            "image_filenames": web_imgs
        }
        manifest.append(entry)

# Write project_metadata.json
with open(os.path.join(WEB_DEST, "project_metadata.json"), "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=4, ensure_ascii=False)

# Mobile needs the same manifest structure but we just list image_filenames (could be mobile specific or web fallback)
mobile_manifest = []
for item in manifest:
    # Need to match the mobile files. They are stored in projects/ folder so let's re-eval.
    mob_files = []
    folder_path = os.path.join(PROJECTS_ROOT, item["id"], "mobile")
    if os.path.exists(folder_path):
        mob_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
    if not mob_files:
        mob_files = item["image_filenames"]
    
    mob_entry = dict(item)
    mob_entry["image_filenames"] = mob_files
    mobile_manifest.append(mob_entry)

with open(os.path.join(MOBILE_DEST, "project_metadata.json"), "w", encoding="utf-8") as f:
    json.dump(mobile_manifest, f, indent=4, ensure_ascii=False)

# Write images.json for the site's random loading (though the site uses it less now)
all_web_images.sort()
all_mobile_images.sort()

with open(os.path.join(WEB_DEST, "images.json"), "w", encoding="utf-8") as f:
    json.dump(all_web_images, f, indent=4, ensure_ascii=False)
    
with open(os.path.join(MOBILE_DEST, "images.json"), "w", encoding="utf-8") as f:
    json.dump(all_mobile_images, f, indent=4, ensure_ascii=False)

print(f"Successfully synced {len(manifest)} projects.")
print(f"Web images: {len(all_web_images)}, Mobile images: {len(all_mobile_images)}")

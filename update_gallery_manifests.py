import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

def generate_manifest(folder_name):
    target_dir = os.path.join(ASSETS_DIR, folder_name)
    if not os.path.exists(target_dir):
        print(f"Directory {target_dir} does not exist.")
        return

    images = []
    # extensions to include
    exts = ('.jpg', '.jpeg', '.png', '.webp', '.gif', '.mp4')

    for filename in os.listdir(target_dir):
        if filename.lower().endswith(exts) and filename != "images.json" and not filename.endswith(".json"):
            images.append(filename)
    
    # Sort for consistency
    images.sort()

    output_path = os.path.join(target_dir, "images.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(images, f, indent=4, ensure_ascii=False)
    
    print(f"Generated {output_path} with {len(images)} images.")

if __name__ == "__main__":
    generate_manifest("grid_web")
    generate_manifest("grid_mobile")

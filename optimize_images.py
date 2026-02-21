from PIL import Image
import os
import sys

# Constants
MOBILE_MAX_WIDTH = 800
WEB_MAX_WIDTH = 1200
QUALITY = 80

def optimize_folder(folder_path, max_width):
    print(f"Optimizing folder: {folder_path} with max_width={max_width}...")
    
    if not os.path.exists(folder_path):
        print(f"Folder not found: {folder_path}")
        return

    files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    count = 0
    saved_bytes = 0

    for filename in files:
        filepath = os.path.join(folder_path, filename)
        try:
            with Image.open(filepath) as img:
                original_size = os.path.getsize(filepath)
                width, height = img.size
                
                # Check if resize is needed
                if width > max_width:
                    ratio = max_width / width
                    new_height = int(height * ratio)
                    img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
                    # print(f"Resized {filename}: {width}x{height} -> {max_width}x{new_height}")

                # Save with optimization
                # Convert to RGB if RGBA and saving as JPEG (though we keep extension mostly)
                # If PNG, we can use optimize=True.
                
                if filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg'):
                     if img.mode != 'RGB':
                         img = img.convert('RGB')
                     img.save(filepath, 'JPEG', quality=QUALITY, optimize=True)
                elif filename.lower().endswith('.png'):
                     img.save(filepath, 'PNG', optimize=True)

                new_size = os.path.getsize(filepath)
                saved = original_size - new_size
                if saved > 0:
                    saved_bytes += saved
                    # print(f"Optimized {filename}: {original_size//1024}KB -> {new_size//1024}KB")
                count += 1
        except Exception as e:
            print(f"Error processing {filename}: {e}")

    print(f"Finished {folder_path}. Processed {count} images. Saved {saved_bytes / 1024 / 1024:.2f} MB.")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 1. Optimize Mobile Grid
    mobile_dir = os.path.join(base_dir, 'assets', 'grid_mobile')
    optimize_folder(mobile_dir, MOBILE_MAX_WIDTH)

    # 2. Optimize Web Grid (optional but good practice)
    web_dir = os.path.join(base_dir, 'assets', 'grid_web')
    optimize_folder(web_dir, WEB_MAX_WIDTH)

import fitz  # PyMuPDF
import sys
import os

pdf_path = sys.argv[1]
output_dir = sys.argv[2]

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

doc = fitz.open(pdf_path)
total_images = 0

print(f"Processing {pdf_path}...")

for page_index in range(len(doc)):
    page = doc[page_index]
    image_list = page.get_images()

    for image_index, img in enumerate(image_list, start=1):
        xref = img[0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        image_ext = base_image["ext"]
        
        # Construct filename
        filename = f"image_p{page_index+1}_{image_index}.{image_ext}"
        filepath = os.path.join(output_dir, filename)

        with open(filepath, "wb") as f:
            f.write(image_bytes)
        
        print(f"Saved {filename}")
        total_images += 1

print(f"Extraction complete. {total_images} images saved to {output_dir}")

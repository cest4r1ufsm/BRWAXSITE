import json
import re
import urllib.request
import os

html_file = 'canva_dump.html'
output_dir = r"c:\Users\HP Victus 15\Downloads\BRWAX_site_v1_pudim\BRWAX_site_v1_pudim\site_creator\assets\extracted_pdf_images"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Extract the JSON block
match = re.search(r"window\['bootstrap'\] = JSON\.parse\('(.*?)'\);", content)
if not match:
    # try single quotes or double quotes
    match = re.search(r'window\[\'bootstrap\'\] = JSON\.parse\(\'(.*?)\'\);', content)

urls_to_download = set()
# Let's also just extract all image urls from the raw text, it might be simpler
media_matches = re.finditer(r'(_assets/media/[a-zA-Z0-9_]+\.(jpg|jpeg|png|webp))', content)

for m in media_matches:
    url = f"https://brwax.my.canva.site/{m.group(1)}"
    urls_to_download.add(url)

print(f"Found {len(urls_to_download)} unique media URLs.")

if len(urls_to_download) == 0:
    # try full urls
    media_matches = re.finditer(r'(https://[^\"\']+\.(?:jpg|jpeg|png|webp))', content)
    for m in media_matches:
        if 'media' in m.group(1):
            urls_to_download.add(m.group(1))

print(f"Found {len(urls_to_download)} total media URLs.")

import requests
count = 1
for url in urls_to_download:
    filename = url.split('/')[-1]
    # We will name them scraped_canva_1, scraped_canva_2 etc. because getting the exact name from the JSON graph is very difficult 
    # and the user already matched the images to the projects before.
    # Actually wait. If we can get names, we should. Let's look for texts.
    print(f"Downloading {url}")
    try:
        resp = requests.get(url)
        if resp.status_code == 200:
            with open(os.path.join(output_dir, f"site_img_{count}_{filename}"), 'wb') as img_f:
                img_f.write(resp.content)
            count += 1
    except Exception as e:
        print(e)

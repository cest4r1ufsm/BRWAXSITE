import os
import json
import shutil
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
PROJECTS_ROOT = os.path.join(ASSETS_DIR, "projects")

# Pastas de origem
WEB_SRC = os.path.join(ASSETS_DIR, "grid_web")
MOBILE_SRC = os.path.join(ASSETS_DIR, "grid_mobile")
NEW_SRC = os.path.join(ASSETS_DIR, "grid_imagens_novas")

# Carrega metadata existente para usar como base de IDs e Títulos
metadata_path = os.path.join(WEB_SRC, "project_metadata.json")
with open(metadata_path, "r", encoding="utf-8") as f:
    existing_metadata = json.load(f)

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '_', text).strip('_')
    return text

def get_base_name(filename):
    # Remove extensões e sufixos de numeração/data para agrupar
    name = os.path.splitext(filename)[0]
    name = re.sub(r'(_+| +| -+)\d*$', '', name) # Remove _1, _2024, etc no final
    name = re.sub(r'(_+| +| -+)\d{4}.*$', '', name) # Remove anos
    return name.strip()

# 1. Mapear arquivos para projetos
project_map = {} # slug -> {title, web: [], mobile: []}

# Primeiro, popula com o que já está no metadata oficial
for p in existing_metadata:
    slug = slugify(p['title'])
    if slug not in project_map:
        project_map[slug] = {
            "title": p['title'],
            "description": p.get('description', ''),
            "services": p.get('services', ''),
            "year": p.get('year', ''),
            "web": [],
            "mobile": []
        }
    # Adiciona os arquivos citados no metadata
    for f in p['image_filenames']:
        project_map[slug]['web'].append(f)

# 2. Scannear pastas físicas para encontrar variantes (como Anitta 2025, Anitta Global)
all_srcs = [WEB_SRC, MOBILE_SRC, NEW_SRC]
for src_dir in all_srcs:
    if not os.path.exists(src_dir): continue
    is_mobile = "mobile" in src_dir
    for f in os.listdir(src_dir):
        if not f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif', '.mp4')): continue
        
        # Tenta encontrar um projeto que contenha o nome base deste arquivo
        base = get_base_name(f).lower()
        matched = False
        for slug, data in project_map.items():
            if base in data['title'].lower() or data['title'].lower() in base:
                if is_mobile: data['mobile'].append(f)
                else: data['web'].append(f)
                matched = True
                break
        
        # Se não deu match, cria um projeto novo baseado no nome do arquivo
        if not matched:
            new_title = get_base_name(f).upper()
            slug = slugify(new_title)
            if slug not in project_map:
                project_map[slug] = {"title": new_title, "web": [], "mobile": [], "description": "", "services": "VISUAL CONTENT", "year": "2024"}
            if is_mobile: project_map[slug]['mobile'].append(f)
            else: project_map[slug]['web'].append(f)

# 3. Executar a migração física
if not os.path.exists(PROJECTS_ROOT): os.makedirs(PROJECTS_ROOT)

final_manifest = []

for slug, data in project_map.items():
    proj_path = os.path.join(PROJECTS_ROOT, slug)
    web_dest = os.path.join(proj_path, "web")
    mob_dest = os.path.join(proj_path, "mobile")
    
    os.makedirs(web_dest, exist_ok=True)
    os.makedirs(mob_dest, exist_ok=True)
    
    # Limpa duplicatas mantendo ordem
    data['web'] = list(dict.fromkeys(data['web']))
    data['mobile'] = list(dict.fromkeys(data['mobile']))

    # Move/Copia arquivos
    def move_files(files, dest, is_mobile):
        moved = []
        for f in files:
            src_paths = [
                os.path.join(MOBILE_SRC if is_mobile else WEB_SRC, f),
                os.path.join(NEW_SRC, f),
                os.path.join(WEB_SRC if is_mobile else MOBILE_SRC, f) # Fallback cruzado
            ]
            for s in src_paths:
                if os.path.exists(s):
                    shutil.copy2(s, os.path.join(dest, f))
                    moved.append(f)
                    break
        return moved

    actual_web = move_files(data['web'], web_dest, False)
    actual_mob = move_files(data['mobile'], mob_dest, True)
    
    if actual_web:
        entry = {
            "id": slug,
            "title": data['title'],
            "year": data['year'],
            "services": data['services'],
            "description": data['description'],
            "cover": actual_web[0], # Primeira imagem é a capa no grid
            "images": actual_web,
            "mobile_images": actual_mob if actual_mob else actual_web
        }
        final_manifest.append(entry)

# Salva manifesto central
with open(os.path.join(ASSETS_DIR, "works_manifest.json"), "w", encoding="utf-8") as f:
    json.dump(final_manifest, f, indent=4, ensure_ascii=False)

print(f"Organização completa! {len(final_manifest)} projetos criados em assets/projects/")

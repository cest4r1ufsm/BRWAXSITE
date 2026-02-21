import json
import os

BASE_DIR = r"c:\Users\HP Victus 15\Downloads\BRWAX_site_v1_pudim\BRWAX_site_v1_pudim\site_creator\assets"

# Read the texts we just generated
project_texts = {
    "anitta_global_citizen": "Desenvolvimento do conteúdo visual do show da Anitta na COP30, criando uma experiência audiovisual alinhada à força da performance e à relevância do evento. Os visuais foram pensados para integrar narrativa, ritmo e identidade artística, atuando como parte ativa do espetáculo e potencializando o impacto da apresentação em um contexto global.",
    "disney_alien_earth": "Para o lançamento de Alien: Earth, nova série do FX no Disney+, desenvolvemos uma ativação imersiva que trouxe o universo da franquia para o mundo real. A ação simulou a queda da nave em solo brasileiro, criando uma experiência visual impactante em São Paulo e Rio de Janeiro. O objetivo foi transformar o lançamento da série em um evento urbano, despertando curiosidade, conversa e engajamento, como se a invasão tivesse acabado de acontecer.",
    "turne_caetano_2024": "TURNÊ CAETANO VELOSO E MARIA BETHÂNIA 2024",
    "cabelinho_rock_in_rio": "No Rock in Rio Lisboa 2024, tivemos o prazer de produzir os conteúdos visuais para o show do Cabelinho, sob a direção de Drica Lara. Utilizamos uma combinação de filmagem, motion design e 3D nas animações para compor o setlist dessa apresentação única. A fusão desses elementos trouxe uma experiência visual inesquecível ao palco.",
    "ludmilla_coachella": "No Festival Coachella, realizado na Califórnia, tivemos o prazer de produzir os conteúdos visuais para o show da Ludmilla, sob a direção talentosa de Nidia Aranha e Drica Lara. A fusão desses elementos trouxe uma experiência visual inesquecível ao palco.",
    "ambev_25_anos": "Celebramos os 25 anos da Ambev com um evento especial. Criamos animações com uma estética de colagem que trouxe à vida a história da Ambev, desde seu nascimento, passando pela fusão, até os dias atuais. Esse conceito visual foi amplamente elogiado."
}

def update_metadata(folder_name):
    json_path = os.path.join(BASE_DIR, folder_name, "project_metadata.json")
    if not os.path.exists(json_path):
        return
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    updated = 0
    for item in data:
        if item['id'] in project_texts:
            item['description'] = project_texts[item['id']]
            updated += 1
            
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    print(f"Updated {updated} records in {folder_name}/project_metadata.json")

update_metadata("grid_web")
update_metadata("grid_mobile")

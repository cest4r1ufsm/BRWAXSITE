import os

BASE_DIR = r"c:\Users\HP Victus 15\Downloads\BRWAX_site_v1_pudim\BRWAX_site_v1_pudim\site_creator\assets\projects"

project_data = {
    "anitta_global_citizen": {
        "text": "Desenvolvimento do conteúdo visual do show da Anitta na COP30, criando uma experiência audiovisual alinhada à força da performance e à relevância do evento. Os visuais foram pensados para integrar narrativa, ritmo e identidade artística, atuando como parte ativa do espetáculo e potencializando o impacto da apresentação em um contexto global.",
        "site_name": "Anitta_Global_Citizen_Festival"
    },
    "anita_golbal_citizen": {
        "text": "Desenvolvimento do conteúdo visual do show da Anitta na COP30, criando uma experiência audiovisual alinhada à força da performance e à relevância do evento. Os visuais foram pensados para integrar narrativa, ritmo e identidade artística, atuando como parte ativa do espetáculo e potencializando o impacto da apresentação em um contexto global.",
        "site_name": "Anitta_Global_Citizen_Festival"
    },
    "disney_alien_earth": {
        "text": "Para o lançamento de Alien: Earth, nova série do FX no Disney+, desenvolvemos uma ativação imersiva que trouxe o universo da franquia para o mundo real. A ação simulou a queda da nave em solo brasileiro, criando uma experiência visual impactante em São Paulo e Rio de Janeiro. O objetivo foi transform o lançamento da série em um evento urbano, despertando curiosidade, conversa e engajamento, como se a invasão tivesse acabado de acontecer.",
        "site_name": "Disney_Alien_Earth"
    },
    "turn_caetano_e_bethania": {
        "text": "TURNÊ CAETANO VELOSO E MARIA BETHÂNIA 2024",
        "site_name": "Caetano_E_Bethania"
    },
    "turn_caetano_e_bet_nia": {
        "text": "TURNÊ CAETANO VELOSO E MARIA BETHÂNIA 2024",
        "site_name": "Caetano_E_Bethania"
    },
    "turn_caetano_veloso_e_maria_beth_nia": {
        "text": "TURNÊ CAETANO VELOSO E MARIA BETHÂNIA 2024",
        "site_name": "Caetano_E_Bethania"
    },
    "show_cabelinho_rock_in_rio_lisboa": {
        "text": "No Rock in Rio Lisboa 2024, tivemos o prazer de produzir os conteúdos visuais para o show do Cabelinho, sob a direção de Drica Lara. Utilizamos uma combinação de filmagem, motion design e 3D nas animações para compor o setlist dessa apresentação única. A fusão desses elementos trouxe uma experiência visual inesquecível ao palco.",
        "site_name": "Show_Cabelinho_RIR_Lisboa"
    },
    "mc_cabelinho": {
        "text": "No Rock in Rio Lisboa 2024, tivemos o prazer de produzir os conteúdos visuais para o show do Cabelinho, sob a direção de Drica Lara. Utilizamos uma combinação de filmagem, motion design e 3D nas animações para compor o setlist dessa apresentação única. A fusão desses elementos trouxe uma experiência visual inesquecível ao palco.",
        "site_name": "Show_Cabelinho_RIR_Lisboa"
    },
    "ludmilla_coachella": {
        "text": "No Festival Coachella, realizado na Califórnia, tivemos o prazer de produzir os conteúdos visuais para o show da Ludmilla, sob a direção talentosa de Nidia Aranha e Drica Lara. A fusão desses elementos trouxe uma experiência visual inesquecível ao palco.",
        "site_name": "Ludmilla_Show_Coachella"
    },
    "ludmilla_show_coachella": {
        "text": "No Festival Coachella, realizado na Califórnia, tivemos o prazer de produzir os conteúdos visuais para o show da Ludmilla, sob a direção talentosa de Nidia Aranha e Drica Lara. A fusão desses elementos trouxe uma experiência visual inesquecível ao palco.",
        "site_name": "Ludmilla_Show_Coachella"
    },
    "ambev_25_anos": {
        "text": "Celebramos os 25 anos da Ambev com um evento especial. Criamos animações com uma estética de colagem que trouxe à vida a história da Ambev, desde seu nascimento, passando pela fusão, até os dias atuais. Esse conceito visual foi amplamente elogiado.",
        "site_name": "Ambev_25_Anos"
    },
    "ambev_25_anos_extra": {
        "text": "Celebramos os 25 anos da Ambev com um evento especial. Criamos animações com uma estética de colagem que trouxe à vida a história da Ambev, desde seu nascimento, passando pela fusão, até os dias atuais. Esse conceito visual foi amplamente elogiado.",
        "site_name": "Ambev_25_Anos"
    }
}

count_renamed = 0
for folder in os.listdir(BASE_DIR):
    folder_path = os.path.join(BASE_DIR, folder)
    if not os.path.isdir(folder_path): continue
    
    if folder in project_data:
        data = project_data[folder]
        
        # Create text file
        txt_path = os.path.join(folder_path, "descritivo.txt")
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(data["text"])
            
        print(f"Created/updated descritivo.txt for: {folder}")
        
        # Rename images in web and mobile folders
        for sub in ["web", "mobile"]:
            sub_path = os.path.join(folder_path, sub)
            if not os.path.exists(sub_path): continue
            
            # First pass: identify files to rename
            files_to_rename = []
            for img_file in os.listdir(sub_path):
                if not img_file.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif')): continue
                if img_file.startswith(data["site_name"]): continue # already standardized somewhat
                files_to_rename.append(img_file)
                
            idx = 1
            for img_file in files_to_rename:
                ext = os.path.splitext(img_file)[1]
                new_name = f'{data["site_name"]}_{idx}{ext}'
                new_path = os.path.join(sub_path, new_name)
                
                # Check if target exists
                while os.path.exists(new_path):
                    idx += 1
                    new_name = f'{data["site_name"]}_{idx}{ext}'
                    new_path = os.path.join(sub_path, new_name)
                    
                os.rename(os.path.join(sub_path, img_file), new_path)
                print(f"[{sub}] Renamed {img_file} -> {new_name}")
                idx += 1
                count_renamed += 1

print(f"Successfully processed project folders. Renamed {count_renamed} files.")

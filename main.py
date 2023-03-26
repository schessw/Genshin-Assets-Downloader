import json
import requests
import os.path

url = "https://enka.network/ui/{}.png"

# Parse JSON contents
artifact_obj_list = json.loads(requests.get("https://gitlab.com/Dimbreath/AnimeGameData/-/raw/master/ExcelBinOutput/ReliquaryExcelConfigData.json").text)
character_obj_list = json.loads(requests.get("https://gitlab.com/Dimbreath/AnimeGameData/-/raw/master/ExcelBinOutput/AvatarExcelConfigData.json").text)
text_map_CN_obj = json.loads(requests.get("https://gitlab.com/Dimbreath/AnimeGameData/-/raw/master/TextMap/TextMapCHS.json").text)
text_map_EN_obj = json.loads(requests.get("https://gitlab.com/Dimbreath/AnimeGameData/-/raw/master/TextMap/TextMapEN.json").text)

# Configurations (specify your own path here)
artifact_local_folder_path = "C:/Users/shenw/Pictures/Genshin Impact/Artifacts/{0} ({1}).png"
character_local_folder_path = "C:/Users/shenw/Pictures/Genshin Impact/Characters/{0} ({1}).png"

def download_artifact_files():
    # Initialize artifact list
    artifact_list = []

    # Create own artifact list with property: file_name, cn_name, en_name
    for artifact in artifact_obj_list:
        try: 
            artifact_list.append({
                "file_name": artifact['icon'], 
                "cn_name": text_map_CN_obj[str(artifact['nameTextMapHash'])],
                "en_name": text_map_EN_obj[str(artifact['nameTextMapHash'])]
            })
        except Exception:
            # print('Not Found: ' + str(artifact['nameTextMapHash']))
            pass

    # Create unique artifact list
    artifact_list = [dict(s) for s in set(frozenset(artifact.items()) for artifact in artifact_list)]

    for artifact in artifact_list:
        asset_path = url.format(artifact['file_name'])
        file_name = artifact_local_folder_path.format(artifact['en_name'], artifact['cn_name'])
        
        if not os.path.isfile(file_name):
            response = requests.get(asset_path)
            if response.status_code == 200:
                with open(file_name, 'wb') as f:
                    f.write(response.content)
                print('File downloaded successfully: [{}] {} ({}).png'.format(artifact['file_name'], artifact['en_name'], artifact['cn_name']))
            else:
                print('File downloaded failed: [{}] {} ({}).png'.format(artifact['file_name'], artifact['en_name'], artifact['cn_name']))

def download_character_files():
    # Initialize artifact list
    character_list = []

    # Create own artifact list with property: file_name, cn_name, en_name
    for character in character_obj_list:
        try: 
            character_list.append({
                "file_name": character['iconName'], 
                "cn_name": text_map_CN_obj[str(character['nameTextMapHash'])],
                "en_name": text_map_EN_obj[str(character['nameTextMapHash'])]
            })
        except Exception:
            # print('Not Found: ' + str(artifact['nameTextMapHash']))
            pass
    
    # Create unique character list
    character_list = [dict(s) for s in set(frozenset(character.items()) for character in character_list)]

    for character in character_list:
        asset_path = url.format(character['file_name'])
        file_name = character_local_folder_path.format(character['en_name'], character['cn_name'])
        
        if not os.path.isfile(file_name):
            response = requests.get(asset_path)
            if response.status_code == 200:
                with open(file_name, 'wb') as f:
                    f.write(response.content)
                print('File downloaded successfully: [{}] {} ({}).png'.format(character['file_name'], character['en_name'], character['cn_name']))
            else:
                print('File downloaded failed: [{}] {} ({}).png'.format(character['file_name'], character['en_name'], character['cn_name']))

download_artifact_files()
download_character_files()
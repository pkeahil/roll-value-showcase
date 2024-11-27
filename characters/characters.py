
import requests

from localization.localization import localization


def get_character_info():
    github_url = "https://raw.githubusercontent.com"
    enka_repo = "EnkaNetwork/API-docs/refs/heads/master"
    character_endpoint = "store/characters.json"

    url = f"{github_url}/{enka_repo}/{character_endpoint}"
    response = requests.get(url)
    return response.json()


character_info = get_character_info()


def get_character_name(avatarInfo: dict):
    avatar_id = str(avatarInfo["avatarId"])
    character_name_hash = character_info[avatar_id]["NameTextMapHash"]
    character_name = localization["en"][str(character_name_hash)]
    return character_name


def get_artifact_list(avatarInfo: dict) -> list:
    artifact_list = avatarInfo["equipList"]
    artifact_list = ([
        artifact for artifact in artifact_list if "reliquary" in artifact
    ])
    return artifact_list

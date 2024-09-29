
import json

from localization.localization import localization

character_info = json.loads(open("characters/characters.json").read())


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

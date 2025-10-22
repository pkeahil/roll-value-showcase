import json
from collections import defaultdict

import characters.characters as characters
import profiles.profiles as profiles


def get_character_showcase(uid: str):
    if not uid:
        return
    userInfo = profiles.get_user_info(uid)
    profiles.print_player_info(userInfo["playerInfo"])

    avatarInfoList = userInfo["avatarInfoList"]

    result = defaultdict(dict)
    for avatarInfo in avatarInfoList:
        character_name = characters.get_character_name(avatarInfo)
        result[character_name]["avatarInfo"] = avatarInfo
        result[character_name]["id"] = str(avatarInfo["avatarId"])
        result[character_name]["player_uid"] = str(uid)

        avatar = [
            avatar for avatar in userInfo["playerInfo"]["showAvatarInfoList"]
            if avatar["avatarId"] == avatarInfo["avatarId"]
        ][0]
        energy_type = avatar["energyType"]
        result[character_name]["energy_type"] = str(energy_type)

    return dict(result)

from collections import defaultdict

import artifacts.artifacts as artifacts
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
        artifact_list = characters.get_artifact_list(avatarInfo)
        total_cv = 0.0
        total_rv = 0
        for artifact in artifact_list:
            artifact_type = artifacts.artifact_type_map[
                artifact["flat"]["equipType"]
            ]
            cv = artifacts.calculate_artifact_cv(artifact)
            rv = artifacts.calculate_artifact_rv(artifact, character_name)
            total_cv += cv
            total_rv += rv
            result[character_name][artifact_type] = {"CV": cv}
            result[character_name][artifact_type].update({"RV": rv})
        result[character_name]["Total"] = {"CV": total_cv}
        result[character_name]["Total"].update({"RV": total_rv})

    return dict(result)

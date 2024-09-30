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
    character_cvs = {}
    character_rvs = {}
    for avatarInfo in avatarInfoList:
        character_name = characters.get_character_name(avatarInfo)
        artifact_list = characters.get_artifact_list(avatarInfo)
        total_cv = 0.0
        total_rv = 0
        for artifact in artifact_list:
            total_cv += artifacts.calculate_artifact_cv(artifact)
            total_rv += artifacts.calculate_artifact_rv(
                artifact, character_name
            )
        character_cvs[character_name] = total_cv
        character_rvs[character_name] = total_rv

    character_cvs = character_cvs.items()
    sorted_cvs = sorted(character_cvs, key=lambda item: item[1], reverse=True)

    result = defaultdict(dict)
    for character, cv in sorted_cvs:
        result[character]["CV"] = cv
        result[character]["RV"] = character_rvs[character]

    print(dict(result))
    return dict(result)

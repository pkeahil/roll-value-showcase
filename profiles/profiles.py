import json

import requests

from redis_client import redis_client

enka_api = "https://enka.network/api"


# get user info
def get_user_info(uid: str) -> dict:
    user_key = f"{uid}_user_info"

    if redis_client.exists(user_key):
        return json.loads(redis_client.get(user_key))
    else:
        response = requests.get(f"{enka_api}/uid/{uid}")
        user = response.json()
        redis_client.set(
            user_key,
            json.dumps(user),
            ex=user["ttl"]
        )
        if not redis_client.exists(f"{uid}_player_info"):
            redis_client.set(
                f"{uid}_player_info",
                json.dumps(user["playerInfo"]),
                ex=user["ttl"]
            )
        return user


# get player info
def get_player_info(uid: str) -> dict:
    user_key = f"{uid}_player_info"
    if redis_client.exists(user_key):
        return json.loads(redis_client.get(user_key))

    else:
        response = requests.get(f"{enka_api}/uid/{uid}/?info")
        user = response.json()
        redis_client.set(
            user_key,
            json.dumps(user["playerInfo"]),
            ex=user["ttl"]
        )
        return user["playerInfo"]

# get avatar info list


# print user info
def print_player_info(userInfo: dict) -> None:
    print(f"Nickname: {userInfo['nickname']}")
    print(f"AR level: {userInfo['level']}")
    print(f"World level: {userInfo['worldLevel']}")
    print(f"Number of achievements: {userInfo['finishAchievementNum']}")
    print(
        "Abyss level reached: "
        f"{userInfo['towerFloorIndex']}-{userInfo['towerLevelIndex']}"
    )

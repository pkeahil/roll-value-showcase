
import requests


def get_localization():
    github_url = "https://raw.githubusercontent.com"
    enka_repo = "EnkaNetwork/API-docs/refs/heads/master"
    localization_endpoint = "store/gi/locs.json"

    url = f"{github_url}/{enka_repo}/{localization_endpoint}"
    response = requests.get(url)
    return response.json()


localization = get_localization()

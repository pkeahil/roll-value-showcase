import re
import sys

import requests
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright, character: str) -> None:
    browser = playwright.firefox.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://genshin-impact.fandom.com/wiki/Wish/Gallery", wait_until="domcontentloaded")

    character_with_underscores = re.sub(r' ', '_', character)
    page.locator(f"#{character_with_underscores}_Wish-png").get_by_role("link", name=f"{character} view image").click()

    element =  page.get_by_role("img", name=f"{character_with_underscores}_Wish")  # needs underscore if multiple words
    src_url = element.get_attribute("src")
    response = requests.get(src_url)

    with open(f"./images/splash_arts/{character}.png", "wb") as f:
        f.write(response.content)

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    character = sys.argv[1]
    run(playwright, character)

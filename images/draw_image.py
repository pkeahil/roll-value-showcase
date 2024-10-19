# ok so artifacts section

# 50, 250, 450, 650, 850 y
# 1200 x
from io import BytesIO

import requests
from PIL import Image, ImageDraw, ImageFont

from artifacts import artifacts

enka_api = "https://enka.network/"


def draw_artifact_icon(im: Image, icon: str, x: int, y: int):
    response = requests.get(f"{enka_api}/ui/{icon}.png")
    artifact_icon = Image.open(BytesIO(response.content)).resize((100, 100))
    im.paste(artifact_icon, (x + 25, y), artifact_icon)


def draw_artifact_box(draw: ImageDraw, x: int, y: int, bg_color: str):
    draw.rounded_rectangle(
        (x, y, x + 600, y + 150),
        fill=bg_color,
        width=10,
        radius=20
    )
    draw.rounded_rectangle(
        (x + 5, y + 5, x + 595, y + 145),
        fill="black",
        width=10,
        radius=20
    )


def draw_artifact_substats(
        im: Image,
        draw: ImageDraw,
        font: ImageFont,
        artifact: dict,
        x_start: int,
        y_start: int):
    x = x_start
    y = y_start
    i = 0

    # Main stat:
    main_stat = artifact["reliquaryMainstat"]
    main_stat_image = Image.open(
        f"images/stat_icons/{main_stat['mainPropId']}.png"
    )
    main_stat_value = main_stat["statValue"]
    main_stat_is_pct = (
        main_stat["mainPropId"] in include_percentage_substats
        or main_stat["mainPropId"].endswith("_PERCENT")
        or main_stat["mainPropId"].endswith("_ADD_HURT")
    )
    im.paste(main_stat_image, (x - 175, y + 75), main_stat_image)
    draw.text(
        (x - 140, y + 75),
        (f"{main_stat_value}{'%' if main_stat_is_pct else ''}"),
        fill="white",
        font=font
    )

    # Substats:
    for substat in artifact["reliquarySubstats"]:
        substat_icon = substat["appendPropId"]
        is_percentage = (
            substat_icon in include_percentage_substats
            or substat_icon.endswith("_PERCENT")
            or substat_icon.endswith("_ADD_HURT")
        )
        substat_value = substat["statValue"]
        substat_image = Image.open(f"images/stat_icons/{substat_icon}.png")
        im.paste(substat_image, (x - 35, y - 3), substat_image)
        draw.text(
            (x, y),
            (f"{substat_value}{'%' if is_percentage else ''}"),
            fill="white",
            font=font
        )
        x = x_start + (((i + 1) % 2) * 200)
        y = y_start + (((i + 1) // 2) * 55)
        i += 1


def draw_splash_art(im: Image, character: str) -> Image:
    splash_art = Image.open(f"images/splash_arts/{character}.png")
    splash_art = splash_art.crop(
        (150, 0, splash_art.width - 150, splash_art.height)
    )
    new_width = int(splash_art.width * 1.5)
    new_height = new_width * splash_art.height // splash_art.width

    splash_art = splash_art.resize((new_width, new_height))
    im.paste(splash_art, (0, 0), splash_art)


def draw_roll_value(
        im: Image,
        font: ImageFont,
        roll_value: int,
        roll_value_color: str,
        x: int,
        y: int):

    # we want to draw the roll value vertically instead of horizontally
    temp_blank_image = Image.new("RGB", (200, 200), "black")
    temp_font = font
    temp_draw = ImageDraw.Draw(temp_blank_image)
    temp_draw.text(
        (0, 0),
        f"{roll_value}%RV",
        fill=roll_value_color,
        font=temp_font
    )
    temp_blank_image = temp_blank_image.crop((0, 0, 125, 50))
    temp_blank_image = temp_blank_image.rotate(270, expand=True)

    im.paste(temp_blank_image, (x + 525, y + 15))

    # draw.text(
    #     (x, y),
    #     f"{roll_value}%RV",
    #     fill=roll_value_color,
    #     font=font
    # )


include_percentage_substats = [
    "FIGHT_PROP_CRITICAL",
    "FIGHT_PROP_CRITICAL_HURT",
    "FIGHT_PROP_CHARGE_EFFICIENCY",
]


def draw_character_showcase(character: str, artifacts_list: list) -> Image:

    # Create base image, initialize font
    im = Image.new("RGB", (1920, 1080), "black")
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype("fonts/JA-JP.TTF", 24)

    # Draw character splash art
    draw_splash_art(im, character)

    # Draw artifacts
    x_box = 1200
    y_box = 50
    for artifact in artifacts_list:
        flat = artifact["flat"]
        if flat["itemType"] == "ITEM_RELIQUARY":
            roll_value, roll_value_color = (
                artifacts.calculate_artifact_rv(artifact, character)
            )

            draw_artifact_box(draw, x_box, y_box, roll_value_color)
            draw_artifact_icon(im, flat["icon"], x_box, y_box)
            draw_artifact_substats(
                im, draw, font, flat, x_box + 200, y_box + 25
            )
            draw_roll_value(
                im,
                font,
                roll_value,
                roll_value_color,
                x_box,
                y_box
            )

            y_box += 200

    return im

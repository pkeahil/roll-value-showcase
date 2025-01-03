# ok so artifacts section

# 50, 250, 450, 650, 850 y
# 1200 x
import json
from io import BytesIO

import requests
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageChops

from artifacts import artifacts
from characters import characters
from localization.localization import localization

enka_api = "https://enka.network/"


def draw_artifact_icon(im: Image, icon: str, x: int, y: int):
    response = requests.get(f"{enka_api}/ui/{icon}.png")
    artifact_icon = Image.open(BytesIO(response.content)).resize((100, 100))
    im.paste(artifact_icon, (x + 25, y), artifact_icon)


def draw_artifact_box(draw: ImageDraw, x: int, y: int, bg_color: str):
    draw.rounded_rectangle(
        (x, y, x + 280, y + 200),
        fill=bg_color,
        width=10,
        radius=20
    )
    draw.rounded_rectangle(
        (x + 5, y + 5, x + 275, y + 195),
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
    im.paste(main_stat_image, (x - 160, y + 75), main_stat_image)
    draw.text(
        (x - 125, y + 75),
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
        im.paste(substat_image, (x - 35, y - 8), substat_image)
        draw.text(
            (x, y - 5),
            (f"{substat_value}{'%' if is_percentage else ''}"),
            fill="white",
            font=font
        )
        y = y + 45
        i += 1


def draw_splash_art(im: Image, character: str) -> Image:
    splash_art = Image.open(f"images/splash_arts/{character}.png")
    middle_x = splash_art.width // 2
    middle_y = splash_art.height // 2
    splash_art = splash_art.crop(
        (middle_x - 200, middle_y - 200, middle_x + 200, middle_y + 200)
    )

    new_width = 1000
    new_height = new_width * splash_art.height // splash_art.width

    splash_art = splash_art.resize((new_width, new_height))
    splash_art.thumbnail((750, 750))

    mask = Image.open("images/ui/splash_art_mask.png").convert("L")
    mask = mask.resize((splash_art.size[0], splash_art.size[1]), Image.NEAREST)
    # mask = mask.rotate(180)

    alpha = splash_art.split()[-1]

    new_alpha = ImageOps.invert(mask)
    alpha = ImageChops.multiply(alpha, new_alpha)

    result = splash_art.copy()
    result.putalpha(alpha)

    im.paste(result, (50, 50), result)


def draw_character_stats(
        im: Image,
        draw: ImageDraw,
        font: ImageFont,
        total_stats: dict,
        x: int,  # start at 5
        y: int):  # start at 825
    draw.rounded_rectangle(
        (x, y, x + 550, y + 380),
        fill="black",
        outline="white",
        width=3,
        radius=10
    )
    im.paste(
        Image.open("images/stat_icons/FIGHT_PROP_HP.png"),
        (x + 10, y + 25),
        Image.open("images/stat_icons/FIGHT_PROP_HP.png")
    )
    # paste image of atk on image
    im.paste(
        Image.open("images/stat_icons/FIGHT_PROP_ATTACK.png"),
        (x + 10, y + 75),
        Image.open("images/stat_icons/FIGHT_PROP_ATTACK.png")
    )
    im.paste(
        Image.open("images/stat_icons/FIGHT_PROP_DEFENSE.png"),
        (x + 10, y + 125),
        Image.open("images/stat_icons/FIGHT_PROP_DEFENSE.png")
    )
    im.paste(
        Image.open("images/stat_icons/FIGHT_PROP_CRITICAL.png"),
        (x + 10, y + 175),
        Image.open("images/stat_icons/FIGHT_PROP_CRITICAL.png")
    )
    im.paste(
        Image.open("images/stat_icons/FIGHT_PROP_CRITICAL_HURT.png"),
        (x + 10, y + 225),
        Image.open("images/stat_icons/FIGHT_PROP_CRITICAL_HURT.png")
    )
    im.paste(
        Image.open("images/stat_icons/FIGHT_PROP_CHARGE_EFFICIENCY.png"),
        (x + 10, y + 275),  # x + 560, y + 25
        Image.open("images/stat_icons/FIGHT_PROP_CHARGE_EFFICIENCY.png")
    )
    im.paste(
        Image.open("images/stat_icons/FIGHT_PROP_ELEMENT_MASTERY.png"),
        (x + 10, y + 325),
        Image.open("images/stat_icons/FIGHT_PROP_ELEMENT_MASTERY.png")
    )

    # paste image of def on image
    draw.text(
        (x + 60, y + 25),  # x + 60, y + 25
        f"HP: {int(total_stats['2000'])}",
        fill="white",
        font=font
    )
    draw.text(
        (x + 60, y + 75),  # x + 60, y + 75
        f"ATK: {int(total_stats['2001'])}",
        fill="white",
        font=font
    )
    draw.text(
        (x + 60, y + 125),  # x + 60, y + 125
        f"DEF: {int(total_stats['2002'])}",
        fill="white",
        font=font
    )
    draw.text(
        (x + 60, y + 175),  # x + 270, y + 25
        f"CRIT Rate: {round(total_stats['20'] * 100, 1)}%",
        fill="white",
        font=font
    )
    draw.text(
        (x + 60, y + 225),  # x + 270, y + 75
        f"CRIT DMG: {round(total_stats['22'] * 100, 1)}%",
        fill="white",
        font=font
    )
    draw.text(
        (x + 60, y + 275),  # x + 610, y + 25
        f"Energy Recharge: {round(total_stats['23'] * 100, 1)}%",
        fill="white",
        font=font
    )
    draw.text(
        (x + 60, y + 325),  # x + 610, y + 75
        f"Elemental Mastery: {int(round(total_stats['28'], 0))}",
        fill="white",
        font=font
    )


def draw_character_talents(
        im: Image,
        draw: ImageDraw,
        font: ImageFont,
        avatarInfo: dict,
        char_info: dict,
        x: int,
        y: int):
    talent_levels = avatarInfo["skillLevelMap"]
    talent_ids = [str(talent_id) for talent_id in char_info["SkillOrder"]]

    for talent_id in talent_ids:
        talent = char_info["Skills"][talent_id]
        talent_response = requests.get(f"{enka_api}/ui/{talent}.png")
        talent_icon = (
            Image.open(
                BytesIO(talent_response.content)
            ).resize((60, 60))
        )
        talent_level = talent_levels[talent_id]
        crowned = talent_levels[talent_id] == 10

        if "proudSkillExtraLevelMap" in avatarInfo:
            extra_levels = avatarInfo["proudSkillExtraLevelMap"]
            id = str(char_info["ProudMap"][talent_id])
            if id in extra_levels:
                talent_level += extra_levels[id]

        draw.circle(
            (x, y),
            33,
            fill="black",
            outline="#FFD700" if crowned else "white",
            width=3
        )
        im.paste(talent_icon, (x - 30, y - 30), talent_icon)
        draw.circle(
            (x + 25, y + 25),
            20,
            fill="black"
        )
        draw.text(
            (x + 12, y + 13),
            f"{talent_level}",
            fill="#FFD700" if crowned else "white",
            font=font,
            align="center"
        )

        y += 85


def draw_character_constellations(
        im: Image,
        draw: ImageDraw,
        avatarInfo: dict,
        char_info: dict,
        x: int,
        y: int):
    x_start = x
    bg_colors = {
        "Water": "#00BFFF",
        "Fire": "#EC4923",
        "Wind": "#359697",
        "Rock": "#debd6c",
        "Electric": "#945dc4",
        "Grass": "#608a00",
        "Ice": "#4682B4"
    }
    constellation = 0
    if "talentIdList" in avatarInfo:
        constellation = len(avatarInfo["talentIdList"])
        bg_color = bg_colors[char_info["Element"]]
        for i in range(constellation):
            const = char_info["Consts"][i]
            const_response = requests.get(f"{enka_api}/ui/{const}.png")
            const_icon = (
                Image.open(
                    BytesIO(const_response.content)
                ).resize((60, 60))
            )
            draw.circle(
                (x + 30, y + 30),
                30,
                fill=bg_color,
                outline="white"
            )
            im.paste(const_icon, (x, y), const_icon)
            y += 70

    for i in range(constellation, 6):
        locked = Image.open("images/ui/LOCKED.png").resize((30, 30))
        draw.circle(
            (x + 30, y + 30),
            30,
            fill="black",
            outline="white",
        )
        im.paste(locked, (x + 15, y + 15), locked)
        y += 70


def draw_roll_value(
        font: ImageFont,
        draw: ImageDraw,
        roll_value: int,
        roll_value_color: str,
        x: int,
        y: int):

    draw.text(
        (x + 20, y + 150),
        f"{roll_value}%RV",
        fill=roll_value_color,
        font=font
    )


def draw_character_weapon(
    im: Image,
    draw: ImageDraw,
    font: ImageFont,
    avatarInfo: dict,
    x: int,
    y: int
):
    # Draw weapon
    print(x, x + 550)
    draw.rounded_rectangle(
        (x, y, x + 550, y + 125),  # (805, 400, 1100, 500),
        radius=10,
        fill="black",
        outline="white",
        width=3
    )
    flat = avatarInfo["equipList"][-1]["flat"]

    weapon_icon = flat["icon"]
    weapon_response = requests.get(f"{enka_api}/ui/{weapon_icon}.png")
    weapon = Image.open(BytesIO(weapon_response.content)).resize((100, 100))
    im.paste(weapon, (x, y), weapon)

    weapon_name_hash = flat["nameTextMapHash"]
    weapon_name: str = localization["en"][weapon_name_hash]
    needs_ellipses = len(weapon_name) > 30

    weapon_name = (weapon_name[:27] + "..." if needs_ellipses else weapon_name)
    draw.text(
        (x + 300, y + 10),
        f"{weapon_name}",
        fill="white",
        font=font,
        anchor="mt"
    )

    weapon_base_atk = flat["weaponStats"][0]
    atk_icon = Image.open(
        "images/stat_icons/FIGHT_PROP_ATTACK.png"
    ).resize((30, 30))
    im.paste(atk_icon, (x + 110, y + 40), atk_icon)

    draw.text(
        (x + 150, y + 40),
        f"{weapon_base_atk['statValue']}",
        fill="white",
        font=font
    )

    secondary_stat = flat["weaponStats"][1]
    secondary_stat_icon = Image.open(
        f"images/stat_icons/{secondary_stat['appendPropId']}.png"
    ).resize((30, 30))
    secondary_stat_id = secondary_stat["appendPropId"]
    im.paste(secondary_stat_icon, (x + 110, y + 75), secondary_stat_icon)
    draw.text(
        (x + 150, y + 75),
        f"""{secondary_stat['statValue']}{
            '%' if secondary_stat_id in include_percentage_substats
            else ''
        }""",
        fill="white",
        font=font
    )


def draw_akasha_ranking(
    player_uid: str,
    character: str,
    draw: ImageDraw,
    font: ImageFont,
    x: int,
    y: int
):
    # Get Akasha ranking
    akasha_api_url = "https://akasha.cv/api"
    response = requests.get(
        f"{akasha_api_url}/getCalculationsForUser/{player_uid}"
    )
    ranking_data = response.json()["data"]
    our_characters_data = [
        item for item in ranking_data if item["name"] == character
    ]
    has_leaderboard = True
    if not our_characters_data:
        leaderboard_name = "No Leaderboard Data"
        has_leaderboard = False
    else:
        our_characters_data = our_characters_data[0]
        rank_calc = our_characters_data["calculations"]["fit"]
        rank = rank_calc["ranking"]
        out_of = rank_calc["outOf"]
        leaderboard_name = rank_calc["short"]
        if "variant" in rank_calc:
            leaderboard_name += f" {rank_calc['variant']['displayName']}"

    draw.rounded_rectangle(
        (x, y, x + 550, y + 100),
        radius=10,
        fill="black",
        outline="white",
        width=3
    )

    draw.text(
        (x + 275, y + 10),
        f"{leaderboard_name}",
        fill="white",
        font=font,
        align="center",
        anchor="mt"
    )

    if has_leaderboard:
        percentage = 100 - int((out_of - rank) / out_of * 100)
        draw.text(
            (x + 275, y + 50),
            f"Top {percentage}%\t{rank} / {out_of // 1000}k",
            fill="white",
            font=font,
            anchor="mt"
        )


include_percentage_substats = [
    "FIGHT_PROP_CRITICAL",
    "FIGHT_PROP_CRITICAL_HURT",
    "FIGHT_PROP_CHARGE_EFFICIENCY",
]


def draw_character_showcase(
        character: str,
        avatarInfo: dict,
        player_uid: str) -> Image:
    # Create base image, initialize font
    im = Image.new("RGB", (1525, 1080), "black")
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype("fonts/JA-JP.TTF", 24)

    # Draw character splash art
    draw_splash_art(im, character)

    # Draw player's uid
    draw.text(
        (10, 10),
        f"UID: {player_uid}",
        fill="white",
        font=font
    )

    # Draw character total stats
    draw_character_stats(im, draw, font, avatarInfo["fightPropMap"], 925, 50)

    # Draw character talents
    char_info = characters.character_info[str(avatarInfo["avatarId"])]
    draw_character_talents(im, draw, font, avatarInfo, char_info, 855, 90)

    # Draw character constellations
    draw_character_constellations(im, draw, avatarInfo, char_info, 825, 340)

    # Draw weapon
    draw_character_weapon(im, draw, font, avatarInfo, 925, 435)

    # Draw character name
    larger_font = ImageFont.truetype("fonts/JA-JP.TTF", 36)
    draw.text(
        (60, 60),
        f"{character}",
        fill="white",
        font=larger_font
    )

    # Draw character level
    character_level = avatarInfo["propMap"]["4001"]["val"]
    draw.text(
        (60, 100),
        f"Lv. {character_level}",
        fill="white",
        font=font
    )

    # Draw character friendship
    friendship_icon = Image.open(
        "images/stat_icons/friendship.png"
    ).resize((30, 30))
    im.paste(friendship_icon, (60, 130), friendship_icon)
    friendship_level = avatarInfo["fetterInfo"]["expLevel"]
    draw.text(
        (90, 130),
        f"{friendship_level}",
        fill="white",
        font=font
    )

    # Get Akasha ranking
    draw_akasha_ranking(player_uid, character, draw, font, 925, 565)

    # Draw artifacts
    x_box = 50
    y_box = 825
    artifacts_list = characters.get_artifact_list(avatarInfo)
    for artifact in artifacts_list:
        flat = artifact["flat"]
        if flat["itemType"] == "ITEM_RELIQUARY":
            roll_value, roll_value_color = (
                artifacts.calculate_artifact_rv(artifact, character)
            )

            draw_artifact_box(draw, x_box, y_box, roll_value_color)
            draw_artifact_icon(im, flat["icon"], x_box, y_box)
            draw_artifact_substats(
                im, draw, font, flat, x_box + 185, y_box + 25
            )
            draw_roll_value(
                font,
                draw,
                roll_value,
                roll_value_color,
                x_box,
                y_box
            )

            x_box += 285

    return im

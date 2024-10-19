# some things we can note about artifact roll values:
# - the substat starts with a 101, 201, 301, 401, 501
#   (start # is artifact star, 5* 4* etc)
# - last number is the strength of the roll value (70%, 80%, 90%, 100%)
# - group is the 4th and 5th numbers (03 for 3, etc).

import json


def get_substat_map():
    substats = json.loads(open("artifacts/artifact_substats.json").read())
    substat_map = {}
    for substat in substats:
        substat_map[substat["id"]] = substat
    return substat_map


substat_map = get_substat_map()

artifact_type_map = {
    "EQUIP_BRACER": "Flower",
    "EQUIP_NECKLACE": "Feather",
    "EQUIP_SHOES": "Sands",
    "EQUIP_RING": "Goblet",
    "EQUIP_DRESS": "Circlet"
}
stat_map = {
    "FIGHT_PROP_HP": " HP",
    "FIGHT_PROP_ATTACK": " ATK",
    "FIGHT_PROP_DEFENSE": " DEF",
    "FIGHT_PROP_HP_PERCENT": "% HP",
    "FIGHT_PROP_ATTACK_PERCENT": "% ATK",
    "FIGHT_PROP_DEFENSE_PERCENT": "% DEF",
    "FIGHT_PROP_CRITICAL": "% Crit Rate",
    "FIGHT_PROP_CRITICAL_HURT": "% Crit DMG",
    "FIGHT_PROP_CHARGE_EFFICIENCY": "% Energy Recharge",
    "FIGHT_PROP_HEAL_ADD": "% Healing Bonus",
    "FIGHT_PROP_ELEMENT_MASTERY": " Elemental Mastery",
    "FIGHT_PROP_PHYSICAL_ADD_HURT": "% Physical DMG Bonus",
    "FIGHT_PROP_FIRE_ADD_HURT": "% Pyro DMG Bonus",
    "FIGHT_PROP_ELEC_ADD_HURT": "% Electro DMG Bonus",
    "FIGHT_PROP_WATER_ADD_HURT": "% Hydro DMG Bonus",
    "FIGHT_PROP_WIND_ADD_HURT": "% Anemo DMG Bonus",
    "FIGHT_PROP_ICE_ADD_HURT": 	"% Cryo DMG Bonus",
    "FIGHT_PROP_ROCK_ADD_HURT": "% Geo DMG Bonus",
    "FIGHT_PROP_GRASS_ADD_HURT": "% Dendro DMG Bonus",
}


def calculate_artifact_cv(artifact: dict):
    crit_value = 0.0
    reliquary = artifact["reliquary"]
    artifact_rolls = reliquary["appendPropIdList"]
    for artifact_roll in artifact_rolls:
        substat = substat_map[artifact_roll]
        substat_name = stat_map[substat["propType"]]
        if substat_name == "% Crit Rate":
            crit_value += substat["propValue"] * 2.0 * 100
        elif substat_name == "% Crit DMG":
            crit_value += substat["propValue"] * 100
    if reliquary["mainPropId"] == 13008 or reliquary["mainPropId"] == 13007:
        crit_value += 62.2
    return crit_value


def get_roll_value_color(roll_value: int) -> str:
    if roll_value >= 800:
        return "lightpurple"
    elif roll_value >= 700:
        return "aqua"
    elif roll_value >= 600:
        return "lightgreen"
    elif roll_value >= 500:
        return "yellow"
    elif roll_value >= 400:
        return "orange"
    elif roll_value >= 300:
        return "red"
    else:
        return "gray"


def calculate_artifact_rv(artifact: dict, character: str) -> tuple[int, str]:
    useful_substats = json.loads(
        open("artifacts/character_useful_substats.json")
        .read()
    )
    roll_value = 0.0

    reliquary = artifact["reliquary"]
    artifact_rolls = reliquary["appendPropIdList"]
    for artifact_roll in artifact_rolls:
        substat = substat_map[artifact_roll]["propType"]
        if (character in useful_substats
                and substat in useful_substats[character]["useful_substats"]):
            current_roll_strength = int(str(artifact_roll)[-1])
            current_roll_value = (current_roll_strength + 6) * 10
            roll_value += current_roll_value

    roll_value = int(roll_value)
    return roll_value, get_roll_value_color(roll_value)

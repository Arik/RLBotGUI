from functools import lru_cache
from os import path
from copy import deepcopy

import json

@lru_cache(maxsize=8)
def read_json(filepath):
    with open(filepath) as fh:
        return json.load(fh)


def story_id_to_file(story_id):
    if isinstance(story_id, str):
        filepath = path.join(path.dirname(__file__), f"story-{story_id}.json")
    else:
        # custom story
        filepath = story_id["storyPath"]

    return filepath 


def get_story_config(story_id):
    specific_challenges_file = story_id_to_file(story_id)
    return read_json(specific_challenges_file)


def get_cities(story_id):
    """
    Get the challenges file specificed by the story_id
    """
    return get_story_config(story_id)["cities"]


def get_story_settings(story_id):
    """
    Return the settings associated with this story config
    """
    config = get_story_config(story_id)
    return config.get("settings", {})


def get_challenges_by_id(story_id):
    cities = get_cities(story_id)
    challenges_by_id = { }
    for city_id, city in cities.items():
        for challenge in  city["challenges"]:
            challenges_by_id[challenge["id"]] = deepcopy(challenge)
            challenges_by_id[challenge["id"]]["city_description"] = city["description"]
    return challenges_by_id


def get_bots_configs(story_id):
    """
    Get the base bots config and merge it with the bots in the
    story config
    """
    specific_bots_file = story_id_to_file(story_id)
    base_bots_file = path.join(path.dirname(__file__), f"bots-base.json")

    bots: dict = read_json(base_bots_file)
    if path.exists(specific_bots_file):
        bots.update(read_json(specific_bots_file)["bots"])

    return bots


def get_scripts_configs(story_id):
    """
    Get the base scripts config and merge it with the scripts in the
    story config
    """
    specific_scripts_file = story_id_to_file(story_id)
    base_scripts_file = path.join(path.dirname(__file__), f"scripts-base.json")

    scripts: dict = read_json(base_scripts_file)
    if path.exists(specific_scripts_file):
        specific_scripts_file_json = read_json(specific_scripts_file)
        if "scripts" in specific_scripts_file_json:  # A "scripts" field is optional
            scripts.update(specific_scripts_file_json["scripts"])

    return scripts


def get_universal_scripts(story_id):
    """
    Get the list of universal script ids
    """
    specific_universal_scripts_file = story_id_to_file(story_id)

    universal_scripts: list = []
    if path.exists(specific_universal_scripts_file):
        specific_universal_scripts_file_json = read_json(specific_universal_scripts_file)
        if "universal-scripts" in specific_universal_scripts_file_json:  # A "universal-scripts" field is optional
            universal_scripts.extend(specific_universal_scripts_file_json["universal-scripts"])

    return universal_scripts


def get_upgrades(story_id):
    """
    Get the upgrades in the story config, if the "upgrades"
    field does not exist use the base upgrades
    """
    specific_upgrades_file = story_id_to_file(story_id)
    base_upgrades_file = path.join(path.dirname(__file__), f"upgrades-base.json")

    upgrades: list = []
    if path.exists(specific_upgrades_file):
        specific_upgrades_file_json = read_json(specific_upgrades_file)
        if "upgrades" in specific_upgrades_file_json:
            upgrades.extend(specific_upgrades_file_json["upgrades"])
        else:
            upgrades.extend(read_json(base_upgrades_file))

    return upgrades

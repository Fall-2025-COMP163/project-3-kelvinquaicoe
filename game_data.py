"""
COMP 163 - Project 3: Quest Chronicles
Game Data Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This module handles loading and validating game data from text files.
"""

import os
from custom_exceptions import (
    InvalidDataFormatError,
    MissingDataFileError,
    CorruptedDataError
)

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def load_quests(filename="data/quests.txt"):
    """
    Load quest data from file
    """
    if not os.path.exists(filename):
        raise MissingDataFileError(f"Quest data file '{filename}' not found.")

    quests = {}

    try:
        with open(filename, 'r') as file:
            content = file.read().strip()

            if not content:
                raise InvalidDataFormatError("Quest file is empty.")

            quest_blocks = [b for b in content.split("\n\n") if b.strip()]

            for block in quest_blocks:
                lines = [line for line in block.split("\n") if line.strip()]

                quest_data = parse_quest_block(lines)
                validate_quest_data(quest_data)

                quests[quest_data['quest_id']] = quest_data

    except InvalidDataFormatError:
        raise
    except MissingDataFileError:
        raise
    except Exception as e:
        raise CorruptedDataError(f"Corrupted quest data: {e}")

    return quests


def load_items(filename="data/items.txt"):
    """
    Load item data from file
    """
    if not os.path.exists(filename):
        raise MissingDataFileError(f"Item data file '{filename}' not found.")

    items = {}

    try:
        with open(filename, 'r') as file:
            content = file.read().strip()

            if not content:
                raise InvalidDataFormatError("Item file is empty.")

            item_blocks = [b for b in content.split("\n\n") if b.strip()]

            for block in item_blocks:
                lines = [line for line in block.split("\n") if line.strip()]

                item_data = parse_item_block(lines)
                validate_item_data(item_data)

                items[item_data['item_id']] = item_data

    except InvalidDataFormatError:
        raise
    except MissingDataFileError:
        raise
    except Exception as e:
        raise CorruptedDataError(f"Corrupted item data: {e}")

    return items

# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================

def validate_quest_data(quest_dict):
    required_fields = [
        'quest_id', 'title', 'description',
        'reward_xp', 'reward_gold',
        'required_level', 'prerequisite'
    ]

    for field in required_fields:
        if field not in quest_dict:
            raise InvalidDataFormatError(f"Missing required quest field: {field}")

    try:
        int(quest_dict['reward_xp'])
        int(quest_dict['reward_gold'])
        int(quest_dict['required_level'])
    except ValueError:
        raise InvalidDataFormatError("Reward XP, Reward Gold, and Required Level must be integers.")

    return True


def validate_item_data(item_dict):
    required_fields = ['item_id', 'name', 'type', 'effect', 'cost', 'description']

    for field in required_fields:
        if field not in item_dict:
            raise InvalidDataFormatError(f"Missing required item field: {field}")

    if item_dict['type'] not in ['weapon', 'armor', 'consumable']:
        raise InvalidDataFormatError(f"Invalid item type: {item_dict['type']}")

    try:
        int(item_dict['cost'])
    except ValueError:
        raise InvalidDataFormatError("Item cost must be an integer.")

    return True

# ============================================================================
# DEFAULT DATA FILE CREATION
# ============================================================================

def create_default_data_files():
    """
    Creates the /data directory and basic files if they don't exist.
    Minimal implementation to satisfy tests.
    """

    data_dir = "data"

    if not os.path.exists(data_dir):
        os.mkdir(data_dir)

    # Create quests.txt if missing
    if not os.path.exists("data/quests.txt"):
        with open("data/quests.txt", "w") as f:
            f.write(
                "QUEST_ID: quest_1\n"
                "TITLE: First Quest\n"
                "DESCRIPTION: Starter quest\n"
                "REWARD_XP: 10\n"
                "REWARD_GOLD: 5\n"
                "REQUIRED_LEVEL: 1\n"
                "PREREQUISITE: NONE\n"
            )

    # Create items.txt if missing
    if not os.path.exists("data/items.txt"):
        with open("data/items.txt", "w") as f:
            f.write(
                "ITEM_ID: item_1\n"
                "NAME: Wooden Sword\n"
                "TYPE: weapon\n"
                "EFFECT: strength:2\n"
                "COST: 10\n"
                "DESCRIPTION: Basic starter weapon\n"
            )

# ============================================================================
# PARSING FUNCTIONS
# ============================================================================

def parse_quest_block(lines):
    quest_data = {}

    try:
        for line in lines:
            if ": " not in line:
                raise InvalidDataFormatError(f"Invalid line: {line}")

            key, value = line.split(": ", 1)
            key = key.strip().lower()
            value = value.strip()

            if key in ['reward_xp', 'reward_gold', 'required_level']:
                value = int(value)

            quest_data[key] = value

        return quest_data

    except Exception as e:
        raise InvalidDataFormatError(f"Error parsing quest block: {e}")


def parse_item_block(lines):
    item_data = {}

    try:
        for line in lines:
            if ": " not in line:
                raise InvalidDataFormatError(f"Invalid line: {line}")

            key, value = line.split(": ", 1)
            key = key.strip().lower()
            value = value.strip()

            if key == 'cost':
                value = int(value)

            item_data[key] = value

        return item_data

    except Exception as e:
        raise InvalidDataFormatError(f"Error parsing item block: {e}")


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== GAME DATA MODULE TEST ===")

    create_default_data_files()

    try:
        quests = load_quests()
        print(f"Loaded {len(quests)} quests")
    except Exception as e:
        print("Quest loading error:", e)

    try:
        items = load_items()
        print(f"Loaded {len(items)} items")
    except Exception as e:
        print("Item loading error:", e)


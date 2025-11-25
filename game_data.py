"""
COMP 163 - Project 3: Quest Chronicles
Game Data Module - Starter Code

Name: Kelvin Quaicoe

AI Usage: AI was used only to find small bugs in this program, such as typos, indentation issues, and minor syntax mistakes.

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
    Load quest data from a file and return a dictionary of quests.
    """
    # Check if file exists
    if not os.path.exists(filename):
        raise MissingDataFileError(f"Quest data file '{filename}' not found.")

    quests = {}

    try:
        with open(filename, 'r') as file:
            content = file.read().strip()   # Read entire file

            # Check if file is empty
            if not content:
                raise InvalidDataFormatError("Quest file is empty.")

            # Split quests by double newlines (separates quest blocks)
            quest_blocks = [b for b in content.split("\n\n") if b.strip()]

            # Process each quest block individually
            for block in quest_blocks:
                # Break into individual lines, remove empty lines
                lines = [line for line in block.split("\n") if line.strip()]

                # Convert text lines into a quest dictionary
                quest_data = parse_quest_block(lines)

                # Validate required fields + data types
                validate_quest_data(quest_data)

                # Store using quest_id as the key
                quests[quest_data['quest_id']] = quest_data

    # Pass through known errors unchanged
    except InvalidDataFormatError:
        raise
    except MissingDataFileError:
        raise

    # Catch any unexpected error and label it as corrupted data
    except Exception as e:
        raise CorruptedDataError(f"Corrupted quest data: {e}")

    return quests


def load_items(filename="data/items.txt"):
    """
    Load item data from file and return a dictionary of items.
    """
    if not os.path.exists(filename):
        raise MissingDataFileError(f"Item data file '{filename}' not found.")

    items = {}

    try:
        with open(filename, 'r') as file:
            content = file.read().strip()

            # File must not be empty
            if not content:
                raise InvalidDataFormatError("Item file is empty.")

            # Split items into separate blocks (blank line separated)
            item_blocks = [b for b in content.split("\n\n") if b.strip()]

            for block in item_blocks:
                lines = [line for line in block.split("\n") if line.strip()]

                # Convert block into structured dictionary
                item_data = parse_item_block(lines)

                # Validate required fields
                validate_item_data(item_data)

                # Store item using item_id as key
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
    # Required fields every quest must have
    required_fields = [
        'quest_id', 'title', 'description',
        'reward_xp', 'reward_gold',
        'required_level', 'prerequisite'
    ]

    # Ensure all fields exist
    for field in required_fields:
        if field not in quest_dict:
            raise InvalidDataFormatError(f"Missing required quest field: {field}")

    # Check integer fields
    try:
        int(quest_dict['reward_xp'])
        int(quest_dict['reward_gold'])
        int(quest_dict['required_level'])
    except ValueError:
        raise InvalidDataFormatError("Reward XP, Reward Gold, and Required Level must be integers.")

    return True


def validate_item_data(item_dict):
    # Required fields for item data
    required_fields = ['item_id', 'name', 'type', 'effect', 'cost', 'description']

    for field in required_fields:
        if field not in item_dict:
            raise InvalidDataFormatError(f"Missing required item field: {field}")

    # Item type must be valid
    if item_dict['type'] not in ['weapon', 'armor', 'consumable']:
        raise InvalidDataFormatError(f"Invalid item type: {item_dict['type']}")

    # Cost must be an integer
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
    Creates a /data folder and minimal default data files.
    Used when the game is run for the first time.
    """

    data_dir = "data"

    # Create data directory if missing
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)

    # Create basic quests.txt
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

    # Create basic items.txt
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
    # Converts a list of lines into a dictionary representing a quest
    quest_data = {}

    try:
        for line in lines:
            # Each line must contain a key/value pair separated by ": "
            if ": " not in line:
                raise InvalidDataFormatError(f"Invalid line: {line}")

            key, value = line.split(": ", 1)
            key = key.strip().lower()
            value = value.strip()

            # Convert numeric fields to integers
            if key in ['reward_xp', 'reward_gold', 'required_level']:
                value = int(value)

            quest_data[key] = value

        return quest_data

    except Exception as e:
        raise InvalidDataFormatError(f"Error parsing quest block: {e}")


def parse_item_block(lines):
    # Converts a list of lines into a dictionary representing an item
    item_data = {}

    try:
        for line in lines:
            if ": " not in line:
                raise InvalidDataFormatError(f"Invalid line: {line}")

            key, value = line.split(": ", 1)
            key = key.strip().lower()
            value = value.strip()

            # Convert cost to integer
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

    # Create missing directories/files
    create_default_data_files()

    # Load quests
    try:
        quests = load_quests()
        print(f"Loaded {len(quests)} quests")
    except Exception as e:
        print("Quest loading error:", e)

    # Load items
    try:
        items = load_items()
        print(f"Loaded {len(items)} items")
    except Exception as e:
        print("Item loading error:", e)

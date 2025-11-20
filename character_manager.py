import os
from custom_exceptions import (
    InvalidCharacterClassError,
    CharacterNotFoundError,
    SaveFileCorruptedError,
    InvalidSaveDataError,
    CharacterDeadError
)

# ============================================================================
# CHARACTER MANAGEMENT FUNCTIONS
# ============================================================================

def create_character(name, character_class):
    valid_classes = ["Warrior", "Mage", "Rogue", "Cleric"]
    if character_class not in valid_classes:
        raise InvalidCharacterClassError(f"Invalid class: {character_class}")
    
    if character_class == "Warrior":
        health, strength, magic = 120, 15, 5
    elif character_class == "Mage":
        health, strength, magic = 80, 8, 20
    elif character_class == "Rogue":
        health, strength, magic = 90, 12, 10
    else:  # Cleric
        health, strength, magic = 100, 10, 15

    return {
        "name": name,
        "class": character_class,
        "level": 1,
        "health": health,
        "max_health": health,
        "strength": strength,
        "magic": magic,
        "experience": 0,
        "gold": 100,
        "inventory": [],
        "active_quests": [],
        "completed_quests": []
    }


def save_character(character, save_directory="data/save_games"):
    if not os.path.isdir(save_directory):
        os.makedirs(save_directory)

    file_path = os.path.join(save_directory, f"{character['name']}_save.txt")

    with open(file_path, "w") as file:
        for key, value in character.items():
            if isinstance(value, list):
                value = ",".join(value)
            file.write(f"{key.upper()}: {value}\n")
    return True


def load_character(character_name, save_directory="data/save_games"):
    file_path = os.path.join(save_directory, f"{character_name}_save.txt")
    
    if not os.path.exists(file_path):
        raise CharacterNotFoundError(f"Character '{character_name}' does not exist.")
    
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
    except Exception as e:
        raise SaveFileCorruptedError(f"Could not read save file for '{character_name}'.") from e

    character = {}
    for line in lines:
        if ": " not in line:
            raise SaveFileCorruptedError(f"Malformed line in save file: {line}")

        key, value = line.strip().split(": ", 1)
        key = key.lower()
        value = value.strip()

        if key in ["inventory", "active_quests", "completed_quests"]:
            character[key] = [v for v in value.split(",") if v] if value else []
        elif key in ["level", "health", "max_health", "strength", "magic", "experience", "gold"]:
            try:
                character[key] = int(value)
            except ValueError:
                raise InvalidSaveDataError(f"Invalid numeric value for {key}: {value}")
        else:
            character[key] = value

    validate_character_data(character)
    return character


def list_saved_characters(save_directory="data/save_games"):
    if not os.path.exists(save_directory):
        return []

    result = []
    for filename in os.listdir(save_directory):
        if filename.endswith("_save.txt"):
            result.append(filename[:-9])  # remove _save.txt
    return result


def delete_character(character_name, save_directory="data/save_games"):
    file_path = os.path.join(save_directory, f"{character_name}_save.txt")

    if not os.path.exists(file_path):
        raise CharacterNotFoundError(f"Character '{character_name}' does not exist.")

    os.remove(file_path)
    return True


# ============================================================================
# CHARACTER OPERATIONS
# ============================================================================

def gain_experience(character, xp_amount):
    if character['health'] <= 0:
        raise CharacterDeadError("Cannot gain experience: character is dead.")

    character['experience'] += xp_amount

    while character['experience'] >= character['level'] * 100:
        character['experience'] -= character['level'] * 100
        character['level'] += 1
        character['max_health'] += 10
        character['strength'] += 2
        character['magic'] += 2
        character['health'] = character['max_health']


def add_gold(character, amount):
    if character['gold'] + amount < 0:
        raise ValueError("Insufficient gold.")
    character['gold'] += amount
    return character['gold']


def heal_character(character, amount):
    if character['health'] >= character['max_health']:
        return 0

    new_health = min(character['health'] + amount, character['max_health'])
    healed_amount = new_health - character['health']
    character['health'] = new_health
    return healed_amount


def is_character_dead(character):
    return character['health'] <= 0


def revive_character(character):
    if character['health'] > 0:
        return False
    character['health'] = character['max_health'] // 2
    return True


# ============================================================================
# VALIDATION
# ============================================================================

def validate_character_data(character):
    required_fields = [
        "name", "class", "level", "health", "max_health",
        "strength", "magic", "experience", "gold",
        "inventory", "active_quests", "completed_quests"
    ]

    for field in required_fields:
        if field not in character:
            raise InvalidSaveDataError(f"Missing field: {field}")

    numeric_fields = [
        "level", "health", "max_health",
        "strength", "magic", "experience", "gold"
    ]

    for field in numeric_fields:
        if not isinstance(character[field], int):
            raise InvalidSaveDataError(f"Field '{field}' must be an integer.")

    list_fields = ["inventory", "active_quests", "completed_quests"]
    for field in list_fields:
        if not isinstance(character[field], list):
            raise InvalidSaveDataError(f"Field '{field}' must be a list.")

    return True


# ============================================================================
# TESTING (OPTIONAL)
# ============================================================================

if __name__ == "__main__":
    print("=== CHARACTER MANAGER TEST ===")

    try:
        char = create_character("TestHero", "Warrior")
        print(f"Created: {char['name']} the {char['class']}")
    except InvalidCharacterClassError as e:
        print(f"Invalid class: {e}")

    try:
        save_character(char)
        print("Character saved successfully")
    except Exception as e:
        print(f"Save error: {e}")

    try:
        loaded = load_character("TestHero")
        print(f"Loaded: {loaded['name']}")
    except Exception as e:
        print(f"Load error: {e}")

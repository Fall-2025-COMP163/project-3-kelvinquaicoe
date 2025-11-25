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
    # Define which classes are valid
    valid_classes = ["Warrior", "Mage", "Rogue", "Cleric"]

    # Raise error if the player picks a class that doesn't exist
    if character_class not in valid_classes:
        raise InvalidCharacterClassError(f"Invalid class: {character_class}")
    
    # Assign stat values based on chosen class
    if character_class == "Warrior":
        health, strength, magic = 120, 15, 5
    elif character_class == "Mage":
        health, strength, magic = 80, 8, 20
    elif character_class == "Rogue":
        health, strength, magic = 90, 12, 10
    else:  # Cleric
        health, strength, magic = 100, 10, 15

    # Return structured character data as a dictionary
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
    import os

    # Create save directory if it doesn’t exist
    os.makedirs(save_directory, exist_ok=True)

    # Build the file path for the specific character
    file_path = os.path.join(save_directory, f"{character['name']}_save.txt")

    try:
        # Write each key-value pair into the save file
        with open(file_path, "w") as f:
            for key, value in character.items():
                f.write(f"{key}: {value}\n")
        return True

    except Exception as e:
        # Return False for any unexpected issue
        return False


def load_character(character_name, save_directory="data/save_games"):
    import os

    # Find the save file for this character
    file_path = os.path.join(save_directory, f"{character_name}_save.txt")

    # If missing, raise custom "not found" error
    if not os.path.exists(file_path):
        raise CharacterNotFoundError(f"Character '{character_name}' does not exist.")

    character = {}

    try:
        # Read all lines from the file
        with open(file_path, "r") as f:
            lines = f.readlines()

        # Process each line individually
        for line in lines:
            line = line.strip()
            if not line:
                continue  # Skip blank lines

            # Ensure the line has a key/value structure
            if ": " not in line:
                raise SaveFileCorruptedError(f"Malformed line in save file: {line}")

            key, value = line.split(": ", 1)

            # Convert numeric strings back into integers
            if value.isdigit():
                value = int(value)

            # Convert list strings back into Python lists
            elif value.startswith("[") and value.endswith("]"):
                value = eval(value)

            character[key] = value

        return character

    except Exception as e:
        # Wrap any error into a "corrupted save file" exception
        raise SaveFileCorruptedError(
            f"Could not read save file for '{character_name}'"
        ) from e


def list_saved_characters(save_directory="data/save_games"):
    # If directory doesn't exist, no characters are saved
    if not os.path.exists(save_directory):
        return []

    result = []

    # Loop over all files and extract character names
    for filename in os.listdir(save_directory):
        if filename.endswith("_save.txt"):
            result.append(filename[:-9])  # remove "_save.txt"

    return result


def delete_character(character_name, save_directory="data/save_games"):
    # Build file path
    file_path = os.path.join(save_directory, f"{character_name}_save.txt")

    # If file doesn't exist, raise an error
    if not os.path.exists(file_path):
        raise CharacterNotFoundError(f"Character '{character_name}' does not exist.")

    # Delete the file and confirm success
    os.remove(file_path)
    return True


# ============================================================================
# CHARACTER OPERATIONS
# ============================================================================

def gain_experience(character, xp_amount):
    # Dead characters cannot receive XP
    if character['health'] <= 0:
        raise CharacterDeadError("Cannot gain experience: character is dead.")

    character['experience'] += xp_amount

    # Loop in case multiple level-ups happen at once
    while character['experience'] >= character['level'] * 100:
        character['experience'] -= character['level'] * 100
        character['level'] += 1

        # Increase stats each level
        character['max_health'] += 10
        character['strength'] += 2
        character['magic'] += 2

        # Restore full health on level up
        character['health'] = character['max_health']


def add_gold(character, amount):
    # Prevent gold from going below zero
    if character['gold'] + amount < 0:
        raise ValueError("Insufficient gold.")

    character['gold'] += amount
    return character['gold']


def heal_character(character, amount):
    # If already fully healed, return 0 healing done
    if character['health'] >= character['max_health']:
        return 0

    # Heal but do not exceed max health
    new_health = min(character['health'] + amount, character['max_health'])
    healed_amount = new_health - character['health']
    character['health'] = new_health

    return healed_amount


def is_character_dead(character):
    # Return True if health is zero or less
    return character['health'] <= 0


def revive_character(character):
    # Cannot revive characters that are already alive
    if character['health'] > 0:
        return False

    # Revive to half of max health
    character['health'] = character['max_health'] // 2
    return True


# ============================================================================
# VALIDATION
# ============================================================================

def validate_character_data(character):
    # Ensure all required fields are present
    required_fields = [
        "name", "class", "level", "health", "max_health",
        "strength", "magic", "experience", "gold",
        "inventory", "active_quests", "completed_quests"
    ]

    for field in required_fields:
        if field not in character:
            raise InvalidSaveDataError(f"Missing field: {field}")

    # Ensure numeric fields are integers
    numeric_fields = [
        "level", "health", "max_health",
        "strength", "magic", "experience", "gold"
    ]

    for field in numeric_fields:
        if not isinstance(character[field], int):
            raise InvalidSaveDataError(f"Field '{field}' must be an integer.")

    # Ensure list fields are actually lists
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

    # Test character creation
    try:
        char = create_character("TestHero", "Warrior")
        print(f"Created: {char['name']} the {char['class']}")
    except InvalidCharacterClassError as e:
        print(f"Invalid class: {e}")

    # Test saving
    try:
        save_character(char)
        print("Character saved successfully")
    except Exception as e:
        print(f"Save error: {e}")

    # Test loading
    try:
        loaded = load_character("TestHero")
        print(f"Loaded: {loaded['name']}")
    except Exception as e:
        print(f"Load error: {e}")

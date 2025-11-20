"""
COMP 163 - Project 3: Quest Chronicles
Inventory System Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This module handles inventory management, item usage, and equipment.
"""
# inventory_system.py
from custom_exceptions import (
    InventoryFullError,
    ItemNotFoundError,
    InsufficientResourcesError,
    InvalidItemTypeError
)
from collections import Counter

MAX_INVENTORY_SIZE = 20

# -------------------------
# INVENTORY MANAGEMENT
# -------------------------

def add_item_to_inventory(character, item_id):
    if len(character['inventory']) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory is full.")
    character['inventory'].append(item_id)
    return True

def remove_item_from_inventory(character, item_id):
    if item_id not in character['inventory']:
        raise ItemNotFoundError(f"Item '{item_id}' not found in inventory.")
    character['inventory'].remove(item_id)
    return True

def has_item(character, item_id):
    return item_id in character['inventory']

def count_item(character, item_id):
    return character['inventory'].count(item_id)

def get_inventory_space_remaining(character):
    return MAX_INVENTORY_SIZE - len(character['inventory'])

def clear_inventory(character):
    removed_items = character['inventory'][:]
    character['inventory'].clear()
    return removed_items

# -------------------------
# ITEM USAGE
# -------------------------

def use_item(character, item_id, item_data):
    if item_id not in character['inventory']:
        raise ItemNotFoundError(f"Item '{item_id}' not found in inventory.")
    if item_data['type'] != 'consumable':
        raise InvalidItemTypeError(f"Item '{item_id}' is not a consumable.")
    stat_name, value = parse_item_effect(item_data['effect'])
    apply_stat_effect(character, stat_name, value)
    remove_item_from_inventory(character, item_id)
    return f"Used {item_data['name']}, {stat_name} increased by {value}."

# -------------------------
# EQUIPMENT
# -------------------------

def equip_item(character, item_id, item_data, item_data_dict, slot):
    """Generic equip function for 'weapon' or 'armor'"""
    if item_id not in character['inventory']:
        raise ItemNotFoundError(f"Item '{item_id}' not found in inventory.")
    if item_data['type'] != slot:
        raise InvalidItemTypeError(f"Item '{item_id}' is not a {slot}.")

    equipped_slot = f"equipped_{slot}"
    # Unequip old item if exists
    if character.get(equipped_slot):
        old_id = character[equipped_slot]
        old_data = item_data_dict[old_id]
        stat_name, value = parse_item_effect(old_data['effect'])
        apply_stat_effect(character, stat_name, -value)
        add_item_to_inventory(character, old_id)

    # Equip new item
    stat_name, value = parse_item_effect(item_data['effect'])
    apply_stat_effect(character, stat_name, value)
    character[equipped_slot] = item_id
    remove_item_from_inventory(character, item_id)
    return f"Equipped {item_data['name']}, {stat_name} increased by {value}."

def unequip_item(character, item_data_dict, slot):
    equipped_slot = f"equipped_{slot}"
    if not character.get(equipped_slot):
        return None
    item_id = character[equipped_slot]
    item_data = item_data_dict[item_id]
    stat_name, value = parse_item_effect(item_data['effect'])
    apply_stat_effect(character, stat_name, -value)
    add_item_to_inventory(character, item_id)
    character[equipped_slot] = None
    return item_id

# -------------------------
# SHOP SYSTEM
# -------------------------

def purchase_item(character, item_id, item_data):
    if character['gold'] < item_data['cost']:
        raise InsufficientResourcesError("Not enough gold to purchase item.")
    if len(character['inventory']) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory is full.")
    character['gold'] -= item_data['cost']
    character['inventory'].append(item_id)
    return True

def sell_item(character, item_id, item_data):
    if item_id not in character['inventory']:
        raise ItemNotFoundError(f"Item '{item_id}' not found in inventory.")
    sell_price = item_data['cost'] // 2
    character['inventory'].remove(item_id)
    character['gold'] += sell_price
    return sell_price

# -------------------------
# HELPERS
# -------------------------

def parse_item_effect(effect_string):
    stat_name, value_str = effect_string.split(":")
    return stat_name.strip(), int(value_str.strip())

def apply_stat_effect(character, stat_name, value):
    if stat_name not in character:
        character[stat_name] = 0
    character[stat_name] += value
    if stat_name == 'health':
        # Clamp health between 0 and max_health
        character['health'] = min(max(character['health'], 0), character.get('max_health', character['health']))

def display_inventory(character, item_data_dict):
    inventory_count = Counter(character['inventory'])
    print("Inventory:")
    for item_id, count in inventory_count.items():
        item_name = item_data_dict[item_id]['name'] if item_id in item_data_dict else "Unknown"
        item_type = item_data_dict[item_id]['type'] if item_id in item_data_dict else "Unknown"
        print(f"- {item_name} (Type: {item_type}) x{count}")

# -------------------------
# TESTING
# -------------------------

if __name__ == "__main__":
    print("=== INVENTORY SYSTEM TEST ===")
    
    test_char = {'inventory': [], 'gold': 100, 'health': 80, 'max_health': 80}
    
    # Add item
    try:
        add_item_to_inventory(test_char, "health_potion")
        print(f"Inventory: {test_char['inventory']}")
    except InventoryFullError:
        print("Inventory is full!")

    # Use item
    test_item = {'item_id': 'health_potion', 'type': 'consumable', 'effect': 'health:20'}
    try:
        result = use_item(test_char, "health_potion", test_item)
        print(result)
        print(f"Health after use: {test_char['health']}")
    except ItemNotFoundError:
        print("Item not found")



"""
COMP 163 - Project 3: Quest Chronicles
Quest Handler Module - Enhanced Version

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This module handles quest management, dependencies, completion, and item rewards.
"""

from custom_exceptions import (
    QuestNotFoundError,
    QuestRequirementsNotMetError,
    QuestAlreadyCompletedError,
    QuestNotActiveError,
    InsufficientLevelError
)
from inventory_system import add_item_to_inventory, ItemNotFoundError, InventoryFullError

# ============================================================================  
# QUEST MANAGEMENT
# ============================================================================  

def accept_quest(character, quest_id, quest_data_dict):
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest '{quest_id}' not found.")
    quest_data = quest_data_dict[quest_id]
    if character['level'] < quest_data['required_level']:
        raise InsufficientLevelError(f"Character level {character['level']} is below required level {quest_data['required_level']}.")
    prerequisite = quest_data['prerequisite']
    if prerequisite != "NONE" and prerequisite not in character['completed_quests']:
        raise QuestRequirementsNotMetError(f"Prerequisite quest '{prerequisite}' not completed.")
    if quest_id in character['completed_quests']:
        raise QuestAlreadyCompletedError(f"Quest '{quest_id}' has already been completed.")
    if quest_id in character['active_quests']:
        raise QuestRequirementsNotMetError(f"Quest '{quest_id}' is already active.")
    character['active_quests'].append(quest_id)
    return True


def complete_quest(character, quest_id, quest_data_dict, item_data_dict=None):
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest '{quest_id}' not found.")
    if quest_id not in character['active_quests']:
        raise QuestNotActiveError(f"Quest '{quest_id}' is not active.")

    quest_data = quest_data_dict[quest_id]
    character['active_quests'].remove(quest_id)
    character['completed_quests'].append(quest_id)
    character['experience'] += quest_data['reward_xp']
    character['gold'] += quest_data['reward_gold']

    # Handle item rewards if any
    rewarded_items = []
    if item_data_dict and 'reward_items' in quest_data:
        for item_id in quest_data['reward_items']:
            try:
                add_item_to_inventory(character, item_id)
                rewarded_items.append(item_id)
            except InventoryFullError:
                print(f"Inventory full! Could not receive item '{item_id}'.")

    return {
        'reward_xp': quest_data['reward_xp'],
        'reward_gold': quest_data['reward_gold'],
        'reward_items': rewarded_items
    }


def abandon_quest(character, quest_id):
    if quest_id not in character['active_quests']:
        raise QuestNotActiveError(f"Quest '{quest_id}' is not active.")
    character['active_quests'].remove(quest_id)
    return True


# ============================================================================  
# QUEST DATA RETRIEVAL
# ============================================================================  

def get_active_quests(character, quest_data_dict):
    return [quest_data_dict[qid] for qid in character['active_quests'] if qid in quest_data_dict]


def get_completed_quests(character, quest_data_dict):
    return [quest_data_dict[qid] for qid in character['completed_quests'] if qid in quest_data_dict]


def get_available_quests(character, quest_data_dict):
    return [qdata for qid, qdata in quest_data_dict.items() if can_accept_quest(character, qid, quest_data_dict)]


def is_quest_completed(character, quest_id):
    return quest_id in character['completed_quests']


def is_quest_active(character, quest_id):
    return quest_id in character['active_quests']


def can_accept_quest(character, quest_id, quest_data_dict):
    if quest_id not in quest_data_dict:
        return False
    quest_data = quest_data_dict[quest_id]
    if character['level'] < quest_data['required_level']:
        return False
    prereq = quest_data['prerequisite']
    if prereq != "NONE" and prereq not in character['completed_quests']:
        return False
    if quest_id in character['completed_quests'] or quest_id in character['active_quests']:
        return False
    return True


def get_quest_prerequisite_chain(quest_id, quest_data_dict):
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest '{quest_id}' not found.")
    chain = []
    current = quest_id
    while current != "NONE":
        if current not in quest_data_dict:
            raise QuestNotFoundError(f"Quest '{current}' not found.")
        chain.insert(0, current)
        current = quest_data_dict[current]['prerequisite']
    return chain


# ============================================================================  
# QUEST STATISTICS
# ============================================================================  

def get_quest_completion_percentage(character, quest_data_dict):
    total = len(quest_data_dict)
    return (len(character['completed_quests']) / total) * 100 if total > 0 else 0.0


def get_total_quest_rewards_earned(character, quest_data_dict):
    total_xp = sum(quest_data_dict[qid]['reward_xp'] for qid in character['completed_quests'] if qid in quest_data_dict)
    total_gold = sum(quest_data_dict[qid]['reward_gold'] for qid in character['completed_quests'] if qid in quest_data_dict)
    return {'total_xp': total_xp, 'total_gold': total_gold}


def get_quests_by_level(quest_data_dict, min_level, max_level):
    return [q for q in quest_data_dict.values() if min_level <= q['required_level'] <= max_level]


# ============================================================================  
# DISPLAY FUNCTIONS
# ============================================================================  

def display_quest_info(quest_data):
    print(f"\n=== {quest_data['title']} ===")
    print(f"Description: {quest_data['description']}")
    print(f"Required Level: {quest_data['required_level']}")
    print(f"Prerequisite: {quest_data['prerequisite']}")
    print(f"Rewards: XP={quest_data['reward_xp']}, Gold={quest_data['reward_gold']}")
    if 'reward_items' in quest_data and quest_data['reward_items']:
        print(f"Reward Items: {', '.join(quest_data['reward_items'])}")


def display_quest_list(quest_list):
    for quest in quest_list:
        print(f"- {quest['title']} (Level {quest['required_level']})")


def display_character_quest_progress(character, quest_data_dict):
    active = len(character['active_quests'])
    completed = len(character['completed_quests'])
    percent = get_quest_completion_percentage(character, quest_data_dict)
    rewards = get_total_quest_rewards_earned(character, quest_data_dict)
    print(f"\n=== Quest Progress ===")
    print(f"Active Quests: {active}")
    print(f"Completed Quests: {completed}")
    print(f"Completion Percentage: {percent:.2f}%")
    print(f"Total XP Earned: {rewards['total_xp']}")
    print(f"Total Gold Earned: {rewards['total_gold']}")


# ============================================================================  
# VALIDATION
# ============================================================================  

def validate_quest_prerequisites(quest_data_dict):
    for qid, qdata in quest_data_dict.items():
        prereq = qdata['prerequisite']
        if prereq != "NONE" and prereq not in quest_data_dict:
            raise QuestNotFoundError(f"Quest '{qid}' has invalid prerequisite '{prereq}'.")
    return True


# ============================================================================  
# TESTING
# ============================================================================  

if __name__ == "__main__":
    print("=== QUEST HANDLER TEST ===")
    
    # Test character and quest
    test_char = {'level': 1, 'active_quests': [], 'completed_quests': [], 'experience': 0, 'gold': 100, 'inventory': []}
    test_item_data = {'healing_potion': {'name': 'Healing Potion', 'type': 'consumable', 'effect': 'health:20'}}
    test_quests = {
        'first_quest': {
            'quest_id': 'first_quest',
            'title': 'First Steps',
            'description': 'Complete your first quest',
            'reward_xp': 50,
            'reward_gold': 25,
            'required_level': 1,
            'prerequisite': 'NONE',
            'reward_items': ['healing_potion']
        }
    }

    accept_quest(test_char, 'first_quest', test_quests)
    print("Quest accepted!")
    rewards = complete_quest(test_char, 'first_quest', test_quests, test_item_data)
    print(f"Quest completed! Rewards: {rewards}")

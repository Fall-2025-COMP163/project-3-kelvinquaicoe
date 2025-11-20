"""
COMP 163 - Project 3: Quest Chronicles
Main Game Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This is the main game file that ties all modules together.
Demonstrates module integration and complete game flow.
"""

# Import all our custom modules
import character_manager
import inventory_system
import quest_handler
import combat_system
import game_data
from custom_exceptions import *

# ============================================================================
# GAME STATE
# ============================================================================

# Global variables for game data
current_character = None
all_quests = {}
all_items = {}
game_running = False

# ============================================================================
# MAIN MENU
# ============================================================================

def main_menu():
    """
    Display main menu and get player choice
    
    Options:
    1. New Game
    2. Load Game
    3. Exit
    
    Returns: Integer choice (1-3)
    """
    # TODO: Implement main menu display
    # Show options
    # Get user input
    # Validate input (1-3)
    # Return choice
    while True:
        print("\nMain Menu:")
        print("1. New Game")
        print("2. Load Game")
        print("3. Exit")
        
        choice = input("Select an option (1-3): ").strip()
        
        if choice in ['1', '2', '3']:
            return int(choice)
        else:
            print("Invalid choice. Please select a number between 1 and 3.")

def new_game():
    """
    Start a new game
    
    Prompts for:
    - Character name
    - Character class
    
    Creates character and starts game loop
    """
    global current_character
    
    # TODO: Implement new game creation
    # Get character name from user
    # Get character class from user
    # Try to create character with character_manager.create_character()
    # Handle InvalidCharacterClassError
    # Save character
    # Start game loop
    while True:
        name = input("Enter your character's name: ").strip()
        print("Select your character's class:")
        print("1. Warrior")
        print("2. Mage")
        print("3. Rogue")
        class_choice = input("Enter class number (1-3): ").strip()
        
        class_map = {'1': 'Warrior', '2': 'Mage', '3': 'Rogue'}
        
        if class_choice in class_map:
            character_class = class_map[class_choice]
            try:
                current_character = character_manager.create_character(name, character_class)
                character_manager.save_character(current_character)
                print(f"Character '{name}' the {character_class} created successfully!")
                game_loop()
                return
            except InvalidCharacterClassError as e:
                print(f"Error: {e}")
        else:
            print("Invalid class choice. Please select 1, 2, or 3.")

def load_game():
    """
    Load an existing saved game
    
    Shows list of saved characters
    Prompts user to select one
    """
    global current_character
    
    # TODO: Implement game loading
    # Get list of saved characters
    # Display them to user
    # Get user choice
    # Try to load character with character_manager.load_character()
    # Handle CharacterNotFoundError and SaveFileCorruptedError
    # Start game loop
    saved_characters = character_manager.list_saved_characters()
    if not saved_characters:
        print("No saved characters found.")
        return
    print("\nSaved Characters:")
    for idx, char_name in enumerate(saved_characters, start=1):
        print(f"{idx}. {char_name}")
    while True:
        choice = input(f"Select a character to load (1-{len(saved_characters)}): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(saved_characters):
            selected_name = saved_characters[int(choice) - 1]
            try:
                current_character = character_manager.load_character(selected_name)
                print(f"Character '{selected_name}' loaded successfully!")
                game_loop()
                return
            except (CharacterNotFoundError, SaveFileCorruptedError) as e:
                print(f"Error: {e}")
        else:
            print(f"Invalid choice. Please select a number between 1 and {len(saved_characters)}.")

# ============================================================================
# GAME LOOP
# ============================================================================

def game_loop():
    """
    Main game loop - shows game menu and processes actions
    """
    global game_running, current_character
    
    game_running = True
    
    # TODO: Implement game loop
    # While game_running:
    #   Display game menu
    #   Get player choice
    #   Execute chosen action
    #   Save game after each action
    while game_running:
        choice = game_menu()
        
        if choice == 1:
            view_character_stats()
        elif choice == 2:
            view_inventory()
        elif choice == 3:
            quest_menu()
        elif choice == 4:
            explore()
        elif choice == 5:
            shop()
        elif choice == 6:
            save_game()
            print("Exiting to main menu...")
            break
        else:
            print("Invalid choice. Please select a valid option.")

def game_menu():
    """
    Display game menu and get player choice
    
    Options:
    1. View Character Stats
    2. View Inventory
    3. Quest Menu
    4. Explore (Find Battles)
    5. Shop
    6. Save and Quit
    
    Returns: Integer choice (1-6)
    """
    # TODO: Implement game menu
    while True:
        print("\nGame Menu:")
        print("1. View Character Stats")
        print("2. View Inventory")
        print("3. Quest Menu")
        print("4. Explore (Find Battles)")
        print("5. Shop")
        print("6. Save and Quit")
        
        choice = input("Select an option (1-6): ").strip()
        
        if choice in ['1', '2', '3', '4', '5', '6']:
            return int(choice)
        else:
            print("Invalid choice. Please select a number between 1 and 6.")

# ============================================================================
# GAME ACTIONS
# ============================================================================

def view_character_stats():
    """Display character information"""
    global current_character
    
    # TODO: Implement stats display
    # Show: name, class, level, health, stats, gold, etc.
    # Use character_manager functions
    # Show quest progress using quest_handler
    if not current_character:
        print("No character loaded.")
        return
    print(f"\nCharacter Stats for {current_character['name']}:")
    print(f"Class: {current_character['class']}")
    print(f"Level: {current_character['level']}")
    print(f"Health: {current_character['health']}/{current_character['max_health']}")
    print(f"Gold: {current_character['gold']}")
    print("Stats:")
    for stat, value in current_character['stats'].items():
        print(f"  {stat.capitalize()}: {value}")
    print("Active Quests:")
    active_quests = quest_handler.get_active_quests(current_character, all_quests)
    if active_quests:
        for quest_id in active_quests:
            quest = all_quests[quest_id]
            print(f"  - {quest['name']}: {quest['description']}")
    else:
        print("  None")

def view_inventory():
    """Display and manage inventory"""
    global current_character, all_items
    
    # TODO: Implement inventory menu
    # Show current inventory
    # Options: Use item, Equip weapon/armor, Drop item
    # Handle exceptions from inventory_system
    from inventory_system import InventoryFullError, ItemNotFoundError, InsufficientResourcesError
    if not current_character:
        print("No character loaded.")
        return
    print("\nInventory:")
    if current_character['inventory']:
        for item_id in current_character['inventory']:
            item = all_items.get(item_id, {'name': 'Unknown Item'})
            print(f"  - {item['name']} (ID: {item_id})")
    else:
        print("  Inventory is empty.")

def quest_menu():
    """Quest management menu"""
    global current_character, all_quests
    
    # TODO: Implement quest menu
    # Show:
    #   1. View Active Quests
    #   2. View Available Quests
    #   3. View Completed Quests
    #   4. Accept Quest
    #   5. Abandon Quest
    #   6. Complete Quest (for testing)
    #   7. Back
    # Handle exceptions from quest_handler
    from quest_handler import QuestNotFoundError, QuestAlreadyAcceptedError, QuestNotAcceptedError
    while True:
        print("\nQuest Menu:")
        print("1. View Active Quests")
        print("2. View Available Quests")
        print("3. View Completed Quests")
        print("4. Accept Quest")
        print("5. Abandon Quest")
        print("6. Complete Quest (for testing)")
        print("7. Back")
        
        choice = input("Select an option (1-7): ").strip()
        
        if choice == '1':
            active_quests = quest_handler.get_active_quests(current_character, all_quests)
            print("\nActive Quests:")
            if active_quests:
                for quest_id in active_quests:
                    quest = all_quests[quest_id]
                    print(f"  - {quest['name']}: {quest['description']}")
            else:
                print("  None")
        elif choice == '2':
            available_quests = quest_handler.get_available_quests(current_character, all_quests)
            print("\nAvailable Quests:")
            if available_quests:
                for quest_id in available_quests:
                    quest = all_quests[quest_id]
                    print(f"  - {quest['name']}: {quest['description']}")
            else:
                print("  None")
        elif choice == '3':
            completed_quests = quest_handler.get_completed_quests(current_character, all_quests)
            print("\nCompleted Quests:")
            if completed_quests:
                for quest_id in completed_quests:
                    quest = all_quests[quest_id]
                    print(f"  - {quest['name']}: {quest['description']}")
            else:
                print("  None")
        elif choice == '4':
            quest_id = input("Enter Quest ID to accept: ").strip()
            try:
                quest_handler.accept_quest(current_character, quest_id, all_quests)
                print(f"Quest '{quest_id}' accepted!")
            except (QuestNotFoundError, QuestAlreadyAcceptedError) as e:
                print(f"Error: {e}")
        elif choice == '5':
            quest_id = input("Enter Quest ID to abandon: ").strip()
            try:
                quest_handler.abandon_quest(current_character, quest_id)
                print(f"Quest '{quest_id}' abandoned.")
            except QuestNotAcceptedError as e:
                print(f"Error: {e}")
        elif choice == '6':
            quest_id = input("Enter Quest ID to complete (for testing): ").strip()
            try:
                quest_handler.complete_quest(current_character, quest_id, all_quests)
                print(f"Quest '{quest_id}' completed!")
            except QuestNotAcceptedError as e:
                print(f"Error: {e}")
        elif choice == '7':
            break
        else:
            print("Invalid choice. Please select a number between 1 and 7.")


def explore():
    """Find and fight random enemies"""
    global current_character
    
    # TODO: Implement exploration
    # Generate random enemy based on character level
    # Start combat with combat_system.SimpleBattle
    # Handle combat results (XP, gold, death)
    # Handle exceptions
    from combat_system import SimpleBattle, CharacterDeadError
    import random
    if not current_character:
        print("No character loaded.")
        return
    enemy_levels = [current_character['level'], current_character['level'] + 1]
    enemy_level = random.choice(enemy_levels)
    enemy = combat_system.generate_random_enemy(enemy_level)
    print(f"\nA wild {enemy['name']} (Level {enemy['level']}) appears!")
    battle = SimpleBattle(current_character, enemy)
    try:
        result = battle.start_battle()
        if result == 'victory':
            xp_gained = enemy['xp_reward']
            gold_gained = enemy['gold_reward']
            character_manager.gain_experience(current_character, xp_gained)
            current_character['gold'] += gold_gained
            print(f"You defeated the {enemy['name']}!")
            print(f"Gained {xp_gained} XP and {gold_gained} gold.")
        elif result == 'defeat':
            handle_character_death()
    except CharacterDeadError:
        handle_character_death()

def shop():
    """Shop menu for buying/selling items"""
    global current_character, all_items
    
    # TODO: Implement shop
    # Show available items for purchase
    # Show current gold
    # Options: Buy item, Sell item, Back
    # Handle exceptions from inventory_system
    from inventory_system import InsufficientResourcesError, ItemNotFoundError, InventoryFullError
    while True:
        print("\nShop Menu:")
        print("1. Buy Item")
        print("2. Sell Item")
        print("3. Back")
        choice = input("Select an option (1-3): ").strip()
        if choice == '1':
            print("\nItems for Sale:")
            for item_id, item in all_items.items():
                print(f"  - {item['name']} (ID: {item_id}) - Cost: {item['cost']} gold")
            item_id = input("Enter Item ID to buy: ").strip()
            item_data = all_items.get(item_id)
            if item_data:
                try:
                    inventory_system.add_item_to_inventory(current_character, item_id, item_data)
                    print(f"Purchased '{item_data['name']}' for {item_data['cost']} gold.")
                except (InsufficientResourcesError, InventoryFullError) as e:
                    print(f"Error: {e}")
            else:
                print("Invalid Item ID.")
        elif choice == '2':
            print("\nYour Inventory:")
            if current_character['inventory']:
                for item_id in current_character['inventory']:
                    item = all_items.get(item_id, {'name': 'Unknown Item'})
                    print(f"  - {item['name']} (ID: {item_id})")
                item_id = input("Enter Item ID to sell: ").strip()
                item_data = all_items.get(item_id)
                if item_data:
                    try:
                        sell_price = inventory_system.sell_item(current_character, item_id, item_data)
                        print(f"Sold '{item_data['name']}' for {sell_price} gold.")
                    except ItemNotFoundError as e:
                        print(f"Error: {e}")
                else:
                    print("Invalid Item ID.")
            else:
                print("  Inventory is empty.")
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please select a number between 1 and 3.")

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def save_game():
    """Save current game state"""
    global current_character
    
    # TODO: Implement save
    # Use character_manager.save_character()
    # Handle any file I/O exceptions
    import character_manager
    try:
        character_manager.save_character(current_character)
        print("Game saved successfully!")
    except Exception as e:
        print(f"Error saving game: {e}")

def load_game_data():
    """Load all quest and item data from files"""
    global all_quests, all_items
    
    # TODO: Implement data loading
    # Try to load quests with game_data.load_quests()
    # Try to load items with game_data.load_items()
    # Handle MissingDataFileError, InvalidDataFormatError
    # If files missing, create defaults with game_data.create_default_data_files()
    all_quests = game_data.load_quests()
    all_items = game_data.load_items()

def handle_character_death():
    """Handle character death"""
    global current_character, game_running
    
    # TODO: Implement death handling
    # Display death message
    # Offer: Revive (costs gold) or Quit
    # If revive: use character_manager.revive_character()
    # If quit: set game_running = False
    if not current_character:
        return
    print(f"\n{current_character['name']} has fallen in battle!")
    while True:
        choice = input("Do you want to Revive (R) or Quit (Q)? ").strip().upper()
        if choice == 'R':
            try:
                character_manager.revive_character(current_character)
                print(f"{current_character['name']} has been revived!")
                return
            except InsufficientGoldError:
                print("Not enough gold to revive!")
        elif choice == 'Q':
            game_running = False
            print("Thank you for playing Quest Chronicles!")
            return
        else:
            print("Invalid choice. Please enter R or Q.")
        
def display_welcome():
    """Display welcome message"""
    print("=" * 50)
    print("     QUEST CHRONICLES - A MODULAR RPG ADVENTURE")
    print("=" * 50)
    print("\nWelcome to Quest Chronicles!")
    print("Build your character, complete quests, and become a legend!")
    print()

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main game execution function"""
    
    # Display welcome message
    display_welcome()
    
    # Load game data
    try:
        load_game_data()
        print("Game data loaded successfully!")
    except MissingDataFileError:
        print("Creating default game data...")
        game_data.create_default_data_files()
        load_game_data()
    except InvalidDataFormatError as e:
        print(f"Error loading game data: {e}")
        print("Please check data files for errors.")
        return
    
    # Main menu loop
    while True:
        choice = main_menu()
        
        if choice == 1:
            new_game()
        elif choice == 2:
            load_game()
        elif choice == 3:
            print("\nThanks for playing Quest Chronicles!")
            break
        else:
            print("Invalid choice. Please select 1-3.")

if __name__ == "__main__":
    main()

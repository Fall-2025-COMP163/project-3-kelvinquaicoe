"""
COMP 163 - Project 3: Quest Chronicles
Combat System Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

Handles combat mechanics
"""

from custom_exceptions import (
    InvalidTargetError,
    CombatNotActiveError,
    CharacterDeadError,
    AbilityOnCooldownError
)

# ============================================================================
# ENEMY DEFINITIONS
# ============================================================================

def create_enemy(enemy_type):
    """
    Create an enemy based on type
    
    Example enemy types and stats:
    - goblin: health=50, strength=8, magic=2, xp_reward=25, gold_reward=10
    - orc: health=80, strength=12, magic=5, xp_reward=50, gold_reward=25
    - dragon: health=200, strength=25, magic=15, xp_reward=200, gold_reward=100
    
    Returns: Enemy dictionary
    Raises: InvalidTargetError if enemy_type not recognized
    """
    # TODO: Implement enemy creation
    # Return dictionary with: name, health, max_health, strength, magic, xp_reward, gold_reward
    if enemy_type == "goblin":
        return {
            "name": "Goblin",
            "health": 50,
            "max_health": 50,
            "strength": 8,
            "magic": 2,
            "xp_reward": 25,
            "gold_reward": 10
        }
    elif enemy_type == "orc":
        return {
            "name": "Orc",
            "health": 80,
            "max_health": 80,
            "strength": 12,
            "magic": 5,
            "xp_reward": 50,
            "gold_reward": 25
        }
    elif enemy_type == "dragon":
        return {
            "name": "Dragon",
            "health": 200,
            "max_health": 200,
            "strength": 25,
            "magic": 15,
            "xp_reward": 200,
            "gold_reward": 100
        }
    else:
        raise InvalidTargetError(f"Unknown enemy type: {enemy_type}")
    


def get_random_enemy_for_level(character_level):
    """
    Get an appropriate enemy for character's level
    
    Level 1-2: Goblins
    Level 3-5: Orcs
    Level 6+: Dragons
    
    Returns: Enemy dictionary
    """
    # TODO: Implement level-appropriate enemy selection
    # Use if/elif/else to select enemy type
    # Call create_enemy with appropriate type
    
    if character_level <= 2:
        return create_enemy("goblin")
    elif 3 <= character_level <= 5:
        return create_enemy("orc")
    else:
        return create_enemy("dragon")

# ============================================================================
# COMBAT SYSTEM
# ============================================================================

class SimpleBattle:
    """
    Simple turn-based combat system
    
    Manages combat between character and enemy
    """
    
    def __init__(self, character, enemy):
        """Initialize battle with character and enemy"""
        # TODO: Implement initialization
        # Store character and enemy
        # Set combat_active flag
        # Initialize turn counter
        self.character = character
        self.enemy = enemy
        self.combat_active = True
        self.turn_counter = 0
    
    def start_battle(self):
        """
        Start the combat loop
        
        Returns: Dictionary with battle results:
                {'winner': 'player'|'enemy', 'xp_gained': int, 'gold_gained': int}
        
        Raises: CharacterDeadError if character is already dead
        """
        # TODO: Implement battle loop
        # Check character isn't dead
        # Loop until someone dies
        # Award XP and gold if player wins
        if self.character['health'] <= 0:
            raise CharacterDeadError("Character is dead and cannot fight.")
        while self.combat_active:
            display_combat_stats(self.character, self.enemy)

            # Player chooses an action
            self.player_turn()
            # Check if enemy died
            if self.enemy['health'] <= 0:
                xp = self.enemy['xp_reward']
                gold = self.enemy['gold_reward']
                display_battle_log(f"You defeated the {self.enemy['name']}! Gained {xp} XP and {gold} gold.")
                self.combat_active = False
                return {'winner': 'player', 'xp_gained': xp, 'gold_gained': gold}

            # Enemy takes a turn
            self.enemy_turn()
            # Check if player died
            if self.character['health'] <= 0:
                display_battle_log("You have been defeated!")
                self.combat_active = False
                return {'winner': 'enemy', 'xp_gained': 0, 'gold_gained': 0}
    
    def player_turn(self):
        """
        Handle player's turn
        
        Displays options:
        1. Basic Attack
        2. Special Ability (if available)
        3. Try to Run
        
        Raises: CombatNotActiveError if called outside of battle
        """
        # TODO: Implement player turn
        # Check combat is active
        # Display options
        # Get player choice
        # Execute chosen action
        if self.combat_active == False:
            raise CombatNotActiveError("Cannot take turn, combat is not active.")
        print("\nYour turn! Choose an action:")
        print("1. Basic Attack")
        print("2. Special Ability")
        print("3. Try to Run")
        choice = input("Enter the number of your choice: ")
        if choice == '1':
            damage = self.calculate_damage(self.character, self.enemy)
            self.apply_damage(self.enemy, damage)
            display_battle_log(f"You attack the {self.enemy['name']} for {damage} damage!")
        elif choice == '2':
            result = use_special_ability(self.character, self.enemy)
            display_battle_log(result)
        elif choice == '3':
            escaped = self.attempt_escape()
            if escaped:
                display_battle_log("You successfully escaped the battle!")
            else:
                display_battle_log("Escape failed! The battle continues.")
        else:
            print("Invalid choice. Please select a valid action.")
    
    def enemy_turn(self):
        """
        Handle enemy's turn - simple AI
        
        Enemy always attacks
        
        Raises: CombatNotActiveError if called outside of battle
        """
        # TODO: Implement enemy turn
        # Check combat is active
        # Calculate damage
        # Apply to character
        if self.combat_active == False:
            raise CombatNotActiveError("Cannot take turn, combat is not active.")
        damage = self.calculate_damage(self.enemy, self.character)
        self.apply_damage(self.character, damage)
        display_battle_log(f"The {self.enemy['name']} attacks you for {damage} damage!")

    
    def calculate_damage(self, attacker, defender):
        """
        Calculate damage from attack
        
        Damage formula: attacker['strength'] - (defender['strength'] // 4)
        Minimum damage: 1
        
        Returns: Integer damage amount
        """
        # TODO: Implement damage calculation
        base_damage = attacker['strength'] - (defender['strength'] // 4)
        return max(base_damage, 1) 
    
    def apply_damage(self, target, damage):
        """
        Apply damage to a character or enemy
        
        Reduces health, prevents negative health
        """
        # TODO: Implement damage application
        target['health'] = max(target['health'] - damage, 0)
    
    def check_battle_end(self):
        """
        Check if battle is over
        
        Returns: 'player' if enemy dead, 'enemy' if character dead, None if ongoing
        """
        # TODO: Implement battle end check
        if self.enemy['health'] <= 0:
            return 'player'
        elif self.character['health'] <= 0:
            return 'enemy'
        else:
            return None
    
    def attempt_escape(self):
        """
        Try to escape from battle
        
        50% success chance
        
        Returns: True if escaped, False if failed
        """
        # TODO: Implement escape attempt
        # Use random number or simple calculation
        # If successful, set combat_active to False
        import random
        if random.random() < 0.5:
            self.combat_active = False
            return True
        else:
            return False

# ============================================================================
# SPECIAL ABILITIES
# ============================================================================

def use_special_ability(character, enemy):
    """
    Use character's class-specific special ability
    
    Example abilities by class:
    - Warrior: Power Strike (2x strength damage)
    - Mage: Fireball (2x magic damage)
    - Rogue: Critical Strike (3x strength damage, 50% chance)
    - Cleric: Heal (restore 30 health)
    
    Returns: String describing what happened
    Raises: AbilityOnCooldownError if ability was used recently
    """
    # TODO: Implement special abilities
    # Check character class
    # Execute appropriate ability
    # Track cooldowns (optional advanced feature)
    char_class = character.get('class')
    if char_class == "Warrior":
        warrior_power_strike(character, enemy)
        return f"{character['name']} uses Power Strike!"
    elif char_class == "Mage":
        mage_fireball(character, enemy)
        return f"{character['name']} casts Fireball!"
    elif char_class == "Rogue":
        rogue_critical_strike(character, enemy)
        return f"{character['name']} attempts a Critical Strike!"
    elif char_class == "Cleric":
        cleric_heal(character)
        return f"{character['name']} casts Heal!"
    else:
        return "No special ability available."

def warrior_power_strike(character, enemy):
    """Warrior special ability"""
    # TODO: Implement power strike
    # Double strength damage
    damage = character['strength'] * 2 
    enemy['health'] = enemy['health'] - damage
    if enemy['health'] < 0:
        enemy['health'] = 0
    return damage

def mage_fireball(character, enemy):
    """Mage special ability"""
    # TODO: Implement fireball
    # Double magic damage
    damage = character['magic'] * 2
    enemy['health'] = enemy['health'] - damage
    if enemy['health'] < 0:
        enemy['health'] = 0
    return damage

def rogue_critical_strike(character, enemy):
    """Rogue special ability"""
    # TODO: Implement critical strike
    # 50% chance for triple damage
    import random
    if random.random() < 0.5:
        damage = character['strength'] * 3
    else:
        damage = character['strength']
    enemy['health'] = enemy['health'] - damage
    if enemy['health'] < 0:
        enemy['health'] = 0
    return damage

def cleric_heal(character):
    """Cleric special ability"""
    # TODO: Implement healing
    # Restore 30 HP (not exceeding max_health)
    heal_amount = 30
    if character['health'] + heal_amount > character['max_health']:
        character['health'] = character['max_health']
    else:
        character['health'] += heal_amount
    return heal_amount

# ============================================================================
# COMBAT UTILITIES
# ============================================================================

def can_character_fight(character):
    """
    Check if character is in condition to fight
    
    Returns: True if health > 0 and not in battle
    """
    # TODO: Implement fight check
    return character['health'] > 0

def get_victory_rewards(enemy):
    """
    Calculate rewards for defeating enemy
    
    Returns: Dictionary with 'xp' and 'gold'
    """
    # TODO: Implement reward calculation
    return {
        'xp': enemy['xp_reward'],
        'gold': enemy['gold_reward']
    }

def display_combat_stats(character, enemy):
    """
    Display current combat status
    
    Shows both character and enemy health/stats
    """
    # TODO: Implement status display
    print(f"\n{character['name']}: HP={character['health']}/{character['max_health']}")
    print(f"{enemy['name']}: HP={enemy['health']}/{enemy['max_health']}")
    pass

def display_battle_log(message):
    """
    Display a formatted battle message
    """
    # TODO: Implement battle log display
    print(f">>> {message}")
    pass

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== COMBAT SYSTEM TEST ===")
    
    # Test enemy creation
    # try:
    #     goblin = create_enemy("goblin")
    #     print(f"Created {goblin['name']}")
    # except InvalidTargetError as e:
    #     print(f"Invalid enemy: {e}")
    try:
        goblin = create_enemy("goblin")
        print(f"Created {goblin['name']}")
    except InvalidTargetError as e:
        print(f"Invalid enemy: {e}")

    
    # Test battle
    # test_char = {
    #     'name': 'Hero',
    #     'class': 'Warrior',
    #     'health': 120,
    #     'max_health': 120,
    #     'strength': 15,
    #     'magic': 5
    # }
    #
    # battle = SimpleBattle(test_char, goblin)
    # try:
    #     result = battle.start_battle()
    #     print(f"Battle result: {result}")
    # except CharacterDeadError:
    #     print("Character is dead!")
    test_char = {
        'name': 'Hero',
        'class': 'Warrior',
        'health': 120,
        'max_health': 120,
        'strength': 15,
        'magic': 5
    }
    
    battle = SimpleBattle(test_char, goblin)
    try:
        result = battle.start_battle()
        print(f"Battle result: {result}")
    except CharacterDeadError:
        print("Character is dead!")


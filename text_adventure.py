# Authors: Kahekili Spears, Woody Churchward, & Jack O'Brien
# Date Created: 9/24/26
# Date Modified: 9/25/26
# Purpose: To create a fun text adventure game
import time
import random
player = ""
player_hp = 20
player_evasion = 15 #15% chance to dodge the attack
enemies = [
    {"name": "goblin", "hp": 3, "damage": 1, "evasion": 30},
    {"name": "goblin", "hp": 3, "damage": 1, "evasion": 30},
    {"name": "orc", "hp": 8, "damage": 3, "evasion": 10},
]
inventory = [
    {"weapon": "iron sword", "damage": 2}
]

# Code by Claude Code

FILLER = {"the", "a", "an", "to", "at", "on", "my", "toward", "towards",
          "up", "some", "that", "this", "around", "through", "I", "then"}

VERBS = {
    "attack": "attack", "hit": "attack", "fight": "attack", "kill": "attack",
    "strike": "attack", "stab": "attack", "slash": "attack", "punch": "attack",
    "go": "move", "move": "move", "walk": "move", "run": "move",
    "head": "move", "flee": "move",
    "take": "take", "grab": "take", "get": "take", "pick": "take",
    "drop": "drop", "discard": "drop",
    "use": "use", "equip": "use",
    "inventory": "inventory", "inv": "inventory", "i": "inventory",
    "look": "look", "l": "look", "examine": "look", "inspect": "look",
    "help": "help",
    "quit": "quit", "exit": "quit",
}

DIRECTIONS = {
    "n": "north", "north": "north", "s": "south", "south": "south",
    "e": "east", "east": "east", "w": "west", "west": "west",
    "up": "up", "down": "down", "left": "left", "right": "right"
}


def match(names, words):
    """Return the entry in names that the words refer to, or None.
    Handles plurals ('goblins' -> 'goblin') and partial names ('rusty' -> 'rusty sword')."""
    query = " ".join(words)
    options = {query, query.rstrip("s")}
    for name in names:
        low = str(name).lower()
        if any(o and (o in low or low in o) for o in options):
            return name
    return None


def parse(text):
    global enemies
    global inventory
    global player

    result = {"action": None, "target": None, "item": None}

    words = [w.strip(".,!?;:'\"") for w in text.lower().split()]
    words = [w for w in words if w and w not in FILLER]

    if not words:
        return result

    # A bare direction ("north", "n") counts as moving
    if words[0] in DIRECTIONS:
        result["action"], args = "move", words
    elif words[0] in VERBS:
        result["action"], args = VERBS[words[0]], words[1:]
    else:
        return result

    # Split "goblin with sword" into target words and item words
    target_words, item_words = args, []
    for marker in ("with", "using"):
        if marker in args:
            i = args.index(marker)
            target_words, item_words = args[:i], args[i + 1:]
            break

    action = result["action"]
    enemy_names = [e["name"] if isinstance(e, dict) else e for e in enemies]

    if action == "attack":
        if not target_words:
            result["error"] = "no_target"
        else:
            result["target"] = match(enemy_names, target_words)
            if result["target"] is None:
                result["error"] = "unknown_target"
        if item_words:
            result["item"] = match(inventory, item_words)
            if result["item"] is None and result["error"] is None:
                result["error"] = "unknown_item"

    elif action == "move":
        result["target"] = next((DIRECTIONS[w] for w in args if w in DIRECTIONS), None)
        if result["target"] is None:
            result["error"] = "no_target"

    elif action in ("drop", "use"):
        if not args:
            result["error"] = "no_item"
        else:
            result["item"] = match(inventory, args)
            if result["item"] is None:
                result["error"] = "unknown_item"

    elif action == "take":
        if not args:
            result["error"] = "no_item"
        else:
            result["item"] = " ".join(args)  # not in inventory yet, so no matching

    return result

# Kahekili's ppr

def tutorial():
    print("Welcome to the game")
    gameloop("There are two goblins and an orc here.")

def gameloop(prompt):
    global enemies
    global inventory
    global player
    print(prompt)

    while True:
        player_input = input("\nChoose an action: ")
        command = parse(player_input)

        if not command['action']:
            print("I don't understand that command. Try 'attack goblin' or 'quit'.")
            continue

        if command['action'] == 'quit':
            print("Thanks for playing!")
            break

        elif command['action'] == 'attack':
            attack(command)

        elif command['action'] == 'move':
            print("You move " + str(command["target"]))
            # move(command['target'])
# Woody's ppr
def attack(command):
    global enemies
    global player_hp
    global inventory

    target_name = command['target']

    # Locate enemy to attack
    current_enemy = None
    for e in enemies:
        if e["name"] == target_name and e["hp"] > 0:
            current_enemy = e
            break

    if current_enemy is None:
        print(f"There is no living {target_name} here to attack!")
        return

    # Pick players weapon and damage
    weapon_used = command['item']
    player_damage = 1  # Default unarmed damage (punches!)
    weapon_name = "fists"


    if isinstance(weapon_used, dict):
        player_damage = weapon_used.get("damage", 1)
        weapon_name = weapon_used.get("weapon", "weapon")
    elif inventory:
        # Use whatever is in inventory if unclear
        player_damage = inventory[0]["damage"]
        weapon_name = inventory[0]["weapon"]

    print(f"\n--- BATTLE START: Player vs {current_enemy['name'].upper()} ---")

    # Battle keeps looping till something dies
    while current_enemy["hp"] > 0 and player_hp > 0:

        # Players turn
        time.sleep(1)  # Add small delay for stylistic pleasure
        print(f"\nYou attack the {current_enemy['name']} with your {weapon_name}!")
        # Roll a number between 1 and 100. If it's less than or equal to evasion, it's a dodge!
        if random.randint(1, 100) <= current_enemy.get("evasion", 0):
            print(f"The {current_enemy['name']} dodged your attack!")
        else:
            current_enemy["hp"] -= player_damage
            print(f"You dealt {player_damage} damage! The {current_enemy['name']} has {current_enemy['hp']} HP left.")


        # Check if enemy died
        if current_enemy["hp"] <= 0:
            print(f"*** You defeated the {current_enemy['name']}! ***")
            break  # Break out of the battle

        # enemy turn
        time.sleep(1.5)
        print(f"\nThe {current_enemy['name']} attacks you!")
        # Check if the player dodges
        if random.randint(1, 100) <= player_evasion:
            print(f"You dodged the {current_enemy['name']}'s attack!")
        else:
            player_hp -= current_enemy["damage"]
            print(f"It dealt {current_enemy['damage']} damage! You have {player_hp} HP left.")

        # Check if you died
        if player_hp <= 0:
            print("\n*** You have been defeated... GAME OVER ***")
            exit()  # Ends the python thing

        time.sleep(1.5)
        print("-" * 30)

#def attack(command)
    # blah balh bulh ahbul habul hubal howabble bowarb humbug

rooms = {
    "hut": {
        "description": "You are inside your small hut. Your journey begins here.",
        "exits": {"north": "forest_path"}
    },
    "forest_path": {
        "description": "You are on a forest path. Goblins roam nearby.",
        "exits": {
            "south": "hut",
            "north": "guard_outpost",
            "west": "cave",
            "east": "village"
        }
    },
    "cave": {
        "description": "You are inside a dark cave. You can use your torch to see.",
        "exits": {"east": "forest_path"}
    },
    "village": {
        "description": "You are in a village. There is a blacksmith, a potion shop, a tavern, and a general store.",
        "exits": {"west": "forest_path"}
    },
    "guard_outpost": {
        "description": "You are at a guarded outpost. An orc stands watch.",
        "exits": {
            "south": "forest_path",
            "north": "castle"
        }
    },
    "castle": {
        "description": "You have reached Groluth's Castle. Groluth awaits.",
        "exits": {"south": "guard_outpost"}
    }
}

current_room = "hut"

# Jack's ppr
def move(Diection):
    global current_room


gameloop('There are two goblins and an orc')
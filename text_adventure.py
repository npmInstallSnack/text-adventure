# Authors: Kahekili Spears, Woody Churchward, & Jack O'Brien
# Date Created: 9/24/26
# Date Modified: 9/25/26
# Purpose: To create a fun text adventure game

player = ""
enemies = [
    {"name": "goblin", "hp": 3},
    {"name": "goblin", "hp": 3},
    {"name": "orc", "hp": 8},
]
inventory = ["iron sword", "torch"]

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
    gameloop("")
def gameloop(prompt):
    global enemies
    global inventory
    global player
    print(prompt)
    player = input("Choose an action: ")
    command = parse(player)
    print(command)
    if command['action'] == 'attack':
        print("You attack the " + str(command["target"]) + ' with your ' + str(command["item"]))
        #attack(command)
    if command['action'] == 'move':
        print("You move " + str(command["target"]))
        #move(command['target'])
    if command['action'] == 'inventory':
        print("Your inventory:", inventory)

# Woody's ppr

#def attack(command)
    # blah balh bulh ahbul habul hubal howabble bowarb humbug

# Jack's ppr

# def move(command)
# blah balh bulh ahbul habul hubal howabble bowarb humbug

gameloop('There are two goblins and an orc')
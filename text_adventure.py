# Authors: Kahekili Spears, Woody Churchward, & Jack O'Brien
# Date Created: 9/24/26
# Date Modified: 10/13/26
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
   {"name": "groluth", "hp": 20, "damage": 5, "evasion": 50},
]


inventory = [
    {"weapon": "iron sword", "damage": 2},
    {"weapon": "bronze hammer", "damage": 1},
]
food =[
    {"food": "apple", "heal": 3},
    {"food": "health potion", "heal": 6},
]


# Code by Claude Code


FILLER = {"the", "a", "an", "to", "at", "on", "my", "toward", "towards",
         "up", "some", "that", "this", "around", "through", "I", "then"}


VERBS = {
   "attack": "attack", "hit": "attack", "fight": "attack", "kill": "attack",
   "strike": "attack", "stab": "attack", "slash": "attack", "punch": "attack",
   "go": "move", "move": "move", "walk": "move", "run": "move",
   "head": "move", "flee": "move",
   "drop": "drop", "discard": "drop",
    "eat": "eat", "drink": "eat", "use": "eat", "consume": "eat",
   "inventory": "inventory", "inv": "inventory", "i": "inventory",
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


   result = {"action": None, "target": None, "item": None, "error": None}


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
   elif action == "drop":
       if not args:
           result["error"] = "no_item"
       else:
           result["item"] = match(inventory, args)
           if result["item"] is None:
               result["error"] = "unknown_item"
   elif action == "eat":
       if not args:
           result["error"] = "no_item"
       else:
           names = [i["food"] for i in food]
           found = match(names, args)
           if found is None:
               result["error"] = "unknown_item"
           else:
               result["item"] = food[names.index(found)]

   return result
# Rooms code
rooms = {
   "hut": {
       "description": "You are inside your small hut. The door leads North.",
       "exits": {"north": "forest_path"}
   },
   "forest_path": {
       "description": "You are on a forest path. Goblins roam nearby. The path branches in all directions.",
       "exits": {
           "south": "hut",
           "north": "guard_outpost",
           "west": "cave",
           "east": "village"
       }
   },
   "cave": {
       "description": "You are inside a dark cave. You can use your torch to see. The forest path lies East.",
       "exits": {"east": "forest_path"}
   },
   "village": {
       "description": "You are in a village. It is bustling with life. It connects with the path to the west.",
       "exits": {"west": "forest_path"}
   },
   "guard_outpost": {
       "description": "You are at a guarded outpost. An orc stands watch. The path lies back south, and a stone road leads North.",
       "exits": {
           "south": "forest_path",
           "north": "castle"
       }
   },
   "castle": {
       "description": "At the end of the road is Groluth's Castle. Groluth awaits. To the south is a guarded outpost.",
       "exits": {"south": "guard_outpost"}
   }
}

current_room = "hut"

# Kahekili's ppr

new_room = False

def tutorial():
   print("You are inside your small hut. Your journey begins here. There is a path leading north.")
   gameloop()

def gameloop():
   global enemies
   global inventory
   global player
   global current_room
   global rooms
   global new_room
   global food
   global player_hp

   while True:
       player_input = input("\n(" + str(player_hp) + " HP) Choose an action: ")
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
           move(command['target'])
       elif command['action'] == 'drop':
           if command['item'] is None:
               print("You don't have that.")
           else:
               print("You drop your " + command['item']['weapon'])
               inventory.remove(command['item'])
       elif command['action'] == 'inventory':
           print("You have " + str(len(inventory)) + " weapons:")
           for weapon in inventory:
               print(f"- {weapon['weapon']} (damage {weapon['damage']})")
           print("You have " + str(len(food)) + " consumables:")
           for item in food:
               print(f"- {item['food']} (heals {item['heal']} HP)")
       elif command['action'] == 'eat':
           if command['item'] is None:
               print("You don't have that.")
           else:
               print("You consume your " + command["item"]["food"] + ", healing " + str(command["item"]["heal"]) + " HP.")
               player_hp += command["item"]["heal"]
               food.remove(command["item"])

# Jack's ppr
def move(direction):
   global new_room
   global current_room
   exits = rooms[current_room]["exits"]
   if direction in exits:
       current_room = exits[direction]
       print(rooms[current_room]["description"])
       new_room = True
   else:
       print("You can't go that way")


#restart
def restart():
   global player_hp, enemies, inventory, current_room, food


   player_hp = 20
   enemies = [
       {"name": "goblin", "hp": 3, "damage": 1, "evasion": 30},
       {"name": "goblin", "hp": 3, "damage": 1, "evasion": 30},
       {"name": "orc", "hp": 8, "damage": 3, "evasion": 10},
   ]

   inventory = [
       {"weapon": "iron sword", "damage": 2},
       {"weapon": "bronze hammer", "damage": 1},
   ]
   food = [
       {"food": "apple", "heal": 3},
       {"food": "health potion", "heal": 6},
   ]
   current_room = "hut"


   print("Your adventure has restarted!")


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
   player_damage = 1  # Default damages, no weapon
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
           current_enemy["hp"] = int(current_enemy["hp"]) - int(player_damage)
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
           restart()  # Ends the python thing


       time.sleep(1.5)
       print("-" * 30)

# Start the game
tutorial()
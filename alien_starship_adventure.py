#!/usr/bin/env python3
"""
Alien Starship Adventure Game
A text-based adventure game set on an abandoned alien starship.
The player must find escape pods before oxygen runs out.
"""

import random
import time

class Room:
    def __init__(self, name, description, items=None, exits=None, requires_item=None):
        self.name = name
        self.description = description
        self.items = items or []
        self.exits = exits or {}
        self.requires_item = requires_item
        self.visited = False

class Player:
    def __init__(self):
        self.inventory = []
        self.current_room = "airlock"
        self.oxygen = 100
        self.alive = True
        self.escaped = False

class Game:
    def __init__(self):
        self.player = Player()
        self.rooms = self.create_rooms()
        self.commands = {
            'look': self.look,
            'l': self.look,
            'go': self.go,
            'take': self.take,
            'get': self.take,
            'inventory': self.inventory,
            'i': self.inventory,
            'use': self.use,
            'help': self.help,
            'quit': self.quit
        }

    def create_rooms(self):
        rooms = {}
        
        # Level 1 - Lower Deck (10 rooms)
        rooms["airlock"] = Room(
            "Airlock Chamber",
            "Emergency lights cast eerie red shadows across corroded metal walls. The outer door is sealed shut, but an inner passage leads deeper into the vessel. Strange symbols pulse weakly on a control panel.",
            items=["emergency_beacon"],
            exits={"north": "corridor1"}
        )
        
        rooms["corridor1"] = Room(
            "Lower Corridor",
            "A narrow passage stretches before you, lined with bio-luminescent strips that flicker sporadically. The air tastes metallic. Dark stains mar the floor plates.",
            exits={"south": "airlock", "north": "storage1", "east": "maintenance", "west": "crew_quarters1"}
        )
        
        rooms["storage1"] = Room(
            "Storage Bay Alpha",
            "Towering alien containers line the walls, their surfaces covered in intricate patterns. Most are empty, but strange residues hint at their former contents.",
            items=["plasma_cell"],
            exits={"south": "corridor1", "east": "storage2"}
        )
        
        rooms["storage2"] = Room(
            "Storage Bay Beta",
            "More containers here, but these are cracked and leaking an iridescent fluid that pools on the deck. The smell is overwhelming - sweet yet nauseating.",
            items=["containment_suit"],
            exits={"west": "storage1", "north": "laboratory"}
        )
        
        rooms["laboratory"] = Room(
            "Alien Laboratory",
            "Twisted spires of crystalline equipment rise from hexagonal workstations. Specimen tanks contain floating, unidentifiable forms. A terminal flickers with alien script.",
            items=["research_data", "bio_scanner"],
            exits={"south": "storage2", "east": "specimen_hold"}
        )
        
        rooms["specimen_hold"] = Room(
            "Specimen Containment",
            "Rows of cylindrical chambers line the walls, most shattered from within. Claw marks score the metal. Whatever was held here is long gone.",
            items=["security_override"],
            exits={"west": "laboratory"}
        )
        
        rooms["maintenance"] = Room(
            "Maintenance Bay",
            "A maze of pipes and conduits snake through this cramped space. Tool racks hold implements of unknown purpose. A maintenance shaft leads upward.",
            items=["maintenance_key", "repair_kit"],
            exits={"west": "corridor1", "up": "engineering"}
        )
        
        rooms["crew_quarters1"] = Room(
            "Crew Quarters Alpha",
            "Personal chambers with sleeping alcoves sized for beings much larger than humans. Personal effects lie scattered - crystalline ornaments and metallic clothing.",
            items=["personal_log"],
            exits={"east": "corridor1", "north": "crew_quarters2"}
        )
        
        rooms["crew_quarters2"] = Room(
            "Crew Quarters Beta",
            "More living spaces, but these show signs of struggle. Furniture is overturned, and deep gouges mark the walls. A sense of dread permeates the air.",
            items=["crew_id_card"],
            exits={"south": "crew_quarters1", "north": "mess_hall"}
        )
        
        rooms["mess_hall"] = Room(
            "Mess Hall",
            "A communal eating area with tables designed for non-human anatomy. Food dispensers hang open, their contents long since spoiled or crystallized.",
            items=["nutrient_pack"],
            exits={"south": "crew_quarters2"}
        )
        
        # Level 2 - Main Deck (10 rooms)
        rooms["engineering"] = Room(
            "Engineering Section",
            "Massive alien machinery hums with residual power. Conduits pulse with bioluminescent energy. The air shimmers with heat from the reactor core.",
            items=["power_core"],
            exits={"down": "maintenance", "north": "reactor_core", "east": "turbolift_lower"},
            requires_item="maintenance_key"
        )
        
        rooms["reactor_core"] = Room(
            "Reactor Core Chamber",
            "The heart of the ship - a swirling vortex of energy contained within crystalline matrices. The power here could destroy or save you.",
            items=["master_key"],
            exits={"south": "engineering", "east": "power_distribution"}
        )
        
        rooms["power_distribution"] = Room(
            "Power Distribution Hub",
            "A web of energy conduits converge here, routing power throughout the vessel. Control interfaces glow with alien symbols.",
            items=["power_regulator"],
            exits={"west": "reactor_core", "north": "main_corridor"}
        )
        
        rooms["main_corridor"] = Room(
            "Main Corridor",
            "The primary thoroughfare of the vessel, wide enough for large beings to pass. Viewports show the desolate planet below, its surface scarred and lifeless.",
            exits={"south": "power_distribution", "north": "bridge_access", "east": "observation", "west": "computer_core"}
        )
        
        rooms["bridge_access"] = Room(
            "Bridge Access",
            "A security checkpoint blocks access to the bridge. Multiple scanning devices and blast doors suggest this area was heavily protected.",
            exits={"south": "main_corridor", "north": "bridge"},
            requires_item="crew_id_card"
        )
        
        rooms["bridge"] = Room(
            "Command Bridge",
            "The nerve center of the starship, with command stations arranged in a circle around a holographic display showing star charts of unknown space.",
            items=["navigation_data", "captain_log"],
            exits={"south": "bridge_access"}
        )
        
        rooms["observation"] = Room(
            "Observation Deck",
            "Panoramic windows reveal the void of space and the dying planet below. Comfortable seating designed for contemplating the cosmos.",
            items=["stellar_charts"],
            exits={"west": "main_corridor", "north": "communications"}
        )
        
        rooms["communications"] = Room(
            "Communications Array",
            "Banks of communication equipment line the walls. Multiple screens show static from across the galaxy. Emergency broadcasts loop endlessly.",
            items=["distress_beacon"],
            exits={"south": "observation"}
        )
        
        rooms["computer_core"] = Room(
            "Computer Core",
            "Towering data storage units stretch to the ceiling, their surfaces alive with flowing patterns of light. The ship's AI once resided here.",
            items=["ai_fragment", "deck_plans"],
            exits={"east": "main_corridor", "north": "security_station"}
        )
        
        rooms["security_station"] = Room(
            "Security Control",
            "Monitoring stations overlook the entire ship. Weapon lockers stand empty. Security protocols still function, sealing critical areas.",
            items=["security_codes"],
            exits={"south": "computer_core"}
        )
        
        rooms["turbolift_lower"] = Room(
            "Turbolift Lower Access",
            "A vertical transport chamber with alien controls. The lift appears functional but requires proper authorization to operate.",
            exits={"west": "engineering", "up": "turbolift_upper"},
            requires_item="power_core"
        )
        
        # Level 3 - Upper Deck (10 rooms)
        rooms["turbolift_upper"] = Room(
            "Turbolift Upper Access",
            "The turbolift opens onto the upper deck. The architecture here is more ornate, suggesting areas reserved for high-ranking crew members.",
            exits={"down": "turbolift_lower", "north": "upper_corridor"}
        )
        
        rooms["upper_corridor"] = Room(
            "Upper Deck Corridor",
            "An elegant passageway with decorative panels depicting alien constellations. The materials here are finer, with inlaid precious metals.",
            exits={"south": "turbolift_upper", "north": "captain_quarters", "east": "officer_quarters", "west": "conference_room"}
        )
        
        rooms["captain_quarters"] = Room(
            "Captain's Quarters",
            "Luxurious personal chambers with artifacts from across the galaxy. A massive viewport dominates one wall. Personal logs are scattered about.",
            items=["captain_keycard", "star_map"],
            exits={"south": "upper_corridor"}
        )
        
        rooms["officer_quarters"] = Room(
            "Officer Quarters",
            "Living spaces for the ship's senior staff. Each chamber reflects different alien cultures, suggesting a diverse crew complement.",
            items=["officer_manual"],
            exits={"west": "upper_corridor", "north": "tactical_center"}
        )
        
        rooms["tactical_center"] = Room(
            "Tactical Operations",
            "War room with holographic battle displays. Weapon control systems and defensive matrices are still operational but locked down.",
            items=["weapon_codes"],
            exits={"south": "officer_quarters", "east": "armory"}
        )
        
        rooms["armory"] = Room(
            "Weapons Armory",
            "Racks of exotic weapons line the walls. Energy cells glow ominously. Most weapons are depleted, but some still hold a charge.",
            items=["plasma_rifle", "energy_cells"],
            exits={"west": "tactical_center"}
        )
        
        rooms["conference_room"] = Room(
            "Conference Chamber",
            "A circular meeting space with seating for multiple species. Holographic projectors display the last meeting's agenda - an evacuation plan.",
            items=["evacuation_plan"],
            exits={"east": "upper_corridor", "north": "medical_bay"}
        )
        
        rooms["medical_bay"] = Room(
            "Medical Facility",
            "Advanced alien medical equipment fills this sterile chamber. Bio-beds are sized for various anatomies. Medical logs detail a mysterious plague.",
            items=["medical_kit", "plague_data"],
            exits={"south": "conference_room", "east": "quarantine"}
        )
        
        rooms["quarantine"] = Room(
            "Quarantine Section",
            "Sealed chambers once held infected crew members. Warning symbols glow red. The air recycling system here has been permanently disabled.",
            items=["contamination_scanner"],
            exits={"west": "medical_bay", "north": "escape_pods"}
        )
        
        rooms["escape_pods"] = Room(
            "Escape Pod Bay",
            "Salvation at last! Multiple escape pods line the launch bay. Most are damaged, but one pod shows green status lights. Your way home awaits.",
            items=["escape_pod"],
            exits={"south": "quarantine"}
        )
        
        return rooms

    def look(self, args=None):
        room = self.rooms[self.player.current_room]
        print(f"\n=== {room.name} ===")
        print(room.description)
        
        if room.items:
            print(f"\nYou see: {', '.join(room.items)}")
        
        exits = list(room.exits.keys())
        if exits:
            print(f"Exits: {', '.join(exits)}")
        
        if not room.visited:
            room.visited = True
            self.player.oxygen -= 2
            print(f"[Oxygen: {self.player.oxygen}%]")

    def go(self, direction):
        if not direction:
            print("Go where?")
            return
        
        room = self.rooms[self.player.current_room]
        direction = direction.lower()
        
        if direction not in room.exits:
            print("You can't go that way.")
            return
        
        next_room = room.exits[direction]
        next_room_obj = self.rooms[next_room]
        
        if next_room_obj.requires_item and next_room_obj.requires_item not in self.player.inventory:
            item_name = next_room_obj.requires_item.replace('_', ' ')
            print(f"You need a {item_name} to access this area.")
            return
        
        self.player.current_room = next_room
        self.player.oxygen -= 3
        print(f"[Oxygen: {self.player.oxygen}%]")
        self.look()

    def take(self, item):
        if not item:
            print("Take what?")
            return
        
        room = self.rooms[self.player.current_room]
        
        if item == "escape_pod":
            if self.player.current_room == "escape_pods":
                print("\n" + "="*50)
                print("SUCCESS! You've reached the escape pods!")
                print("You activate the pod's systems and launch toward")
                print("the planet's surface. You've survived the alien")
                print("starship and live to tell the tale!")
                print("="*50)
                self.player.escaped = True
                return
            else:
                print("There's no escape pod here.")
                return
        
        if item in room.items:
            room.items.remove(item)
            self.player.inventory.append(item)
            item_name = item.replace('_', ' ')
            print(f"You take the {item_name}.")
            self.player.oxygen -= 1
        else:
            print("That item isn't here.")

    def inventory(self, args=None):
        if self.player.inventory:
            items = [item.replace('_', ' ') for item in self.player.inventory]
            print(f"You are carrying: {', '.join(items)}")
        else:
            print("You aren't carrying anything.")

    def use(self, item):
        if not item:
            print("Use what?")
            return
        
        if item not in self.player.inventory:
            print("You don't have that item.")
            return
        
        print(f"You use the {item.replace('_', ' ')}.")
        
    def help(self, args=None):
        print("\nAvailable commands:")
        print("look/l - examine your surroundings")
        print("go <direction> - move in a direction")
        print("take/get <item> - pick up an item")
        print("inventory/i - check your inventory")
        print("use <item> - use an item")
        print("help - show this help")
        print("quit - exit the game")

    def quit(self, args=None):
        print("Thanks for playing!")
        self.player.alive = False

    def check_oxygen(self):
        if self.player.oxygen <= 0:
            print("\n" + "="*50)
            print("GAME OVER!")
            print("Your oxygen has run out. You collapse in the")
            print("dark corridors of the alien starship, another")
            print("victim of this cursed vessel.")
            print("="*50)
            self.player.alive = False
            return False
        elif self.player.oxygen <= 20:
            print("\n[WARNING: Oxygen critically low!]")
        elif self.player.oxygen <= 40:
            print("\n[WARNING: Oxygen running low.]")
        
        return True

    def process_command(self, command_line):
        parts = command_line.strip().split()
        if not parts:
            return
        
        command = parts[0].lower()
        args = ' '.join(parts[1:]) if len(parts) > 1 else None
        
        if command in self.commands:
            self.commands[command](args)
        else:
            print("I don't understand that command. Type 'help' for assistance.")

    def intro(self):
        print("="*60)
        print("        ALIEN STARSHIP ADVENTURE")
        print("="*60)
        print("\nYou are an explorer who has discovered a derelict")
        print("alien starship in orbit around a dead planet.")
        print("Your oxygen is limited, and the ship's systems")
        print("are failing. You must find the escape pods")
        print("before your air runs out!")
        print("\nType 'help' for commands, 'look' to examine areas.")
        print("="*60)

    def run(self):
        self.intro()
        self.look()
        
        while self.player.alive and not self.player.escaped:
            if not self.check_oxygen():
                break
            
            try:
                command = input("\n> ").strip()
                if command:
                    self.process_command(command)
            except KeyboardInterrupt:
                print("\nThanks for playing!")
                break
            except EOFError:
                break

if __name__ == "__main__":
    game = Game()
    game.run()

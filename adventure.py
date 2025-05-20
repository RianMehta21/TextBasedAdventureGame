"""CSC111 Project 1: Text Adventure Game - Game Manager

Instructions (READ THIS FIRST!)
===============================

This Python module contains the code for Project 1. Please consult
the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2025 CSC111 Teaching Team
"""

from __future__ import annotations
import json
from dataclasses import dataclass
from typing import Optional

from python_ta.contracts import check_contracts

from game_entities import Location, Item, Player, Puzzle
from proj1_event_logger import Event, EventList


# Note: You may add in other import statements here as needed

# Note: You may add helper functions, classes, etc. below as needed

@check_contracts
class AdventureGame:
    """A text adventure game class storing all location, item and map data.

    Instance Attributes:
        - locations: a mapping from location id to Location object, representing all location in the game.
        - items: a mapping of item names to Item objects, representing all items in the game.
        - puzzles: a mapping of location id to any Puzzle object that is located at that location
        - current_location_id: the ID of the location the game is currently in
        - ongiong: True if the game is still being played and False if the game has ended


    Representation Invariants:
        - all(id > 0 for id in self.locations)
        - all item names should be valid items in the game data file
        - all(id in self.locations for id in self.puzzles)
        - len(self.locations) > 0
        - len(self.items) > 0
        - self.current_location_id in self.locations
    """

    locations: dict[int, Location]
    items: dict[str, Item]
    puzzles: dict[int, Puzzle]
    current_location_id: int
    ongoing: bool

    def __init__(self, game_data_file: str, initial_location_id: int) -> None:
        """
        Initialize a new text adventure game, based on the data in the given file, setting starting location of game
        at the given initial location ID.
        (note: you are allowed to modify the format of the file as you see fit)

        Preconditions:
        - game_data_file is the filename of a valid game data JSON file
        - initial_location_id in self.locations
        """
        # Loads location, item, and puzzle information from data file
        self.locations, self.items, self.puzzles = self._load_game_data(game_data_file)

        self.current_location_id = initial_location_id
        self.ongoing = True

    @staticmethod
    def _load_game_data(filename: str) -> tuple[dict[int, Location], dict[str, Item], dict[int, Puzzle]]:
        """Load locations and items from a JSON file with the given filename and
        return a tuple consisting of (1) a dictionary of locations mapping each game location's ID to a Location object,
        and (2) a list of all Item objects.

        Preconditions:
        - filename is a valid game data JSON file
        """

        with open(filename, 'r') as f:
            data = json.load(f)  # This loads all the data from the JSON file

        # adds location data, mapping id to Location
        locations = {}
        for loc_data in data['locations']:  # Go through each element associated with the 'locations' key in the file
            location_obj = Location(loc_data['id'], loc_data['name'], loc_data['brief_description'],
                                    loc_data['long_description'], loc_data['available_commands'],
                                    loc_data['items'])
            locations[loc_data['id']] = location_obj

        # adds item data, mapping item name to Item
        items = {}
        for item_data in data['items']:
            item_obj = Item(item_data['name'], item_data['start_position'],
                            item_data['start_position'],
                            item_data['target_position'], item_data['target_points'])
            items[item_data['name']] = item_obj

        # adds puzzle data, mapping id to Puzzle
        puzzles = {}
        for puzzle_data in data["puzzles"]:
            puzzle_obj = Puzzle(puzzle_data["location_id"], puzzle_data["setup"], puzzle_data["finish"],
                                puzzle_data["puzzle"], puzzle_data["points"], False, puzzle_data["reject"])
            puzzles[puzzle_data['location_id']] = puzzle_obj

        return locations, items, puzzles

    def get_location(self, loc_id: Optional[int] = None) -> Location:
        """Return Location object associated with the provided location ID.
        If no ID is provided, return the Location object associated with the current location.

        Preconditions:
        - loc_id in self.locations

        >>> adventure_game = AdventureGame('game_data.json',2)
        >>> brief_description = "You are at Goldring, you can see varsity athletes playing basketball and volleyball."
        >>> long_description = "You hear the sounds of sneakers squeaking and weights clanking.\\nThe library and the Mining Building where you had your test the day before are nearby."
        >>> available_commands = {"go south" : 1, "go west" : 3}
        >>> items = ["water_bottle"]
        >>> adventure_game.get_location() == Location(2,'Goldring Gym', brief_description,long_description,available_commands,items)
        True
        """
        if loc_id is None:
            return self.locations[self.current_location_id]
        else:
            return self.locations[loc_id]


@dataclass
class Commands:
    """Handles all player commands
    """
    player: Player
    adventure_game: AdventureGame
    event_list: EventList

    def puzzle_loop(self, puzzle: Puzzle, location_id: int) -> str:
        """Helper function for give_puzzle() that performs the main checking if the user input is the correct answer
        and updating the game log, player's items, and printing things accordingly
        """
        while not puzzle.completed:
            if __name__ != "__main__":
                # To check if this code is being run by the simulation, sets answer to the correct one
                answer = puzzle.puzzle[1]
            else:
                answer = input("\nWhat is your answer (or type quit to exit) : ").strip().lower()

            if answer == "quit":
                return puzzle.reject
            elif answer == puzzle.puzzle[1]:  # puzzle.puzzle[1] is the answer
                puzzle.completed = True
                item_name = puzzle.puzzle[2]
                self.player.items.append(item_name)
                self.adventure_game.items[item_name].current_position = -1
                self.player.moves -= 1
                self.event_list.add_event(Event(location_id, self.adventure_game.get_location().name,
                                                description=self.adventure_game.get_location(
                                                    location_id).long_description), 'Solved puzzle')
                return puzzle.finish
            else:
                print("Thats wrong")
        return ''

    def give_puzzle(self) -> None:
        """Prints the puzzle and asks the player if they accept or not and reacts accordingly
        """
        location_id = self.adventure_game.current_location_id
        puzzle = self.adventure_game.puzzles[location_id]
        print(puzzle.setup)

        while True:
            if __name__ != "__main__":  # To check if this code is being run by the simulation
                accept = 'yes'
            else:
                accept = input("Do you accept: ").lower().strip()

            if accept == 'yes':
                print(puzzle.puzzle[0])
                print(self.puzzle_loop(puzzle, location_id))
                break
            elif accept == 'no':
                print(puzzle.reject)
                break
            else:
                print("Invalid input. Please type in yes or no")

    def get_score(self) -> list[int]:
        """Returns a list of the player's score where the first value is the points based on items
        in their target location, the second value is the points based on puzzles completed, and the third value
        is the points based on moves left
        >>> events = EventList()
        >>> test_game = AdventureGame('game_data.json',4)
        >>> player1 = Player(12,2,[])
        >>> test_game.puzzles[4].completed = True
        >>> command = Commands(player1,test_game,events)
        >>> command.get_score()
        [0, 50, 120]
        """
        # checks if current location of item is equal to target position and then sums the points
        curr_item_points = sum([self.adventure_game.items[item].target_points for item in self.adventure_game.items
                                if
                                self.adventure_game.items[item].current_position == self.adventure_game.items[
                                    item].target_position])

        # checks if puzzle is completed and then sums the points
        curr_puzzle_points = sum([self.adventure_game.puzzles[puzzle].points for puzzle in self.adventure_game.puzzles
                                  if self.adventure_game.puzzles[puzzle].completed])
        return [curr_item_points, curr_puzzle_points, self.player.moves * 10]  # 10 points for each move left

    def calculate_time(self) -> str:
        """Calculates and returns the current time and how much time left
        before the game ends at 4:00 PM based on the amount of player moves left
        >>> events = EventList()
        >>> test_game = AdventureGame('game_data.json',4)
        >>> player1 = Player(8,2,[])
        >>> test_game.puzzles[4].completed = True
        >>> command = Commands(player1,test_game,events)
        >>> command.calculate_time()
        'It is currently 2:40 PM. You have 1 hour 20 minutes left before your assignment is due. '
        """

        # helper variables to do the math for f'string
        remaining_minutes = self.player.moves * 10
        hours_left = remaining_minutes // 60
        minutes_left = remaining_minutes % 60
        time_hour = 16 - hours_left - int(minutes_left > 0)  # 16 since it is 4:00 PM
        time_minute = f"{(60 - minutes_left) % 60:02d}"
        am_pm = "PM" if time_hour >= 12 else "AM"

        # returns a formtted time display, with current time, and time left before submission
        return (f'It is currently {12 if time_hour % 12 == 0 else time_hour % 12}:{time_minute} {am_pm}. '
                f'You have{' ' + str(hours_left) + " hour" if hours_left > 0 else ''}{'s' if hours_left > 1 else ''}'
                f'{' ' + str(minutes_left) + " minute" if minutes_left > 0 else ''}{'s' if minutes_left > 1 else ''} '
                f'left before your assignment is due. ')

    def drop(self, item_name: str) -> None:
        """if item is in the player's inventory, it is removed and added to the list of items as the current location.
        The list of all items is updated to reflect the current location ID of the item
        >>> events = EventList()
        >>> test_game = AdventureGame('game_data.json',5)
        >>> player1 = Player(10,2,['money'])
        >>> command = Commands(player1,test_game,events)
        >>> command.drop("money")
        >>> player1.moves == 9
        True
        >>> 'money' in player1.items
        False
        >>> events.last.item_action == ('dropped','money')
        True
        >>> test_game.items["money"].current_position
        5
        """
        location = self.adventure_game.get_location()
        if item_name in self.player.items:  # checks if player has the item
            self.player.items.remove(item_name)
            location.items.append(item_name)
            self.event_list.add_event(Event(location.id_num, location.name, ('dropped', item_name),
                                            location.long_description), f'Drop {item_name}')
            self.adventure_game.items[item_name].current_position = location.id_num
            self.player.moves -= 1
        else:
            print("You don't own that item")

    def take(self, item_name: str) -> None:
        """if item is at the current location, it is removed from the list of items at the current location
        and added to the player's items
        >>> events = EventList()
        >>> test_game = AdventureGame('game_data.json',6)
        >>> player1 = Player(10,2,[])
        >>> command = Commands(player1,test_game,events)
        >>> command.take("lucky_mug")
        >>> player1.moves == 9
        True
        >>> 'lucky_mug' in player1.items
        True
        >>> events.last.item_action == ('took','lucky_mug')
        True
        >>> test_game.items['lucky_mug'].current_position
        -1
        """
        location = self.adventure_game.get_location()
        if item_name in location.items:  # checks if item is available for pick up at position
            self.player.items.append(item_name)
            location.items.remove(item_name)
            self.event_list.add_event(
                Event(location.id_num, location.name, ('took', item_name),
                      location.long_description), f'Take {item_name}')
            self.adventure_game.items[item_name].current_position = -1
            self.player.moves -= 1
        else:
            print("This item doesn't not exist at " + location.name)

    def undo(self) -> None:
        """Handles undoing last action performed by player. If the most recent action doesn't involve an item it removes
        it. If the last action involves taking or dropping an item, it reverses it accordingly
        >>> events = EventList()
        >>> test_game = AdventureGame('game_data.json',5)
        >>> player1 = Player(10,2,["lucky_mug"])
        >>> command = Commands(player1,test_game,events)
        >>> command.drop('lucky_mug')
        >>> command.undo()
        >>> player1.moves == 10
        True
        >>> "lucky_mug" in player1.items
        True
        >>> events.display_events() == ''
        True
        >>> command.drop("lucky_mug")
        >>> command.take("lucky_mug")
        >>> command.undo()
        >>> player1.moves
        9
        >>> 'lucky_mug' in test_game.get_location().items
        True
        >>> events.last == Event(5,"Queen's Park",("dropped",'lucky_mug'),test_game.get_location(5).long_description, None)
        True
        >>> test_game.items['lucky_mug'].current_position
        5
        """
        if self.player.undo > 0:
            if self.event_list.last.item_action is None:  # if the last action is movement related and not take/drop
                self.adventure_game.current_location_id = self.event_list.last.prev.id_num
                self.event_list.remove_last_event()
            else:
                action, item = self.event_list.last.item_action  # action will be take/drop and item will be item_name
                if action == 'took':
                    self.drop(item)
                    self.player.moves += 1
                    self.event_list.remove_last_event()
                    self.event_list.remove_last_event()

                elif action == 'dropped':
                    self.take(item)
                    self.player.moves += 1
                    self.adventure_game.items[item].current_position = self.adventure_game.items[item].start_position
                    self.event_list.remove_last_event()
                    self.event_list.remove_last_event()

            self.player.undo -= 1
            self.player.moves += 1
        else:
            print("Sorry you have no undo's left")

    def set_scene(self) -> str:
        """Set the scene of the current location and lets the player know their choices. Then it takes the player's
        command as an input and formats and then returns it
        """
        menu_list = ["look", "time", "inventory", "score", "undo", "log", "quit", "map"]
        location = self.adventure_game.get_location()

        print(f'Location: {location.id_num} - {location.name}')
        if location.id_num in game_log.get_id_log()[:-1]:
            print(location.brief_description)
        else:
            print(location.long_description)

        # Display possible actions at this location
        print(f"What to do? Choose from: {menu_list}")
        print("At this location, you can also:")
        for available_command in location.available_commands:
            print("-", available_command)

        # Validate choice
        choice = input("\nEnter action: ").lower().strip()
        while (choice not in location.available_commands and choice not in menu_list
               and ('take' not in choice and 'drop' not in choice)):
            print("That was an invalid option; try again.")
            choice = input("\nEnter action: ").lower().strip()
        return choice

    def map(self) -> None:
        """Helper function for menu_action that prints out a map of the game if the player is carrying a map
        """
        if "map" in self.player.items:
            print("""
        7  6
           5
    10  9  4  3  2
           8     1""")

        else:
            print("You don't have a map")

    def menu_action(self, choice: str) -> None:
        """Handles all menu commands
        """
        location = self.adventure_game.get_location()
        if choice == 'map':
            self.map()
        elif choice == "log":
            print(self.event_list.display_events().strip())
        elif choice == 'look':
            print(location.long_description)
        elif choice == "time":
            print(self.calculate_time())
        elif choice == 'inventory':
            print(f'You currently have: {self.player.items}')
            print(f'The current location has: {self.adventure_game.get_location().items}')
        elif choice == 'score':
            print(f'Your current score is: {sum(self.get_score()[0:2])}')
        elif choice == 'undo':
            if len(self.event_list.get_id_log()) > 1:  # checks if there is anything to undo
                if self.event_list.last.prev.next_command == "Solved puzzle":
                    print("Sorry you cannot undo a puzzle")
                else:
                    self.undo()
            else:
                print("There are no events to undo")
        else:
            self.adventure_game.ongoing = False

    def non_menu_action(self, choice: str) -> None:
        """Handles all non-menu commands such as movement and taking and dropping items
        """
        location = self.adventure_game.get_location()
        if choice == "puzzle":
            puzzle = self.adventure_game.puzzles[location.id_num]
            if puzzle.completed:
                print("This puzzle is completed")
            elif location.id_num == 4:
                self.give_puzzle()
            elif location.id_num == 7:
                if all(required in location.items for required in ['lighter', 'unlit_lantern']):
                    self.give_puzzle()
                elif any(required in location.items for required in ['lighter', 'unlit_lantern']):
                    print("Still not bright enough. Maybe there is something else you need? ")
                else:
                    print("You cannot see anything. Maybe use (\"drop\") some items to better see.")

        else:
            if choice == "go into my room" and "keycard" not in self.player.items:
                print("You reach into your pocket and realize you don't have your keycard. "
                      "Where could you have left it?")
            else:
                location = self.adventure_game.get_location(location.available_commands[choice])
                self.event_list.add_event(Event(location.id_num, location.name,
                                                description=location.long_description), choice)
                self.adventure_game.current_location_id = location.id_num
                self.player.moves -= 1

    def give_results(self) -> None:
        """Prints the final points breakdown once the player has completed the game and won.
        """
        item_points, puzzle_points, moves_points = self.get_score()
        print("\n----YOU WON----"
              "\nYou submitted your assignment on time and got a 93, saving your grade and your friendship."
              f"\n\n----Final Stats----\nItem Points: {item_points}\nPuzzle Points: {puzzle_points}"
              f"\nMoves Left Points: {moves_points}\nTotal Points: {item_points + puzzle_points + moves_points}")

    def ask_to_continue(self) -> bool:
        """Helper function for check_game_over that run's if they player has put all three key items in their room,
        but all the puzzles are not copmleted. Function asks the player if they want to continue the game, returning
        True if yes and False if no
        """
        while True:
            continue_game = input(
                "You still have some puzzle's left for bonus points. Do you want to continue? ").strip().lower()
            if continue_game == 'yes':
                self.undo()
                self.player.undo += 1
                break
            elif continue_game == 'no':
                self.give_results()
                return False
            else:
                print("Invalid input. Please type in yes or no")
        return True

    def check_game_over(self) -> bool:
        """Checks if the game is won or if a lose condition is met. Prints the scoring breakdown if game is won and
        returns False if game has ended.
        """
        if self.player.moves == 0:
            print("\n----GAME OVER, YOU LOST----"
                  "\nYou ran out of time, you got a 0 on your assignment and lost your friendship")
            return False
        elif all([winning_item in self.adventure_game.get_location(10).items
                  for winning_item in ['lucky_mug', 'usb', 'laptop_charger']]):
            # checks if puzzles are left to finish. If there are, asks user if they want to finish them
            if all(self.adventure_game.puzzles[puzzle_id].completed for puzzle_id in self.adventure_game.puzzles) \
                    or __name__ != "__main__":  # To check if this code is being run by the simulation
                self.give_results()
                return False
            else:
                # calls helper function that validates userinput asking if they want to continue or not
                return self.ask_to_continue()
        elif 'keycard' in self.adventure_game.get_location(10).items and self.adventure_game.current_location_id != 10:
            print("\n----GAME OVER, YOU LOST----\nYou locked yourself out of your room. ")
            return False

        return True

    def process_choice(self, choice: str) -> None:
        """Processes choice and calls the appropriate helper function to execute the corresponding action
        """
        if choice in ["look", "time", "inventory", "score", "undo", "log", "quit", "map"]:
            self.menu_action(choice)

        elif choice in self.adventure_game.get_location().available_commands:
            self.non_menu_action(choice)
        else:
            input_into_list = choice.split()
            player_action, player_item = input_into_list[0], input_into_list[1]
            player_action.strip().lower()
            player_item.strip().lower()
            if player_action == 'take':
                self.take(player_item)
            elif player_action == 'drop':
                self.drop(player_item)
            else:
                print("If you are trying to drop or take an item. Type drop item_name or take item_name")


if __name__ == "__main__":
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['R1705', 'E9998', 'E9999']
    })
    MOVES = 50
    UNDOS = 2
    current_player = Player(MOVES, UNDOS, [])
    game_log = EventList()
    game = AdventureGame('game_data.json', 4)
    command_handler = Commands(current_player, game, game_log)
    player_choice = None
    game_log.add_event(Event(game.current_location_id, game.get_location().name))

    print(f"""
----HOW TO PLAY----
Objective: bring the required items back to your room to submit your assignment on time. However, along the way, you
           may encounter additional opportunities to earn bonus points.


At every location you can select menu options:
look - shows the long description of the location
time - tells you how much time you have left before submission (each move is 10 minutes). you have {MOVES} moves
inventory - shows what items you are carrying and what items are available to pick up at the current location
score - shows you your current score
undo - you have {UNDOS} undos that will revert any movement or taking/droping of items. you cannot undo a puzzle, so
       nothing before a puzzle can be undone either.
log - shows you the log of all your moves. this includes taking/dropping items, movement, and puzzles solved
quit - ends the game


Other actions:
take item_name - allows you to take an item and add it to your inventory if the item exists at the location
drop item_name - allows you to drop an item at the current location and remove it from your inventory if you currently
                 hold the item
go north/south/east/west - you travel to another room in that direction
puzzle - if there is a puzzle at the location you can interact with it
""")

    print(f"""
----GAME START----
You wake up and look around. You somehow fell asleep on a bench outside {game.get_location().name}.
You look at the time, it is {command_handler.calculate_time()[6:]}
You realize you are missing key things. You need your laptop charger, your lucky UofT Mug, \
and most importantly you need to fix your corrupted USB.
You need to take all these things and put (drop) them in your room before the deadline at 4:00 PM \
otherwise you and your best friend will both get a 0.
You stand up and start your journey...""")

    while game.ongoing:
        # Note: If the loop body is getting too long, you should split the body up into helper functions
        # for better organization. Part of your marks will be based on how well-organized your code is.

        print("\n================================")

        player_choice = command_handler.set_scene()
        command_handler.process_choice(player_choice)
        game.ongoing = command_handler.check_game_over()

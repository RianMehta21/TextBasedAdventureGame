"""CSC111 Project 1: Text Adventure Game - Simulator

Instructions (READ THIS FIRST!)
===============================

This Python module contains code for Project 1 that allows a user to simulate an entire
playthrough of the game. Please consult the project handout for instructions and details.

You can copy/paste your code from the ex1_simulation file into this one, and modify it as needed
to work with your game.

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
from proj1_event_logger import Event, EventList
from adventure import AdventureGame, Commands
from game_entities import Player


class AdventureGameSimulation:
    """A simulation of an adventure game playthrough.
    """
    # Private Instance Attributes:
    #   - _game: The AdventureGame instance that this simulation uses.
    #   - _events: A collection of the events to process during the simulation.
    game: AdventureGame
    _events: EventList
    command_handler: Commands
    player: Player

    def __init__(self, game_data_file: str, initial_location_id: int, commands: list[str], undo: int = 2) -> None:
        """Initialize a new game simulation based on the given game data, that runs through the given commands.

        Preconditions:
        - len(commands) > 0
        - all commands in the given list are valid commands at each associated location in the game
        """
        self._events = EventList()
        self.game = AdventureGame(game_data_file, initial_location_id)
        self.player = Player(50, undo, [])
        self.command_handler = Commands(self.player, self.game, self._events)

        start_location = self.game.get_location(initial_location_id)

        self._events.add_event(Event(start_location.id_num, start_location.name))
        self.generate_events(commands)

    def generate_events(self, commands: list[str]) -> None:
        """Generate all events in this simulation.

        Preconditions:
        - len(commands) > 0
        - all commands in the given list are valid commands at each associated location in the game
        """

        for command in commands:
            if self.player.moves > 0:
                self.command_handler.process_choice(command)
                self.command_handler.check_game_over()

    def get_id_log(self) -> list[int]:
        """
        Get back a list of all location IDs in the order that they are visited within a game simulation
        that follows the given commands.

        >>> sim = AdventureGameSimulation('game_data.json', 4, ["go east","go east", "go south"])
        >>> sim.get_id_log()
        [4, 3, 2, 1]

        >>> sim = AdventureGameSimulation('game_data.json', 8, ["go north","go west"])
        >>> sim.get_id_log()
        [8, 4, 9]
        """

        # Note: We have completed this method for you. Do NOT modify it for ex1.

        return self._events.get_id_log()

    def run(self) -> None:
        """Run the game simulation and log location descriptions."""

        # Note: We have completed this method for you. Do NOT modify it for ex1.

        current_event = self._events.first  # Start from the first event in the list

        while current_event:
            print(current_event.description)
            if current_event is not self._events.last:
                print("You choose:", current_event.next_command)

            # Move to the next event in the linked list
            current_event = current_event.next


if __name__ == "__main__":
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['R1705', 'E9998', 'E9999']
    })
    # print("\n\nWIN GAME WALKTHROUGH")
    # Win condition where player drops all 3 required items in their room
    win_walkthrough = ["puzzle", "go east", "go east", "go south", "take keycard", "go north",
                       "go west", "go west", "go south", "take laptop_charger", "go north", "go north", "go north",
                       "take lucky_mug", "go south", "go south", "go west", "go into my room", "drop usb",
                       "drop laptop_charger", "drop lucky_mug"]
    expected_log = [4, 4, 3, 2, 1, 1, 2, 3, 4, 8, 8, 4, 5, 6, 6, 5, 4, 9, 10, 10, 10, 10]
    sim_win = AdventureGameSimulation('game_data.json', 4, win_walkthrough)
    assert expected_log == sim_win.get_id_log()
    assert sim_win.command_handler.get_score()[0] == 130
    assert sim_win.player.items == ["keycard"]

    print("\n\nLOSE GAME WALKTHROUGH")
    # Lose condition where player runs out of moves/time
    lose_demo = ["go east", "go west"] * 25
    sim_lose = AdventureGameSimulation('game_data.json', 4, lose_demo)
    assert sim_lose.player.moves == 0

    print("\n\nANOTHER LOSE GAME WALKTHROUGH")
    # Lose condition where player drops keycard in their room and leaves, locking themselves out
    lose2_demo = ["go east", "go east", "go south", "take keycard", "go north", "go west", "go west", "go west",
                  "go into my room", "drop keycard", "go east"]
    expected_log = [4, 3, 2, 1, 1, 2, 3, 4, 9, 10, 10, 9]
    sim_lose2 = AdventureGameSimulation('game_data.json', 4, lose2_demo)
    assert expected_log == sim_lose2.get_id_log()
    assert sim_lose2.player.items == []
    assert sim_lose2.game.items['keycard'].current_position == 10

    print("\n\nINVENTORY DEMO")
    inventory_demo = ["puzzle", "go east", "take unlit_lantern", "go east", "take water_bottle", "go south",
                      "take keycard", "inventory", "go north", "drop usb", "inventory"]
    expected_log = [4, 4, 3, 3, 2, 2, 1, 1, 2, 2]
    sim_inventory = AdventureGameSimulation('game_data.json', 4, inventory_demo)
    assert expected_log == sim_inventory.get_id_log()
    assert all(check_item in sim_inventory.player.items for check_item in ['unlit_lantern', 'water_bottle', 'keycard'])

    print("\n\nSCORES DEMO")
    scores_demo = ["go east", "go east", "go south", "take keycard", "go north", "go west",
                   "go west", "go south", "take laptop_charger", "go north", "go west", "go into my room",
                   "drop laptop_charger", "score"]
    expected_log = [4, 3, 2, 1, 1, 2, 3, 4, 8, 8, 4, 9, 10, 10]
    sim_scores = AdventureGameSimulation('game_data.json', 4, scores_demo)
    assert expected_log == sim_scores.get_id_log()
    assert sim_scores.command_handler.get_score() == [30, 0, 370]

    print("\n\nOPTIONAL COMPLEX PUZZLE WALKTHROUGH")
    # This complex puzzle requires a lantern and lighter to be dropped in a dark room in order to access the puzzle w
    # which is a riddle
    enhancement1_demo = ["go east", "take unlit_lantern", "go east", "go south", "take keycard", "go north", "go west",
                         "go west", "go west", "go into my room", "take lighter", "go east", "go east", "go north",
                         "go north", "go west", "drop unlit_lantern", "drop lighter", "puzzle"]
    expected_log = [4, 3, 3, 2, 1, 1, 2, 3, 4, 9, 10, 10, 9, 4, 5, 6, 7, 7, 7, 7]
    sim_enhancement1 = AdventureGameSimulation("game_data.json", 4, enhancement1_demo)
    assert 'money' in sim_enhancement1.player.items
    assert sim_enhancement1.command_handler.get_score()[1] == 70
    assert expected_log == sim_enhancement1.get_id_log()

    print("\n\nOPTIONAL COMPLEX PUZZLE FAIL")
    # same demo as above with without dropping the unlit_lantern and the lighter which keeps the puzzle locked
    enhancement1_fail_demo = ["go east", "take unlit_lantern", "go east", "go south", "take keycard", "go north",
                              "go west", "go west", "go west", "go into my room", "take lighter", "go east", "go east",
                              "go north", "go north", "go west", "puzzle"]
    sim_enhancement1 = AdventureGameSimulation("game_data.json", 4, enhancement1_fail_demo)
    assert 'money' not in sim_enhancement1.player.items
    assert sim_enhancement1.command_handler.get_score()[1] == 0

    print("\n\nFULL GAME WALKTHROUGH")
    # This is a win walkthrough of the whole game including completion of an aditional puzzle
    full_game_walkthrough = ["puzzle", "go east", "take unlit_lantern", "go east", "go south", "take keycard",
                             "go north", "go west", "go west", "go south", "take laptop_charger", "go north", "go west",
                             "go into my room", "take lighter", "go east", "go east", "go north", "go north",
                             "go north", "take lucky_mug", "go west", "drop unlit_lantern", "drop lighter", "puzzle",
                             "go east", "go south", "go south", "go west", "go into my room", "drop usb",
                             "drop laptop_charger", "drop lucky_mug"]
    sim_full_game = AdventureGameSimulation("game_data.json", 4, full_game_walkthrough)
    assert sim_full_game.command_handler.get_score()[0] == 250
    assert sim_full_game.command_handler.get_score()[1] == 120
    # checks all puzzles are completed
    assert all(sim_full_game.game.puzzles[puzzle].completed for puzzle in sim_full_game.game.puzzles)

    print("\n\nUNDO DEMO")
    # This is a demonstration of undoing all events in a win walkthrough
    undo_demo = ["puzzle", "go east", "go east", "go south", "take keycard", "go north",
                 "go west", "go west", "go south", "take laptop_charger", "go north", "go north", "go north",
                 "take lucky_mug", "go south", "go south", "go west", "go into my room", "drop usb",
                 "drop laptop_charger", "undo", "undo", "undo", "undo", "undo", "undo", "undo", "undo", "undo",
                 "undo", "undo", "undo", "undo", "undo", "undo", "undo", "undo", "undo", "undo"]
    sim_undo = AdventureGameSimulation("game_data.json", 4, undo_demo, 50)
    assert sim_undo.get_id_log() == [4, 4]
    for item_name in sim_undo.game.items:
        item = sim_undo.game.items[item_name]
        assert item.current_position == item.start_position  # checks all items are returned to start position

"""CSC111 Project 1: Text Adventure Game - Game Entities

Instructions (READ THIS FIRST!)
===============================

This Python module contains the entity classes for Project 1, to be imported and used by
 the `adventure` module.
 Please consult the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2025 CSC111 Teaching Team
"""
from dataclasses import dataclass
from typing import Optional

from python_ta.contracts import check_contracts


@check_contracts
@dataclass
class Location:
    """A location in our text adventure game world.

    Instance Attributes:
        - id_num: Integer id of this event's location
        - name: name of the location
        - brief_description: shorter description of location shown on subsequent visits
        - long_description: full description of location shown on first visit
        - available_commands: dictionary mapping of string commands to the location id the
                                command would lead to
        - items: list of item names at the location ID
        - visited: True if player has been to the location, False if player hasn't been to the locaiton

    Representation Invariants:
        - self.id_num > 0
        - self.brief_description != ''
        - self.long_description != ''
        - all(command != '' in self.available_commands)
        - all(dest != '' in self.available_commands.values())
        - all(item != '' for item in self.items)
    """

    # This is just a suggested starter class for Location.
    # You may change/add parameters and the data available for each Location object as you see fit.
    #
    # The only thing you must NOT change is the name of this class: Location.
    # All locations in your game MUST be represented as an instance of this class.
    id_num: int
    name: str
    brief_description: str
    long_description: str
    available_commands: dict[str, Optional[int]]
    items: list[str]


@dataclass
@check_contracts
class Item:
    """An item in our text adventure game world.

    Instance Attributes:
        - name: the item name
        - description: brief description of the item
        - start_position: location ID of where the object starts.
        - current_position: either shows the starting position if Item is in the player's inventory
                            or location ID of where the object has been dropped
        - target_position: location ID of where the object should be at the end of the game to score points.
                            Target position of -1 a target position of the player's inventory
        - target_points: number of points the player recieves for moving/putting the item in the right location ID

    Representation Invariants:
        - self.name != ''
        - self.start_position > 0
        - self.current_position > 0 or self.current_position == -1
        - self.target_position > 0 or self.target_position == -1
        - self.target_points >= 0
    """

    # NOTES:
    # This is just a suggested starter class for Item.
    # You may change these parameters and the data available for each Item object as you see fit.
    # (The current parameters correspond to the example in the handout).
    #
    # The only thing you must NOT change is the name of this class: Item.
    # All item objects in your game MUST be represented as an instance of this class.

    name: str
    start_position: int
    current_position: int
    target_position: int
    target_points: int


@dataclass()
class Player:
    """The player in our text adventure game world

    Instance Attributes:
        - moves: number of moves the player has left
        - undo: max number of undo's a player is allowed
        - items: list of item names the player currently has

    Representation Invariants:
        - self.moves > 0
        - self.undo >= 0
    """
    moves: int
    undo: int
    items: list[str]


# Note: Other entities you may want to add, depending on your game plan:
# - Puzzle class to represent special locations (could inherit from Location class if it seems suitable)
# - Player class
# etc.
@dataclass()
class Puzzle:
    """Any puzzle in the game world
    Instance Attributes:
        - location_id: location ID of where the puzzle takes place
        - setup: the context and story behind the puzzle
        - finish: the context and story after the puzzle
        - puzzle: tuple of three strings where the first string is the question, the second is the answer, and third
                    is the reward
        - points: the amount of points the player gets for completion of the puzzle
        - completed: True if the puzzle is completed, False otherwise
        - reject: the string output if the player quits the puzzle or says no to the puzzle

    Representation Invariants:
        - self.location_id > 0
        - len(self.setup) > 0
        - len(self.finish) > 0
        - len(self.puzzle[0]) > 0 and len(self.puzzle[1]) > 0
        - len(self.reject) > 0
    """
    location_id: int
    setup: str
    finish: str
    puzzle: tuple[str, str, str]
    points: int
    completed: bool
    reject: str


if __name__ == "__main__":
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['R1705', 'E9998', 'E9999']
    })

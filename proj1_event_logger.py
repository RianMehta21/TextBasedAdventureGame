"""CSC111 Project 1: Text Adventure Game - Event Logger

Instructions (READ THIS FIRST!)
===============================

This Python module contains the code for Project 1. Please consult
the project handout for instructions and details.

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
from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass
class Event:
    """
    A node representing one event in an adventure game.

    Instance Attributes:
        - id_num: ID number of the location where the event took place
        - name: name of the location where the event took place
        - item_action: list of 2 elements, the first one represents if an item has been taken or dropped, and the
                        second represents the item name. if Event is not an item related action, then None
        - next_command: String command which leads this event to the next event
        - next: Event object representing the next event in the game, or None if this is the last game event
        - prev: Event object representing the previous event in the game, None if this is the first game event

    Representation Invariants:
        - id_num > 0
        - len(name) > 0
        - item_action is None or item_action[0] in ["took","dropped"]
        - command is None or len(command)>0
        - next is None or isinstance(next, Event)
        - prev is None or isinstance(prev, Event)
    """

    id_num: int
    name: str
    item_action: Optional[Tuple[str, str]] = None
    description: str = None
    next_command: Optional[str] = None
    next: Optional[Event] = None
    prev: Optional[Event] = None


class EventList:
    """
    A linked list of game events.

    Instance Attributes:
        - first: Event object representing the first event in the game, or None if no events have taken place
        - last: Event object representing the last event int the game, or None if no events have taken place

    Representation Invariants:
        - self.last is None == self.first is None
    """
    first: Optional[Event] = None
    last: Optional[Event] = None

    def add_event(self, event: Event, command: str = None) -> None:
        """Add the given new event to the end of this event list.
        The given command is the command which was used to reach this new event, or None if this is the first
        event in the game.

        Preconditions:
            - event is a valid Event
            - command is a valid command

        >>> events = EventList()
        >>> event1 = Event(1,"Robarts")
        >>> event2 = Event(2,"Athletic Center")
        >>> events.add_event(event1)
        >>> events.add_event(event2,"go north")
        >>> events.last.prev == event1
        True
        >>> events.first.next == event2
        True
        >>> events.first.next_command == "go north"
        True
        """

        if self.is_empty():
            self.first = event
            self.last = event
            self.last.next_command = command
        else:
            event.prev = self.last
            self.last.next = event
            self.last = event
            self.last.prev.next_command = command

    def remove_last_event(self) -> None:
        """Remove the last event from this event list.
        If the list is empty, do nothing.
        >>> events = EventList()
        >>> event1 = Event(1,"Robarts")
        >>> event2 = Event(2,"Athletic Center")
        >>> events.add_event(event1)
        >>> events.add_event(event2,"go north")
        >>> events.remove_last_event()
        >>> events.last == events.first
        True
        >>> events.first.next_command is None
        True
        >>> events.last.next is None
        True
        >>> events.remove_last_event()
        >>> events.first is None and events.last is None
        True
        """

        if self.first == self.last:
            self.first = None
            self.last = None
        elif not self.is_empty():
            self.last = self.last.prev
            self.last.next = None
            self.last.next_command = None

    def display_events(self) -> str:
        """Display all events in chronological order.
        >>> events = EventList()
        >>> events.add_event((Event(4,"Myhal")))
        >>> events.add_event(Event(3,"Lassonde Mining Building"), "go east")
        >>> events.add_event(Event(3, "Lassonde Mining Building",("took", 'unlit_lantern')), "Take unlit_lantern")
        >>> events.display_events() == "Location: Myhal, Command: go east\\nLocation: Lassonde Mining Building, Command: Take unlit_lantern\\nLocation: Lassonde Mining Building, Command: None\\n"
        True
        """
        curr = self.first
        display_events_so_far = ""
        while curr:
            display_events_so_far += f"Location: {curr.name}, Command: {curr.next_command}\n"
            curr = curr.next
        return display_events_so_far

    def is_empty(self) -> bool:
        """Return whether this event list is empty.
        >>> events = EventList()
        >>> events.is_empty()
        True
        >>> events.add_event(Event(4,"Myhal"),"go south")
        >>> events.is_empty()
        False
        """
        return self.first is None

    def get_id_log(self) -> list[int]:
        """Return a list of all location IDs visited for each event in this list, in sequence.
        >>> events = EventList()
        >>> events.add_event(Event(1,"Robarts"), "go north")
        >>> events.add_event(Event(2,"Athletic Center"),"go west")
        >>> events.add_event(Event(3,"Lassonde Mining Building",("took","unlit_lantern")),"Take unlit_lantern")
        >>> events.get_id_log()
        [1, 2, 3]
        """

        id_log_so_far = []
        if not self.is_empty():
            curr = self.first
            while curr is not None:
                id_log_so_far.append(curr.id_num)
                curr = curr.next
        return id_log_so_far

    # Note: You may add other methods to this class as needed


if __name__ == "__main__":
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['R1705', 'E9998', 'E9999']
    })

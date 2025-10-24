#! /bin/python
# gvim: set fileencoding=utf-8
#
# (c) September 2, 2025, José Martinez, Polytech Nantes, University of Nantes
#
# Licence:  proprietary
# The use of this library is not authorised outside the Polytechnic School of the University of Nantes.
#


"""
This module provides the translation of the relational schema of the game into classes.
Notice that the IDs of the relational schema are pointers to class instances.

An instance of the relational schema is split into:

    * permanents facts, named "World," and
    * changing situations, stored in "State," but also referencing the world.

This module is dedicated to the "Army" relation.
"""


__all__ = [
    'Colour',
    'ARMY_COLOURS',
    'Army',
    'Armies',
    ]


from typing import Set, TypeAlias
# from strategy.strategy import Strategy # This would introduce circular imports into the model, hence we use a mere string.


Colour: TypeAlias = str
"""
The natural identifier of an army is its colour.
"""


ARMY_COLOURS = {
    "blue",
    "green",
    "magenta",
    "red",
    "white",
    "yellow",
    }
"""
In the Risk game, there can be up to six armies, the colours of which have to been chosen from a predefined palette.
"""


class Army:
    """
    This class implements the simple functional dependency:

    > Army: Army <-> Colour;
    """

    def __init__ (self,
                  c: Colour,
                  g: 'Strategy'):
        assert c != "", "army colour cannot be null"

        self._colour = c
        self._strategy = g

    @property
    def colour (self) -> Colour:
        """
        An army is identified by its colour.
        """
        return self._colour

    @property
    def strategy (self) -> 'Strategy':
        """
        To each army is associated a strategy, i.e., a way to take a decision at each step.
        The referee and orchestrator is the 'game' function.
        """
        return self._strategy

    def __eq__ (self, other) -> bool:
        return isinstance(other, Army) and self.colour == other.colour

    def __hash__ (self) -> int:
        return hash(self.colour)

    def __str__ (self) -> str:
        return f"Army {self.colour}"


Armies = Set[Army]
"""
Regions form a set.
During a game, there must be at least three armies.
With two players, the third one is a neutral one.
"""

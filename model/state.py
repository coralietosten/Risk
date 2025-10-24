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

This module is dedicated to the "State" relation.
"""


__all__ = [ 'State' ]


from typing import Dict, Tuple, NamedTuple
from model.region import Unit
from model.territory import Territory
from model.army import Army
from model.world import World


class State (NamedTuple):
    """
    This named tuple implements the functional dependency:

    > State:  Territory -> Army Unit;

    The full state consists of:

        * a single world, the permanent facts from the previous classes, and
        * several changing states over this world, this actual 'State' class.

    In order to avoid using two parameters, the permanent world and the actually changing state, in each function, the definition of this class does contain two attributes, one for each part of the "database":

        * The 'world' attribute is the same, duplicated in each and every state, during the game (only the pointer, not the full contents).
        * The 'state' attribute contains actually the 'State' relation of the relational model.
    """

    world: World
    """
    The world is the permanent part of the database.
    """

    state: Dict[Territory, Tuple[Army, Unit]]
    """
    The changing part consists of the occupation of territories by the various armies.
    """

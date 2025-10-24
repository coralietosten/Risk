#! /bin/python
# gvim: set fileencoding=utf-8
#
# (c) September 4, 2025, José Martinez, Polytech Nantes, University of Nantes
#
# Licence:  proprietary
# The use of this library is not authorised outside the Polytechnic School of the University of Nantes.
#


"""
This module introduces the generation of instances of operations in the Risk game.
They are not necessarily to be used directly.
Indeed, they are not be used at all!

Reinforcements introduce the risk of an exponential blow up!
Also, attacks can be conducted in so many different ways, that it is worthless to try them all.
Even maneuvers can lead to an infinite complexity...
"""

__all__ = [
    'Description',
    'reinforcements',
    'attacks',
    'maneuvers',
    ]


from typing import Any, List, Tuple, Dict, TypeAlias
from itertools import permutations
from utilities.combinatorics import power_set, sum_composition
from model.region import Unit
from model.territory import Territory
from model.army import Army
from model.state import State
from model.state_informations import territory_occupant, territory_units, is_defeated_army, territories_occupied_by_army, reinforcement_units


Description: TypeAlias = Any
"""
The description generally a tuple containing:

    * the name of the operation, and
    * the currified parameters.
"""


def reinforcements (s: State,
                    a: Army) -> List[Tuple[Description, State, Dict[Territory, Unit]]]:
    """
    Generating all the possible reinforcements for the given army.

    :bug:  This function generates an exponential number of results!
    """
    assert isinstance(s, State)
    assert isinstance(a, Army)
    assert a in s.world.armies, "the reinforced army must exist in the world"
    assert not is_defeated_army(s, a), "the reinforced army has not been defeated yet"

    T_a = territories_occupied_by_army(s, a)
    u_a = reinforcement_units(s, a)
    return [ (("reinforce", a, "by", u_a, "units as", f), s, f)
             for X in power_set(T_a)
             if X != set()
             for N in sum_composition(u_a, len(X))
             for U in permutations(N)
             for f in [ dict(zip(list(X), U)) ] ] # let


def attacks (s: State,
             a: Army) -> List[Tuple[Description, State, Territory, Territory, Unit]]:
    """
    Generating all the single attacks between an army and all of its enemies.

    :bug:  This function generates a very large number of results, too!
    """
    assert isinstance(s, State)
    assert isinstance(a, Army)
    assert a in s.world.armies, "attacking army must exist"

    return [ ((a, "fights", d, "with", u_a + 1, "units from", t_a, "to", t_d), s, t_a, t_d, n + 1)
             for (t_a, t_d) in s.world.adjacencies
             if territory_occupant(s, t_a) == a
             if (d := territory_occupant(s, t_d)) != a
             if (u_a := territory_units(s, t_a)) > 1
             for n in range(min(3, u_a)) ]


def maneuvers (s: State,
               a: Army) -> List[Tuple[Description, State, Territory, Territory, Unit]]:
    """
    Generating all the unit movements from a territory to an adjacent territory belonging to the same army, leaving at least one unit behind.

    :bug:  Although only quadratic between territories, this function generates too many maneuvers to be used directly in the game, up to infinite for players that pile up units!
    """
    assert isinstance(s, State)
    assert isinstance(a, Army)
    assert a in s.world.armies, "moving army must exist"

    return [ ((a, "moves", n + 1, "units from", t_0, "to", t_1), s, t_0, t_1, n + 1)
             for (t_0, t_1) in s.world.adjacencies
             if territory_occupant(s, t_0) == a
             if territory_occupant(s, t_1) == a
             if (u_0 := territory_units(s, t_0)) > 1
             for n in range(u_0) ]

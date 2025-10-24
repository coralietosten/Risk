#! /bin/python
# gvim: set fileencoding=utf-8
#
# (c) September 11, 2025, José Martinez, Polytech Nantes, University of Nantes
#
# Licence:  proprietary
# The use of this library is not authorised outside the Polytechnic School of the University of Nantes.
#
#


"""
Several strategies are provided in order to move units between adjacent territories occupied by an army.

Notice that the pre- and post-conditions of these functions would not need to be tested.
They are already ensured by the strategies.
However, they are repeated to the programmer for clarity and documentation.
Also, this allows to detect a possible flaw closer to its source.
A model is given below.
Notice that post-conditions can be strengthen.

def model_of_maneuver_function (s: State,
                                a: Army) -> Optional[Tuple[Territory, Territory, Unit]]:
    '''
    :parameter s:  the current state
    :parameter t_a:  the army that might maneuvers

    :pre:  The army must belong to the current state

    :return (t_a, t_d, n):  the number of maneuvering units from a territory to another one, when applied

    :post:  The starting territory belongs to the current state
    :post:  The ending territory belongs to the current state
    :post:  The starting territory is occupied by the army
    :post:  The defending territory is occupied by the army
    :post:  At least one unit is maneuvering
    :post:  At least one unit must be left behind
    '''
    # PRE-CONDITION
    assert isinstance(s, State)
    assert isinstance(a, Army)
    assert a in s.world.armies, "The army must belong to the current state"

    # POST-CONDITION
    if result is not None:
        (t_0, t_1, n) = result
        assert isinstance(t_0, Territory)
        assert isinstance(t_1, Territory)
        assert t_0 in s.state, "The starting territory belongs to the current state"
        assert t_1 in s.state, "The ending territory belongs to the current state"
        assert territory_occupant(s, t_0) == a, "The starting territory is occupied by the army"
        assert territory_occupant(s, t_1) == a, "The defending territory is occupied by the army"
        assert n > 0, "At least one unit is maneuvering"
        assert n < territory_units(s, t_0), "At least one unit must be left behind"

    return result
"""


__all__ = [
    'no_maneuver',
    'random_maneuver',
    'random_uniform_maneuver',
    'random_uniform_largest_maneuver',
    ]


from typing import Tuple, Optional
from random import randint, choice
from model.region import Unit
from model.territory import Territory
from model.army import Army
from model.state import State
from model.state_informations import territory_occupant, territory_units, bordering_territories, territories_occupied_by_army


def no_maneuver (s: State,
                 a: Army) -> Optional[Tuple[Territory, Territory, Unit]]:
    """
    A peculiar behaviour is *not* to move.

    :return:  Always ineffective
    """
    assert isinstance(s, State)
    assert isinstance(a, Army)
    assert a in s.world.armies, "The army must belong to the current state"

    result = None

    assert result is None, "Always ineffective"

    return result


def random_maneuver (s: State,
                     a: Army) -> Optional[Tuple[Territory, Territory, Unit]]:
    """
    A totally random maneuver.

    :post:  Effective unless the army has only isolated territories or no more than one unit left
    """
    assert isinstance(s, State)
    assert isinstance(a, Army)
    assert a in s.world.armies, "The army must belong to the current state"

    M = [ (t_0, t_1, randint(1, u_t_0 - 1))
          for (t_0, t_1) in s.world.adjacencies
          if territory_occupant(s, t_0) == a
          if territory_occupant(s, t_1) == a
          if (u_t_0 := territory_units(s, t_0)) > 1 ]
    if len(M) == 0:
        result = None
    else:
        result = choice(M)

    if result is not None:
        (t_0, t_1, n) = result
        assert isinstance(t_0, Territory)
        assert isinstance(t_1, Territory)
        assert t_0 in s.state, "The starting territory belongs to the current state"
        assert t_1 in s.state, "The ending territory belongs to the current state"
        assert territory_occupant(s, t_0) == a, "The starting territory is occupied by the army"
        assert territory_occupant(s, t_1) == a, "The defending territory is occupied by the army"
        assert n > 0, "At least one unit is maneuvering"
        assert n < territory_units(s, t_0), "At least one unit must be left behind"
    else:
        assert all(territory_occupant(s, b) != a
                   for t in territories_occupied_by_army(s, a)
                   if territory_units(s, t) > 1
                   for b in bordering_territories(s, t)), "Effective unless the army has only isolated territories or no more than one unit left"

    return result


def random_uniform_maneuver (s: State,
                             a: Army) -> Optional[Tuple[Territory, Territory, Unit]]:
    """
    A partly random maneuver that tends to distribute uniformly the units among the territories occupied by the army.

    :post:  Effective unless the army has only isolated territories or not enough units to maneuver
    """
    assert isinstance(s, State)
    assert isinstance(a, Army)
    assert a in s.world.armies, "The army must belong to the current state"

    M = [ (t_0, t_1, u_t_0 - u_t_1 )
          for (t_0, t_1) in s.world.adjacencies
          if territory_occupant(s, t_0) == a
          if territory_occupant(s, t_1) == a
          if (u_t_0 := territory_units(s, t_0)) > (u_t_1 := territory_units(s, t_1)) + 1 ]
    if len(M) == 0:
        result = None
    else:
        result = choice(M)

    if result is not None:
        (t_0, t_1, n) = result
        assert isinstance(t_0, Territory)
        assert isinstance(t_1, Territory)
        assert t_0 in s.state, "The starting territory belongs to the current state"
        assert t_1 in s.state, "The ending territory belongs to the current state"
        assert territory_occupant(s, t_0) == a, "The starting territory is occupied by the army"
        assert territory_occupant(s, t_1) == a, "The defending territory is occupied by the army"
        assert n > 0, "At least one unit is maneuvering"
        assert n < territory_units(s, t_0), "At least one unit must be left behind"
    else:
        assert all(territory_occupant(s, b) != a or abs(territory_units(s, t) - territory_units(s, b)) < 2
                   for t in territories_occupied_by_army(s, a)
                   for b in bordering_territories(s, t)), "Effective unless the army has only isolated territories or not enough units to maneuver"

    return result


def random_uniform_largest_maneuver (s: State,
                                     a: Army) -> Optional[Tuple[Territory, Territory, Unit]]:
    """
    A partly random maneuver that tends to distribute uniformly the units among the territories occupied by the army.
    Large maneuvers are preferred over small ones.

    :post:  Effective unless the army has only isolated territories or not enough units to maneuver
    """
    assert isinstance(s, State)
    assert isinstance(a, Army)
    assert a in s.world.armies, "The army must belong to the current state"

    M = [ (t_0, t_1, u_t_0 - u_t_1 )
          for (t_0, t_1) in s.world.adjacencies
          if territory_occupant(s, t_0) == a
          if territory_occupant(s, t_1) == a
          if (u_t_0 := territory_units(s, t_0)) > (u_t_1 := territory_units(s, t_1)) ]
    if len(M) == 0:
        result = None
    else:
        n_max = max(n for (_, _, n) in M)
        result = choice([ ttn
                          for ttn in M
                          if ttn[2] == n_max ])

    if result is not None:
        (t_0, t_1, n) = result
        assert isinstance(t_0, Territory)
        assert isinstance(t_1, Territory)
        assert t_0 in s.state, "The starting territory belongs to the current state"
        assert t_1 in s.state, "The ending territory belongs to the current state"
        assert territory_occupant(s, t_0) == a, "The starting territory is occupied by the army"
        assert territory_occupant(s, t_1) == a, "The defending territory is occupied by the army"
        assert n > 0, "At least one unit is maneuvering"
        assert n < territory_units(s, t_0), "At least one unit must be left behind"
    else:
        assert all(territory_occupant(s, b) != a or abs(territory_units(s, t) - territory_units(s, b)) < 2
                   for t in territories_occupied_by_army(s, a)
                   for b in bordering_territories(s, t)), "Effective unless the army has only isolated territories or not enough units to maneuver"

    return result

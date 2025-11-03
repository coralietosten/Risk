#! /bin/python
# gvim: set fileencoding=utf-8
#
# (c) September 2, 2025, José Martinez, Polytech Nantes, University of Nantes
#
# Licence:  proprietary
# The use of this library is not authorised outside the Polytechnic School of the University of Nantes.
#


"""
Various functions that give derived informations about a state.
In other words, these are queries over the state of the world.
"""


__all__ = [
    'territory_occupant',
    'territory_units',
    'territories_occupied_by_army',
    'bordering_territories',
    'armies_in_region',
    'armies_in_territories',
    'region_occupant',
    'regions_occupied_by_army',
    'is_occupied_region',
    'territory_fronts',
    'army_units',
    'is_defeated_army',
    'reinforcement_units',
    'undefeated_armies',
    'winning_army',
    'game_over',
    'sort_territories_by_units',
    ]


from typing import Optional, Set, Tuple, List
from model.region import Region, Unit
from model.territory import Territory
from model.army import Army
from model.state import State


def territory_occupant (s: State,
                        t: Territory) -> Army:
    """
    At any moment, any territory is occupied by exactly one army.

    :parameter s:  the current state
    :parameter t:  a territory in the state

    :return:  the army that occupies this territory at that moment

    :post:  the occupying army belongs to the armies of the state, hence of the world
    """
    assert isinstance(s, State)
    assert isinstance(t, Territory)
    assert t in s.world.territories, "the territory belongs to the territories of the world"
    assert t in s.state, "the territory belongs to the territories of the state"

    result = s.state[t][0]

    assert isinstance(result, Army)
    assert result in s.world.armies, "the occupying army belongs to the armies of the world"

    return result


def territory_units (s: State,
                     t: Territory) -> Unit:
    """
    At any moment, any territory is occupied by a given number of units, never none.

    :parameter s:  the current state
    :parameter t:  a territory in the state

    :return:  the army that occupies this territory at that moment

    :post:  the number of units is strictly positive
    """
    assert isinstance(s, State)
    assert isinstance(t, Territory)
    assert t in s.world.territories, "the territory belongs to the territories of the world"
    assert t in s.state, "the territory belongs to the territories of the state"

    result = s.state[t][1]

    assert isinstance(result, Unit)
    assert result >= 1, "there is always at least one unit on any territory"

    return result


def territories_occupied_by_army (s: State,
                                  a: Army) -> Set[Territory]:
    """
    The territories that are occupied by an army.

    :parameter s:  the current state
    :parameter a:  an army in the state

    :return:  the territories that are occupied by units of this army

    :post:  the territories are a sub-set of the territories of the world
    """
    assert isinstance(s, State)
    assert isinstance(a, Army)
    assert a in s.world.armies, "the army must belong to the world"

    result = { t
               for t in s.world.territories
               if territory_occupant(s, t) == a }

    assert isinstance(result, Set)
    assert all(isinstance(t, Territory) for t in result)
    assert result <= s.world.territories, "the territories are a sub-set of the territories of the world"
    assert len(result) == len(s.world.territories) - len({ t
                                                           for t in s.world.territories
                                                           if territory_occupant(s, t) != a })

    return result


def bordering_territories (s: State,
                           t: Territory) -> Set[Territory]:
    """
    The set of territories that have a common border with the given one.
    """
    assert isinstance(s, State)
    assert isinstance(t, Territory)

    result = { t2
               for t2 in s.world.territories
               if (t, t2) in s.world.adjacencies }

    assert isinstance(result, Set)
    assert all(isinstance(t, Territory) for a in result)

    return result

def armies_in_region (s: State,
                      r: Region) -> Set[Army]:
    """
    The set of armies that have units deployed on the given region.

    :parameter s:  the current state
    :parameter a:  a region of the world

    :return:  the territories that are occupied by units of this army

    :post:  the territories are a sub-set of the territories of the world
    """
    assert isinstance(s, State)
    assert isinstance(r, Region)
    assert r in s.world.regions, "the region must belong to the world"

    result = { territory_occupant(s, t)
                for t in s.state
                if t.region == r }

    assert isinstance(result, Set)
    assert all(isinstance(a, Army) for a in result)

    return result


def armies_in_territories (s: State,
                           T: Set[Territory]) -> Set[Army]:
    """
    The set of armies that have units deployed on the given territories.
    """
    assert isinstance(s, State)
    assert all(isinstance(t, Territory) for t in T)
    assert all(t in s.world.territories for t in T)
    assert all(t in s.state for t in T)

    result = { territory_occupant(s, t)
               for t in T }

    assert isinstance(result, Set)
    assert all(isinstance(a, Army) for a in result)

    return result


def region_occupant (s: State,
                     r: Region) -> Optional[Army]:
    """
    A region is occupied by an army when all its territories are occupied by that army.
    """
    assert isinstance(s, State)
    assert isinstance(r, Region)
    assert r in s.world.regions

    result = ( None          if len(A := armies_in_region(s, r)) > 0 else
               next(iter(A)) )

    assert result is None or isinstance(result, Army)

    return result


def regions_occupied_by_army (s:State,
                              a: Army) -> Set[Region]:
    """
    A region is occupied by an army when all its territories are occupied by that army.
    """
    assert isinstance(s, State)
    assert isinstance(a, Army)
    assert a in s.world.armies

    T_a = territories_occupied_by_army(s, a)
    result = { r
               for r in s.world.regions
               if s.world.region_territories[r] <= T_a }

    assert isinstance(result, Set)
    assert all(isinstance(r, Region) for r in result)

    return result


def is_occupied_region (s: State,
                        r: Region) -> bool:
    """
    A region is occupied when an army occupies all of its territories.
    """
    assert isinstance(s, State)
    assert isinstance(r, Region)
    assert r in s.world.regions

    return region_occupant(s, r) is not None


def territory_fronts (s: State) -> Set[Tuple[Territory, Army, Territory, Army]]:
    assert isinstance(s, State)

    result = { (t1, a1, t2, a2)
               for (t1, t2) in s.world.adjacencies
               if (a1 := territory_occupant(s, t1)) != (a2 := territory_occupant(s, t1)) }

    assert isinstance(result, Set)
    assert all(isinstance(t, tuple) for t in result)
    assert all(len(t) == 4 for t in result)
    assert all(isinstance(t, Territory) for (t, _, _, _) in result)
    assert all(isinstance(a, Army) for (_, a, _, _) in result)
    assert all(isinstance(t, Territory) for (_, _, t, _) in result)
    assert all(isinstance(a, Army) for (_, _, _, a) in result)

    return result


def army_units (s: State,
                a: Army) -> Unit:
    """
    The sum of the active units over all the territories occupied by the given army.
    """
    assert isinstance(s, State)
    assert isinstance(a, Army)
    assert a in s.world.armies

    result = sum(territory_units(s, t)
                 for t in s.state
                 if territory_occupant(s, t) == a)

    assert isinstance(result, Unit)
    assert result >= 0, "there is always at least one unit on any territory, unless the army has been defeated"

    return result


def is_defeated_army (s: State,
                      a: Army) -> bool:
    """
    An army is defeated when it is left without any unit.
    Equivalently, it does not occupy any territory.
    """
    assert isinstance(s, State)
    assert isinstance(a, Army)
    assert a in s.world.armies

    return army_units(s, a) == 0


def reinforcement_units (s: State,
                         a: Army) -> Unit:
    """
    The number of reinforcement units per turn is the under-rounded number of occupied territories divided by 3 plus the sum of the values of occupied regions.
    However, the number of units can never be less than 3.
    """
    assert isinstance(s, State)
    assert isinstance(a, Army)
    assert a in s.world.armies
    assert not is_defeated_army(s, a), "a defeated army cannot claim fresh units"

    T_a = territories_occupied_by_army(s, a)
    R_a = regions_occupied_by_army(s, a)
    result = max(3, len(T_a) // 3 + sum(r.value
                                        for r in R_a))

    assert isinstance(result, Unit)
    assert result >= 3, "the minimal reinforcement units is three"

    return result


def undefeated_armies (s: State) -> Set[Army]:
    """
    The set of armies that still have units deployed on the map, i.e., still undefeated ones.
    """
    assert isinstance(s, State)

    result = { territory_occupant(s, t)
               for t in s.state }

    assert isinstance(result, Set)
    assert all(isinstance(a, Army) for a in result)

    return result

def winning_army (s: State) -> Optional[Army]:
    """
    An army wins the game when it occupies all the territories on the map.
    """
    assert isinstance(s, State)

    result = ( None          if len(A := undefeated_armies(s)) > 1 else
               next(iter(A)) )

    assert result is None or isinstance(result, Army)

    return result


def game_over (s: State) -> bool:
    """
    The game ends when there is a winner, the last standing army.
    """
    assert isinstance(s, State)

    return winning_army(s) is not None


def sort_territories_by_units(s, t_a : Set[Territory])-> List[Tuple[Territory,Unit]]:
    """
    renvoie une liste de couple : territoire, unité. Trié dans l'ordre décroissant
    """
    result = []
    for t in t_a :
        u = territory_units(s, t)
        result.append((t,u))
    result.sort(key = lambda x:x[1],reverse=True) #tri de la liste selon le nombre d'units
    return result



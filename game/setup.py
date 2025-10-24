#! /bin/python
# gvim: set fileencoding=utf-8
#
# (c) August 29, 2025, José Martinez, Polytech Nantes, University of Nantes
#
# Licence:  proprietary
# The use of this library is not authorised outside the Polytechnic School of the University of Nantes.
#


"""
Setting up the board could be done in various ways.
Hereafter, we provide only a random start.

Generally, the set up is played by the armies:

    * Firstly, each army, in turn, takes possession of a free territory.

    * Then, they place in turn, one by one, additional units on their territories.
      These steps can be seen as reinforcements by one unit.
      Therefore, we could easily provide a variant of a totally random and uniform set up.
      We would keep the initial random assignments of territories.
      Next, turn-based reinforcements would be run till the placement of all the units.
"""


__all__ = [ 'random_initial_state' ]


from random import shuffle
from model.state_informations import territory_occupant, territory_units, territories_occupied_by_army
from model.world import World
from model.state import State
from model.army import ARMY_COLOURS


def random_initial_state (w: World) -> State:
    """
    An initial state where territories are evenly distributed at random among the players.
    Each territory receives two units.

    :parameter w:  the world contains the description of regions, territories, and armies
    
    :pre:  there must be at least one army in the world (as a limit case)
    :pre:  there cannot more armies than available colours
    :pre:  there must be at least one territory per army

    :return:  a random configuration by evenly allocating territories to armies, each one with two units
    
    :post:  the given world remains unchanged in the resulting state
    :post:  all the territories have been included in the initial state
    :post:  all the territories are occupied by known armies
    :post:  all the territories are occupied by at least one unit
    :post:  the territories are evenly distributed among armies
    """
    assert isinstance(w, World)
    assert (n := len(w.armies)) >= 1, "there must be at least one army in the world (as a limit case)"
    assert n <= len(ARMY_COLOURS), "there cannot more armies than available colours: {len(ARMY_COLOURS)}"
    assert len(w.territories) >= n , "there must be at least one territory per army"

    A = list(w.armies)
    shuffle(A)
    T = list(w.territories)
    shuffle(T)
    P = [ (a, 2)
          for a in A ] * (len(w.territories) // len(w.armies)) # fair placements
    Q = [ (a, 2)
          for a in A ] # some lucky armies get an additional territory
    shuffle(Q)
    result = State(w, dict(zip(T, P + Q)))

    assert isinstance(result, State)
    assert result.world == w, "the given world remains unchanged in the resulting state"
    assert all(t in result.state
               for t in w.territories), "all the territories have been included in the initial state"
    assert all(territory_occupant(result, t) in w.armies
               for t in w.territories), "all the territories are occupied by known armies"
    assert all(territory_units(result, t) >= 1
               for t in w.territories), "all the territories are occupied by at least one unit"
    assert all(abs(len(territories_occupied_by_army(result, a1)) - len(territories_occupied_by_army(result, a2))) <= 1
               for a1 in w.armies
               for a2 in w.armies
               if a1 != a2), "the territories are evenly distributed among armies"

    return result

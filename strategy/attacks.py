#! /bin/python
# gvim: set fileencoding=utf-8
#
# (c) September 8, 2025, José Martinez, Polytech Nantes, University of Nantes
#
# Licence:  proprietary
# The use of this library is not authorised outside the Polytechnic School of the University of Nantes.
#


"""
Several strategies are provided in order to attack an opponent army.

Notice that the pre- and post-conditions of these functions would not need to be tested.
They are already ensured by the strategies.
However, they are repeated to the programmer for clarity and documentation.
Also, this allows to detect a possible flaw closer to its source.
A model is given below.
Notice that post-conditions can be strengthen.

def model_of_attack_function (s: State,
                              a: Army) -> Optional[Tuple[Territory, Territory, Unit]]:
    '''
    :parameter s:  a current state
    :parameter a:  an army to reinforce

    :pre:  The army must belong to the current state
    :pre:  The army must not be defeated

    :post:  The attacking territory belongs to the current state
    :post:  The defending territory belongs to the current state
    :post:  The attacking territory is occupied by the army
    :post:  The defending territory is not occupied by the army
    :post:  The attacking units is between one and three
    :post:  The attacking units is strictly less than the number of available units
    '''
    # PRE-CONDITION
    assert isinstance(s, State)
    assert isinstance(a, Army)
    assert a in s.world.armies, "The army must belong to the current state"
    assert not is_defeated_army(s, a), "The army must not be defeated"

    result = DO_SOME_STUFF

    # POST-CONDITION
    if result is not None:
        (t_a, t_d, n) = result
        assert isinstance(t_a, Territory)
        assert isinstance(t_d, Territory)
        assert t_a in s.state, "The attacking territory belongs to the current state"
        assert t_d in s.state, "The defending territory belongs to the current state"
        assert territory_occupant(s, t_a) == a, "The attacking territory is occupied by the army"
        assert territory_occupant(s, t_d) != a, "The defending territory is not occupied by the army"
        assert n in { 1, 2, 3 }, "The attacking units is between one and three"
        assert n < territory_units(s, t_a), "The attacking units is strictly less than the number of available units"

    return result
"""


__all__ = [
    'random_attack',
    ]


from typing import Tuple, Optional
from random import choice
from model.region import Unit
from model.army import Army
from model.territory import Territory
from model.state import State
from model.state_informations import territory_occupant, territory_units, is_defeated_army


def random_attack (s: State,
                   a: Army) -> Optional[Tuple[Territory, Territory, Unit]]:
    """
    A totally random attack between any two bordering and enemy territories with any number of units.
    """
    assert isinstance(s, State)
    assert isinstance(a, Army)
    assert a in s.world.armies, "the army must belong to the current state"
    assert not is_defeated_army(s, a), "The army must not be defeated"

    A = [ (t_a, t_d, n)
          for (t_a, t_d) in s.world.adjacencies
          if territory_occupant(s, t_a) == a
          if territory_occupant(s, t_d) != a
          if (u_a := territory_units(s, t_a)) > 1
          for n in range(1, min(3, u_a - 1) + 1) ]
    if len(A) == 0:
        result = None
    else:
        result = choice(A)

    if result is not None:
        (t_a, t_d, n) = result
        assert isinstance(t_a, Territory)
        assert isinstance(t_d, Territory)
        assert t_a in s.state, "The attacking territory belongs to the current state"
        assert t_d in s.state, "The defending territory belongs to the current state"
        assert territory_occupant(s, t_a) == a, "The attacking territory is occupied by the army"
        assert territory_occupant(s, t_d) != a, "The defending territory is not occupied by the army"
        assert n in { 1, 2, 3 }, "The attacking units is between one and three"
        assert n < territory_units(s, t_a), "The attacking units is strictly less than the number of available units"

    return result

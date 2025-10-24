#! /bin/python
# gvim: set fileencoding=utf-8
#
# (c) September 11, 2025, José Martinez, Polytech Nantes, University of Nantes
#
# Licence:  proprietary
# The use of this library is not authorised outside the Polytechnic School of the University of Nantes.
#


"""
Several strategies are provided in order to invade a conquered territory.

Notice that the pre- and post-conditions of these functions would not need to be tested.
They are already ensured by the strategies.
However, they are repeated to the programmer for clarity and documentation.
Also, this allows to detect a possible flaw closer to its source.
A model is given below.
Notice that post-conditions can be strengthen.

def model_of_invasion_function (s:   State,
                                t_a: Territory,
                                t_d: Territory,
                                n_a: Unit,
                                p_a: Unit) -> Unit:
    '''
    :parameter s:  the current state
    :parameter t_a:  the attacking territory
    :parameter t_d:  the defended but to be lost territory
    :parameter n_a:  the number of engaged units by the attacker
    :parameter p_a:  the number of lost units of the attacker

    :pre:  The attacking territory must belong to the current state
    :pre:  The defending territory must belong to the current state
    :pre:  The armies of the two territories must be distinct
    :pre:  At least one unit must invade

    :return n:  the number of invading units

    :post:  At least the left units from the last battle must invade, i.e., n_a - p_a
    :post:  At least one unit must be left behind
    '''
    # PRE-CONDITION
    assert isinstance(s, State)
    assert isinstance(t_a, Territory)
    assert isinstance(t_d, Territory)
    assert t_a in s.state, "The attacking territory must belong to the current state"
    assert t_d in s.state, "The defending territory must belong to the current state"
    assert territory_occupant(s, t_a) != territory_occupant(s, t_d), "The armies of the two territories must be distinct"
    assert n_a > 0, "At least one unit must invade"

    result = DO_SOME_STUFF

    # POST-CONDITION
    assert n_a - p_a <= result, f"At least the left units from the last battle must invade, i.e., {n_a} - {p_a} = {n_a - p_a}"
    assert result <= territory_units(s, t_a) - p_a - 1, "At least one unit must be left behind"

    return result
"""


__all__ = [
    'minimal_invasion',
    'random_uniform_invasion',
    'uniform_invasion',
    ]

from random import randint
from model.region import Unit
from model.territory import Territory
from model.state import State
from model.state_informations import territory_occupant, territory_units


def minimal_invasion (s:   State,
                      t_a: Territory,
                      t_d: Territory,
                      n_a: Unit,
                      p_a: Unit) -> Unit:
    """
    Only the attacking and victorious units enter the new territory.
    """
    assert isinstance(s, State)
    assert isinstance(t_a, Territory)
    assert isinstance(t_d, Territory)
    assert t_a in s.state, "The attacking territory must belong to the current state"
    assert t_d in s.state, "The defending territory must belong to the current state"
    assert territory_occupant(s, t_a) != territory_occupant(s, t_d), "The armies of the two territories must be distinct"
    assert n_a > 0, "At least one unit must invade"

    result = n_a - p_a

    assert n_a - p_a <= result, f"At least the left units from the last battle must invade, i.e., {n_a} - {p_a} = {n_a - p_a}"
    assert result <= territory_units(s, t_a) - p_a - 1, "At least one unit must be left behind"

    return result


def random_uniform_invasion (s:   State,
                             t_a: Territory,
                             t_d: Territory,
                             n_a: Unit,
                             p_a: Unit) -> Unit:
    """
    The attacking and victorious units plus a random number of additional units enter the new territory.
    """
    assert isinstance(s, State)
    assert isinstance(t_a, Territory)
    assert isinstance(t_d, Territory)
    assert t_a in s.state, "The attacking territory must belong to the current state"
    assert t_d in s.state, "The defending territory must belong to the current state"
    assert territory_occupant(s, t_a) != territory_occupant(s, t_d), "The armies of the two territories must be distinct"
    assert n_a > 0, "At least one unit must invade"

    result = max(n_a - p_a, randint(1, territory_units(s, t_a) - 1))

    assert n_a - p_a <= result, f"At least the left units from the last battle must invade, i.e., {n_a} - {p_a} = {n_a - p_a}"
    assert result <= territory_units(s, t_a) - p_a - 1, "At least one unit must be left behind"

    return result


def uniform_invasion (s:   State,
                      t_a: Territory,
                      t_d: Territory,
                      n_a: Unit,
                      p_a: Unit) -> Unit:
    """
    The remaining units of the attacker are split evenly between the attacking territory and the conquered one.
    """
    assert isinstance(s, State)
    assert isinstance(t_a, Territory)
    assert isinstance(t_d, Territory)
    assert t_a in s.state, "The attacking territory must belong to the current state"
    assert t_d in s.state, "The defending territory must belong to the current state"
    assert territory_occupant(s, t_a) != territory_occupant(s, t_d), "The armies of the two territories must be distinct"
    assert n_a > 0, "At least one unit must invade"

    result = max(n_a - p_a, (territory_units(s, t_a) - p_a) // 2)

    assert n_a - p_a <= result, f"At least the left units from the last battle must invade, i.e., {n_a} - {p_a} = {n_a - p_a}"
    assert result <= territory_units(s, t_a) - p_a - 1, "At least one unit must be left behind"

    return result

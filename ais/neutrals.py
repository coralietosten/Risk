#! /bin/python
# gvim: set fileencoding=utf-8
#
# (c) September 8, 2025, José Martinez, Polytech Nantes, University of Nantes
#
# Licence:  proprietary
# The use of this library is not authorised outside the Polytechnic School of the University of Nantes.
#

"""
Neutral players are AIs, though dumb ones.
Their main characteristic is to _never_ attack, hence never invade, hence never win.
Two special behaviours/functions are defined here (and are not exported) rather than in the dedicated modules.
Nevertheless, it is possible to define strong defenders.
Indeed, the problem that the other players might have, is to face neutral players building impenetrable citadels...
"""


__all__ = [
    'strategy_neutral_fully_random',
    'strategy_neutral_uniform_random',
    ]


from typing import Tuple, Optional
from model.region import Unit
from model.army import Army
from model.territory import Territory
from model.state import State
from model.state_informations import territory_occupant
from strategy.strategy import Strategy
from strategy.reinforcements import random_reinforcement, random_uniform_reinforcement
from strategy.defenses import random_defense, maximum_defense
from strategy.maneuvers import random_maneuver, random_uniform_maneuver


def never_attack (s: State,
                  a: Army) -> Optional[Tuple[Territory, Territory, Unit]]:
    """
    A neutral army is never an attacker.
    
    :parameter s:  a current state
    :parameter a:  an army in this world, hence state too

    :return:  always 'None'
    """
    assert isinstance(s, State)
    assert isinstance(a, Army)
    assert a in s.world.armies, "the army must belong to the world"

    return None



def never_invade (s:   State,
                  t_a: Territory,
                  t_d: Territory,
                  n_a: Unit,
                  p_a: Unit) -> Unit:
    """
    Since a neutral army is never an attacker, it should not invade.
    
    :return:  *never*, raises an exception if called
    """
    assert isinstance(s, State)
    assert isinstance(t_a, Territory)
    assert isinstance(t_d, Territory)
    assert t_a in s.state
    assert t_d in s.state
    assert territory_occupant(s, t_a) != territory_occupant(s, t_d), "the armies of the two territories must be distinct"
    assert n_a > 0, "invasion requires at least one unit"

    raise Exception("A neutral army should never invade since it has never attacked")


strategy_neutral_fully_random = Strategy("neutral, fully random",
                                          random_reinforcement,
                                          never_attack,
                                          random_defense,
                                          never_invade,
                                          random_maneuver)
"""
A neutral player that plays totally at random.
"""


strategy_neutral_uniform_random = Strategy("neutral, uniform random",
                                           random_uniform_reinforcement,
                                           never_attack,
                                           maximum_defense,
                                           never_invade,
                                           random_uniform_maneuver)
"""
A neutral player that defends all of its territories uniformly and aggressively.
"""

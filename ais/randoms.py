#! /bin/python
# gvim: set fileencoding=utf-8
#
# (c) September 14, 2025, José Martinez, Polytech Nantes, University of Nantes
#
# Licence:  proprietary
# The use of this library is not authorised outside the Polytechnic School of the University of Nantes.
#

"""
Randoms players are AIs.
Most of them are expected to be dumb ones.
However, in face of such an unpredictable player, other players can have a hard time since it is impossible to adapt to them in a meaningful way.
"""


__all__ = [
    'strategy_fully_random',
    'strategy_uniform_random',
    ]


from strategy.strategy import Strategy
from strategy.reinforcements import random_reinforcement, random_uniform_reinforcement
from strategy.attacks import random_attack
from strategy.defenses import random_defense, maximum_defense
from strategy.invasions import random_uniform_invasion, uniform_invasion
from strategy.maneuvers import random_maneuver, random_uniform_maneuver


strategy_fully_random = Strategy("random, fully",
                                 random_reinforcement,
                                 random_attack,
                                 random_defense,
                                 random_uniform_invasion,
                                 random_maneuver)
"""
A player that plays totally at random.
"""


strategy_uniform_random = Strategy("random, uniform",
                                   random_uniform_reinforcement,
                                   random_attack,
                                   maximum_defense,
                                   uniform_invasion,
                                   random_uniform_maneuver)
"""
A player that plays totally at random but by uniformly distributing its units and always defending with the maximal resistance.
"""

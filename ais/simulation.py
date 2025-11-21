#! /bin/python
# gvim: set fileencoding=utf-8
#
# (c) 21 November, 2025, Bryan LEVY, Polytech Nantes, University of Nantes
#
# Licence:  proprietary
# The use of this library is not authorised outside the Polytechnic School of the University of Nantes.
#



__all__ = [
    'strategy_simulation',
    ]


from strategy.strategy import Strategy
from strategy.reinforcements import basic_reinforcement
from strategy.attacks import simulation_strategie_attack
from strategy.defenses import basic_defenses
from strategy.invasions import basic_invasion
from strategy.maneuvers import basic_maneuver


strategy_simulation = Strategy("simulation",
                                 basic_reinforcement,
                                 simulation_strategie_attack,
                                 basic_defenses,
                                 basic_invasion,
                                 basic_maneuver)
"""
A player that plays by simulating all his moves before playing.
"""



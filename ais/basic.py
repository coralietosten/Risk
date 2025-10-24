from strategy.strategy import Strategy
from strategy.reinforcements import basic_reinforcement
from strategy.attacks import basic_attack
from strategy.defenses import basic_defenses
from strategy.invasions import basic_invasion
from strategy.maneuvers import basic_maneuver


strategy_basic = Strategy("basic",
                                 basic_reinforcement,
                                 basic_attack,
                                 basic_defenses,
                                 basic_invasion,
                                 basic_maneuver)

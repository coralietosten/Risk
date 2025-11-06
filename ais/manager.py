from strategy.strategy import Strategy
from strategy.reinforcements import basic_reinforcement
from strategy.attacks import basic_attack, basic_improved_attack,manager_attack
from strategy.defenses import basic_defenses
from strategy.invasions import manager_invasion
from strategy.maneuvers import basic_maneuver, manager_maneuver


strategy_manager = Strategy("manager",
                                 basic_reinforcement,
                                 manager_attack,
                                 basic_defenses,
                                 manager_invasion,
                                 manager_maneuver)

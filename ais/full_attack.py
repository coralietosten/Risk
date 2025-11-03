from strategy.strategy import Strategy
from strategy.reinforcements import full_attack_reinforcement
from strategy.attacks import full_attack
from strategy.defenses import full_attack_defenses
from strategy.invasions import full_attack_invasion
from strategy.maneuvers import full_attack_maneuver


strategy_full_attack = Strategy("full_attack",
                                 full_attack_reinforcement,
                                 full_attack,
                                 full_attack_defenses,
                                 full_attack_invasion,
                                 full_attack_maneuver)

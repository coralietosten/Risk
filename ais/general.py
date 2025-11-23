from strategy.strategy import Strategy
from strategy.reinforcements import basic_reinforcement
from strategy.attacks import proba_attack , general_attack #ok
from strategy.defenses import basic_defenses #ok
from strategy.invasions import full_attack_invasion
from strategy.maneuvers import full_attack_maneuver


strategy_general = Strategy("general",
                                 basic_reinforcement,
                                 general_attack,
                                 basic_defenses,
                                 full_attack_invasion,
                                 full_attack_maneuver)
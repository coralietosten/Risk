#! /bin/python
# gvim: set fileencoding=utf-8
#
# (c) September 14, 2025, José Martinez, Polytech Nantes, University of Nantes
#
# Licence:  proprietary
# The use of this library is not authorised outside the Polytechnic School of the University of Nantes.
#


"""
This is the main program.
It runs the game after a random initialisation.
Two visualisation are provided:

    * one simply displays the successive states of the board, which allows to follow the situation at a glance,
    * another one shows all the details between the consecutive boards.
"""


from typing import Optional
from time import sleep
from model.region import Unit
from model.world import World
from model.state_informations import undefeated_armies, army_units, is_defeated_army
from boards.polytech_board import risk_map, risk_display
# from boards.classic_board import risk_map, risk_display
from boards.rendering import risk_colour_map, colour_map, BRIGHT_BACKGROUND_COLOUR_MAP
from ais.neutrals import strategy_neutral_fully_random, strategy_neutral_uniform_random
from ais.randoms import strategy_fully_random, strategy_uniform_random
from ais.basic import strategy_basic, strategy_basic_improved
from ais.manager import strategy_manager
from ais.full_attack import strategy_full_attack
# from ais.general import strategy_general
from game.game import game
from game.setup import random_initial_state
from strategy.attacks import arbre_proba


def format_units (n: Unit) -> str:
    """
    Simple function that formats a number of units with or without the plural ending in 's'.

    :parameter n:  a number of units

    :precondition: n >= 0

    :return: either "0 unit", "1 unit", or "n units"
    """
    assert n >= 0

    return ( f"{n} unit"  if n <= 1 else
             f"{n} units" )


def play_and_display (w:     World,
                      r_max: Optional[int]):
    """
    Plays a game and displays the consecutive turns with the full description of each turn.

    :parameter w:  a world, i.e., a board and armies
    :parameter r_max:  an optional maximal number of rounds
    """

    (text_map, legend, numbering) = risk_display()
    s_0 = random_initial_state(w)
    print("State 0")
    print(colour_map(risk_colour_map(s_0, legend, BRIGHT_BACKGROUND_COLOUR_MAP),
                     text_map.format(* [ s_0.state[s_0.world.territory(t)][1]
                                         for t in numbering ])))
    sleep(0.1)
    P = game(s_0, r_max)
    for (j, ((R, A, I, m), s_j)) in enumerate(P, start = 1):
        a = s_j.state[next(iter(R))][0]
        print(f"State {j} / {len(P)}:  Army ``{a.colour}'' turn ({a.strategy.name})")
        print("Reinforcements:")
        for t in R:
            print(f"   - ``{t.name}'' with {format_units(R[t])}")
        print("Attacks:")
        if len(A) == 0:
            print("   - None")
        else:
            for (t_a, t_d, n_a, n_d, p_a, p_d) in A:
                print(f"   - From ``{t_a.name}'' attacking ``{t_d.name}'' with {format_units(n_a)}")
                print(f"   - Defending with {format_units(n_d)}")
                print(f"   - Losses are {format_units(p_a)}, for the attacker, and {format_units(p_d)}, for the defender")
        print("Invasions:  ", end="")
        if len(I) == 0:
            print("None")
        else:
            print()
            for (t_a, t_d, n_i) in I:
                print(f"   - From ``{t_a.name}'' to ``{t_d.name}'' with {format_units(n_i)}")
        print("Maneuver:  ", end="")
        if m is None:
            print("None")
        else:
            (t_0, t_1, n) = m
            print(f"``{t_0.name}'' to ``{t_1.name}'' with {format_units(n)}")
        print(colour_map(risk_colour_map(s_j, legend, BRIGHT_BACKGROUND_COLOUR_MAP), text_map.format(* [ s_j.state[s_j.world.territory(t)][1]
                                                                                                         for t in numbering ])))
    print("undefeated armies:")
    s_f = s_0 if len(P) == 0 else P[-1][1]
    for a in sorted(undefeated_armies(s_f),
                    key = lambda a: army_units(s_f, a),
                    reverse = True):
        print(f"   - {a.colour} ({a.strategy.name}): {army_units(s_f, a)} units")


def play_and_animate (w:     World,
                      r_max: Optional[int],
                      d:     float = 0.5):
    """
    Plays a game and displays only the consecutive boards, with a delay between each frame, the default value of which is half a second.

    :parameter w:  a world, i.e., a board and armies
    :parameter r_max:  an optional maximal number of rounds
    :parameter d:  a time delay between frames of the consecutive boards
    """

    def clear_console () -> str:
        return "\033[2J\033[1;1H"

    def top_console () -> str:
        return "\033[1;1H"

    def highlight (t: str) -> str:
        return "\x1b[30;103m" + t + "\x1b[0m"

    def downlight (t: str) -> str:
        return "\x1b[37;40m" + t + "\x1b[0m"

    (text_map, legend, numbering) = risk_display()
    s_0 = random_initial_state(w)

    print(f"{clear_console()}State 0")
    print(colour_map(risk_colour_map(s_0, legend, BRIGHT_BACKGROUND_COLOUR_MAP),
                     text_map.format(* [ s_0.state[s_0.world.territory(t)][1]
                                         for t in numbering ])))
    sleep(d)
    P = game(s_0, r_max)
    A = list(s_0.world.armies)
    for (j, ((R, _, _, _), s_j)) in enumerate(P, start = 1):
        a_j = s_j.state[next(iter(R))][0]
        print(f"{top_console()}State {j} / {len(P)}: " + ", ".join([ ( highlight(t) if a == a_j                 else
                                                                       downlight(t) if is_defeated_army(s_j, a) else
                                                                       t )
                                                                     for a in A
                                                                     for t in [ f"{a.colour} ({a.strategy.name})" ] ]))
        print(colour_map(risk_colour_map(s_j, legend, BRIGHT_BACKGROUND_COLOUR_MAP), text_map.format(* [ s_j.state[s_j.world.territory(t)][1]
                                                                                                         for t in numbering ])), end="")
        sleep(d)


R_MAX = 500
"""
The maximal number of turns before stopping the game even if there is no winner.
"""


AIs = {
    -2: strategy_neutral_fully_random,
    -1: strategy_neutral_uniform_random,
    1: strategy_fully_random,
    2: strategy_basic,
    3: strategy_basic_improved,
    4: strategy_manager,
    5 : strategy_full_attack,
    # 6 : strategy_general
    }
"""
The available AIs, identified by indices in order to be selected later.
"""


GAME = [3,1,-1]
"""
A selection of the strategies to be used by different armies.
"""

import pickle
import os
if __name__ == '__main__':
    #play_and_display(World([ AIs[i] for i in GAME ], *risk_map()), R_MAX)
    #play_and_animate(World([ AIs[i] for i in GAME ], *risk_map()), R_MAX, 0.1)
    arbre= None
    if os.path.exists('file.pkl'):
        with open('file.pkl', 'rb') as file:
            arbre = pickle.load(file)
    if arbre == None:
        arbre = arbre_proba(4,3)
        with open('file.pkl', 'wb') as file:
            pickle.dump(arbre, file)
    print(arbre[1])
#! /bin/python
# gvim: set fileencoding=utf-8
#
# (c) September 8, 2025, José Martinez, Polytech Nantes, University of Nantes
#
# Licence:  proprietary
# The use of this library is not authorised outside the Polytechnic School of the University of Nantes.
#


"""
This module provides the main function, namely 'game'.
It runs full as well as truncated games.
It returns the consecutive states of the game, along with the way each turn was played, a 'Play'.
In that way, the game can be analysed *post-mortem*.
Also, it could be used for learning, or to predict possible outcomes on medium runs.
"""


__all__ = [
    'Play',
    'game',
    ]


from typing import List, Tuple, Dict, Optional
from functools import reduce
from random import randint
from model.region import Unit
from model.territory import Territory
from model.state import State
from model.state_informations import territory_units, game_over, is_defeated_army
from strategy.state_actions import do_reinforce, do_bury, do_invade, do_maneuver
# from histogram import frequency_histogram # for testing the statistics of battle w.r.t. their probabilities


Play = Tuple[Dict[Territory, Unit],
             List[Tuple[Territory, Territory, Unit, Unit, Unit, Unit]],
             List[Tuple[Territory, Territory, Unit]],
             Optional[Tuple[Territory, Territory, Unit]]]
"""
This somewhat complex type only describes the three main steps in a player's turn:

    * firstly, how it reinforces its territories,
    * next, the various battles,
    * possibly, the invasion outcomes,
    * finally, its optional last maneuver.

The first and last step have exactly the same type as the corresponding functions of their 'Strategy'.

The second one is the full list of the consecutive battles.
It contains the two confronting territories, the units of the attacker, followed by the ones of the defender, and finally the respective losses.

The third component describes all the invasions following successful battles.

:bug:  Notice that they should be interleaved with the battles, whereas they are only recorded after.
"""


def game (s:     State,
          r_max: Optional[int]) -> List[Tuple[Play, State]]:
    """
    Starting from a given state, and associating a strategy to each army, the game is played until the conquest of the world by one of the armies.
    However, in order to avoid too lengthy or even infinite games, an optional limit can be set on the number of round, 'r_max'.
    The whole game is returned, hence it can be replayed or analysed.

    :parameter s:  the initial state, which is not repeated in the result
    :parameter r_max:  the maximal number of rounds, unlimited when it is 'None'

    :return:  the sequence of states from the initial state, excluded, along with the way armies played their turns
    """
    assert isinstance(s, State)

    A = list(s.world.armies)
    j = 0
    S = [] # type: List[Tuple[Play, State]]
    while (r_max is None or j // len(A) < r_max) and not game_over(s):
        a = A[j % len(A)]
        if not is_defeated_army(s, a):
            R = a.strategy.reinforce(s, a)
            s = do_reinforce(s, R)
            K = []
            I = []
            while (k := a.strategy.attack(s, a)) is not None:
                (t_a, t_d, n_a) = k
                n_d = a.strategy.defend(s, t_a, t_d, n_a)
                (p_a, p_d) = fight_random_outcome(n_a, n_d)
                K.append((t_a, t_d, n_a, n_d, p_a, p_d))
                if p_d == territory_units(s, t_d):
                    n_i = a.strategy.invade(s, t_a, t_d, n_a, p_a)
                    s = do_invade(s, t_a, t_d, n_a, p_a, n_i)
                    I.append((t_a, t_d, n_i))
                else:
                    s = do_bury(s, t_a, t_d, p_a, p_d)
            if (m := a.strategy.maneuver(s, a)) is not None:
                (t_0, t_1, n) = m
                s = do_maneuver(s, t_0, t_1, n)
            S.append(((R, K, I, m), s))
        j = j + 1

    return S


def fight_random_outcome (n: int,
                          m: int) -> Tuple[int, int]:
    """
    This "function" takes care of conducting a single battle between the given units of two armies.
    Dice are rolled by it.
    The outcome, i.e., the number of lost units for the attacker and the defendant respectively, is returned.

    :parameter n:  the number of units of the attacker
    :parameter m:  the number of units of the defender
    
    :return:  the tuple containing the corresponding losses of the two armies, attacker first, then defender
    """

    def dice (k: int) -> List[int]:
        """
        One to three six-faces dice are rolled and their values presented in descending order.

        :parameter k:  the number of dice to roll

        :return:  a non-increasing list of 'k' dice values
        """
        assert 1 <= k <= 3

        return sorted([ randint(1, 6)
                        for _ in range(k) ], reverse=True)

    def dice_fight_outcome (v_a: int,
                            v_d: int) -> Tuple[int, int]:
        """
        Given two dice values corresponding respectively to the attacker and the defender, determines which one win or lose.

        :parameter v_a:  dice value of the attacker
        :parameter v_d:  dice value of the defender

        :return:  either (0, 1) if the defender loses, or (1, 0) if it is the attacker
        """
        return ( (0, 1) if v_a > v_d else
                 (1, 0) )

    def sum_outcomes (p: Tuple[int, int],
                      q: Tuple[int, int]) -> Tuple[int, int]:
        """
        Given two couples of integers, sums up the components pairwise.

        :parameter p:  a couple of integers
        :parameter q:  another couple of integers

        :return:  a couple consisting of the sum of the first components followed by the sum of the second components
        """
        (p_a, p_d) = p
        (q_a, q_d) = q
        return (p_a + q_a, p_d + q_d)

    assert 1 <= n <= 3, "number of attacking units between 1 and 3"
    assert 1 <= m <= 2, "number of defending units between 1 and 2"

    result = reduce(sum_outcomes, [ dice_fight_outcome(v_a, v_d)
                                    for (v_a, v_d) in zip(dice(n),
                                                          dice(m)) ])

    assert result in ( { (0, 1), (1, 0) }         if (n == 1 or m == 1) else
                       { (2, 0), (1, 1), (0, 2) } ), f"the possible outcome, {result}, are limited w.r.t. to the engaged units, {n} and {m} for the attacker and defender respectively"
    return result


# Controlling that random battles do follow the probabilities
#
# print(frequency_histogram([ fight_random_outcome(1, 1) for _ in range(10_000) ]))
# print(frequency_histogram([ fight_random_outcome(1, 2) for _ in range(10_000) ]))
# print(frequency_histogram([ fight_random_outcome(2, 1) for _ in range(10_000) ]))
# print(frequency_histogram([ fight_random_outcome(2, 2) for _ in range(10_000) ]))
# print(frequency_histogram([ fight_random_outcome(3, 2) for _ in range(10_000) ]))

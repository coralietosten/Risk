#! /bin/python
# gvim: set fileencoding=utf-8
#
# (c) September 5, 2025, José Martinez, Polytech Nantes, University of Nantes
#
# Licence:  proprietary
# The use of this library is not authorised outside the Polytechnic School of the University of Nantes.
#


"""
Prior analysis in order to determine probabilities of success on a single battle between two armies.
"""


from utilities.histogram import histogram, frequency_histogram


dice_values_1 = [ 1, 2, 3, 4, 5, 6 ]


def battle_losses_11 (a, b):
    return ( (0, 1) if a > b else
             (1, 0) )


def all_battles_11 ():
    return frequency_histogram([ battle_losses_11(a, b)
                                 for a in dice_values_1
                                 for b in dice_values_1 ])


dice_values_2 = [ (max(a, b), min(a, b))
                  for a in dice_values_1
                  for b in dice_values_1  ]


def all_battles_21 ():
    return frequency_histogram([ battle_losses_11(a, b)
                                 for (a, _) in dice_values_2
                                 for b      in dice_values_1 ])


def all_battles_12 ():
    return frequency_histogram([ battle_losses_11(a, b)
                                 for a      in dice_values_1
                                 for (b, _) in dice_values_2 ])


def battle_losses_22 (a, b, c, d):
    assert a >= b
    assert c >= d

    (p_a_max, p_d_max) = battle_losses_11(a, c)
    (p_a_min, p_d_min) = battle_losses_11(b, d)
    return (p_a_max + p_a_min, p_d_max + p_d_min)


def all_battles_22 ():
    return frequency_histogram([ battle_losses_22(a, b, c, d)
                                 for (a, b) in dice_values_2
                                 for (c, d) in dice_values_2 ])


def sorted_dice_values (a, b, c):
    M = max(a, b, c)
    m = min(a, b, c)
    i = ( max(b, c) if a == M else
          max(a, c) if b == M else
          max(a, b) )
    return (M, i, m)


dice_values_3 = [ # sorted_dice_values(a, b, c)
                  tuple(sorted([a, b, c], reverse=True))
                  for a in dice_values_1
                  for b in dice_values_1
                  for c in dice_values_1  ]


def all_battles_31 ():
    return frequency_histogram([ battle_losses_11(a, d)
                                 for (a, _, _) in dice_values_3
                                 for d         in dice_values_1 ])


def all_battles_32 ():
    return frequency_histogram([ battle_losses_22(a, b, d, e)
                                 for (a, b, _) in dice_values_3
                                 for (d, e)    in dice_values_2 ])


def histogram_to_table (h):
    return "\n".join([ f"{x}\t{h[x]}" for x in h ])


if __name__ == '__main__':
    print("Dice combination histograms")
    print("===", "1 D", "===", histogram_to_table(histogram(dice_values_1)), sep="\n")
    print("===", "2 D", "===", histogram_to_table(histogram(dice_values_2)), sep="\n")
    print("===", "3 D", "===", histogram_to_table(histogram(dice_values_3)), sep="\n")

    print("Battle outcome probabilities")
    print("A 1 vs D 1", all_battles_11())
    print("A 1 vs D 2", all_battles_12())
    print("A 2 vs D 1", all_battles_21())
    print("A 3 vs D 1", all_battles_31())
    print("A 2 vs D 2", all_battles_22())
    print("A 3 vs D 2", all_battles_32())

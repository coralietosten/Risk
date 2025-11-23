#! /bin/python
# gvim: set fileencoding=utf-8
#
# (c) September 8, 2025, José Martinez, Polytech Nantes, University of Nantes
#
# Licence:  proprietary
# The use of this library is not authorised outside the Polytechnic School of the University of Nantes.
#


"""
Several strategies are provided in order to attack an opponent army.

Notice that the pre- and post-conditions of these functions would not need to be tested.
They are already ensured by the strategies.
However, they are repeated to the programmer for clarity and documentation.
Also, this allows to detect a possible flaw closer to its source.
A model is given below.
Notice that post-conditions can be strengthen.

def model_of_attack_function (s: State,
                              a: Army) -> Optional[Tuple[Territory, Territory, Unit]]:
    '''
    :parameter s:  a current state
    :parameter a:  an army to reinforce

    :pre:  The army must belong to the current state
    :pre:  The army must not be defeated

    :post:  The attacking territory belongs to the current state
    :post:  The defending territory belongs to the current state
    :post:  The attacking territory is occupied by the army
    :post:  The defending territory is not occupied by the army
    :post:  The attacking units is between one and three
    :post:  The attacking units is strictly less than the number of available units
    '''
    # PRE-CONDITION
    assert isinstance(s, State)
    assert isinstance(a, Army)
    assert a in s.world.armies, "The army must belong to the current state"
    assert not is_defeated_army(s, a), "The army must not be defeated"

    result = DO_SOME_STUFF

    # POST-CONDITION
    if result is not None:
        (t_a, t_d, n) = result
        assert isinstance(t_a, Territory)
        assert isinstance(t_d, Territory)
        assert t_a in s.state, "The attacking territory belongs to the current state"
        assert t_d in s.state, "The defending territory belongs to the current state"
        assert territory_occupant(s, t_a) == a, "The attacking territory is occupied by the army"
        assert territory_occupant(s, t_d) != a, "The defending territory is not occupied by the army"
        assert n in { 1, 2, 3 }, "The attacking units is between one and three"
        assert n < territory_units(s, t_a), "The attacking units is strictly less than the number of available units"

    return result
"""


__all__ = [
    'random_attack',
    ]


from typing import Tuple, Optional, List, Set
from random import choice
from model.region import Unit
from model.army import Army, Armies
from model.territory import Territory
from model.state import State
from model.state_informations import territory_occupant, territory_units, is_defeated_army, territories_occupied_by_army, bordering_territories, sort_territories_by_units, undefeated_armies, probability_win_territory2, arbre_proba, arbre_proba_3

def random_attack (s: State,
                   a: Army) -> Optional[Tuple[Territory, Territory, Unit]]:
    """
    A totally random attack between any two bordering and enemy territories with any number of units.
    """
    assert isinstance(s, State)
    assert isinstance(a, Army)
    assert a in s.world.armies, "the army must belong to the current state"
    assert not is_defeated_army(s, a), "The army must not be defeated"

    A = [ (t_a, t_d, n)
          for (t_a, t_d) in s.world.adjacencies
          if territory_occupant(s, t_a) == a
          if territory_occupant(s, t_d) != a
          if (u_a := territory_units(s, t_a)) > 1
          for n in range(1, min(3, u_a - 1) + 1) ]
    
    if len(A) == 0:
        result = None
    else:
        result = choice(A)

    if result is not None:
        (t_a, t_d, n) = result
        assert isinstance(t_a, Territory)
        assert isinstance(t_d, Territory)
        assert t_a in s.state, "The attacking territory belongs to the current state"
        assert t_d in s.state, "The defending territory belongs to the current state"
        assert territory_occupant(s, t_a) == a, "The attacking territory is occupied by the army"
        assert territory_occupant(s, t_d) != a, "The defending territory is not occupied by the army"
        assert n in { 1, 2, 3 }, "The attacking units is between one and three"
        assert n < territory_units(s, t_a), "The attacking units is strictly less than the number of available units"

    return result


def basic_attack (s: State, a: Army) -> Optional[Tuple[Territory, Territory, Unit]]:
    """
    L'attaquant attaque le territoire qui possède la plus grande différence d'unité avec un de ses territoires.
    Le nombre d'unité engagé dans le combat est le maximum possible pour l'attaquant.
    """

    #precondition
    assert isinstance(s, State)
    assert isinstance(a, Army)
    assert a in s.world.armies, "the army must belong to the current state"
    assert not is_defeated_army(s, a), "The army must not be defeated"

    # l'attaquant et le défenseur ont une différence de dé maximale
    max_diff_de = 0
    A = None
    for (t_a, t_d) in s.world.adjacencies :
        if territory_occupant(s,t_a) == a and territory_occupant(s, t_d) != a : #t_a appartient à l'attaquant et t_d n'appartient pas à l'attaquant
            if territory_units(s, t_a) - territory_units(s,t_d) > max_diff_de and (territory_units(s, t_a)-1) >1: 
                max_diff_de = territory_units(s, t_a) - territory_units(s,t_d)
                A = (t_a, t_d, min(3,territory_units(s, t_a)-1))

    #post-conditions
    if A is not None:
        (t_a, t_d, n) = A
        assert isinstance(t_a, Territory)
        assert isinstance(t_d, Territory)
        assert t_a in s.state, "The attacking territory belongs to the current state"
        assert t_d in s.state, "The defending territory belongs to the current state"
        assert territory_occupant(s, t_a) == a, "The attacking territory is occupied by the army"
        assert territory_occupant(s, t_d) != a, "The defending territory is not occupied by the army"
        assert n in { 1, 2, 3 }, "The attacking units is between one and three"
        assert n < territory_units(s, t_a), "The attacking units is strictly less than the number of available units"

    return A





def full_attack (s:State, a: Army) -> Optional[Tuple[Territory, Territory, Unit]]:
    """
    Le territoire attaquant est le territoire de l'attaquant qui à le plus d'unités pouvant attaquer.
    Le territoire défenseur est le territoire qui à le plus d'unité parmis les territoires adjacents au territoire attaquant.
    Le nombre d'unité choisit pour l'attaque est le maximum possible.
    """

    #precondition
    assert isinstance(s, State)
    assert isinstance(a, Army)
    assert a in s.world.armies, "the army must belong to the current state"
    assert not is_defeated_army(s, a), "The army must not be defeated"


    A = None
    t_as = territories_occupied_by_army(s, a)
    t_as = sort_territories_by_units(s, t_as)
    for t_a in t_as :
        t_ad = bordering_territories(s, t_a[0]) #territoires adjacents 
        t_ad = sort_territories_by_units(s, t_ad) 
        for t_d in t_ad : 
            if territory_occupant(s, t_d[0]) != a  and t_a[1] > 1:
                if A == None : 
                    n = min(3,(territory_units(s, t_a[0])-1)) 
                    A = (t_a[0], t_d[0],n)
    
    #post-conditions
    if A is not None:
        (t_a, t_d, n) = A
        assert isinstance(t_a, Territory)
        assert isinstance(t_d, Territory)
        assert t_a in s.state, "The attacking territory belongs to the current state"
        assert t_d in s.state, "The defending territory belongs to the current state"
        assert territory_occupant(s, t_a) == a, "The attacking territory is occupied by the army"
        assert territory_occupant(s, t_d) != a, "The defending territory is not occupied by the army"
        assert n in { 1, 2, 3 }, "The attacking units is between one and three"
        assert n < territory_units(s, t_a), "The attacking units is strictly less than the number of available units"

    return A


def general_attack(s:State, a:Army) -> Optional[Tuple[Territory,Territory,Unit]]:
    """
    Quand il ne reste que 2 joueur : utilisation de full_attack
    Attaque des terriotires qui ont 1 unité, s'il n'y en a pas ne rien faire
    """

    #precondition
    assert isinstance(s, State)
    assert isinstance(a, Army)
    assert a in s.world.armies, "the army must belong to the current state"
    assert not is_defeated_army(s, a), "The army must not be defeated"

    A = None

    if len(list(undefeated_armies(s))) < len(list(Armies)) :
        #attaque les territoires qui ont 1 unités
        t_as = territories_occupied_by_army(s, a)
        for t_a in t_as :
            t_ad = bordering_territories(s, t_a)
            for d in t_ad :
                if territory_units(s,d) ==1 and territory_occupant(s, d) != a  and  territory_units(s,t_a) > 1 and A==None:
                    A = (t_a, d, min(3,(territory_units(s, t_a)-1)))

    if len(list(undefeated_armies(s))) <=2 :
        A =  full_attack(s, a)
    
    #post-condii=tions
    if A is not None:
        (t_a, t_d, n) = A
        assert isinstance(t_a, Territory)
        assert isinstance(t_d, Territory)
        assert t_a in s.state, "The attacking territory belongs to the current state"
        assert t_d in s.state, "The defending territory belongs to the current state"
        assert territory_occupant(s, t_a) == a, "The attacking territory is occupied by the army"
        assert territory_occupant(s, t_d) != a, "The defending territory is not occupied by the army"
        assert n in { 1, 2, 3 }, "The attacking units is between one and three"
        assert n < territory_units(s, t_a), "The attacking units is strictly less than the number of available units"
    return A


def proba_attack(s: State, a:Army) -> Optional[Tuple[Territory,Territory,Unit]]:
    """
    L'attaquant attaque avec 3 quand la probabilité de gagner contre un autre territoire est supérieur à 50% sinon il n'attaque pas
    S'il ne peut pas attaquer avec 3 il peut attaquer avec 2 ou 1
    """
    #precondition
    assert isinstance(s, State)
    assert isinstance(a, Army)
    assert a in s.world.armies, "the army must belong to the current state"
    assert not is_defeated_army(s, a), "The army must not be defeated"

    global liste_action
    global current_td
    global current_ta

    A = None
    proba_max = 0
    t_attaquant = None
    t_defender = None
    t_as = territories_occupied_by_army(s, a) 
    for t_a in t_as :
        t_ad = bordering_territories(s, t_a)
        for t in t_ad :
            if territory_occupant(s, t) != a  and territory_units(s, t_a) > 1:
                p = arbre_proba_3(territory_units(s, t_a), territory_units(s, t))[1]
                if  p > proba_max :
                    proba_max = p
                    t_attaquant = t_a
                    t_defender = t
    if proba_max >= 0.5 :
        A = (t_attaquant, t_defender, max(3, territory_units(s,t_attaquant) -1))

    #post-conditions
    if A is not None:
        (t_a, t_d, n) = A
        assert isinstance(t_a, Territory)
        assert isinstance(t_d, Territory)
        assert t_a in s.state, "The attacking territory belongs to the current state"
        assert t_d in s.state, "The defending territory belongs to the current state"
        assert territory_occupant(s, t_a) == a, "The attacking territory is occupied by the army"
        assert territory_occupant(s, t_d) != a, "The defending territory is not occupied by the army"
        assert n in { 1, 2, 3 }, "The attacking units is between one and three"
        assert n < territory_units(s, t_a), "The attacking units is strictly less than the number of available units"

    return A
                


    





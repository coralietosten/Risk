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
from model.army import Army
from model.territory import Territory
from model.state import State
from model.state_informations import territory_occupant, territory_units, is_defeated_army, territories_occupied_by_army, bordering_territories, sort_territories_by_units, undefeated_armies, probability_win_territory2
from utilities.histogram import histogram

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
    l'attaquant attaque le territoire qui possède la plus grande différence d'unité avec un de ses territoires
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
        if territory_occupant(s,t_a) == a and territory_occupant(s, t_d) != a : #t_a appartient a l'attaquant et t_d appartient pas a attaquant
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
    le territoire attaquant est le territoire de l'attaquant qui à le plus d'unités pouvant attaquer
    le territoire défenseur est le territoire qui à le plus d'unité parmis les territoires adjacents au territoire attaquant
    le nombre d'unité choisit pour l'attaque est le maximum possible
    """

    #precondition
    assert isinstance(s, State)
    assert isinstance(a, Army)
    assert a in s.world.armies, "the army must belong to the current state"
    assert not is_defeated_army(s, a), "The army must not be defeated"


    A= None
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
    if t_a[1] > 3 :
        print(probability_win_territory2(s,t_a[0], t_d[0]))
    
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
    if len(list(undefeated_armies(s))) <=2 :
        return full_attack(s, a)
    else :
        return basic_attack(s,a)

    
# --- Simulation functions ---
import numpy as np
import random

def possible_attack(a,d):
    l = []
    for i in range(1,min(4,a)):
        for j in range(1,min(3,d+1)):
            l.append((i,j))

    return l


def simulation_attack(a,d,action):
    assert action[0]<4
    assert action[1]<3

    att = []
    for _ in range(action[0]):
        att.append(random.uniform(1,6))
    defs = []
    for _ in range(action[1]):
        defs.append(random.uniform(1,6))

    att.sort(reverse=True)
    defs.sort(reverse=True)
    for i in range(min(action[0],action[1])):
        if att[i]>defs[i]:
            d-=1
        else:
            a-=1

    return a,d

SIMU = dict()
def simulation(a,d,N=1000):
    if (a,d) in SIMU : 
        return SIMU[(a,d)]
    base_a,base_d = a,d
    actions_gagnantes = []
    actions_perdantes = []
    for _ in range(N):
        a=base_a
        d = base_d
        ls_actions= []
        while a >1 and d > 0 :
            actions = possible_attack(a,d)
            ac = random.choice(actions)
            ls_actions.append(ac)
            a,d = simulation_attack(a,d,ac)
        if d==0:
            actions_gagnantes.append(ls_actions)
            
        else:
            actions_perdantes.append(ls_actions)
    SIMU[(base_a,base_d)] = (actions_gagnantes,actions_perdantes)

    return actions_gagnantes,actions_perdantes

def dic_extend(d1:dict,d2:dict):
    for k in d2.keys():
        if k in d1 : 
            d1[k] += d2[k]
        else:
            d1[k] = d2[k]
            
def globalHistogram(parties:list):
    hist= dict()
    h = dict()
    for simu in parties:
        histo = histogram(simu)

        dic_extend(h,histo)

        for k in histo.keys():
            if k in hist:
                hist[k].append(histo[k])
            else:
                hist[k] = [histo[k]]
    
    #On ajoute les clés manquantes
    for k in possible_attack(5,5):
        if k not in hist: 
            hist[k] = 0

    return h,hist

def attack_strategie(a,d,seuil_chance=0.5):
    G,P = simulation(a,d,100)
    nbG = len(G)
    nbP = len(P)
    # print((nbG/(nbG+nbP)))
    if (nbG/(nbG+nbP)) < seuil_chance:
        return None
    _,histG = globalHistogram(G)
    _,histP = globalHistogram(P)
    max_diff = (None,0)
    for i in range(3):
        ls_diff= []
        for j in range(2):
            diff = np.mean(histG[(i+1,j+1)]) - np.mean(histP[(i+1,j+1)])
            ls_diff.append(diff)
        if np.mean(ls_diff)>max_diff[1]:
            max_diff = (i+1,np.mean(ls_diff))
        # print(ls_diff)

        # print(np.mean(ls_diff))
    return max_diff[0]


def simulation_strategie_attack (s:State, a: Army) -> Optional[Tuple[Territory, Territory, Unit]]:
    #precondition
    assert isinstance(s, State)
    assert isinstance(a, Army)
    assert a in s.world.armies, "the army must belong to the current state"
    assert not is_defeated_army(s, a), "The army must not be defeated"

    A = None
    for (t_a, t_d) in s.world.adjacencies :
        if territory_occupant(s,t_a) == a and territory_occupant(s, t_d) != a : #t_a appartient a l'attaquant et t_d appartient pas a attaquant
                atts = territory_units(s,t_a)
                defs = territory_units(s,t_d)
                action = attack_strategie(atts,defs)
                if action is not None:
                    A = (t_a, t_d, action)
                    break

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





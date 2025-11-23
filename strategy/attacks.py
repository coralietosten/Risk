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

from model.state_informations import territory_occupant, territory_units, is_defeated_army, territories_occupied_by_army, bordering_territories, sort_territories_by_units, undefeated_armies, probability_win_territory2,find_path, getTerritoryByName, regions_occupied_by_army, territories_in_regions
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



def basic_improved_attack (s: State, a: Army) -> Optional[Tuple[Territory, Territory, Unit]]:
    """
    Cette fonction reprend le fonctionnement de l'attaque basique, mais prend aussi en compte 
    les armées des territoitres prédécesseurs qui sont isolé de toute attaque à l'instant t.
    """
    # l'attaquant et le défenseur ont une différence de dé maximale
    max_diff_de = 0
    A = None
    for (t_a, t_d) in s.world.adjacencies :
        if territory_occupant(s,t_a) == a and territory_occupant(s, t_d) != a : #t_a appartient a l'attaquant et t_d appartient pas a attaquant
            nb_unit = territory_units(s, t_a)
            
            if nb_unit>=3 and nb_unit - territory_units(s,t_d) > max_diff_de: 
                max_diff_de = territory_units(s, t_a) - territory_units(s,t_d)
                A = (t_a, t_d, min(3,territory_units(s, t_a)-1))

    if A is None: 
        for (t_a, t_d) in s.world.adjacencies :
            if territory_occupant(s,t_a) == a and territory_occupant(s, t_d) != a : #t_a appartient a l'attaquant et t_d appartient pas a attaquant
                safe_predecessor = getSafePredecessor(s,t_a)
                if len(safe_predecessor)>=1:
                    # a=0
                    # for t in safe_predecessor:
                    #     a+=territory_units(s,t)
                    nb_unit = territory_units(s, t_a)
                    if nb_unit >= 20 : 
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




def getSafePredecessor(s:State,t:Territory) : 
    a = territory_occupant(s,t)

    territories = bordering_territories(s,t)
    safe_predecessor = set()
    for ti in territories:
        ti_adj = bordering_territories(s,ti)
        ti_adj_a = territory_occupant(s,ti)
        if ti_adj_a == a:
            for ti_adj_i in ti_adj:
                if ti_adj_i != t:
                    ti_adj_i_a = territory_occupant(s,ti_adj_i)
                    if ti_adj_i_a == a:
                        safe_predecessor.add(ti) #On ajoute ti comme étant un prédecesseur en sécurité
    
    return safe_predecessor

def manager_attack (s: State, a: Army) -> Optional[Tuple[Territory, Territory, Unit]]:
    #precondition
    assert isinstance(s, State)
    assert isinstance(a, Army)
    assert a in s.world.armies, "the army must belong to the current state"
    assert not is_defeated_army(s, a), "The army must not be defeated"
    A=None
    
    A= invade_the_most_invades(s,a)
    
    if A is None: 
        A=invade_the_shortest(s,a)

    #post-conditions
    if A is not None:
        # print(A[0].name,A[1].name)
        # print(mini)
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


def invade_the_shortest(s:State,a:Army):
    A = None
    #On pourrait aussi regarder tous les régions adjacentes ?
    s_r = s.world.regions - regions_occupied_by_army(s,a)

    shortest_reg = None
    for r in s_r : 
        terrs = s.world.region_territories[r]
        if shortest_reg == None or len(terrs)<len(s.world.region_territories[shortest_reg]) :
            shortest_reg = r
    if shortest_reg is not None:

        mini = None
        for t in s.world.region_territories[shortest_reg]:
            t_a = territory_occupant(s,t)
            if a != t_a:
                for t2 in territories_occupied_by_army(s, a):
                    nb_t2 = territory_units(s,t2)
                    if nb_t2>=2:
                        path = find_path(s,t2,t)
                        if mini is None or len(mini)>len(path):
                            # print(path,t2.name,t.name)
                            for i in range(len(path)-1):
                                att = getTerritoryByName(s,path[i])
                                defs = getTerritoryByName(s,path[i+1])

                                if territory_occupant(s,att) ==a and territory_occupant(s,defs) !=a :
                                    if territory_units(s,att) >=2:
                                        mini = path
                                    break
        if mini is not None:
            att = None
            defs = None
            for i in range(len(mini)-1):
                att = getTerritoryByName(s,mini[i])
                defs = getTerritoryByName(s,mini[i+1])

                if territory_occupant(s,att) ==a and territory_occupant(s,defs) !=a :
                    break
            nb_att = territory_units(s,att)
            A=(att, defs, min(3,nb_att-1))
    return A


def invade_the_most_invades(s:State,a:Army):
    A = None
    s_t = territories_occupied_by_army(s,a)
    region_set = set()
    nbTerr = dict()
    for terr in s_t:
        region_set.add(terr.region)
        if terr.region not in nbTerr : 
            nbTerr[terr.region] = 0
        nbTerr[terr.region] +=1
    
    ratioReg = dict()
    maxi = (None,0)
    for reg in region_set:
        ratio =  nbTerr[reg]/len(territories_in_regions(s,reg))
        ratioReg[reg] = ratio

        if ratio>maxi[1] and ratio < 1: #On cherche la région le plus conquis mais pas completement
            maxi = (reg,ratio)

    r_terr = territories_in_regions(s,maxi[0])
    # print("---")
    mini = None
    for t in r_terr:
        t_a = territory_occupant(s,t)
        if a != t_a:
            for t2 in s_t:
                nb_t2 = territory_units(s,t2)
                if nb_t2>=2:
                    path = find_path(s,t2,t)
                    if mini is None or len(mini)>len(path):
                        # print(path,t2.name,t.name)
                        for i in range(len(path)-1):
                            att = getTerritoryByName(s,path[i])
                            defs = getTerritoryByName(s,path[i+1])

                            if territory_occupant(s,att) ==a and territory_occupant(s,defs) !=a :
                                if territory_units(s,att) >=2:
                                    mini = path
                                break
                    
    if mini is not None:
        att = None
        defs = None
        for i in range(len(mini)-1):
            att = getTerritoryByName(s,mini[i])
            defs = getTerritoryByName(s,mini[i+1])

            if territory_occupant(s,att) ==a and territory_occupant(s,defs) !=a :
                break
        nb_att = territory_units(s,att)
        A=(att, defs, min(3,nb_att-1))
    return A

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





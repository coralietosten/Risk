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


from typing import Tuple, Optional
from random import choice
from model.region import Unit
from model.army import Army
from model.territory import Territory
from model.state import State
from model.state_informations import find_path, getTerritoryByName, regions_occupied_by_army, territories_in_regions, territories_occupied_by_army, territory_occupant, territory_units, is_defeated_army,bordering_territories


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
            if territory_units(s, t_a) - territory_units(s,t_d) > max_diff_de: 
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



def basic_improved_attack (s: State, a: Army) -> Optional[Tuple[Territory, Territory, Unit]]:
    """
    Cette fonction reprend le fonctionnement de l'attaque basique, mais prend aussi en compte 
    les armées des territoitres prédécesseurs qui sont isolé de toute attaque à l'instant t.
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
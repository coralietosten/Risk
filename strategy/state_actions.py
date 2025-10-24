#! /bin/python
# gvim: set fileencoding=utf-8
#
# (c) September 4, 2025, José Martinez, Polytech Nantes, University of Nantes
#
# Licence:  proprietary
# The use of this library is not authorised outside the Polytechnic School of the University of Nantes.
#


"""
Actions that _actually_ create a new state are described here.
They are to be used only by the main program.
"""


__all__ = [
    'do_reinforce',
    'do_bury',
    'do_invade',
    'do_maneuver',
    ]


from typing import Dict
from model.region import Unit
from model.territory import Territory
from model.army import Army
from model.state import State
from model.state_informations import armies_in_territories, territory_occupant, territory_units, reinforcement_units


def do_reinforce (s: State,
                  R: Dict[Territory, Unit]) -> State:
    """
    Effectively add at least one unit on a non-empty sub-set of the territories occupied by a single army.
    """
    assert isinstance(s, State)
    assert len(R) > 0, "there is actually a reinforcement"
    assert all(t in s.world.territories for t in R), "territories to reinforce must exist"
    assert len(A := armies_in_territories(s, set(R))) == 1, "reinforcement applies to a single army"
    assert all(territory_occupant(s, t) in A for t in R), "territories must be occupied by the reinforcing army"
    assert all(territory_units(s, t) >= 1 for t in R), "territories must be occupied by at least one unit"
    assert all(R[t] > 0 for t in R), "strictly positive reinforcement units per territory"
    assert sum(R[t] for t in R) == sum(reinforcement_units(s, a) for a in A), "all the reinforcement units have to be deployed"

    result = s._replace(state = s.state | { t: (territory_occupant(s, t), territory_units(s, t) + R[t])
                                            for t in R })

    assert all(territory_units(result, t) == territory_units(s, t) + R[t] for t in R), "all the reinforced territory have been actually reinforced with the corresponding number of units"
    assert all(result.state[t] == s.state[t] for t in s.state if t not in R), "the other territories remain unchanged"

    return result


def do_bury (s:   State,
             t_a: Territory,
             t_d: Territory,
             p_a: Unit,
             p_d: Unit) -> State:
    """
    Update the state with the removal of killed units after a battle.
    """
    assert isinstance(s, State)
    assert isinstance(t_a, Territory)
    assert isinstance(t_d, Territory)
    assert t_a in s.state, "attacking territory must exist"
    assert t_d in s.state, "defending territory must exist"
    assert (t_a, t_d) in s.world.adjacencies, "attacking and defending territories must be adjacent"
    assert isinstance(a := territory_occupant(s, t_a), Army)
    assert isinstance(d := territory_occupant(s, t_d), Army)
    assert a in s.world.armies, "attacking army must exist"
    assert d in s.world.armies, "defending army must exist"
    assert a != d, "attacking and defending armies must be distinct"
    assert (p_a, p_d) in { (0, 1), (1, 0), (2, 0), (1, 1), (0, 2) }
    assert p_a < territory_units(s, t_a), "the attacking territory can never be defeated"
    assert p_d < territory_units(s, t_d), "the defending territory must not be defeated"

    result = s._replace(state = s.state | { t_a: (territory_occupant(s, t_a), territory_units(s, t_a) - p_a),
                                            t_d: (territory_occupant(s, t_d), territory_units(s, t_d) - p_d) })

    assert territory_occupant(result, t_a) == territory_occupant(s, t_a), "the attacking territory remains to the attacker"
    assert territory_occupant(result, t_d) == territory_occupant(s, t_d), "the defending territory remains to the defender"
    assert territory_units(result, t_a) == territory_units(s, t_a) - p_a, "the lost units of the attacker have been buried"
    assert territory_units(result, t_d) == territory_units(s, t_d) - p_d, "the lost units of the defender have been buried"
    assert all(result.state[t] == s.state[t] for t in s.state if t != t_a if t != t_d), "the other territories remain unchanged"

    return result


def do_invade (s:   State,
               t_a: Territory,
               t_d: Territory,
               n_a: Unit,
               p_a: Unit,
               n:   Unit) -> State:
    """
    Update the state with the resulting invasion of a territory after a victorious battle.

    :parameter s:  the current state
    :parameter t_a:  the attacking territory
    :parameter t_d:  the defending territory
    :parameter n_a:  the engaged units by the attacking army
    :parameter p_a:  the losses of the attacking army (the defending one has been destroyed)
    :parameter n:  the final number of units that are going to take place in the defending territory

    :return:  the state where the attacker has lost 'p_a' units in 't_a' and moved 'n' units from 't_a' to 't_d'
    """
    assert isinstance(s, State)
    assert isinstance(t_a, Territory)
    assert isinstance(t_d, Territory)
    assert t_a in s.state, "attacking territory must exist"
    assert t_d in s.state, "defending territory must exist"
    assert (t_a, t_d) in s.world.adjacencies, "attacking and defending territories must be adjacent"
    assert isinstance(a := territory_occupant(s, t_a), Army)
    assert isinstance(d := territory_occupant(s, t_d), Army)
    assert a in s.world.armies
    assert d in s.world.armies
    assert a != d, "attacking and defending armies must be distinct"
    assert p_a < n_a, "not all the units of the attacker have been killed"
    assert n_a - p_a <= n, f"at least the units from the last battle must invade: {n_a} - {p_a} <= {n}"
    assert 0 < n_a - p_a <= n <= territory_units(s, t_a) - p_a - 1, f"{n_a} - {p_a} <= {n} <= {territory_units(s, t_a)} - {p_a} - 1"

    result = s._replace(state = s.state | { t_a: (territory_occupant(s, t_a), territory_units(s, t_a) - p_a - n),
                                            t_d: (territory_occupant(s, t_a), n) })

    assert territory_units(result, t_a) == territory_units(s, t_a) - p_a - n, "the killed units of the attacker have been buried and its invading units have quit the attacking territory"
    assert territory_units(result, t_d) == n, "the newly win territory receives the moving units"
    assert territory_occupant(result, t_d) == territory_occupant(s, t_a), "the conquered and invaded territory is occupied by the attacking army"
    assert territory_occupant(result, t_a) == territory_occupant(s, t_a), "the attacking territory still belongs to the attacking army"
    assert all(result.state[t] == s.state[t] for t in s.state if t != t_a if t != t_d), "the other territories remain unchanged"

    return result


def do_maneuver (s:   State,
                 t_0: Territory,
                 t_1: Territory,
                 n:   Unit) -> State:
    """
    Move at least one unit from a territory to an adjacent territory belonging to the same army, leaving at least one unit behind.
    """
    assert isinstance(s, State)
    assert isinstance(t_0, Territory)
    assert isinstance(t_1, Territory)
    assert isinstance(a := territory_occupant(s, t_0), Army)
    assert t_0 in s.state
    assert t_1 in s.state
    assert isinstance(u_t0 := territory_units(s, t_0), int)
    assert isinstance(u_t1 := territory_units(s, t_1), int)
    assert u_t0 > 0
    assert u_t1 > 0
    assert (t_0, t_1) in s.world.adjacencies, "movements are limited from a territory to an adjacent one"
    assert a == territory_occupant(s, t_1), "territories must be occupied by the same army"
    assert n > 0, "at least one unit must be moved"
    assert n < u_t0, "at least one unit must stay on the initial territory"

    result = s._replace(state = s.state | { t_0: (territory_occupant(s, t_0), territory_units(s, t_0) - n),
                                            t_1: (territory_occupant(s, t_1), territory_units(s, t_1) + n) })

    assert territory_units(result, t_0) == territory_units(s, t_0) - n, "n units left the starting territory"
    assert territory_units(result, t_1) == territory_units(s, t_1) + n , "n units reached the arrival territory"
    assert all(result.state[t] == s.state[t] for t in s.state if t != t_0 if t != t_1), "the other territories remain unchanged"

    return result

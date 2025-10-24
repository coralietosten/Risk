#! /bin/python
# gvim: set fileencoding=utf-8
#
# (c) September 8, 2025, José Martinez, Polytech Nantes, University of Nantes
#
# Licence:  proprietary
# The use of this library is not authorised outside the Polytechnic School of the University of Nantes.
#


"""
A strategy is a mere container for five functions that are necessary to build an army behaviour.
"""


__all__ = [ 'Strategy' ]


from typing import Tuple, Dict, Callable, Optional
from model.region import Unit
from model.territory import Territory
from model.army import Army
from model.state import State
from model.state_informations import territory_occupant, territory_units, is_defeated_army, reinforcement_units, territories_occupied_by_army


class Strategy:
    """
    This ``pseudo'' class mainly groups five functions that, together, define the strategy of a player.
    It also ensures that:

        * the pre-conditions are met before invoking the proposed strategy, and
        * the post-conditions are also satisfied in order to certify that the strategy played along the rules.
    """

    def __init__ (self,
                  name:      str,
                  reinforce: Callable[[State, Army],                              Dict[Territory, Unit]],
                  attack:    Callable[[State, Army],                              Optional[Tuple[Territory, Territory, Unit]]],
                  defend:    Callable[[State, Territory, Territory, Unit], Unit],
                  invade:    Callable[[State, Territory, Territory, Unit, Unit],  Unit],
                  maneuver:  Callable[[State, Army],                              Optional[Tuple[Territory, Territory, Unit]]]):
        self._name      = name
        self._reinforce = reinforce
        self._attack    = attack
        self._defend    = defend
        self._invade    = invade
        self._maneuver  = maneuver

    @property
    def name (self) -> str:
        """
        A textual description of the strategy.
        """
        return self._name

    def reinforce (self,
                   s: State,
                   a: Army) -> Dict[Territory, Unit]:
        """
        Let n, with n > 0, be the number of new units to deploy to the benefit of army a.
        The reinforcement strategy consists in distributing them all over a sub-set of its territories.
        """
        assert isinstance(s, State)
        assert isinstance(a, Army)
        assert a in s.world.armies, "the army must belong to the current state"
        assert not is_defeated_army(s, a), "a defeated army cannot be reinforced"
        assert reinforcement_units(s, a) > 0, "reinforcements units have to be strictly positive"

        result = self._reinforce(s, a)

        assert all(t in territories_occupied_by_army(s, a) for t in result), "all the reinforced territories belong to the army"
        assert sum(result[t] for t in result) == reinforcement_units(s, a), "all the units have been deployed"

        return result

    def attack (self,
                s: State,
                a: Army) -> Optional[Tuple[Territory, Territory, Unit]]:
        """
        When it is its turn, an army has to decide if and which bordering territory to attack with how many units.
        This can occur repetitively.
        Since the situation has changed, based on the outcome of a previous battle, it must be reassessed each time.
        """
        assert isinstance(s, State)
        assert isinstance(a, Army)
        assert a in s.world.armies, "unknown attacking territory in the current world"

        result = self._attack(s, a)

        if result is not None:
            (t_a, t_d, n) = result
            assert t_a in s.world.territories, "unknown attacking territory in the current world"
            assert t_d in s.world.territories, "unknown defending territory in the current world"
            assert territory_occupant(s, t_a) == a, "attack must be launched from a territory belonging to the attacker"
            assert a != territory_occupant(s, t_d), "fighting units must belong to distinct armies"
            assert n > 0, "needs at least one unit to attack"
            assert n < territory_units(s, t_a), "at least one unit must stay on the attacking territory"
            assert n <= 3, "no more than three units can be used per battle"

        return result

    def defend (self,
                s:   State,
                t_a: Territory,
                t_d: Territory,
                n:   Unit) -> Unit:
        """
        When under attack by an adversary army, the defender has to decide on the number of units to oppose.
        This decision is also to be taken for every attack.
        It can change based on the state of the game.
        """
        assert isinstance(s, State)
        assert isinstance(t_a, Territory)
        assert isinstance(t_d, Territory)
        assert t_a in s.world.territories, "unknown attacking territory in the current world"
        assert t_a in s.state
        assert t_d in s.state
        assert territory_occupant(s, t_a) != territory_occupant(s, t_d), "fighting units must belong to distinct armies"
        assert t_d in s.world.territories, "unknown defending territory in the current world"
        assert n > 0, "needs at least one unit to attack"
        assert n < territory_units(s, t_a), "at least one unit must stay on the attacking territory"
        assert n <= 3, "no more than three units can be used per battle"

        result = self._defend(s, t_a, t_d, n)

        assert result > 0, "at least one unit must defend the territory under attack"
        assert result <= territory_units(s, t_d), "no more than the available troops on the defending territory can be used"
        assert result <= 2, "anyway, no more than two units can be used to defend"

        return result

    def invade (self,
                s:   State,
                t_a: Territory,
                t_d: Territory,
                n_a: Unit,
                p_a: Unit) -> Unit:
        """
        In case of a successful campaign against a territory, the attacker has to place some units there.
        The minimum is the remaining units units of the last, victorious, attack, i.e., 'n_a' - 'p_a'.
        It can be increased.
        This resembles a maneuver tactic.
        """
        assert isinstance(s, State)
        assert isinstance(t_a, Territory)
        assert isinstance(t_d, Territory)
        assert t_a in s.world.territories, "unknown attacking territory in the current world"
        assert t_d in s.world.territories, "unknown defending territory in the current world"
        assert t_a in s.state
        assert t_d in s.state
        assert territory_occupant(s, t_a) != territory_units(s, t_d), "fighting units must belong to distinct armies"
        assert n_a > 0, "at least one unit has attacked"
        assert p_a in { 0, 1 }, "no more than one unit could have been killed on the attacker side (in order to invade)"

        result = self._invade(s, t_a, t_d, n_a, p_a)

        assert result >= n_a - p_a, "at least the remaining units must take possession of the vanquished territory"
        assert result <= territory_units(s, t_a) - 1, "at least one unit must stay in the winner territory"

        return result

    def maneuver (self,
                  s: State,
                  a: Army) -> Optional[Tuple[Territory, Territory, Unit]]:
        """
        At the end of its turn, an army has to decide whether it wants to move units.
        May be, it could not since the its territories must be adjacent.
        """
        assert isinstance(s, State)
        assert isinstance(a, Army)
        assert a in s.world.armies, "the army must belong to the current state"

        result = self._maneuver(s, a)

        if result is not None:
            (t_0, t_1, n) = result
            assert t_0 in s.state
            assert t_1 in s.state
            assert territory_occupant(s, t_0) == a, "the left territory must belong to the army"
            assert territory_occupant(s, t_1) == a, "the arrival territory must belong to the army"
            assert (t_0, t_1) in s.world.adjacencies, "territories must be adjacent"
            assert n > 0, "at least one unit must move"
            assert n < territory_units(s, t_0), "at least one unit must be left behind"

        return result

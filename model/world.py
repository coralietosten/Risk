#! /bin/python
# gvim: set fileencoding=utf-8
#
# (c) September 2, 2025, José Martinez, Polytech Nantes, University of Nantes
#
# Licence:  proprietary
# The use of this library is not authorised outside the Polytechnic School of the University of Nantes.
#


"""
This module provides the translation of the relational schema of the game into classes.
Notice that the IDs of the relational schema are pointers to class instances.

An instance of the relational schema is split into:

    * permanents facts, named "World," and
    * changing situations, stored in "State," but also referencing the world.

This module is dedicated to the "World," i.e., the description of the whole relational schema but 'State'.
"""


__all__ = [
    'Adjacencies',
    'RegionAdjacencies',
    'World',
    ]


from typing import List, Dict, Tuple, Set
# import strategy.strategy as S # Strategy contains circular imports into the model
from model.region import Region, RegionName, Regions
from model.territory import Territory, TerritoryName, Territories
from model.army import Army, Colour, Armies, ARMY_COLOURS


Adjacencies = Set[Tuple[Territory, Territory]]
"""
Adjacencies is the relational way to represent edges in a graph.
"""


RegionAdjacencies = Set[Tuple[Region, Region]]
"""
Adjacencies can be extended from territories to regions.
Two bordering territories from distinct regions imply that their regions are adjacent too.
"""


class World:
    """
    The so-called world consist of all the information that remain unchanged during a game.
    It is everything except the class 'State'.
    """

    def __init__ (self,
                  G:      List['Strategy'],
                  M:      Dict[RegionName, Set[TerritoryName]],
                  Gamma:  Dict[TerritoryName, Set[TerritoryName]]):
        """
        :param G:  the list of strategies that are going to play against each other
        :param M:  the map of the world, as regions containing territories
        :param Gamma:  the (maybe _partial_) bordering relationship between territories 

        :pre:  there must be at least one strategy/army, as a limit case
        :pre:  there are at least as many territories as armies
        :pre:  the graph has to be connected, minimally no Gamma is empty
        :pre:  the graph has to be connected, minimally any territory of a region appears in Gamma

        :post:  The number of armies is the number of strategies
        :post:  The regions is the domain of the map
        """
        assert len(G) >= 1, "there must be at least one strategy/army, as a limit case"
        assert len({ t
                     for r in M
                     for t in M[r] }) >= len(G), "there are at least as many territories as armies"
        assert all(Gamma[t] != set()
                   for t in Gamma), "the graph has to be connected, minimally no Gamma is empty"
        assert all(t in Gamma
                   for r in M
                   for t in M[r]), "the graph has to be connected, minimally any territory of a region appears in Gamma"

        A = { c: Army(c, g)
              for (c, g) in zip(ARMY_COLOURS, G) }
        R = { r: Region(r, (n := len(M[r])) // 2 + n % 2)
              for r in M }
        T = { t: Territory(t, R[r])
              for r in M
              for t in M[r] }
        D = { (T[t1], T[t2])
              for t1 in Gamma
              for t2 in Gamma[t1]
              if t1 != t2 } | { (T[t2], T[t1])
                                for t1 in Gamma
                                for t2 in Gamma[t1]
                                if t1 != t2 } # adjacencies ensured irreflexive and symmetrical
        self._armies_index = A
        self._armies = { A[a] for a in A }
        self._regions_index = R
        self._regions = { R[r] for r in R }
        self._territories_index = T
        self._territories = { T[t] for t in T }
        self._adjacencies = D
        self._region_adjacencies = { (t.region, s.region)
                                      for (t, s) in D }
        self._region_territories = { R[r]: { T[t]
                                              for t in T
                                              if T[t].region == R[r] } # R[r] rather than r previously: NO thanks to mypy and pyright!
                                      for r in R }

        assert len(self.armies) == len(G), "The number of armies is the number of strategies"
        assert len(self.regions) == len(M), "The regions is the domain of the map"
        assert { r.name for r in self.regions } == set(M), "The regions is the domain of the map"
        assert len(self.territories) == sum(len(M[r]) for r in M)
        assert { t.name for t in self.territories } == { t for r in M for t in M[r] }
        assert { (t.name, s.name) for (t, s) in self.adjacencies } == { (t, s) for t in Gamma for s in Gamma[t] } | { (s, t) for t in Gamma for s in Gamma[t] }
        assert all(any(t.region == r and u.region == s for (t, u) in self.adjacencies) for (r, s) in self.region_adjacencies)
        assert { r.name:  { t.name for t in self.region_territories[r] } for r in self.region_territories } == M
        assert all(isinstance(self.region(r), Region) for r in M)
        assert all(isinstance(self.territory(t), Territory) for t in Gamma)

    @property
    def armies (self) -> Armies:
        """
        From one (!) to six armies fighting against each other on the board.
        """
        return self._armies

    @property
    def regions (self) -> Regions:
        """
        The regions of the used board.
        """
        return self._regions

    @property
    def territories (self) -> Territories:
        """
        The territories of the used board.
        """
        return self._territories

    @property
    def adjacencies (self) -> Adjacencies:
        """
        The borders between territories as pairs of territories.
        """
        return self._adjacencies

    @property
    def region_adjacencies (self) -> RegionAdjacencies:
        """
        The quotient set of territory adjacencies to their including regions.
        """
        return self._region_adjacencies

    @property
    def region_territories (self) -> Dict[Region, Set[Territory]]:
        """
        This is the regional view of the world.
        To each region are associated all of its territories.
        """
        return self._region_territories

    def army (self,
              a: Colour) -> Army:
        """
        Each army is externally identified by its colour.
        This function allows to retrieve it, i.e., its 'ID', based on its colour.
        """
        assert isinstance(a, Colour)
        assert a in self._armies_index

        return self._armies_index[a]

    def region (self,
                r: RegionName) -> Region:
        """
        Each region is externally identified by its name.
        This function allows to retrieve it, i.e., its 'ID', based on its name.
        """
        assert isinstance(r, RegionName)
        assert r in self._regions_index

        return self._regions_index[r]

    def territory (self,
                   t: TerritoryName) -> Territory:
        """
        Each territory is externally identified by its name.
        This function allows to retrieve it, i.e., its 'ID', based on its name.
        """
        assert isinstance(t, TerritoryName)
        assert t in self._territories_index

        return self._territories_index[t]

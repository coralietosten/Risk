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

This module is dedicated to the 'Territory' relation.
"""


__all__ = [
    'TerritoryName',
    'Territory',
    'Territories',
    'TerritoriesIndex',
    ]


from typing import Set, Dict, TypeAlias
from model.region import Region


TerritoryName: TypeAlias = str
"""
Each territory is identified by a name.
"""


class Territory:
    """
    This class implements the following functional dependencies:

    > Territory: Territory <-> Territory.name;
    > Territory -> Region;
    """
    def __init__ (self,
                  t: TerritoryName,
                  r: Region):
        assert t != "", "a territory name cannot be null"

        self._name = t
        self._region = r

    @property
    def name (self) -> TerritoryName:
        """
        The name of a territory is its natural key.
        """
        return self._name

    @property
    def region (self) -> Region:
        """
        Each territory belongs to one, and only one, region.
        """
        return self._region

    def __eq__ (self, other) -> bool:
        """
        Since the name is a natural identifier, equality is based on comparing them, not the regions that they belong to.
        """
        return isinstance(other, Territory) and self.name == other.name

    def __hash__ (self) -> int:
        """
        Turned hashable to be used in sets and dictionaries.
        """
        return hash(self.name)


Territories = Set[Territory]
"""
Regions from a set, hopefully a non empty one.
"""


TerritoriesIndex = Dict[TerritoryName, Territory]
"""
As a relation, a set of territories is a mapping from their name to their full contents.
"""

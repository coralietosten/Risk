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

This module is dedicated to the "Region" relation.
"""


__all__ = [
    'Unit',
    'RegionName',
    'Region',
    'Regions',
    'RegionsIndex',
    ]


from typing import Set, Dict, TypeAlias


RegionName: TypeAlias = str
"""
Regions are sub-sets of connected territories.
"""


Unit: TypeAlias = int
"""
Unit corresponds to the number of units.
It appears in different roles:  bonuses, occupation, attack, etc.
It is identified to strictly positive natural integers.
"""


class Region:
    """
    This class implements the functional dependencies:

    > Region: Region <-> Region.name;
    > Region -> Value;
    """
    def __init__ (self,
                  r: RegionName,
                  v: Unit):
        assert r != "", "region name cannot be null"
        assert v > 0, "each contient must provide a strictly positive value"

        self._name = r
        self._value = v

    @property
    def name (self) -> RegionName:
        """
        The name of a region is a natural identifier.
        """
        return self._name

    @property
    def value (self) -> Unit:
        """
        A region is worth a bonus of units when it is entirely occupied by a single army.
        """
        return self._value

    def __eq__ (self, other) -> bool:
        """
        Equality between regions depends only on their names, not their associated values.
        """
        return isinstance(other, Region) and self.name == other.name

    def __hash__ (self) -> int:
        """
        Since regions have to be stored in sets, or dictionaries, they have to be made hashable.
        """
        return hash(self.name)


Regions = Set[Region]
"""
Regions form a set, hopefully a non empty one.
"""


RegionsIndex = Dict[RegionName, Region]
"""
As a relation, a set of regions is a mapping from their names to their full contents.
"""

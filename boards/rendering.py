#! /bin/python
# gvim: set fileencoding=utf-8
#
# (c) August 29, 2025, José Martinez, Polytech Nantes, University of Nantes
#
# Licence:  proprietary
# The use of this library is not authorised outside the Polytechnic School of the University of Nantes.
#


"""
A simple way to draw a board and its current state in text mode in an ANSI console.
"""


from typing import Dict, TypeAlias, List
from model.territory import TerritoryName
from model.state import State


TextMap = str
"""
A textual map is a multi-line string.
Some of the characters can represent some territory.
"""


Char: TypeAlias = str
"""
A mere alias to emphasise the fact that the underlying string contains exactly one character.
"""


Legend = Dict[Char, TerritoryName]
"""
The legend is a mapping from some characters to their associated territory.
"""


Numbering = List[TerritoryName]
"""
Numbering is a ``mapping'' from (implicit) integers, i.e., the indices, to territories.
More precisely, those integers are place-holders in the textual map.
"""

Colour = str
"""
A colour is an ANSI code, i.e., a sub-string.
"""


ColourMap = Dict[Char, Colour]
"""
A colour map associates to some characters a colour.
"""


BACKGROUND_COLOUR_MAP = {
    "black":   "\033[40m",
    "white":   "\033[47m",
    "red":     "\033[41m",
    "yellow":  "\033[43m",
    "green":   "\033[42m",
    "cyan":    "\033[46m",
    "blue":    "\033[44m",
    "magenta": "\033[45m",
    }
"""
A colour map that associates to meaningful colour names their corresponding ANSI code sequence.
"""


BRIGHT_BACKGROUND_COLOUR_MAP = {
    "black":   "\033[100m",
    "white":   "\033[107m",
    "red":     "\033[101m",
    "yellow":  "\033[103m",
    "green":   "\033[102m",
    "cyan":    "\033[106m",
    "blue":    "\033[104m",
    "magenta": "\033[105m",
    }
"""
Another colour map with bright colours.
"""


RESET_COLOUR = '\033[0m'
"""
ANSI code that removes colouring in the following characters.
"""


def risk_colour_map (s: State,
                     legend: Legend,
                     colouring: ColourMap) -> ColourMap:
    """
    Composition of the labels of a map with the colour of the occupying army, through the territories and their occupant.
    More precisely, to characters are associated territories, thanks to the 'legend' parameter.
    Territories are occupied by armies, which have a colour.
    Then, through the 'colouring' parameter, this colour is associated to the ANSI code sequence.
    Finally, to some of the characters appearing in a map, we associate the colour of its occupying army in the current state.
    """
    assert isinstance(s, State)
    assert all(legend[c] in { t.name for t in s.world.territories }
               for c in legend), "Territories in legend must be known in the Risk world"

    return { c: colouring[a]
             for c in legend
             if (a := s.state[s.world.territory(legend[c])][0].colour) in colouring }


def colour_map (colouring: ColourMap,
                text:      str) -> str:
    """
    Adding colours to some characters of a string based on a partial colour map from characters to ANSI codes.
    """
    return "".join([ c if c not in colouring else (colouring[c] + c + RESET_COLOUR)
                     for c in text ])

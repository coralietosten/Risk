#! /bin/python
# gvim: set fileencoding=utf-8
#
# (c) August 29, 2025, José Martinez, Polytech Nantes, University of Nantes
#
# Licence:  proprietary
# The use of this library is not authorised outside the Polytechnic School of the University of Nantes.
#


# pylint: disable=invalid-name


"""
This module describes the board for the Risk game adapted to the world of Polytech Nantes.
"""


__all__ = [
    'risk_map',
    'risk_display',
    ]


from typing import Tuple, Dict, Set
from model.region import RegionName
from model.territory import TerritoryName
from boards.rendering import TextMap, Legend, Numbering


# Regions


iht = "IHT"
isitem = "Isitem"
ireste = "Ireste"
gavy = "Gavy"


# Territories


si = "Service informatique"
lsh = "Langues et sciences humaines"
peip = "Peip"

bureaux = "Bureaux"
hall = "Hall d'entrée"
chaud = "Salles chaudes"
froid = "Salles froides"

amphi = "Amphithéâtres"
direction = "Direction"
info = "Département d'informatique"
eon = "Département d'électronique"
machines = "Salles des machines"
srt = "Département S.R.T."

mer = "Océan Atlantique"
biere = "Laboratoire de bière bleue"
labo = "Laboratoires"
degustation = "Dégustation"


def risk_map () -> Tuple[Dict[RegionName, Set[TerritoryName]], Dict[TerritoryName, Set[TerritoryName]]]:
    """
    A map is essentially described as a graph.
    This is the second component of the result, as a graph of successors.
    Furthermore, territories are grouped into regions.
    This information is given by the first component of the result.
    """
    regional_nodes = {
        iht:    { si, lsh, peip },
        isitem: { bureaux, hall, chaud, froid, machines },
        ireste: { amphi, direction, info, eon, srt },
        gavy:   { mer, biere, labo, degustation },
        }
    Gamma = {
        si:          { lsh, peip },
        lsh:         { si, peip, bureaux },
        peip:        { si, lsh, amphi, hall, mer },
        bureaux:     { lsh, chaud, hall },
        chaud:       { bureaux, froid },
        froid:       { chaud, hall },
        hall:        { bureaux, froid, amphi, peip },
        amphi:       { peip, hall, direction, machines },
        direction:   { amphi, eon, labo},
        machines:    { amphi, info, eon },
        info:        { machines, eon },
        eon:         { machines, direction, srt, info },
        srt:         { eon },
        mer:         { biere, peip, direction },
        biere:       { mer, degustation, labo },
        degustation: { biere, labo },
        labo:        { biere, degustation },
        }
    return (regional_nodes, Gamma)


def risk_display () -> Tuple[TextMap, Legend, Numbering]:
    """
    In order to display a board, we return three values:

        * a textual map as a multi-line string,
        * a mapping from characters used to represent territories into their names,
        * a list of territory names that represent the place-holder where the number of units in a given state is to be displayed.
    """
    text_map = \
"""
 ...: iht :.........................      ...: isitem :.............................
:{00:6} SSSSSSSS  {01:6} HHHHHHHHHH :    :{02:6}  BBBBBBBBBBB    {03:6}  CCCCCCCCCC :
:       S s.i. S---------H l.s.h. H--------------BB bureaux BB---------CCCC chaud   :
:       SSSSSSSS         HHHHHHHHHH :    :        BBBBBBBBBBB            CCCCCCCCCC :
:         |               |         :    :           |                       |      :
:{04:6} PPPPPPPPPPPPPPPPPPPPP       :    :{05:6}  EEEEEE         {06:6}  FFFFFFFFFF :
:        PPPP p.e.i.p. PPPPP----------------------EE entrée------------FFFFF froid  :
:         PPPPPPPPPPPPPPPP          :    :      EEE    EEE               FFFFFFFFFF :
 ................|...|..............     :       EEEEEEE                            :
                 |   |                    ........|.................................
                 |   |                            |
                 |   |         ...: ireste :......|...............................
                 |   |        :{07:6} AAAAAAAAAAAAAA  {08:6}  DDDDDDDDDDDDDDD     :
                 |   +-----------------AA amphis AA----------DDD direction DDD-------+
                 |            :         AAAAAAAAAA            DDDDDDDDDDDDDDD     :  |
                 |            :             |                       |             :  |
                 |            :{09:6} MMMMMMMMMMMM         +--------+             :  |
                 |            :       M machines M-----+   |            T    T    :  |
                 |            :       MMMMMMMMMMMM     |   |            T    T    :  |
                 |            :           |            |   |            T    T    :  |
                 |            :{10:6} IIIIIIII {11:6}  OOOOO   {12:6} TTTTTTTTTT  :  |
                 |            :       I info I--------O éon O--------TT s.r.t. TT :  |
                 |            :       IIIIIIII         OOOOO          TTTTTTTTTT  :  |
                 |            :     IIIIIIII           O   O                      :  |
                 |             ...................................................   |
 ...: heinlex :..|...................                                                |
:{13:6} RR RR RR |  RR RR RR RR RR   :                                               |
:       R  R  R mer R  R  R  R  R    :                                               |
:      RRRRRRRRRRRRRRRRRRRRRRRRRRRR  :                                               |
:          |                         :                                               |
:{14:6} XXXXXXXX  {15:6} LLLLLLLLLLL :                                               |
:       X b.b. X---------LL labos LL-------------------------------------------------+
:       XXXXXXXX         LLLLLLLLLLL :
:          |               |         :
: {16:6} GGGGGGGGGGGGGGGGGGGGG       :
:        GGG  dégustation  GGG       :
:        GGGGGGGGGGGGGGGGGGGGG       :
 ....................................
 """
    legend = {
        'A': amphi,
        'B': bureaux,
        'C': chaud,
        'D': direction,
        'E': hall,
        'F': froid,
        'G': degustation,
        'H': lsh,
        'I': info,
        'L': labo,
        'M': machines,
        'O': eon,
        'P': peip,
        'R': mer,
        'S': si,
        'T': srt,
        'X': biere,
        }
    numbering = [
        si,
        lsh,
        bureaux,
        chaud,
        peip,
        hall,
        froid,
        amphi,
        direction,
        machines,
        info,
        eon,
        srt,
        mer,
        biere,
        labo,
        degustation,
        ]
    return (text_map, legend, numbering)

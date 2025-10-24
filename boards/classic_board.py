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
This module describes the classical board of the Risk game.
It has the same functions as the Polytech one and can be used as a replacement for the aficionados.
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


North_America = "North America"
South_America = "South America"
Europe = "Europe"
Africa = "Africa"
Asia = "Asia"
Australia = "Australia"


# Territories


Afghanistan = "Afghanistan"
Alaska = "Alaska"
Alberta = "Alberta"
Argentina = "Argentina"
Brazil = "Brazil"
Central_America = "Central America"
China = "China"
Congo = "Congo"
East_Africa = "East Africa"
Eastern_Australia = "Eastern Australia"
Eastern_United_States = "Eastern United States"
Egypt = "Egypt"
Great_Britain = "Great Britain"
Greenland = "Greenland"
Iceland = "Iceland"
India = "India"
Indonesia = "Indonesia"
Irkutsk = "Irkutsk"
Japan = "Japan"
Kamchatka = "Kamchatka"
Madagascar = "Madagascar"
Middle_East = "Middle East"
Mongolia = "Mongolia"
New_Guinea = "New Guinea"
North_Africa = "North Africa"
Northern_Europe = "Northern Europe"
Northwest_Territory = "Northwest Territory"
Ontario = "Ontario"
Peru = "Peru"
Quebec = "Quebec"
Scandinavia = "Scandinavia"
Siam = "Siam"
Siberia = "Siberia"
South_Africa = "South Africa"
Southern_Europe = "Southern Europe"
Ukraine = "Ukraine"
Ural = "Ural"
Venezuela = "Venezuela"
Western_Australia = "Western Australia"
Western_Europe = "Western Europe"
Western_United_States = "Western United States"
Yakutsk = "Yakutsk"


def risk_map () -> Tuple[Dict[RegionName, Set[TerritoryName]], Dict[TerritoryName, Set[TerritoryName]]]:
    """
    A map is essentially described as a graph.
    This is the second component of the result, as a graph of successors.
    Furthermore, territories are grouped into regions.
    This information is given by the first component of the result.
    """
    regional_nodes = {
        North_America: { Alaska, Alberta, Central_America, Eastern_United_States, Greenland, Northwest_Territory, Ontario, Quebec, Western_United_States },
        South_America: { Argentina, Brazil, Peru, Venezuela },
        Europe:        { Great_Britain, Iceland, Northern_Europe, Scandinavia, Southern_Europe, Ukraine, Western_Europe },
        Africa:        { Congo, East_Africa, Egypt, Madagascar, North_Africa, South_Africa },
        Asia:          { Afghanistan, China, India, Irkutsk, Japan, Kamchatka, Middle_East, Mongolia, Siam, Siberia, Ural, Yakutsk },
        Australia:     { Eastern_Australia, Indonesia, New_Guinea, Western_Australia },
        }
    gamma = {
        Afghanistan:           { Ukraine, Ural, China, India, Middle_East },
        Alaska:                { Northwest_Territory, Alberta, Kamchatka },
        Alberta:               { Alaska, Northwest_Territory, Ontario, Western_United_States },
        Argentina:             { Brazil, Peru },
        Brazil:                { Venezuela, Argentina, Peru, North_Africa },
        Central_America:       { Western_United_States, Eastern_United_States, Venezuela },
        China:                 { Afghanistan, Ural, Siberia, Mongolia, India, Siam },
        Congo:                 { North_Africa, East_Africa, South_Africa },
        East_Africa:           { Egypt, Congo, South_Africa, North_Africa, Madagascar, Middle_East },
        Eastern_Australia:     { New_Guinea, Western_Australia },
        Eastern_United_States: { Ontario, Quebec, Western_United_States, Central_America },
        Egypt:                 { Southern_Europe, North_Africa, East_Africa, Middle_East },
        Great_Britain:         { Iceland, Western_Europe, Northern_Europe, Scandinavia },
        Greenland:             { Northwest_Territory, Ontario, Quebec, Iceland },
        Iceland:               { Greenland, Great_Britain, Scandinavia },
        India:                 { Afghanistan, China, Siam, Middle_East },
        Indonesia:             { Siam, New_Guinea, Western_Australia },
        Irkutsk:               { Siberia, Yakutsk, Kamchatka, Mongolia },
        Japan:                 { Kamchatka, Mongolia },
        Kamchatka:             { Yakutsk, Irkutsk, Mongolia, Japan, Alaska },
        Madagascar:            { East_Africa, South_Africa },
        Middle_East:           { Ukraine, Afghanistan, India, East_Africa, Egypt, Southern_Europe },
        Mongolia:              { Siberia, Irkutsk, Kamchatka, Japan, China },
        New_Guinea:            { Indonesia, Eastern_Australia, Western_Australia },
        North_Africa:          { Brazil, Western_Europe, Southern_Europe, Egypt, East_Africa, Congo },
        Northern_Europe:       { Great_Britain, Ukraine, Scandinavia, Western_Europe, Southern_Europe },
        Northwest_Territory:   { Alaska, Alberta, Ontario, Greenland },
        Ontario:               { Northwest_Territory, Alberta, Western_United_States, Eastern_United_States, Quebec, Greenland },
        Peru:                  { Venezuela, Brazil, Argentina },
        Quebec:                { Ontario, Eastern_United_States, Greenland },
        Scandinavia:           { Iceland, Ukraine, Northern_Europe, Great_Britain },
        Siam:                  { India, China, Indonesia },
        Siberia:               { Ural, China, Mongolia, Irkutsk, Yakutsk },
        South_Africa:          { Congo, East_Africa, Madagascar },
        Southern_Europe:       { Western_Europe, Northern_Europe, Ukraine, Egypt, North_Africa, Middle_East },
        Ukraine:               { Ural, Afghanistan, Middle_East, Southern_Europe, Northern_Europe, Scandinavia },
        Ural:                  { Ukraine, Afghanistan, China, Siberia },
        Venezuela:             { Central_America, Brazil, Peru },
        Western_Australia:     { Indonesia, New_Guinea, Eastern_Australia },
        Western_Europe:        { Great_Britain, Northern_Europe, Southern_Europe, North_Africa },
        Western_United_States: { Alberta, Ontario, Eastern_United_States, Central_America },
        Yakutsk:               { Siberia, Irkutsk, Kamchatka },
        }
    return (regional_nodes, gamma)


def risk_display () -> Tuple[TextMap, Legend, Numbering]:
    """
    In order to display a board, we return three values:

        * a textual map as a multi-line string,
        * a mapping from characters used to represent territories into their names,
        * a list of territory names that represent the place-holder where the number of units in a given state is to be displayed.
    """
    text_map = \
"""
     aaaa             bbbbbbbb  bb              cccccccccccccccc |                pppppp           |BB  BB  BBCCCCCCCCCCDDDDDDDDDDDDDDDDFFFFFFFF              
...aaa  aaaaaaaabbbbbbb      bbbbbbb............c          c     |              ppp    ptttt   tt  +BBBBBBBBBBC        CD            DFFF      FFFFFFFFFFFFF...
   a           ab                 bb        ... ccccc    ccc +---+              p  pppppt  t  ttttttB        BC        CD        DDDDDF                  FFF  
   a           ab                  bbb  ....       .c    c   |  nnnnn..........pp  p  ppt  tttt    tB        BC        CD        DFFFFF                  F  FF
   a           abbbbbbbbbbbbbbbbbbbbbb .          . cccccc......nn  n          p ppp  ppt  tttt    tB        BC    CCCCCDDDDDDDDDDF                  FFFFF  FF
   a           aaaddddddddddddddee    .   ffff   .    cc     |   nnnn...oo   ppp p    ttt          tB        BC   CCEEEEEEEEEEEEEEF                  F        
   aaaaaaaaaaaaaaad            dee   .    f  f  .     cc     |          oo...ppp p    tt           tB        BC   CCE            EF    FFFFFFFFFFFFFFF        
     aa         aad            deeeeee    f  fff             |        oooo     p p  rrrt           tB        BC   CEE            EF    F        FF            
     aa         aad            de    e    f    f             |        o  o     ppp  r rt       tttttBBBBB    BC   CE     EEEEEEEEEFFF  F        FF            
                aad           dde    eeefff    fff           |        o  ooo..rrrrrrr rt       tGGGGGGGGBB   BC  CCE     EHHHHHHHHHHF  FFF       .            
                aaddd         dde      ef      fff           |        oooooo  r       rt       tG      GBBBBBBCCCCEEEEEEEEH        HFFFFFF       .            
                    d         dde      ef      f  ff         |            qqqqr       rt       tG      GGGGGBBIIIIIIIIHHHHH        HHHHH        JJ            
                    ddddddddddddeeeeeeeef      f  ff         |            q  qrrrrrrrrrtttt    tGGG        GBBI      IHHH              H      JJJJJ           
                    gggggggggggggghhhh  f      f             |           qq  qsssssssssssst    t  G        GGGI      IIIH              H......J  JJ           
                    g            gh  h  ffffffff             |          qq  qqs          st  ttt  G         GGI        IHHHHHHHHHHHHHHHH    JJJ JJ            
                    g            gh  hhhhhhh                 |      qqqqq  qq s  ssss    st  t    G          GI        IIIIIIIIIIIII        J  JJ                
                    ggg          gh      hhh                 |      q     qq  ssss  s  ssstttt    GGGGGGGGGGGGI                IIIII      JJJ  J                 
                      g         ggh      h                   |      qq   qq     ss  s  sAAAAAAAAAAAAKKKKKKGGGGI                I  II    JJJ    J                 
                      g      gggghh      h                   |       qqqqq      ss  ssssAA         AK    KGGGGIII              I  II    JJ  JJJ                 
                      g      ghhhh       h                   +---------+uuuuuuu .   .    AA        AK    KKKKKKKI              I         JJJJ                  
                      ggg    gh    hhhhhhh                   |          u     uu    .     A        AK          KIII            I
                        g    gh    h  hh                     |        uuu      uuuvvvvvvvvA        AK          KKKI            I
                        gggggghhhhhh  hh                     |        u          uv      vAAA      AKKKKK        KIIIIIIIIIII  I
                           iiiii                             |      uuu          uv      v  AAA    A    K        KKKLLLLLLLLI  I                              
                           ii  i                             |      u            uv      v    A    A    KKK      KKKL      LIIII                              
                           ii  i                             |      u            uv      vvv  AA   A      K      K  L      L                                  
                           iii i                             |      u            uvvvvvvvvvv   A  AA      KKK  KKK  L    LLL                                  
                            ii iiiiii                        |      u            uuuwwwwwwww   AAAA         K KK    L    L                                    
                            ii      iiii  +------------------+--+ . u              uw      w....AA          K KK    LLLLLL                                    
                             iiiiii    iiijjjj                  |.  u              uw      www  |           KK        . LL +------------------                
                                  iiiiiiiij  j                  .   uuu           uuwww      w  +---+       KK        . LL |   MMM                            
                                +------+jjj  jjjjj             .|     u          uxxxxw      www    |         KK   +--.----+ MM MM     NNNN                    
                                |       jjj    jjj            . |     uuuuuuuuuuuux  xw    wwwww    |         KK   |  MM    MM MMM     N  N                    
                                |      kkkjj   jmmmmmmmm     .  |               xxx  xw   ww        |              |    MMMMM  M.....NNN  NNN                    
                                |      k kkjjjjjm      m    .   |               x    xw   ww.       +--------------+    MM    MM    .NNNNN NN                    
                                |      k  kkkkmmm      mmmmm    |               xx   xw   ww .                     |     MMMMMM.  ..     NNNN                  
                                |      kk    kmmm        mmm    |               yxxxxxwwwwww  .                    |           . .       . NN                  
                                |       kk   kkkm        m      |               yyyyyyyyyyyy  zzzz                 |           ..       .                      
                                |        kkkkkkkm        m      |               y        yyy  z zz                 |           .  PPPPPPPP                    
                                |           llkkkkm      m      |               yy       y    z z                  |          OOOOP      PPP                  
                                |           llkkkkmmmmmmmm      |                yy      y....z z                  |          O  OPPPPP    P                  
                                |           llllllllll          |                 y      y    z z                  |        OOO  OOOOOP    PPP                
                                |           l      lll          |                 y    yyy    zzz                  |        OOO      OP      P                
                                |           l      l            |                 y    y                           |          O      OPP     P                
                                |           l    lll            |                 y  yyy                           |          OOOOOOOOOP     P                
                                |           llllll              |                 yyyy                             |          OOOO     PPPPPPP 
"""
    legend = {
        'a': Alaska,
        'b': Northwest_Territory,
        'c': Greenland,
        'd': Alberta,
        'e': Ontario,
        'f': Quebec,
        'g': Western_United_States,
        'h': Eastern_United_States,
        'i': Central_America,
        'j': Venezuela,
        'k': Peru,
        'l': Argentina,
        'm': Brazil,
        'n': Iceland,
        'o': Great_Britain,
        'p': Scandinavia,
        'q': Western_Europe,
        'r': Northern_Europe,
        's': Southern_Europe,
        't': Ukraine,
        'u': North_Africa,
        'v': Egypt,
        'w': East_Africa,
        'x': Congo,
        'y': South_Africa,
        'z': Madagascar,
        'A': Middle_East,
        'B': Ural,
        'C': Siberia,
        'D': Yakutsk,
        'E': Irkutsk,
        'F': Kamchatka,
        'G': Afghanistan,
        'H': Mongolia,
        'I': China,
        'J': Japan,
        'K': India,
        'L': Siam,
        'M': Indonesia,
        'N': New_Guinea,
        'O': Western_Australia,
        'P': Eastern_Australia,
        }
    return (text_map, legend, [])

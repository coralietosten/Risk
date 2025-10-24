#! /bin/python
# gvim: set fileencoding=utf-8
#
# (c) 2011, February 9, 2023, José Martinez, Polytech Nantes, Nantes University
#
# Licence:  proprietary
# The use of this library is not authorised outside the Polytechnic School of the University of Nantes.
#


"""
Very basic statistics.
"""


__all__ = [
    'histogram',
    'frequency_histogram',
    ]


from typing import List, Any, Dict


def histogram (X:  List[Any]) -> Dict[Any, int]:
    """
    Builds the histogram of the values of the list.
    The time complexity is in O(len(X)) thanks to the average constant complexity of accessing Python's dictionaries.
    """
    h = {} # type: Dict[Any, int]
    for x in X:
        if x in h:
            h[x] += 1
        else:
            h[x]  = 1
    return h


def frequency_histogram (X: List[Any]) -> Dict[Any, float]:
    """
    Builds the frequency histogram of the values of the list.
    """
    n = len(X)
    h = histogram(X)
    return { x: h[x] / n
             for x in histogram(X) }

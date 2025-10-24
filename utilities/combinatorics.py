#! /bin/python
# gvim: set fileencoding=utf-8
#
# (c) September 4, 2025, José Martinez, Polytech Nantes, University of Nantes
#
# Licence:  proprietary
# The use of this library is not authorised outside the Polytechnic School of the University of Nantes.
#


"""
Some iterators for generating exponential spaces without blowing up the memory of the computer.
"""


from typing import Any, List, Set, Iterable


def power_set (A: Set[Any]) -> Iterable[Set[Any]]:
    """
    Iterator over all the sub-sets of the given set, from the empty set to the set itself.

    Example:
    >>> list(power_set({1, 2, 3}))
    [set(), {1}, {2}, {1, 2}, {3}, {1, 3}, {2, 3}, {1, 2, 3}]

    :time:  in O(2^n) where n is the cardinal of the set
    """
    if A == set():
        yield set()
    else:
        x = next(iter(A))
        for X in power_set(A - {x}):
            yield X
            yield X | {x}


def sum_composition (n: int,
                     k: int) -> Iterable[List[int]]:
    """
    Iterator over all the sums of exactly k positive integers that sum up to n, without permutations.

    @pre 0 < k <= n.

    @post Summands appear in non-decreasing order.

    Example:
    >>> list(sum_composition(7, 3))
    [[1, 1, 5], [1, 2, 4], [1, 3, 3], [2, 2, 3]]

    :time:  in O(C_{n-1}^{k-1}), i.e., from 1 to close to a power of 2
    """
    assert n > 0, "the sum must be strictly positive"
    assert 0 < k, "the number of summands cannot be null"
    assert k <= n, "the number of summands cannot be larger than the sum"

    if k == 1:
        yield [n]
    else:
        for i in range(1, n // 2 + 1):
            if k - 1 <= n - i:
                for S in sum_composition(n - i, k - 1):
                    if i <= S[0]:
                        result = [i] + S

                        assert len(result) == k
                        assert sum(result) == n

                        yield result


if __name__ == "__main__":
    print("power sets")
    for n in range(0, 5):
        print(n, list(power_set(set(list(range(n))))))
    print("sum compositions")
    for n in range(0, 7):
        for k in range(1, n + 1):
            print(n, k, list(sum_composition(n, k)))

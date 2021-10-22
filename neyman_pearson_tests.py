# -*- coding: utf-8 -*-
"""
@author: Cosmo

Provides functions to illustrate Neyman-Pearson tests.

See README.md for details.
"""


import matplotlib.pyplot as plt
import itertools
from operator import itemgetter


# recipe from itertools page
def powerset(iterable):
    """Returns a stream of all subsets of the iterable.

    For example: [1,2,3] --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3).
    """
    s = list(iterable)
    return itertools.chain.from_iterable(
        itertools.combinations(s, r)
        for r in range(len(s)+1)
    )


# recipe from itertools page
def pairwise(iterable):
    """Returns stream of pairs, overlapping, from the iterable.

    For example: [1, 2, 3, 4] -> (1, 2), (2, 3), (3, 4).
    """
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


def weakly_dominates(a, b):
    """Returns True if a[i] >= b[i] for all i and a[j] > b[j] for some j."""
    return all(x >= y for x, y in zip(a, b)) \
        and any(x > y for x, y in zip(a, b))


def is_weakly_dominated(a, x):
    """Returns True if a is weakly dominated by an item in x."""
    return any(weakly_dominates(b, a) for b in x)


def discrete_regions(null, alt):
    """Computes the size and power of each rejection region.

    Args:
        null: List of likelihoods under the null hypothesis.
        alt: List of likelihoods under the alternative hypothesis.

    Returns:
        Two lists. The first contains the sizes of all the rejection regions
          and the second contains the powers, ordered like the powerset stream.
    """
    sizes = [sum(region) for region in powerset(null)]
    powers = [sum(region) for region in powerset(alt)]
    return sizes, powers


def print_discrete_regions(null, alt):
    """Prints the size and power of each rejection region.

    Args:
        null: List of likelihoods under the null hypothesis.
        alt: List of likelihoods under the alternative hypothesis.
    """
    regions = powerset(range(1, len(null) + 1))
    sizes, powers = discrete_regions(null, alt)
    print('region, size, power')
    for region, size, power in zip(regions, sizes, powers):
        print(f'{region}, {size}, {power}')


def plot_discrete_regions(null, alt):
    """Plots the size and power of each rejection region.

    Args:
        null: List of likelihoods under the null hypothesis.
        alt: List of likelihoods under the alternative hypothesis.

    Returns:
        figure and axis objects, to allow additional modification if desired.
    """
    sizes, powers = discrete_regions(null, alt)
    fig, ax = plt.subplots()
    ax.scatter(sizes, powers, alpha=0.5)
    ax.set(xlabel='size', ylabel='power')
    return fig, ax


def discrete_regions_plus(null, alt):
    """Computes sizes, powers, domination, and LRTs.

    Args:
        null: List of likelihoods under the null hypothesis.
        alt: List of likelihoods under the alternative hypothesis.

    Returns:
        Four lists, containing the sizes, the powers, Boolean flags for which
        regions are dominated, Boolean flags for which regions are LRTs, all
        ordered like the powerset stream.
    """

    sizes, powers = discrete_regions(null, alt)

    # compute flags for dominated regions
    neg_sizes = (1 - size for size in sizes)
    d_data = list(zip(neg_sizes, powers))
    dom_flags = [is_weakly_dominated(x, d_data) for x in d_data]

    # compute flags for likelihood ratio tests
    likelihood_ratios = [y / x for x, y in zip(null, alt)]
    outcomes_and_ratios = sorted(
        zip(itertools.count(), likelihood_ratios),
        key=itemgetter(1),
        reverse=True,
    )

    # empty set and whole space are always lrt, so add them immediately.
    lrt_sets = {
        frozenset(),
        frozenset(range(len(null)))
    }

    cum_set = set()
    for (o1, r1), (o2, r2) in pairwise(outcomes_and_ratios):
        cum_set.add(o1)
        if r1 > r2:
            lrt_sets.add(frozenset(cum_set))
    regions = powerset(range(len(null)))
    lrt_flags = [set(x) in lrt_sets for x in regions]

    return sizes, powers, dom_flags, lrt_flags


def print_discrete_regions_plus(null, alt):
    """Prints rich data about rejection regions."""
    regions = powerset(range(len(null)))
    sizes, powers, dom_flags, lrt_flags = discrete_regions_plus(null, alt)
    print('region, size, power, dominated?, LRT?')
    for r, s, p, d, lrt in zip(regions, sizes, powers, dom_flags, lrt_flags):
        print(r, s, p, d, lrt)


def plot_discrete_regions_plus(null, alt):
    """Plots rich data about rejection regions."""
    sizes, powers, dom_flags, lrt_flags = discrete_regions_plus(null, alt)
    marker_colors = ['orange' if x else 'blue' for x in dom_flags]
    marker_sizes = [100 if x else 30 for x in lrt_flags]

    fig, ax = plt.subplots()
    ax.scatter(sizes, powers, marker_sizes, marker_colors, alpha=0.5)
    ax.set(xlabel='size', ylabel='power')

    return fig, ax


def which_region(null, alt, alpha):
    """Returns the index of the LRT region of max power subject to size < alpha."""
    sizes, powers, _, lrt_flags = discrete_regions_plus(null, alt)
    return max(range(len(sizes)),
               key=lambda i: (sizes[i] < alpha) * lrt_flags[i] * powers[i])


def plot_select_region(null, alt, alpha):
    """Plots which rejection region is selected under the standard protocol.

    Args:
        null: List of likelihoods under the null hypothesis.
        alt: List of likelihoods under the alternative hypothesis.
        alpha: The maximum acceptable size.

    Returns:
        figure and axis objects, to allow additional modification if desired."""
    sizes, powers = discrete_regions(null, alt)
    fig, ax = plot_discrete_regions_plus(null, alt)
    ax.plot([alpha, alpha], [0, 1], color='red')
    index = which_region(null, alt, alpha)
    ax.scatter(sizes[index], powers[index], s=100, color='darkblue')

    return fig, ax
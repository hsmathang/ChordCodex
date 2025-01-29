from itertools import permutations

def lazy_full(perm_min, perm_max):
    """
    Generate permutations lazily for numbers from 0 to 12 with configurable permutation sizes.
    
    :param perm_min: Minimum size of permutations.
    :param perm_max: Maximum size of permutations.
    :return: Yields one permutation at a time.
    """
    # Define the set of numbers from 0 to 12
    elements = list(range(0, 13))
    
    # Lazily generate permutations for each size in the range
    for r in range(perm_min, perm_max + 1):
        yield from permutations(elements, r)


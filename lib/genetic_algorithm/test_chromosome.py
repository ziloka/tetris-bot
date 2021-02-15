"""
Unit tests for chromosome.py
"""
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import unittest

import numpy as np

from lib.genetic_algorithm.chromosome import Chromosome

class TestChromosome(unittest.TestCase):
    def test_init(self): # pylint: disable=no-self-use
        genes = np.array([1, 2, 0.3])
        chromosome = Chromosome(genes, None)
        np.testing.assert_equal(chromosome.genes, genes)

    def test_cross_no_mutation(self): # pylint: disable=no-self-use
        # Test equally weighted chromosomes.
        # pylint: disable=invalid-name, protected-access
        c1 = Chromosome(np.array([2, 3, 2]), 0.5)
        c2 = Chromosome(np.array([3, 3, 5]), 0.5)
        result = Chromosome._cross_(c1, c2, mutation_chance=0)
        np.testing.assert_almost_equal(result, [2.5, 3, 3.5])

        # Test chromosomes with different fitnesses.
        c1 = Chromosome(np.array([1, 1, 1]), 0.2)
        c2 = Chromosome(np.array([3, 2, 5]), 0.8)
        result = Chromosome._cross_(c1, c2, mutation_chance=0)
        np.testing.assert_almost_equal(result, [2.6, 1.8, 4.2])

        c1 = Chromosome(np.array([-2, -0.5, 1]), 0.4)
        c2 = Chromosome(np.array([4, 2, 0.25]), 0.6)
        result = Chromosome._cross_(c1, c2, mutation_chance=0)
        np.testing.assert_almost_equal(result, [1.6, 1, 0.55])

    def test_cross_with_mutation(self): # pylint: disable=no-self-use
        np.random.seed(0)
        # pylint: disable=invalid-name, protected-access
        c1 = Chromosome(np.array([2, 3, 2]), 0.25)
        c2 = Chromosome(np.array([3, 3, 4]), 0.75)
        result = Chromosome._cross_(c1, c2, mutation_chance=0.7)
        np.testing.assert_almost_equal(result, [0.08976, 3, 0.29178],
                                       decimal=5)

if __name__ == '__main__':
    unittest.main()

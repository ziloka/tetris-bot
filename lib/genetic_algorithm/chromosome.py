"""
The Chromosome class holds genetic data for a single agent within our genetic
algorithm framework.
"""

import numpy as np

DEFAULT_MUTATION_CHANCE = 0.075

class Chromosome(): # pylint: disable=missing-class-docstring

    @staticmethod
    def random(n_genes):
        """
        Returns a randomly initialized array for the genetic values inside
        a Chromosome. The genetic values are sampled from the open interval from
        -1 to 1.
        """
        return (np.random.random_sample(n_genes) * 2) - 1

    def __init__(self, genes, fitness):
        """
        Initializes a Chromosome.
        """
        self.genes = genes
        self.fitness = fitness

    def __str__(self):
        """
        Returns a string representation of the chromosome's genes.
        """
        return str(self.genes)

    def cross(self, other, mutation_chance=DEFAULT_MUTATION_CHANCE):
        """
        Performs genetic crossing between this chromosome and another
        chromosome, returning a new chromosome.

        The genetic values stored in a chromosome are all numeric in the open
        interval from -1 to 1. When we cross two chromosomes, we will take the
        weighted average between the genetic values of the two chromosomes,
        weighting it according to the fitness value of each chromosome.

        During chromosomal crossing, a mutation has a chance to occur for each
        genetic value. If one occurs, that genetic value will be set to a new
        random number in the open interval from -1 to 1.
        """
        assert isinstance(other, Chromosome)
        w_sum = self.fitness + other.fitness
        genes = (self.genes * self.fitness / w_sum) + (
            other.genes * other.fitness / w_sum)
        # Each gene value has a chance to mutate by becoming a random number.
        mutated_genes = np.random.random_sample(
            len(self.genes)) < mutation_chance
        if np.any(mutated_genes):
            mutation = Chromosome.random(len(self.genes))
            # Compose the original genetic values with the mutated genetic
            # values.
            genes = (genes * np.logical_not(mutated_genes)) + (
                mutation * mutated_genes)
        return Chromosome(genes, None)

"""
The Chromosome class holds genetic data for a single agent within our genetic
algorithm framework.
"""

import numpy as np

class Chromosome(): # pylint: disable=missing-class-docstring

    def __init__(self, genes, fitness=1):
        """
        Initializes a Chromosome. Every chromosome has a default fitness of 1.
        """
        self.genes = genes
        self.fitness = fitness

    def __str__(self):
        """
        Returns a string representation of the chromosome's genes.
        """
        return str(self.genes)

    def cross(self, other, mutation_chance):
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
        assert len(self.genes) == len(other.genes)
        w_sum = self.fitness + other.fitness
        n_genes = len(self.genes)
        new_genes = (self.genes * self.fitness / w_sum) + (
            other.genes * other.fitness / w_sum)
        # Each gene value has a chance to mutate by becoming a random number.
        mutated_genes = np.random.random_sample(n_genes) < mutation_chance
        if np.any(mutated_genes):
            mutation = (np.random.random_sample(n_genes) * 2) - 1
            # Compose the original genetic values with the mutated genetic
            # values.
            new_genes = (new_genes * np.logical_not(mutated_genes)) + (
                mutation * mutated_genes)
        return Chromosome(new_genes)

    def recalculate_fitness(self): # pylint: disable=missing-function-docstring
        raise NotImplementedError('Method not implemented!')

    def get_fitness(self): # pylint: disable=missing-function-docstring
        return self.fitness

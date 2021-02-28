"""
The Chromosome class holds genetic data for a single agent within our genetic
algorithm framework.
"""

import numpy as np

class Chromosome(): # pylint: disable=missing-class-docstring

    def __init__(self, genes, fitness=1):
        """
        Initializes a Chromosome. Every chromosome has a default fitness of 1.
        The higher the fitness, the better the Chromosome.
        """
        self.genes = genes
        self.fitness = fitness

    def __str__(self):
        """
        Returns a string representation of the chromosome's genes.
        """
        return f'Fitness: {self.fitness} \t Genes: {str(self.genes)}'

    @staticmethod
    def _cross_(c1, c2, mutation_chance): # pylint: disable=invalid-name
        """
        Performs genetic crossing between two given chromosomes, returning the
        new chromosome's gene sequence.

        The genetic values stored in a chromosome are all numeric in the open
        interval from -1 to 1. When we cross two chromosomes, we will take the
        weighted average between the genetic values of the two chromosomes,
        weighting it according to the fitness value of each chromosome.

        During chromosomal crossing, a mutation has a chance to occur for each
        genetic value. If one occurs, that genetic value will be set to a new
        random number in the open interval from -1 to 1.
        """
        assert isinstance(c1, Chromosome) and isinstance(c2, Chromosome)
        assert len(c1.genes) == len(c2.genes)
        w_sum = c1.fitness + c2.fitness
        n_genes = len(c1.genes)
        new_genes = (c1.genes * c1.fitness / w_sum) + (
            c2.genes * c2.fitness / w_sum)
        # Each gene value has a chance to mutate by becoming a random number.
        mutated_genes = np.random.random_sample(n_genes) < mutation_chance
        if np.any(mutated_genes):
            mutation = (np.random.random_sample(n_genes) * 2) - 1
            # Compose the original genetic values with the mutated genetic
            # values.
            new_genes = (new_genes * np.logical_not(mutated_genes)) + (
                mutation * mutated_genes)
        return new_genes

    def cross(self, other, mutation_chance):
        # pylint: disable=missing-function-docstring
        raise NotImplementedError('Method not implemented!')

    def recalculate_fitness(self): # pylint: disable=missing-function-docstring
        raise NotImplementedError('Method not implemented!')

    def get_fitness(self): # pylint: disable=missing-function-docstring
        return self.fitness

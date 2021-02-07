"""
File containing the Population class, which contains a group of Chromosomes
for training in the genetic algorithm.
"""

import random

class Population(): # pylint: disable=missing-class-docstring

    def __init__(self, population):
        """
        Initializes a Population of individuals/chromosomes.
        """
        assert len(population) % 4 == 0
        self.population = population
        self.generations = 0

    def run(self, generations):
        """
        This method will run the genetic algorithm on the population for the
        given number of generations.
        """
        cut = len(self.population) // 2
        for _ in range(generations):
            # Sort the population of chromosomes by their fitness
            population_by_fitness = sorted(
                self.population, key=lambda gene: gene.get_fitness())
            print('Generation: {}'.format(self.generations))
            print([member.get_fitness() for member in population_by_fitness])
            # Select the top half of the fittest members.
            fittest = population_by_fitness[cut:]
            # Shuffle and cross breed the fittest members.
            random.shuffle(fittest)
            for i in range(0, cut, 2):
                # Add two children so the population size remains the same.
                fittest += [fittest[i].cross(fittest[i + 1])]
                fittest += [fittest[i].cross(fittest[i + 1])]
            self.population = fittest
            for chromosome in self.population:
                chromosome.recalculate_fitness()
            self.generations += 1

    def get_fittest_member(self):
        """
        Returns the fittest member present in the population.
        """
        return sorted(self.population, key=lambda gene: gene.get_fitness())[-1]

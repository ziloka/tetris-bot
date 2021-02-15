"""
File containing the Population class, which contains a group of Chromosomes
for training in the genetic algorithm.
"""

import random

from lib.genetic_algorithm.chromosome import Chromosome

class Population(): # pylint: disable=missing-class-docstring

    DEFAULT_MUTATION_CHANCE = 0.075

    def __init__(self, population, mutation_chance=DEFAULT_MUTATION_CHANCE):
        """
        Initializes a Population of chromosomes.
        """
        assert len(population) % 4 == 0
        for chromosome in population:
            assert isinstance(chromosome, Chromosome)
        self.population = population
        self.mutation_chance = mutation_chance
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
                fittest += [fittest[i].cross(
                    fittest[i + 1], self.mutation_chance)]
                fittest += [fittest[i].cross(
                    fittest[i + 1], self.mutation_chance)]
            self.population = fittest
            for chromosome in self.population:
                chromosome.recalculate_fitness()
            self.generations += 1

    def get_fittest_member(self):
        """
        Returns the fittest member present in the population.
        """
        return sorted(self.population, key=lambda gene: gene.get_fitness())[-1]

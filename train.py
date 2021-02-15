"""
Author: omgimanerd (Alvin Lin)

Executable CLI to run the genetic algorithm.
Parameterizable via command line options, invoke with the -h flag.
"""
# pylint: disable=missing-function-docstring

import argparse
import pickle
import random

from lib.genetic_algorithm.population import Population
from lib.genetic_algorithm.tetris_chromosome import TetrisChromosome

def main():
    parser = argparse.ArgumentParser(description='Runs genetic algorithm.')
    parser.add_argument('outfile', type=argparse.FileType('wb'))

    parser.add_argument('--seed', type=argparse.FileType('rb'))
    parser.add_argument('--generations', type=int, default=25)
    parser.add_argument('--population_size', type=int, default=16)

    parser.add_argument('--n_simulations', type=int,
                        default=TetrisChromosome.N_SIMULATIONS)
    parser.add_argument('--max_simulation_length', type=int,
                        default=TetrisChromosome.MAX_SIMULATION_LENGTH)
    parser.add_argument('--mutation_chance', type=float,
                        default=Population.DEFAULT_MUTATION_CHANCE)
    args = parser.parse_args()

    random.seed(0)

    chromosomes = []
    if args.seed:
        with args.seed as seed:
            genes = pickle.load(seed)
            for _ in range(args.population_size):
                chromosomes.append(TetrisChromosome.create(
                    genes, args.n_simulations, args.max_simulation_length))
    else:
        for _ in range(args.population_size):
            chromosomes.append(TetrisChromosome.random(
                args.n_simulations, args.max_simulation_length))

    population = Population(chromosomes, args.mutation_chance)
    population.run(args.generations)
    fittest = population.get_fittest_member()

    with args.outfile as outfile:
        pickle.dump(fittest.genes, outfile)
        print('Fittest member: {}'.format(fittest))
        print('Result dumped to {}'.format(outfile))

if __name__ == '__main__':
    main()

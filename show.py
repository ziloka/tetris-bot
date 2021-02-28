"""
Author: omgimanerd (Alvin Lin)

Utility script to run a gene against Tetris to simulate and verify its
performance.
Invoke with the -h flag for help.
"""
# pylint: disable=missing-function-docstring

import argparse
import pickle
import time

from lib.tetris_driver import TetrisDriver
from lib.genetic_algorithm.tetris_chromosome import TetrisChromosome

FIELDS = [
    'Gap Count:\t\t\t{:0.8f}',
    'Mean Column Heights:\t\t{:0.8f}',
    'Stddev Column Heights:\t\t{:0.8f}',
    'Maxmin Height Difference:\t{:0.8f}',
    'ediff1d sum:\t\t\t{:0.8f}'
]

def show(genes):
    driver = TetrisDriver.create()
    chromosome = TetrisChromosome.create(genes)
    while driver.play(chromosome.strategy_callback):
        print(driver.field)
        time.sleep(0.25)

def main():
    parser = argparse.ArgumentParser(
        description='Plays tetris with a given gene file.')
    parser.add_argument('gene', type=argparse.FileType('rb'))
    parser.add_argument(
        '--no_sim',
        help='Show the numeric values in the chromosome instead of simulating '
             'it on Tetris',
        action='store_true')

    args = parser.parse_args()
    with args.gene as gene:
        genes = pickle.load(gene)
        if args.no_sim:
            for i, field in enumerate(FIELDS):
                print(field.format(genes[i]))
        else:
            show(genes)

if __name__ == '__main__':
    main()

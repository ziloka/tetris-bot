"""
ChromosomeStrategy represents a strategy of playing Tetris by permutating all
the possible positions of the given tetromino and held tetromino, and weighting
each position by the Chromosome's internal values (trained by a genetic
algorithm).
"""

import math

import numpy as np

from lib.field import Field
from lib.tetris_driver import TetrisDriver, TetrisAction
from lib.genetic_algorithm.chromosome import Chromosome

class TetrisChromosome(Chromosome): # pylint: disable=missing-class-docstring

    N_SIMULATIONS = 4
    MAX_SIMULATION_LENGTH = 1000

    N_FIELDS = 5

    def __init__(self, genes, n_simulations, max_simulation_length):
        Chromosome.__init__(self, genes)
        self.n_simulations = n_simulations
        self.max_simulation_length = max_simulation_length
        self.recalculate_fitness()

    @staticmethod
    def create(genes, n_simulations=N_SIMULATIONS,
               max_simulation_length=MAX_SIMULATION_LENGTH):
        """
        Factory method for creating a TetrisChromosome with a given gene
        ndarray.
        """
        return TetrisChromosome(genes, n_simulations, max_simulation_length)

    @staticmethod
    def random(n_simulations=N_SIMULATIONS,
               max_simulation_length=MAX_SIMULATION_LENGTH):
        """
        Returns a TetrisChromosome with randomly seeded genes.
        """
        return TetrisChromosome(np.random.random_sample(
            TetrisChromosome.N_FIELDS), n_simulations, max_simulation_length)

    def _get_field_score_(self, field):
        """
        Given a field, this helper method fetches all the input data points we
        care about from the field and computes the dot product of that input
        vector with the underlying Chromosome's genes to score the given field.
        """
        heights = field.heights()
        ediff1d = np.ediff1d(heights)
        field_values = np.array([
            field.count_gaps(),            # Gap count
            np.mean(heights),              # Average height
            np.std(heights),               # Standard deviation of heights
            heights.max() - heights.min(), # Max height diff
            abs(ediff1d).max(),            # Max consecutive height diff
        ])
        assert len(field_values) == TetrisChromosome.N_FIELDS
        return field_values.dot(self.genes)

    def strategy_callback(self, field, tetromino, held_tetromino):
        """
        This callback is passed into TetrisDriver in order to play an actual
        game of Tetris using this class's underlying Chromosome to decide the
        positioning of the next Tetromino.

        This callback takes the current field, tetromino, and held tetromino and
        calculates the best tetromino (and orientation) position to play.
        """
        candidates = [
            tetromino,
            tetromino.copy().rotate_right(),
            tetromino.copy().flip(),
            tetromino.copy().rotate_left(),
        ]
        if held_tetromino is not None and (
                held_tetromino.tetromino_type != tetromino.tetromino_type):
            candidates += [
                held_tetromino,
                held_tetromino.copy().rotate_right(),
                held_tetromino.copy().flip(),
                held_tetromino.copy().rotate_left(),
            ]
        best_column = None
        best_tetromino_orientation = None
        best_field_score = math.inf
        for candidate in candidates:
            for column in range(Field.WIDTH):
                test_field = field.copy()
                # Scenario where this is an invalid column to drop into
                if test_field.drop(candidate, column) < 0:
                    continue
                # Get the field score and with this chromosome's genetic values
                # applied to it and try to minimize it.
                field_score = self._get_field_score_(test_field)
                if field_score < best_field_score:
                    best_column = column
                    best_tetromino_orientation = candidate
                    best_field_score = field_score
        if best_column is None:
            return None
        return TetrisAction(best_tetromino_orientation, best_column)

    def cross(self, other, mutation_chance):
        """
        Performs genetic crossing between two TetrisChromosomes using the
        underlying Chromosome.cross() implementation.
        """
        return TetrisChromosome(
            Chromosome._cross_(self, other, mutation_chance),
            self.n_simulations,
            self.max_simulation_length)

    def recalculate_fitness(self):
        """
        Performs a simulation to evaluate the fitness of the chromosome. This
        will be called multiple times and the overall performance of the
        chromosome is the median of all the runs.

        For a TetrisChromosome, the fitness of the chromosome is the number of
        Tetrominos it can place before losing plus the number of lines cleared.
        """
        fitnesses = []
        for _ in range(self.n_simulations):
            driver = TetrisDriver.create()
            for sim_length in range(self.max_simulation_length):
                if not driver.play(self.strategy_callback):
                    break
            fitnesses.append(sim_length + driver.lines_cleared)
        self.fitness = np.median(fitnesses)
        return self.fitness

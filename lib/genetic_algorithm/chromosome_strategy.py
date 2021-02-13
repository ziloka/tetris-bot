"""
ChromosomeStrategy represents a strategy of playing Tetris by permutating all
the possible positions of the given tetromino and held tetromino, and weighting
each position by the Chromosome's internal values (trained by a genetic
algorithm).
"""

from lib.field import Field
from lib.tetromino import Tetromino

N_SIMULATIONS = 4
MAX_SIMULATION_LENGTH = 1000
MUTATION_CHANCE = 0.075

class ChromosomeStrategy(): # pylint: disable=missing-class-docstring

    def __init__(self, chromosome):
        self.chromosome = chromosome

        self.simulations = Chromosome.N_SIMULATIONS
        self.max_simulation_length = Chromosome.MAX_SIMULATION_LENGTH
        self.mutation_chance = Chromosome.MUTATION_CHANCE

    def _get_fitness_(self):
        """
        Helper method to perform a single simulation to evaluate the performance
        of the chromosome. This will be called multiple times and the overall
        performance of the chromosome is the average of all the runs.
        """
        tetrominos = [
            Tetromino.ITetromino(),
            Tetromino.OTetromino(),
            Tetromino.TTetromino(),
            Tetromino.STetromino(),
            Tetromino.ZTetromino(),
            Tetromino.JTetromino(),
            Tetromino.LTetromino()
        ]
        field = Field.create()
        field_score = -1
        for length in range(self.max_simulation_length):
            tetromino = random.choice(tetrominos)
            _, __, _field, _field_score = field.get_optimal_drop(
                tetromino, self.genes)
            if _field_score == math.inf:
                return length, field_score
            field = _field
            field_score = _field_score
        return length, field_score

    def get_fitness(self):
        """
        Returns the fitness of the chromosome. If it is cached, it will fetch
        the cached fitness value, otherwise it will compute it and return it.
        """
        if self.fitness is not None:
            return self.fitness
        self.recalculate_fitness()
        return self.fitness

    def recalculate_fitness(self):
        """
        Calculates the fitness values of the chromosome by running a number
        of Tetris simulations using the chromosome and averaging their
        performance.
        """
        scores = np.array([
            self._get_fitness_() for _ in range(self.simulations)])
        self.fitness, self.field_score = np.mean(scores, axis=0)

"""
TetrisDriver allows for a game to played with a given input strategy.
"""

import random

from lib.field import Field
from lib.tetromino import Tetromino

class TetrisAction(): # pylint: disable=too-few-public-methods
    """
    A data class encapsulating actions that a player can take on a TetrisDriver,
    such as the column to place a tetromino and whether or not to use the held
    tetromino.
    """
    def __init__(self, column, use_held):
        assert isinstance(column, int) and isinstance(use_held, bool)
        assert 0 <= column < Field.HEIGHT
        self.column = column
        self.use_held = use_held

class TetrisDriver(): # pylint: disable=missing-class-docstring

    TETROMINOS = [
        Tetromino.ITetromino(),
        Tetromino.OTetromino(),
        Tetromino.TTetromino(),
        Tetromino.STetromino(),
        Tetromino.ZTetromino(),
        Tetromino.JTetromino(),
        Tetromino.LTetromino()
    ]

    def __init__(self, field):
        self.field = field
        self.held_tetromino = None
        self.num_placed = 0
        self.lines_cleared = 0

    @staticmethod
    def create(field=None):
        """
        Factory method to create a TetrisDriver, taking an optional Field with
        which to initialize the game with.
        """
        return TetrisDriver(Field.create() if field is None else field)

    def play(self, strategy):
        """
        Given a strategy callback which takes the current Field, the next
        Tetromino, and the held Tetromino, and returns a TetrisAction or None.
        This method will play the TetrisAction if provided, or return None if
        one if the TetrisAction was None, indicating the game is over.
        """
        tetromino = random.choice(TetrisDriver.TETROMINOS)
        action = strategy(self.field, tetromino, self.held_tetromino)
        if action is None:
            return False
        lines_cleared = 0
        if action.use_held:
            lines_cleared = self.field.drop(
                self.held_tetromino, action.column)
            self.held_tetromino = tetromino
        else:
            lines_cleared = self.field.drop(
                tetromino, action.column)
        self.num_placed += 1
        self.lines_cleared += lines_cleared if lines_cleared > 0 else 0
        return True

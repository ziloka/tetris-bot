"""
The Tetromino class encapsulates a Tetris tetromino as a numpy array.
"""

import numpy as np

class Tetromino(): # pylint: disable=missing-class-docstring

    TYPES = [' ', 'I', 'O', 'T', 'S', 'Z', 'J', 'L']
    TYPES_D = {
        ' ': 0,
        'I': 1,
        'O': 2,
        'T': 3,
        'S': 4,
        'Z': 5,
        'J': 6,
        'L': 7
    }

    def __init__(self, state):
        self.state = np.array(state, dtype=np.uint8, copy=True)

    @staticmethod
    def ITetromino(): # pylint: disable=invalid-name, missing-function-docstring
        return Tetromino(
            [
                [1, 1, 1, 1]
            ]
        )

    @staticmethod
    def OTetromino(): # pylint: disable=invalid-name, missing-function-docstring
        return Tetromino(
            [
                [2, 2],
                [2, 2]
            ]
        )

    @staticmethod
    def TTetromino(): # pylint: disable=invalid-name, missing-function-docstring
        return Tetromino(
            [
                [3, 3, 3],
                [0, 3, 0]
            ]
        )

    @staticmethod
    def STetromino(): # pylint: disable=invalid-name, missing-function-docstring
        return Tetromino(
            [
                [0, 4, 4],
                [4, 4, 0]
            ]
        )

    @staticmethod
    def ZTetromino(): # pylint: disable=invalid-name, missing-function-docstring
        return Tetromino(
            [
                [5, 5, 0],
                [0, 5, 5]
            ]
        )

    @staticmethod
    def JTetromino(): # pylint: disable=invalid-name, missing-function-docstring
        return Tetromino(
            [
                [6, 6, 6],
                [0, 0, 6]
            ]
        )

    @staticmethod
    def LTetromino(): # pylint: disable=invalid-name, missing-function-docstring
        return Tetromino(
            [
                [7, 7, 7],
                [7, 0, 0]
            ]
        )

    @staticmethod
    def create(letter):
        """
        Creates a Tetromino from the given letter for the tetromino type.
        """
        if letter.upper() in Tetromino.TYPES[1:]:
            raise ValueError('No Tetromino of type {}'.format(letter))
        return getattr(Tetromino, '{}Tetromino'.format(letter.upper()))()

    def __str__(self):
        return str(np.vectorize(Tetromino.TYPES.__getitem__)(self.state))

    def __getitem__(self, key):
        return self.state[key]

    def copy(self):
        """
        Returns a new copy of the given Tetromino.
        """
        return Tetromino(self.state)

    def rotate(self, change):
        """
        Given an integer n from [0, 4), this function performs a 90 * n degree
        rotation clockwise on this Tetromino.
        """
        while change < 0:
            change += 4
        change %= 4
        if change == 0:
            return
        if change == 1:
            self.rotate_right()
        elif change == 2:
            self.flip()
        elif change == 3:
            self.rotate_left()

    def rotate_right(self):
        """
        This method rotates this Tetromino 90 degrees clockwise.
        """
        self.state = np.rot90(self.state, 3)
        return self

    def rotate_left(self):
        """
        This method rotates this Tetromino 90 degrees counterclockwise.
        """
        self.state = np.rot90(self.state, 1)
        return self

    def flip(self):
        """
        This method rotates this Tetromino 180 degrees.
        """
        self.state = np.rot90(self.state, 2)
        return self

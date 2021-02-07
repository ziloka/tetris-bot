"""
Unit tests for tetromino.py
"""
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import unittest

import numpy as np

from lib.tetromino import Tetromino

class TetrominoAssertions: # pylint: disable=too-few-public-methods, no-self-use
    def assertTetrominosEqual(self, t1, t2): # pylint: disable=invalid-name
        """
        Helper method for asserting that two Tetrominos are equal.
        """
        assert isinstance(t1, Tetromino) and isinstance(t2, Tetromino)
        assert t1.state.shape == t2.state.shape
        assert (t1.state == t2.state).all()

class TestTetromino(unittest.TestCase, TetrominoAssertions):

    def test_ITetromino(self): # pylint: disable=invalid-name
        tetromino = Tetromino.ITetromino()
        expected1 = Tetromino([
            [1, 1, 1, 1]
        ])
        expected2 = Tetromino([
            [1],
            [1],
            [1],
            [1],
        ])
        self.assertTetrominosEqual(tetromino, expected1)
        self.assertTetrominosEqual(tetromino.rotate_right(), expected2)
        self.assertTetrominosEqual(tetromino.rotate_right(), expected1)
        self.assertTetrominosEqual(tetromino.rotate_left(), expected2)
        self.assertTetrominosEqual(tetromino.flip(), expected2)

    def test_OTetromino(self): # pylint: disable=invalid-name
        tetromino = Tetromino.OTetromino()
        expected = Tetromino([
            [2, 2],
            [2, 2],
        ])
        self.assertTetrominosEqual(tetromino.rotate_right(), expected)
        self.assertTetrominosEqual(tetromino.rotate_right(), expected)
        self.assertTetrominosEqual(tetromino.rotate_left(), expected)
        self.assertTetrominosEqual(tetromino.rotate_left(), expected)
        self.assertTetrominosEqual(tetromino.flip(), expected)

    def test_TTetromino(self): # pylint: disable=invalid-name
        tetromino = Tetromino.TTetromino()
        expected1 = Tetromino([
            [3, 3, 3],
            [0, 3, 0],
        ])
        expected2 = Tetromino([
            [0, 3],
            [3, 3],
            [0, 3],
        ])
        expected3 = Tetromino([
            [0, 3, 0],
            [3, 3, 3],
        ])
        expected4 = Tetromino([
            [3, 0],
            [3, 3],
            [3, 0],
        ])
        self.assertTetrominosEqual(tetromino, expected1)
        self.assertTetrominosEqual(tetromino.rotate_right(), expected2)
        self.assertTetrominosEqual(tetromino.rotate_right(), expected3)
        self.assertTetrominosEqual(tetromino.rotate_right(), expected4)
        self.assertTetrominosEqual(tetromino.flip(), expected2)
        self.assertTetrominosEqual(tetromino.rotate_left(), expected1)

    def test_STetromino(self): # pylint: disable=invalid-name
        tetromino = Tetromino.STetromino()
        expected1 = Tetromino([
            [0, 4, 4],
            [4, 4, 0],
        ])
        expected2 = Tetromino([
            [4, 0],
            [4, 4],
            [0, 4],
        ])
        self.assertTetrominosEqual(tetromino, expected1)
        self.assertTetrominosEqual(tetromino.rotate_right(), expected2)
        self.assertTetrominosEqual(tetromino.rotate_right(), expected1)
        self.assertTetrominosEqual(tetromino.flip(), expected1)
        self.assertTetrominosEqual(tetromino.rotate_left(), expected2)

    def test_ZTetromino(self): # pylint: disable=invalid-name
        tetromino = Tetromino.ZTetromino()
        expected1 = Tetromino([
            [5, 5, 0],
            [0, 5, 5],
        ])
        expected2 = Tetromino([
            [0, 5],
            [5, 5],
            [5, 0],
        ])
        self.assertTetrominosEqual(tetromino, expected1)
        self.assertTetrominosEqual(tetromino.rotate_right(), expected2)
        self.assertTetrominosEqual(tetromino.rotate_right(), expected1)
        self.assertTetrominosEqual(tetromino.flip(), expected1)
        self.assertTetrominosEqual(tetromino.rotate_left(), expected2)

    def test_JTetromino(self): # pylint: disable=invalid-name
        tetromino = Tetromino.JTetromino()
        expected1 = Tetromino([
            [6, 6, 6],
            [0, 0, 6],
        ])
        expected2 = Tetromino([
            [0, 6],
            [0, 6],
            [6, 6],
        ])
        expected3 = Tetromino([
            [6, 0, 0],
            [6, 6, 6],
        ])
        expected4 = Tetromino([
            [6, 6],
            [6, 0],
            [6, 0],
        ])
        self.assertTetrominosEqual(tetromino, expected1)
        self.assertTetrominosEqual(tetromino.rotate_right(), expected2)
        self.assertTetrominosEqual(tetromino.rotate_right(), expected3)
        self.assertTetrominosEqual(tetromino.rotate_right(), expected4)
        self.assertTetrominosEqual(tetromino.rotate_right(), expected1)
        self.assertTetrominosEqual(tetromino.flip(), expected3)
        self.assertTetrominosEqual(tetromino.rotate_left(), expected2)
        self.assertTetrominosEqual(tetromino.rotate_left(), expected1)

    def test_LTetromino(self): # pylint: disable=invalid-name
        tetromino = Tetromino.LTetromino()
        expected1 = Tetromino([
            [7, 7, 7],
            [7, 0, 0],
        ])
        expected2 = Tetromino([
            [7, 7],
            [0, 7],
            [0, 7],
        ])
        expected3 = Tetromino([
            [0, 0, 7],
            [7, 7, 7],
        ])
        expected4 = Tetromino([
            [0, 7],
            [0, 7],
            [7, 7],
        ])
        self.assertTetrominosEqual(tetromino, expected1)
        self.assertTetrominosEqual(tetromino.rotate_right(), expected2)
        self.assertTetrominosEqual(tetromino.rotate_right(), expected3)
        self.assertTetrominosEqual(tetromino.rotate_right(), expected4)
        self.assertTetrominosEqual(tetromino.rotate_right(), expected1)
        self.assertTetrominosEqual(tetromino.flip(), expected3)
        self.assertTetrominosEqual(tetromino.rotate_left(), expected2)
        self.assertTetrominosEqual(tetromino.rotate_left(), expected1)

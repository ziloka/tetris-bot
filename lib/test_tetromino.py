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
        if not isinstance(t1, Tetromino):
            raise AssertionError(f'{t1} is not a Tetromino')
        if not isinstance(t2, Tetromino):
            raise AssertionError(f'{t2} is not a Tetromino')
        if t1.tetromino_type != t2.tetromino_type:
            raise AssertionError(f'{t1} != {t2}')
        np.testing.assert_array_equal(t1.state, t2.state)

class TestTetromino(unittest.TestCase, TetrominoAssertions):
    def test_ITetromino(self): # pylint: disable=invalid-name
        tetromino = Tetromino.ITetromino()
        expected1 = Tetromino([
            [1, 1, 1, 1]
        ], Tetromino.TYPES[1])
        expected2 = Tetromino([
            [1],
            [1],
            [1],
            [1],
        ], Tetromino.TYPES[1])
        self.assertEqual(tetromino.tetromino_type, expected1.tetromino_type)
        self.assertEqual(tetromino.tetromino_type, expected2.tetromino_type)
        self.assertTetrominosEqual(tetromino, expected1)
        self.assertEqual(tetromino.width(), 4)
        self.assertEqual(tetromino.height(), 1)
        self.assertTetrominosEqual(tetromino.rotate_right(), expected2)
        self.assertEqual(tetromino.width(), 1)
        self.assertEqual(tetromino.height(), 4)
        self.assertTetrominosEqual(tetromino.rotate_right(), expected1)
        self.assertTetrominosEqual(tetromino.rotate_left(), expected2)
        self.assertTetrominosEqual(tetromino.flip(), expected2)

    def test_OTetromino(self): # pylint: disable=invalid-name
        tetromino = Tetromino.OTetromino()
        expected = Tetromino([
            [2, 2],
            [2, 2],
        ], Tetromino.TYPES[2])
        self.assertTetrominosEqual(tetromino, expected)
        self.assertTetrominosEqual(tetromino.rotate_right(), expected)
        self.assertEqual(tetromino.width(), 2)
        self.assertEqual(tetromino.height(), 2)
        self.assertTetrominosEqual(tetromino.rotate_right(), expected)
        self.assertEqual(tetromino.width(), 2)
        self.assertEqual(tetromino.height(), 2)
        self.assertTetrominosEqual(tetromino.rotate_left(), expected)
        self.assertTetrominosEqual(tetromino.rotate_left(), expected)
        self.assertTetrominosEqual(tetromino.flip(), expected)

    def test_TTetromino(self): # pylint: disable=invalid-name
        tetromino = Tetromino.TTetromino()
        expected1 = Tetromino([
            [3, 3, 3],
            [0, 3, 0],
        ], Tetromino.TYPES[3])
        expected2 = Tetromino([
            [0, 3],
            [3, 3],
            [0, 3],
        ], Tetromino.TYPES[3])
        expected3 = Tetromino([
            [0, 3, 0],
            [3, 3, 3],
        ], Tetromino.TYPES[3])
        expected4 = Tetromino([
            [3, 0],
            [3, 3],
            [3, 0],
        ], Tetromino.TYPES[3])
        self.assertTetrominosEqual(tetromino, expected1)
        self.assertEqual(tetromino.width(), 3)
        self.assertEqual(tetromino.height(), 2)
        self.assertTetrominosEqual(tetromino.rotate_right(), expected2)
        self.assertEqual(tetromino.width(), 2)
        self.assertEqual(tetromino.height(), 3)
        self.assertTetrominosEqual(tetromino.rotate_right(), expected3)
        self.assertTetrominosEqual(tetromino.rotate_right(), expected4)
        self.assertTetrominosEqual(tetromino.flip(), expected2)
        self.assertTetrominosEqual(tetromino.rotate_left(), expected1)

    def test_STetromino(self): # pylint: disable=invalid-name
        tetromino = Tetromino.STetromino()
        expected1 = Tetromino([
            [0, 4, 4],
            [4, 4, 0],
        ], Tetromino.TYPES[4])
        expected2 = Tetromino([
            [4, 0],
            [4, 4],
            [0, 4],
        ], Tetromino.TYPES[4])
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
        ], Tetromino.TYPES[5])
        expected2 = Tetromino([
            [0, 5],
            [5, 5],
            [5, 0],
        ], Tetromino.TYPES[5])
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
        ], Tetromino.TYPES[6])
        expected2 = Tetromino([
            [0, 6],
            [0, 6],
            [6, 6],
        ], Tetromino.TYPES[6])
        expected3 = Tetromino([
            [6, 0, 0],
            [6, 6, 6],
        ], Tetromino.TYPES[6])
        expected4 = Tetromino([
            [6, 6],
            [6, 0],
            [6, 0],
        ], Tetromino.TYPES[6])
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
        ], Tetromino.TYPES[7])
        expected2 = Tetromino([
            [7, 7],
            [0, 7],
            [0, 7],
        ], Tetromino.TYPES[7])
        expected3 = Tetromino([
            [0, 0, 7],
            [7, 7, 7],
        ], Tetromino.TYPES[7])
        expected4 = Tetromino([
            [7, 0],
            [7, 0],
            [7, 7],
        ], Tetromino.TYPES[7])
        self.assertTetrominosEqual(tetromino, expected1)
        self.assertTetrominosEqual(tetromino.rotate_right(), expected2)
        self.assertTetrominosEqual(tetromino.rotate_right(), expected3)
        self.assertTetrominosEqual(tetromino.rotate_right(), expected4)
        self.assertTetrominosEqual(tetromino.rotate_right(), expected1)
        self.assertTetrominosEqual(tetromino.flip(), expected3)
        self.assertTetrominosEqual(tetromino.rotate_left(), expected2)
        self.assertTetrominosEqual(tetromino.rotate_left(), expected1)

if __name__ == '__main__':
    unittest.main()

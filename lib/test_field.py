"""
Unit tests for field.py
"""
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import unittest

import numpy as np

from lib.field import Field
from lib.tetromino import Tetromino

def generate_valid_state(state):
    """
    Given a partially filled np array (valid column count, but less than 22
    rows), this utility method fills the state the rest of the way.
    """
    height, width = state.shape
    assert width == Field.WIDTH
    return np.vstack([
        np.full((Field.HEIGHT - height, width), 0, dtype=np.uint8),
        state,
    ])

class FieldAssertions: # pylint: disable=too-few-public-methods, no-self-use
    def assertFieldsEqual(self, f1, f2): # pylint: disable=invalid-name
        """
        Helper method for asserting that two Field objects are equal.
        """
        if not isinstance(f1, Field):
            raise AssertionError(f'{f1} is not a Tetromino')
        if not isinstance(f2, Field):
            raise AssertionError(f'{f2} is not a Tetromino')
        np.testing.assert_array_equal(f1.state, f2.state)

class TestField(unittest.TestCase, FieldAssertions):
    def test_init(self):
        # Test that a newly initialized field object is empty.
        field = Field.create()
        self.assertIsNotNone(field)
        self.assertFalse(field.state.any())

        # Test that a valid state results in a properly initialized Field
        state = generate_valid_state(np.array([
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ], dtype=np.uint8))
        field = Field.create(state)
        self.assertIsNotNone(field)
        self.assertTrue((field.state == state).all())

        # Ensure that a copy was made of the input state.
        state[10, 1] = 2
        self.assertFalse((field.state == state).all())

        # Test that a invalid state returns None
        state = np.ones((2, 3))
        self.assertIsNone(Field.create(state))

    def test_drop(self):
        """
        Test various drop sequences and line clears.
        """
        state = generate_valid_state(np.array([
            [1, 1, 0, 1, 1, 0, 1, 1, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        ], dtype=np.uint8))
        field = Field.create(state)
        self.assertIsNotNone(field)

        lines_cleared = field.drop(Tetromino.JTetromino(), 0)
        self.assertEqual(lines_cleared, 0)
        expected_field = Field.create(generate_valid_state(np.array([
            [6, 6, 6, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 6, 1, 1, 0, 1, 1, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        ])))
        self.assertFieldsEqual(field, expected_field)

        lines_cleared = field.drop(
            Tetromino.TTetromino().rotate_right(), 8)
        self.assertEqual(lines_cleared, 1)
        expected_field = Field.create(generate_valid_state(np.array([
            [6, 6, 6, 0, 0, 0, 0, 0, 0, 3],
            [1, 1, 6, 1, 1, 0, 1, 1, 3, 3],
        ])))
        self.assertFieldsEqual(field, expected_field)

        field.drop(Tetromino.OTetromino(), 3)
        field.drop(Tetromino.ZTetromino(), 6)
        field.drop(Tetromino.JTetromino().flip(), 0)
        field.drop(Tetromino.OTetromino(), 8)
        expected_field = Field.create(generate_valid_state(np.array([
            [6, 0, 0, 0, 0, 0, 0, 0, 2, 2],
            [6, 6, 6, 2, 2, 0, 5, 5, 2, 2],
            [6, 6, 6, 2, 2, 0, 0, 5, 5, 3],
            [1, 1, 6, 1, 1, 0, 1, 1, 3, 3],
        ])))
        self.assertFieldsEqual(field, expected_field)
        lines_cleared = field.drop(Tetromino.ITetromino().rotate_right(), 5)
        self.assertEqual(lines_cleared, 2)
        expected_field = Field.create(generate_valid_state(np.array([
            [6, 0, 0, 0, 0, 1, 0, 0, 2, 2],
            [6, 6, 6, 2, 2, 1, 0, 5, 5, 3],
        ])))

    def test_count_gaps(self):
        """
        Test that gap counting works as expected with filled/non-filled columns.
        """
        field = Field.create()
        self.assertEqual(field.count_gaps(), 0)

        field = Field.create(generate_valid_state(np.array([
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 1, 0, 1, 1, 1, 1, 1, 1],
        ])))
        self.assertEqual(field.count_gaps(), 0)

        field = Field.create(generate_valid_state(np.array([
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ])))
        self.assertEqual(field.count_gaps(), 1)

        field = Field.create(generate_valid_state(np.array([
            [1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 1, 1, 0, 0, 0, 0, 0, 1, 0],
            [1, 0, 0, 1, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 1, 0, 0, 0, 1, 1, 1],
        ])))
        self.assertEqual(field.count_gaps(), 6)

    def test_heights(self): # pylint: disable=no-self-use
        """
        Test that height calculation works as expected with filled/non-filled
        columns.
        """
        field = Field.create()
        expected_heights = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        np.testing.assert_array_equal(field.heights(), expected_heights)

        field = Field.create(generate_valid_state(np.array([
            [1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 1, 1, 0, 0, 0, 0, 0, 1, 0],
            [1, 0, 0, 1, 0, 0, 0, 0, 1, 0],
            [0, 0, 1, 1, 0, 0, 0, 1, 1, 1],
        ])))
        expected_heights = np.array([4, 3, 3, 2, 0, 0, 0, 1, 4, 1])
        np.testing.assert_array_equal(field.heights(), expected_heights)

if __name__ == '__main__':
    unittest.main()

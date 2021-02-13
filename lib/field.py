"""
The Field class encapsulates the Tetris game field and the logic to place and
drop tetrominoes within it.
"""

import numpy as np

from lib.tetromino import Tetromino

class Field(): # pylint: disable=missing-class-docstring

    WIDTH = 10
    HEIGHT = 22
    SCORING_ELEMENTS = 6

    def __init__(self, state):
        """
        Initializes a Tetris Field. Rows increase downward and columns increase
        to the right in the np array representation. Invoke Field.create()
        instead.
        """
        self.state = state

    @staticmethod
    def create(state=None):
        """
        Factory method to create a Field object, with an optional input state
        np array parameter. If the input state is not valid, then this method
        returns None. This does not make a copy of the input state.
        """
        if state is not None:
            if state.shape == (Field.HEIGHT, Field.WIDTH):
                return Field(np.array(state, dtype=np.uint8, copy=True))
            return None
        return Field(np.full((Field.HEIGHT, Field.WIDTH), 0, dtype=np.uint8))

    def __str__(self):
        """
        Returns a string representation of the field.
        """
        bars = '   |' + ' '.join(map(str, range(Field.WIDTH))) + '|\n'
        mapped_field = np.vectorize(Tetromino.TYPES.__getitem__)(self.state)
        field = '\n'.join(['{:2d} |'.format(i) + ' '.join(row) + '|'
                           for i, row in enumerate(mapped_field)])
        return bars + field + '\n' + bars

    def _test_tetromino_(self, tetromino, r_start, c_start):
        """
        Tests to see if a tetromino can be placed at the specified row and
        column. It performs the test with the top left corner of the
        tetromino at the specified row and column.
        """
        r_end, c_end = r_start + tetromino.height(), c_start + tetromino.width()
        if c_start < 0 or c_end > Field.WIDTH:
            return False
        if r_start < 0 or r_end > Field.HEIGHT:
            return False
        test_area = self.state[r_start:r_end, c_start:c_end]
        for test_space, tetromino_space in zip(
                test_area.flat, tetromino.state.flat):
            if test_space != 0 and tetromino_space != 0:
                return False
        return True

    def _place_tetromino_(self, tetromino, r_start, c_start):
        """
        Place a tetromino at the specified row and column. The bottom left
        corner of the tetromino will be placed at the specified row and column.
        This function only performs boundary checks and will overwrite filled
        spaces in the field.
        """
        r_end, c_end = r_start + tetromino.height(), c_start + tetromino.width()
        assert c_start >= 0 and c_end <= Field.WIDTH
        assert r_start >= 0 and r_end <= Field.HEIGHT
        for tetromino_row, start_row in enumerate(range(r_start, r_end)):
            for tetromino_col, start_col, in enumerate(range(c_start, c_end)):
                if tetromino[tetromino_row][tetromino_col] != 0:
                    self.state[start_row][start_col] = tetromino[
                        tetromino_row][tetromino_col]

    def _get_tetromino_drop_row_(self, tetromino, column):
        """
        Given a tetromino and a column, returns the row that the top of the
        tetromino would end up in if it were dropped in that column. This helper
        also assumes the leftmost column of the tetromino will be aligned with
        the specified column.
        """
        if column < 0 or column + tetromino.width() > Field.WIDTH:
            return -1
        last_fit = -1
        for row in range(tetromino.height(), Field.HEIGHT):
            if self._test_tetromino_(tetromino, row, column):
                last_fit = row
            else:
                return last_fit
        return last_fit

    def _line_clear_(self):
        """
        Checks and removes all filled lines, returning the number of lines
        cleared.
        """
        filled_lines = np.array([row.all() for row in self.state])
        if filled_lines.any():
            n_filled = filled_lines.sum()
            self.state = np.vstack([
                np.full((n_filled, Field.WIDTH), 0, dtype=np.uint8),
                self.state[np.logical_not(filled_lines)],
            ])
            return n_filled
        return 0

    def copy(self):
        """
        Returns a copy of the field.
        """
        return Field(self.state)

    def drop(self, tetromino, column):
        """
        Drops a tetromino in the specified column. The leftmost column of the
        tetromino will be aligned with the specified column.

        Returns the number of lines cleared, if applicable, or -1 if this
        tetromino cannot be dropped in this column.
        """
        assert isinstance(tetromino, Tetromino)
        if (row := self._get_tetromino_drop_row_(tetromino, column)) == -1:
            return -1
        self._place_tetromino_(tetromino, row, column)
        return self._line_clear_()

    def count_gaps(self):
        """
        Check each column one by one to make sure there are no gaps in the
        column.
        """
        # Find the row of the highest tetromino piece in each column.
        top_indices = np.argmax(self.state.T != 0, axis=1)
        # If a column is empty, then set the top index for it to the bottom so
        # we don't count it.
        top_indices[top_indices == 0] = Field.HEIGHT
        # Count the number of gaps past the first filled space per column
        gaps = [np.count_nonzero(col[top:] == 0) for col, top in zip(
            self.state.T, top_indices)]
        return sum(gaps)

    def heights(self):
        """
        Return an array containing the heights of each column, where heights is
        defined as the furthest distance of a tetromino piece in a given column
        from the bottom of the field, regardless of whether the spaces in
        between are filled.
        """
        top_indices = np.argmax(self.state.T != 0, axis=1)
        top_indices[top_indices == 0] = Field.HEIGHT
        return Field.HEIGHT - top_indices

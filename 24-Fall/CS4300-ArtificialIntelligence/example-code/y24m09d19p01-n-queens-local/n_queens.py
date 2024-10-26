#!/usr/bin/env python3

import copy
import random

class NQueensBoard:
    """
    Represent a state in the N-Queens problem
    A vector of positions. Each slot corresponds to a column on the board.
    The value stored is the row that the queen is on. 
    -1 means not yet placed.
    """

    def __init__(self, n):
        self._data = [-1] * n
        self._n = n
        return

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value
        return

    def __str__(self):
        s = "|"
        for c in range(self._n):
            s += " {} |".format(self._data[c])
        return s

    def __repr__(self):
        return "NQueensBoard<{}>".format(str(self))

NEIGHBORS_ALL_ROWS = 0
NEIGHBORS_NEXT_ROW = 1
class NQueensProblem:
    """
    Represent the N-Queens problem to facilitate search.
    """

    def __init__(self, n):
        self._n = n
        self._neighbors_mode = NEIGHBORS_ALL_ROWS
        return

    def STEP_COST(self, s0, a, s1):
        return 1
        
    def STATE_AS_KEY(self, state):
        key = []
        for c in range(self._n):
            key.append(state[c])
        return tuple(key)

    def ACTIONS(self, state):
        """
        List of legal placements.
        -> [ (row, col), (row, col), ... ]
        
        Only allow placement of queen in first column not yet set
        """
        actions = []
        for col in range(self._n):
            if state[col] != -1: continue
            for row in range(self._n):
                if not self.conflict(state, row, col):
                    actions.append((row, col))
            break
        return actions

    def RESULT(self, state, action):
        """
        place a queen at (row,col) = action.
        return updated state
        """
        (row,col) = action
        state1 = copy.deepcopy(state)
        state1[col] = row
        return state1

    def conflict(self, state, row, col):
        for c0 in range(self._n):
            r0 = state[c0]
            if r0 < 0: continue
            if self.squares_conflict(r0, c0, row, col):
                return True
        return False

    def squares_conflict(self, r0, c0, r1, c1):
        if r0 == r1 or c0 == c1:
            return True
        elif r0 - r1 == c0 - c1 or r0 - r1 == c1 - c0:
            return True
        else:
            return False

    def GOAL_TEST(self, state):
        for c0 in range(self._n):
            if state[c0] < 0:
                return False
        for c0 in range(self._n):
            for c1 in range(c0+1, self._n):
                if self.squares_conflict(c0, state[c0], c1, state[c1]):
                    return False
        return True

    def HEURISTIC(self, state):
        return 0

    # support for local search
    def set_neighbors_all_rows(self):
        self._neighbors_mode = NEIGHBORS_ALL_ROWS
        return

    def set_neighbors_next_row(self):
        self._neighbors_mode = NEIGHBORS_NEXT_ROW
        return

    def _neighbors_all_rows(self, state):
        """We define a neighbor as moving one queen to a different row, for all rows."""
        neighbors = []
        for c in range(self._n):
            for r in range(self._n):
                if state[c] == r: continue
                state1 = copy.deepcopy(state)
                state1[c] = r
                neighbors.append(state1)
        return neighbors

    def _neighbors_next_row(self, state):
        """We define a neighbor as moving one queen up or down a row."""
        neighbors = []
        for c in range(self._n):
            if state[c] > 0:
                state1 = copy.deepcopy(state)
                state1[c] = state1[c]-1
                neighbors.append(state1)
            if state[c] < self._n-1:
                state1 = copy.deepcopy(state)
                state1[c] = state1[c]+1
                neighbors.append(state1)
        return neighbors

    def NEIGHBORS(self, state):
        if self._neighbors_mode == NEIGHBORS_ALL_ROWS:
            return self._neighbors_all_rows(state)
        elif self._neighbors_mode == NEIGHBORS_NEXT_ROW:
            return self._neighbors_next_row(state)
        else:
            raise Exception("Unexpected neighbors mode: {}".format(self._neighbors_mode))
        return []

    def UTILITY(self, state):
        """
        We define utility as negative: the number of piece-piece conflicts.
        The largest utility is 0.0. 
        The more conflicts, the larger the negative utility.
        """
        count = 0.0
        for c0 in range(self._n):
            for c1 in range(c0+1,self._n):
                if self.squares_conflict(state[c0], c0, state[c1], c1):
                    count += 1
        return -count

    def RANDOM_STATE(self):
        state = NQueensBoard(self._n)
        for c in range(self._n):
            state[c] = random.randint(0, self._n-1)
        return state

def main():
    N = 4
    model = NQueensProblem(N)
    board = NQueensBoard(N)
    print(board)
    print(model.ACTIONS(board))

    state = model.RANDOM_STATE()
    print(state)
    print(model.UTILITY(state))
    print(model.NEIGHBORS(state))
    
    return

if __name__ == "__main__":
    main()

import numpy as np
import copy

class UniformCoinsState:
    """A collection of N coins. Turn over coins until all coins are tails, or all coins are heads."""

    def __init__(self, size=5):
        """0 == heads, 1 == tails"""
        self._coins = np.zeros(size, dtype=np.int8)
        self._size = size
        return

    @property
    def size(self):
        return self._size

    def randomize(self, seed=None):
        if seed is not None:
            np.random.seed(seed)
        self._coins = np.random.randint(2, size=self._size, dtype=np.int8)
        return self._coins

    def turn(self, action):
        """action: integer index into coins"""
        self._coins[action] = not self._coins[action]
        return

    @property
    def observation(self):
        return self._coins

    @observation.setter
    def observation(self, value):
        self._coins = value
        self._size = value.shape[0]
        return

    def coin(self, index):
        return self._coins[index]

    def __str__(self):
        s = "|"
        for coin in self._coins:
            s += f" {coin} |"
        return s

if __name__ == "__main__":
    s = UniformCoinsState(7)
    print(s)
    s.randomize()
    print(s)
    s.randomize()
    print(s)
    for i in range(7):
        s.turn(i)
    print(s)

    
class UniformCoinsModel:

    def ACTIONS(state):
        actions = [i for i in range(state.size)]
        return actions

    def RESULT(state, action):
        state1 = copy.deepcopy(state)
        state1.turn(action)
        return state1

    def GOAL_TEST(state):
        for i in range(state.size):
            if state.coin(0) != state.coin(i):
                return False
        return True

    def STEP_COST(state, action, state1):
        if state.coin(action) == 0:
            cost = 0.9
        else:
            cost = 1.1
        return cost

    def HEURISTIC(state):
        estimated_cost = 0.0
        return estimated_cost

if __name__ == "__main__":
    state = UniformCoinsState(7)
    state.randomize()
    actions = UniformCoinsModel.ACTIONS(state)
    print(actions)

    state = UniformCoinsState(13)
    state.randomize()
    actions = UniformCoinsModel.ACTIONS(state)
    print(actions)

    print()
    state = UniformCoinsState(13)
    state.randomize()
    print(state)
    state1 = UniformCoinsModel.RESULT(state, 4)
    print(state1)

    print()
    state = UniformCoinsState(13)
    print(UniformCoinsModel.GOAL_TEST(state))
    state.randomize()
    print(UniformCoinsModel.GOAL_TEST(state))
    
    print()
    state = UniformCoinsState(13)
    state.randomize()
    print(state)
    action = 2
    state1 = UniformCoinsModel.RESULT(state, action)
    print(UniformCoinsModel.STEP_COST(state, action, state1))

    

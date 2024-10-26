#!/usr/bin/env python3

import gymnasium as gym
import uniform_coins
import random

def depth_limited_search(state, max_depth, model):
    # node = (state, parent_node, action, depth)
    frontier = [(state, None, None, 0)]
    goal_node = None
    while len(frontier) > 0:
        node = frontier.pop()
        state, parent, action, depth = node
        if model.GOAL_TEST(state):
            goal_node = node
            break
        if depth + 1 <= max_depth:
            for action in model.ACTIONS(state):
                state1 = model.RESULT(state, action)
                node1 = (state1, node, action, depth+1)
                frontier.append(node1)

    action = None
    if goal_node is not None:
        node = goal_node
        while (node[1] is not None) and (node[1][1] is not None):
            node = node[1]
        if node[1] is None:
            # root node was goal node
            pass
        elif node[1][1] is None:
            action = node[2]
        found_goal = True
    else:
        found_goal = False
                    
    return action, found_goal

def agent_function(state, model):
    """
    state: A uniform_coins.UniformCoinsState object. The current state of the environment.
    
    returns: An integer, the coin to turn over.
    """
    for limit in range(1, state.size+1):
        action, found_goal = depth_limited_search(state, limit, model)
        if found_goal:
            break

    return action

def main():
    model = uniform_coins.UniformCoinsModel
    
    coin_count = 9

    # render_mode = None
    # render_mode = "ansi"
    # render_mode = "rgb_array"
    render_mode = "human"

    env = gym.make('uniform_coins/UniformCoins-v0', render_mode=render_mode, coin_count=coin_count)
    observation, info = env.reset()
    state = uniform_coins.UniformCoinsState()
    state.observation = observation
    
    terminated = truncated = False
    if render_mode == "ansi":
        print("Current state:", env.render())
    while not (terminated or truncated):
        action = agent_function(state, model)
        if render_mode == "ansi":
            print()
            print(f"Action: turn coin {action}.")
        observation, reward, terminated, truncated, info = env.step(action)
        state.observation = observation
        if render_mode == "ansi":
            print("Current state:", env.render())

    env.close()
    return

if __name__ == "__main__":
    main()
    


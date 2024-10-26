#!/usr/bin/env python3

import gymnasium as gym
import random
import math

#
# Documentation
# https://gymnasium.farama.org/environments/classic_control/mountain_car/
#

ACTION_NOOP = 0
ACTION_FIRE_LEFT = 1
ACTION_FIRE_MAIN = 2
ACTION_FIRE_RIGHT = 3
ACTIONS_ALL = [ACTION_NOOP, ACTION_FIRE_LEFT, ACTION_FIRE_MAIN, ACTION_FIRE_RIGHT]

def unpack_observation(observation):
    # the coordinates of the lander in x & y, its linear velocities in x & y, its angle, its angular velocity, and two booleans that represent whether each leg is in contact with the ground or not
    x, y, dx, dy, angle, d_angle, left, right = observation
    print(x, y, dx, dy, angle, d_angle, left, right)
    return x, y, dx, dy, angle, d_angle, left, right

def agent_function(observation):
    """This agent's strategy is to randomly choose an action.
    """
    unpack_observation(observation)
    action = random.choice(ACTIONS_ALL)
    return action

def create_environment():
    env = gym.make('LunarLander-v2', render_mode="human")
    return env

def run_one_episode(env, agent_function):
    observation, info = env.reset()
    terminated = False
    truncated = False
    total_reward = 0
    while not (terminated or truncated):
        action = agent_function(observation)
        observation, reward, terminated, truncated, info = env.step(action)
        total_reward += reward
    return total_reward

def destroy_environment(env):
    env.close()
    return

def main():
    env = create_environment()
    reward = run_one_episode(env, agent_function)
    destroy_environment(env)
    print(f"Reward: {reward}")
    return

if __name__ == "__main__":
    main()


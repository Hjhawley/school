#!/usr/bin/env python3

import gymnasium as gym
import random
import math

#
# Documentation
# https://gymnasium.farama.org/environments/classic_control/mountain_car/
#

ACTION_PUSH_LEFT = 0
ACTION_NOOP = 1
ACTION_PUSH_RIGHT = 2

def unpack_observation(observation):
    position, velocity = observation
    return position, velocity

def agent_function(observation):
    """This agent's strategy is to push the car right when on the left side of the valley.
    Otherwise, do nothing.
    """
    center_x = - math.pi/6.0
    position, velocity = unpack_observation(observation)
    if position < center_x:
        action = ACTION_PUSH_RIGHT
    else:
        action = ACTION_NOOP
    return action

def create_environment():
    env = gym.make('MountainCar-v0', render_mode="human")
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


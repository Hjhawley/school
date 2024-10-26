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
ACTIONS_ALL = [ACTION_PUSH_LEFT, ACTION_NOOP, ACTION_PUSH_RIGHT]

def unpack_observation(observation):
    position, velocity = observation
    return position, velocity

def agent_function(observation):
    """This agent's strategy is to randomly choose an action.
    """
    position, velocity = unpack_observation(observation)
    center_x = -math.pi/6.0
    if velocity < 0:
        action = ACTION_PUSH_LEFT
    else:
        action = ACTION_PUSH_RIGHT
    return action

def create_environment(render_mode):
    env = gym.make('MountainCar-v0', render_mode=render_mode)
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
    render_mode = None
    env = create_environment(render_mode)
    episode_count = 100
    reward_sum = 0
    for i in range(episode_count):
        reward_sum += run_one_episode(env, agent_function)
    destroy_environment(env)
    reward = reward_sum / episode_count
    print(f"Reward: {reward}")
    return

if __name__ == "__main__":
    main()


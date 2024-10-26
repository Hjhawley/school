#!/usr/bin/env python3

import gymnasium as gym
import numpy as np

def random_policy():
    actions = np.array([0, 1, 2, 3])
    policy = np.random.choice(actions, size=48)
    return policy

def evaluate_policy(env, policy):
    observation, info = env.reset()
    terminated = False
    truncated = False
    total_reward = 0
    while not (terminated or truncated):
        action = policy[observation]
        observation, reward, terminated, truncated, info = env.step(action)
        total_reward += reward
    
    return total_reward

env = gym.make("CliffWalking-v0", render_mode=None)
env = gym.wrappers.TimeLimit(env, max_episode_steps=50)

policy = random_policy()
score = evaluate_policy(env, policy)

print(policy)
print(score)

env.close()

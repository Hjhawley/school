#!/usr/bin/env python3

import gymnasium as gym


env = gym.make("CliffWalking-v0", render_mode="human")
env = gym.wrappers.TimeLimit(env, max_episode_steps=50)

observation, info = env.reset()

terminated = False
truncated = False
while not (terminated or truncated):
    action = env.action_space.sample()
    observation, reward, terminated, truncated, info = env.step(action)


env.close()

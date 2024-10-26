#!/usr/bin/env python3

from pettingzoo.classic import connect_four_v3
import connect_four_model
import time
import copy
import random

def player_simple(env, agent):
    observation, reward, termination, truncation, info = env.last()
    if termination or truncation:
        action = None
    else:
        action = None
        searchable_env = connect_four_model.ConnectFour()
        searchable_env.copy_from_env(env)
        for possible_action in searchable_env.legal_moves():
            env1 = copy.deepcopy(searchable_env)
            env1.step(possible_action)
            if env1.game_over():
                action = possible_action
        if action is None:
            action = random.choice(searchable_env.legal_moves())
    return action

def player_random(env, agent):
    observation, reward, termination, truncation, info = env.last()
    if termination or truncation:
        action = None
    else:
        mask = observation["action_mask"]
        action = env.action_space(agent).sample(mask)  # this is where you would insert your policy
    return action

def main():
    agent_function = { "player_0": player_random, "player_1": player_simple }
    times = { "player_0": 0.0, "player_1": 0.0 }

    # env = connect_four_v3.env(render_mode="human")
    env = connect_four_v3.env(render_mode=None)
    env.reset()

    for agent in env.agent_iter():
        if True:
            """text display of board"""
            env1 = connect_four_model.ConnectFour()
            env1.copy_from_env(env)
            print(env1)
            print()
            print()
            print()
        t1 = time.time()
        action = agent_function[agent](env, agent)
        t2 = time.time()
        times[agent] += (t2-t1)

        env.step(action)
        try:
            observation, reward, termination, truncation, info = env.last()
            print("{} took action {}".format(agent, action))
            if termination or truncation:
                print(env.rewards)
        except:
            pass

    # time.sleep(10) # useful for end of game with human render mode
    env.close()

    for agent in times:
        print(f"{agent} took {times[agent]:8.5f} seconds.")
    return

if __name__ == "__main__":
    if False:
        import cProfile
        cProfile.run('main()')
    else:
        main()

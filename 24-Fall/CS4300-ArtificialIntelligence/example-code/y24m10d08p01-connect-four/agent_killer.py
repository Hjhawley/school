#!/usr/bin/env python3

import numpy as np
import time

class AgentRandom:

    def __init__(self):
        """required method"""
        return

    def reset(self):
        """required method"""
        return

    def agent_function(self, observation, agent):
        """required method"""
        # print("observation")
        # print(observation)
        action = np.random.choice(np.where(observation['action_mask'])[0])
        return action

AgentKiller = AgentRandom
ConnectFourAgent = AgentRandom

    

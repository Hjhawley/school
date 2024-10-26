from gymnasium.envs.registration import register

from uniform_coins.envs.uniform_coins_env import UniformCoinsEnv
from uniform_coins.envs.uniform_coins_model import UniformCoinsModel
from uniform_coins.envs.uniform_coins_model import UniformCoinsState

register(
    # uniform_coins is this folder name
    # -v0 is because this first version
    # UniformCoins is the pretty name for gym.make
    id="uniform_coins/UniformCoins-v0",
    
    # uniform_coins.envs is the path uniform_coins/envs
    # UniformCoinsEnv is the class name
    entry_point="uniform_coins.envs:UniformCoinsEnv",
    
    # configure the automatic wrapper to truncate after 50 steps
    max_episode_steps=50,
)

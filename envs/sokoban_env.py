import gym
from gym.utils import seeding
from gym.spaces.discrete import Discrete
from gym.spaces import Box
from .room import creating_room
from .render import room_to_rgb, room_to_tiny_world_rgb
import numpy as np

class SokobanEnv(gym.Env):
    metadata = {
        "render.modes":["human","rgb_array","tiny_human","tiny_rgb_array","raw"],
        "render_modes":["human","rgb_array","tiny_human","tiny_rgb_array","raw"]

    }

    def __init__(self,
                 dim_room=(10,10),
                 max_steps=120,
                 num_boxes=4,
                 num_gen_steps=None,
                 reset=True):
        self.dim_room=dim_room

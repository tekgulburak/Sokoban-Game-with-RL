import gym
from gym.utils import seeding
from gym.spaces.discrete import Discrete
from gym.spaces import Box
from .room import creating_room
from .render import room_to_rgb, room_to_tiny_world_rgb
from .render import ACTION_LOOKUP
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
        if num_gen_steps==None:
            self.num_gen_steps=int(1.7*(self.dim_room[0]+dim_room[1]))

        else:
            self.num_gen_steps=num_gen_steps

        self.num_boxes=num_boxes
        self.boxes_on_target=0

        #penalties and rewards
        self.penalty_for_step=-0.1
        self.penalty_box_off_target=-1
        self.reward_box_on_target=1
        self.reward_finished=10
        self.reward_last=0

        #other settings
        self.viewer=None
        self.max_steps=max_steps
        self.action_space=Discrete(len(ACTION_LOOKUP))
        screen_height,screen_width=(dim_room[0]*16,dim_room[1]*16)
        self.observation_space=Box(low=0,high=255,shape=(screen_height,screen_width,3),dtype=np.uint8)

        if reset:
            _=self.reset()

    def seed(self,seed=None):
        self.np_random,seed=seeding.np_random(seed)
        return [seed]






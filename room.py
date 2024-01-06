import random
import numpy as np
import marshal

def creating_room(dim=(13,13),p_change_directions=0.35,num_steps=25,num_boxes=3,tries=4,second_player=False):

    room_state=np.zeros(shape=dim)
    room_structure=np.zeros(shape=dim)
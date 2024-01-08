import random
import numpy as np
import marshal
"""dim=(13,13)
room_structure=np.zeros(shape=dim)
room_structure[room_structure == 5] = 1
room_structure"""


def creating_room(dim=(13,13),p_change_directions=0.35,num_steps=25,num_boxes=3,tries=4,second_player=False):

    room_state=np.zeros(shape=dim)
    room_structure=np.zeros(shape=dim)

    for x in range(tries):
        room=room_topology_generation(dim,p_change_directions,num_steps)
        room=place_boxes_and_player(room,num_boxes=num_boxes,second_player=second_player)

        room_structure=np.copy(room)
        room_structure[room_structure==5]=1

        room_state=np.copy(room)
        room_state[room_state==2]=4

        room_state,score,box_mapping=reverse_playing(room_state,room_structure)
        room_state[room_state==3]=4

        if score>0:
            break
        
    if score==0:
        raise RuntimeWarning("Generated model with score==0")

    return room_structure,room_state,box_mapping

def room_topology_generation(dim=(10,10)):
    dim_x,dim_y=dim

    masks=[
        [
            [0,0,0],
            [1,1,1],
            [0,0,0]
        ],
        [
            [0,1,0],
            [0,1,0],
            [0,1,0]
        ],
        [
            [0,0,0],
            [1,1,0],
            [0,1,0]
        ],
        [
            [0,0,0],
            [1,1,0],
            [1,1,0]
        ],
        [
            [0,0,0],
            [0,1,1],
            [0,1,0]
        ]

    ]
    import random

    directions=[(1,0),(0,1),(-1,0),(0,-1)]
    direction=random.sample(directions,1)[0]
    dim_x,dim_y=(10,10)
    position=np.array([
        random.randint(1,dim_x-1),
        random.randint(1,dim_y-1)
    ])

    level=np.zeros(dim,dtype=int)

    for s in range(num_steps):
        if random.random() < p_change_directions:
            direction=random.sample(directions,1)[0]

        position=position+direction
        position[0]=max(min(position[0],dim_x-2),1)
        position[1]=max(min(position[1],dim_y-2),1)

        mask=random.sample(masks,1)[0]
        mask_start=position-1
        level[mask_start[0]:mask_start[0]+3,mask_start[1]:mask_start[1]+3]+=mask

    level[level>0]=1
    level[:,[0,dim_y-1]]=0
    level[[0,dim_x-1],:]=0
    return level

def place_boxes_and_player(room,num_boxes,second_player):
    possible_positions=np.where(room==1)
    num_possible_positions=possible_positions[0].shape[0]
    num_players=2 if second_player else 1






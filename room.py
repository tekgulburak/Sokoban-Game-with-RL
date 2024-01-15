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
    """room = np.array([[0, 1, 0, 1],
                     [1, 0, 0, 1],
                     [0, 1, 1, 0]])
    """
    possible_positions=np.where(room==1)
    num_possible_positions=possible_positions[0].shape[0]
    num_players=2 if second_player else 1

    if num_possible_positions<=num_boxes+num_players:
        raise  RuntimeError("not enough (#{}) to place {} player and {} boxes".format(num_possible_positions,num_players,num_boxes))

    ind=np.random.randint(num_possible_positions)
    player_position=possible_positions[0][ind],possible_positions[1][ind]
    room[player_position]=5

    if second_player:
        ind=np.random.randint(num_possible_positions)
        player_position=possible_positions[0][ind],possible_positions[1][ind]
        room[player_position]=5

    for i in range(num_boxes):
        possible_positions=np.where(room==1)
        num_possible_positions=possible_positions[0].shape[0]
        ind=np.random.randint(possible_positions)
        box_position=possible_positions[0][ind],possible_positions[1][ind]
        room[box_position]=2

    return room

explored_states=set()
num_boxes=0
best_room_score=-1
best_room=None
best_box_mapping=None


def reverse_playing(room_state,room_structure,search_depth=100):
    global explored_states,num_boxes,best_room_score,best_room,best_box_mapping

    box_mapping={}
    box_locations=np.where(room_structure==2)
    num_boxes=len(box_locations[0])
    for i in range(num_boxes):
        box=(box_locations[0][i],box_locations[1][i])
        box_mapping[box]=box

    explored_states=set()
    best_room_score=-1
    best_box_mapping=box_mapping
    depth_first_search(room_state,room_structure,box_mapping,box_swaps=0,last_pull=(-1,-1),ttl=300)

    return best_room,best_room_score,best_box_mapping


def depth_first_search(room_state,room_structure,box_mapping,box_swaps=0,last_pull=(-1,-1),ttl=300):

    global explored_states,num_boxes,best_room_score,best_room,best_box_mapping

    ttl-=1
    if ttl<=0 or len(explored_states)>=300000:
        return

    state_tohash=marshal.dumps(room_state)

    if not state_tohash in explored_states:
        room_score=box_swaps*box_displacement_score(box_mapping)
        if np.where(room_state==2)[0].shape[0]!=num_boxes:
            room_score=0

        if room_score>best_room_score:
            best_room=room_state
            best_room_score=room_score
            best_box_mapping=box_mapping

        explored_states.add(state_tohash)

        for action in ACTION_LOOKUP.keys():
            room_state_next=room_state.copy()
            box_mapping_next=box_mapping.copy()

            room_state_next,box_mapping_next,last_pull_next= \
                reverse_move(room_state_next,room_structure,box_mapping_next,last_pull,action)

            box_swaps_next=box_swaps
            if last_pull_next!=last_pull:
                box_swaps_next+=1

            depth_first_search(room_state_next,room_structure,box_mapping_next,box_swaps_next,last_pull,ttl)
#copy fonksiyonu örneklerine bak
#\ ne işe yarıyor
#global burada ne işe yarıyor
#genel olarak bir incele

def reverse_move(room_state,room_structure,box_mapping,last_pull,action):

    player_position=np.where(room_state[0]==5)
    player_position=np.array(player_position[0][0],player_position[1][0])#şunu bir dene değerlere bak

    change=Change_Coordinates[action%4]
    next_position=player_position+change

    if room_state[next_position[0],next_position[1] in [1,2]]:

        room_state[player_position[0],player_position[1]]=room_structure[player_position[0],player_position[1]]
        room_state[next_position[0],next_position[1]]=5








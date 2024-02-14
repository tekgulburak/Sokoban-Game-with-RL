import numpy as np
import pkg_resources
import imageio

def room_to_rgb(room,room_structure):
    resource_package=__name__
    room=np.array(room)

    if not room_structure is None:
        room[room==5 and room_structure==2]=6

    box_filename=pkg_resources.resource_filename(resource_package,"/".join(("surface","box.png")))
    box=imageio.imread(box_filename)

    box_on_target_filename=pkg_resources.resource_filename(resource_package,"/".join(("surface","box_on_target.png")))
    box_on_target=imageio.imread(box_on_target_filename)

    box_target_filename=pkg_resources.resource_filename(resource_package,"/".join(("surface","box_target.png")))
    box_target=imageio.imread(box_target_filename)

    floor_filename=pkg_resources.resource_filename(resource_package,"/".join(("surface","floor.png")))
    floor=imageio.imread(floor_filename)

    player_filename=pkg_resources.resource_filename(resource_package,"/".join(("surface","player.png")))
    player=imageio.imread(player_filename)

    player_on_target_filename=pkg_resources.resource_filename(resource_package,"/".join(("surface","player_on_target.png")))
    player_on_target=imageio.imread(player_on_target_filename)

    wall_file=pkg_resources.resource_filename(resource_package,"/".join(("surface","wall.png")))
    wall=imageio.imread(wall_file)

    surfaces=[wall,floor,box_target,box_on_target,box,player,player_on_target]

    room_rgb=np.zeros(shape=(room.shape[0]*16,room.shape[1]*16,3),dtype=np.uint8)



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
    for i in range(room.shape[0]):
        x_i=i*16

        for j in range(room.shape[1]):
            y_j=j*16
            surfaces_id=room[i,j]

            room_rgb[x_i:(x_i+16),y_j:(y_j+16),:]=surfaces[surfaces_id]

    return room_rgb

    def room_to_tiny_world_rgb(room,room_structure=None,scale=1):

        room=np.array(room)
        if not room_structure is None:
            room[(room==5) & (room==2)]= 6

        wall=[0,0,0]
        floor=[243,248,238]
        box_target=[254,95,56]
        box=[142,121,56]
        player=[160,212,56]
        player_on_target=[219,212,56]

        surfaces=[wall,floor,box_target,box,player,player_on_target]

        room_small_rgb=np.zeros(shape=(room.shape[0]*scale,room.shape[1]*scale,3),dtype=np.uint8)

        for i in range(room.shape[0]):
            x_i=i*scale
            for j in range(room.shape[1]):
                y_j=j*scale
                surfaces_id=int(room[i,j])
                room_small_rgb[x_i:(x_i+scale),y_j:(y_j+scale),:]=np.array((surfaces[surfaces_id]))

        return room_small_rgb

    def room_to_rgb_FT(room,box_mapping,room_structure=None):
        resource_package=__name__

        room=np.array(room)
        if not room_structure is None:
            room[(room==5) & (room==2)]=6

        box_filename=pkg_resources.resource_filename(resource_package,"/".join(("surface","box.png")))
        box=imageio.imread(box_filename)

        box_on_target_filename=pkg_resources.resource_filename(resource_package,"/".join(("surface","box_on_target.png")))
        box_on_target=imageio.imread(box_on_target_filename)

        box_target_filename = pkg_resources.resource_filename(resource_package, '/'.join(('surface', 'box_target.png')))
        box_target = imageio.imread(box_target_filename)

        floor_filename = pkg_resources.resource_filename(resource_package, '/'.join(('surface', 'floor.png')))
        floor = imageio.imread(floor_filename)

        player_filename = pkg_resources.resource_filename(resource_package, '/'.join(('surface', 'player.png')))
        player = imageio.imread(player_filename)

        player_on_target_filename = pkg_resources.resource_filename(resource_package,
                                                                    '/'.join(('surface', 'player_on_target.png')))
        player_on_target = imageio.imread(player_on_target_filename)

        wall_filename = pkg_resources.resource_filename(resource_package, '/'.join(('surface', 'wall.png')))
        wall = imageio.imread(wall_filename)

        surfaces = [wall, floor, box_target, box_on_target, box, player, player_on_target]

        room_rgb=np.zeros(shape=(room.shape[0]*16,room.shape[1]*16,3),dtype=np.uint8)
        for i in range(room.shape[0]):
            x_i=i*16

            for j in range(room.shape[1]):
                y_j=j*16

                surfaces_id=room[i,j]
                surface=surfaces[surfaces_id]
                if 1<surfaces_id<5:
                    try:
                        surface=get_proper_box_surface(surfaces_id,box_mapping,i,j)
                    except:
                        pass

                room_rgb[x_i:(x_i+16),y_j:(y_j+16),:]=surface

        return room_rgb

    def get_proper_box_surface(surfaces_id,box_mapping,i,j):
        box_id=0
        situation=""
        if surfaces_id==2:
            situation="_target"
            box_id=list(box_mapping.keys()).index((i,j))

        elif surfaces_id==3:
            box_id=list(box_mapping.values()).index((i,j))
            box_key=list(box_mapping.keys()).index((i,j))
            if box_key==(i,j):
                situation="_on_target"

            else:
                situation="_on_wrong_target"

            pass
        elif surfaces_id==4:
            box_id=list(box_mapping.values()).index((i,j))

        surface=[255,255,255]
        if box_id==0:
            if situation=="target":
                surface=[111,27,232]

            elif situation=="on_target":
                surface=[6,33,130]

            elif situation=="on_wrong_target":
                surface=[69,81,122]

            else:
                surface=[11,60,237]




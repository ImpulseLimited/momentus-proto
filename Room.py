import pygame
import xml.etree.ElementTree as ET
import os
import random

import Config as cfg
from objects.Door import Door

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Room:
    """This class contains all settings related to a room in dungeon.

    """
    def __init__(self, game, doors, type_='default'):
        """__init__ method for Room class

        Args:
            game (<class 'Integrate.Game'>): Integrate.Game class object.
            doors (str): Which door available (NSWE). Possible values : combination of N,S,E and W
            type_ (str): type of room. Possible values (start or default)

        """
        self.game = game
        self.doors = doors
        self.type = type_
        self.w = cfg.WIDTH // cfg.TILESIZE
        self.h = (cfg.HEIGHT - cfg.GUI_HEIGHT) // cfg.TILESIZE
        
        self.visited = False
        self.pos = [0, 0]       # initializing position with [0,0]
        self.dist = -1          # initializing distance with -1
        self.shut_doors_sprites = []    # a list of sprites that represent the closed doors
        self.cleared = False    # boolean for if the player has done all the tasks in a room
        self.is_doors_shut = False
        self.object_data = []

        self.TM_POOL = self.randomize_rooms_tmx()
        # choose a random tmx file for this room
        if self.type == 'start': self.tm_file = 'room_0.tmx'
        else: self.tm_file = 'room_{}.tmx'.format(self.TM_POOL.pop())
        
        self.build()


    def randomize_rooms_tmx(self):
        """Room class method for choosing random tmx file for each room.
        
        """
        TM_POOL = []
        for i in range(cfg.DUNGEON_SIZE[0] * cfg.DUNGEON_SIZE[1]):
            TM_POOL.append(random.choice(cfg.TILEMAP_FILES))

        return TM_POOL

    def is_doors_equal(self, doors_1, doors_2):
        """Room class method for comparing doors.
        
        Args:
            doors_1 (str): doors, possible values are a combination of N,W,E and S.
            doors_2 (Str): doors, possible values are a combination of N,W,E and S.

        Returns:
            doors_equal (bool): True if equal doors, False otherwise.

        """
        doors_equal = True
        if len(doors_1) != len(doors_2):
            doors_equal = False
        
        doors_temp_1 = doors_1
        doors_temp_2 = doors_2
        for doors in doors_1:
            if doors not in doors_temp_2:
                doors_equal = False
            else:
                doors_temp_2 = doors_temp_2.replace(doors, '', 1)

        for doors in doors_2:
            if doors not in doors_temp_1:
                doors_equal = False
            else:
                doors_temp_1 = doors_temp_1.replace(doors, '', 1)
            
        return doors_equal

    def build(self):       
        """Room class method for building room.
        
        """
        for doors in self.game.imageLoader.room_image_dict:
            if self.is_doors_equal(self.doors, doors) == True:
                self.image = self.game.imageLoader.room_image_dict[doors]        
        self.tile_or_wall_doors()

    def tileset_from_tmx(self, filename):
        """Room class method for extracting tileset from tmx file.
        
        Args:
            filename (str): filename of the tmx file.

        """
        # reading xml
        file = os.path.join(cfg.ROOM_FOLDER, filename)
        tree = ET.parse(file)
        root = tree.getroot()
        
        # get tile data from csv node
        data = root[1][0].text
        data = data.replace(' ', '')
        data = data.strip('\n')      
        data = data.split('\n')
        
        tile_array = [line.strip(',').split(',') for line in data]
        
        for i in range(len(tile_array)):
            for j in range(len(tile_array[i])):
                tile_array[i][j] = int(tile_array[i][j]) - 1

        return tile_array  

    def objects_from_tmx(self, filename):
        """Room class method for extracting tileset from tmx file.
        
        Args:
            filename (str): filename of the tmx file.

        """
        file = os.path.join(cfg.ROOM_FOLDER, filename)
        tree = ET.parse(file)
        root = tree.getroot()
        
        raw_objects = root.iter('object')
        objects = []

        for obj in raw_objects:
            a = {}
            for key, value in obj.attrib.items():
                try:
                    a[key] = float(value)
                except ValueError:
                    a[key] = value
            child = obj.iter()
            for node in child:
                na = node.attrib
                if na.get('name') and na.get('name') not in a.keys():
                    if na.get('value') is not None:
                        a[na['name']] = float(na.get('value'))
            objects.append(a)
        
        return objects


    def tile_or_wall_doors(self):
        """Room class method for tiling for doors present and walling for not present.
        
        """
        # door position is in middle of the walls
        door_x = self.w // 2
        door_y = self.h // 2

        # read tileset and object data from files
        self.tiles = self.tileset_from_tmx(self.tm_file)
        self.layout = self.objects_from_tmx(self.tm_file)
            
        # setting tiles for doors that are present in the room
        if 'N' in self.doors:
            for i in range(8,12):
                self.tiles[0][i] = 1
            
        if 'S' in self.doors:
            for i in range(door_x-2, door_x+2):
                self.tiles[self.h - 1][i] = 1
        
        if 'W' in self.doors:
            for i in range(door_y-1, door_y+2):
                self.tiles[i][0] = 1
        
        if 'E' in self.doors:
            for i in range(door_y-1, door_y+2):
                self.tiles[i][self.w - 1] = 1

        # setting Wall for doors that are not present in the room
        if 'N' not in self.doors:
            self.layout.append({'id': 0, 'name': 'Wall', 'x': 360, 'y': 3.1,  'width': 40, 'height': 40})
            self.layout.append({'id': 0, 'name': 'Wall', 'x': 400, 'y': 3.1,  'width': 40, 'height': 40})
            self.layout.append({'id': 0, 'name': 'Wall', 'x': 440, 'y': 3.1,  'width': 40, 'height': 40})
            self.layout.append({'id': 0, 'name': 'Wall', 'x': 320, 'y': 3.1,  'width': 40, 'height': 40})
           
        if 'S' not in self.doors:
            self.layout.append({'id': 0, 'name': 'Wall', 'x': 360, 'y': 558,  'width': 40, 'height': 40})
            self.layout.append({'id': 0, 'name': 'Wall', 'x': 400, 'y': 558,  'width': 40, 'height': 40})
            self.layout.append({'id': 0, 'name': 'Wall', 'x': 440, 'y': 558,  'width': 40, 'height': 40})
            self.layout.append({'id': 0, 'name': 'Wall', 'x': 320, 'y': 558,  'width': 40, 'height': 40})
        
        if 'W' not in self.doors:
            self.layout.append({'id': 0, 'name': 'Wall', 'x': 3, 'y': 240,  'width': 40, 'height': 40})
            self.layout.append({'id': 0, 'name': 'Wall', 'x': 3, 'y': 280,  'width': 40, 'height': 40})
            self.layout.append({'id': 0, 'name': 'Wall', 'x': 3, 'y': 320,  'width': 40, 'height': 40})
            
        if 'E' not in self.doors:
            self.layout.append({'id': 0, 'name': 'Wall', 'x': 758, 'y': 240,  'width': 40, 'height': 40})
            self.layout.append({'id': 0, 'name': 'Wall', 'x': 758, 'y': 280,  'width': 40, 'height': 40})
            self.layout.append({'id': 0, 'name': 'Wall', 'x': 758, 'y': 320,  'width': 40, 'height': 40})

    def open_doors(self):
        """Room class method for opening up doors by deleting the door sprites.
        
        """
        if self.is_doors_shut:
            for d in self.shut_doors_sprites:
                d.kill()
            self.is_doors_shut = False

    def append_door_sprite(self, door):
        """Room class method for placing the door sprite.
        
        Args:
            door (char): the current door character, possible values are N, S, E and W.

        """
        door_pos = (cfg.DOOR_POSITIONS[door][0], cfg.DOOR_POSITIONS[door][1] + cfg.GUI_HEIGHT)
        door_sprite = Door(self.game, door_pos, direction=door)
        self.shut_doors_sprites.append(door_sprite)
    
    def shut_doors(self):
        """Room class method for closing doors placing door sprites.
        
        """
        if self.is_doors_shut == False:
            for door in self.doors:
                if self.type == 'start':
                    door_pos = (cfg.DOOR_POSITIONS[door][0], cfg.DOOR_POSITIONS[door][1] + cfg.GUI_HEIGHT)
                    d = Door(self.game, door_pos, direction=door)
                    self.shut_doors_sprites.append(d)
                else:
                    if self.game.dircheck == UP or self.game.dircheck == RIGHT or self.game.dircheck == LEFT or self.game.dircheck == DOWN:
                        if 'N' in self.doors:
                            self.append_door_sprite('N')
                        if 'E' in self.doors:
                            self.append_door_sprite('E')
                        if 'W' in self.doors:
                            self.append_door_sprite('W')
                        if 'S' in self.doors:
                            self.append_door_sprite('S')
                
                            
            self.is_doors_shut = True
    
                   

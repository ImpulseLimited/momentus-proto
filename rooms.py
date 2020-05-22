import pygame as pg
from random import choice, randint, seed
from datetime import datetime
import traceback

import settings as st
import functions as fn
import sprites as spr

vec = pg.math.Vector2

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Room:
    def __init__(self, game, doors, type_='default'):
        self.game = game
        self.doors = doors
        self.type = type_
        self.w = st.WIDTH // st.TILESIZE
        self.h = (st.HEIGHT - st.GUI_HEIGHT) // st.TILESIZE
        
        self.visited = False
        self.pos = [0, 0]
        self.dist = -1
        
        # choose a random tmx file for this room
        if self.type == 'start':
            self.tm_file = 'room_0.tmx'
        else:
            # pop room layout from rooms pool
            self.tm_file = 'room_{}.tmx'.format(st.TM_POOL.pop())
        
        # a list of doors that are locked
        self.locked_doors = []
        # checks if room is shut (all doors are closed)
        # MEMO make this also a list so that particular doors can be shut
        self.shut = False
        # a list of sprites that represent the closed doors
        self.shut_doors = []
        # boolean for if the player has done all the tasks in a room
        self.cleared = False
        self.clearedcount = 0
        self.build()
        self.object_data = []
   
     
    def build(self):       
        for key in self.game.imageLoader.room_image_dict:
            if fn.compare(self.doors, key):
                self.image = self.game.imageLoader.room_image_dict[key]        
        self.tileRoom()
    
    
    def tileRoom(self):
        # positions of the doors
        door_w = self.w // 2
        door_h = self.h // 2

        # read tileset and object data from file
        self.tiles = fn.tileset_from_tmx(self.tm_file)
        self.layout = fn.objects_from_tmx(self.tm_file)
            
        if 'N' in self.doors:
            # 35, 34, 33
            self.tiles[0][8] = 1
            self.tiles[0][9] = 1
            self.tiles[0][10] = 1
            self.tiles[0][11] = 1
            
           
        # south
        if 'S' in self.doors:
            self.tiles[self.h - 1][door_w + 1] = 1
            self.tiles[self.h - 1][door_w] = 1
            self.tiles[self.h - 1][door_w - 1] = 1
            self.tiles[self.h - 1][door_w - 2] = 1
        
        # west
        if 'W' in self.doors:
            self.tiles[door_h + 1][0] = 1
            self.tiles[door_h][0] = 1
            self.tiles[door_h - 1][0] = 1
        
        # east
        if 'E' in self.doors:
            self.tiles[door_h + 1][self.w - 1] = 1
            self.tiles[door_h][self.w - 1] = 1
            self.tiles[door_h - 1][self.w - 1] = 1

            
        if 'N' not in self.doors:
            self.layout.append({'id': 0, 'name': 'wall', 
                                'x': 360, 'y': 3.1,  
                                'width': 40, 'height': 40})
            self.layout.append({'id': 0, 'name': 'wall', 
                                'x': 400, 'y': 3.1,  
                                'width': 40, 'height': 40})
            self.layout.append({'id': 0, 'name': 'wall', 
                                'x': 440, 'y': 3.1,  
                                'width': 40, 'height': 40})
            self.layout.append({'id': 0, 'name': 'wall', 
                                'x': 320, 'y': 3.1,  
                                'width': 40, 'height': 40})
           
        if 'S' not in self.doors:
            self.layout.append({'id': 0, 'name': 'wall', 
                                'x': 360, 'y': 558,  
                                'width': 40, 'height': 40})
            self.layout.append({'id': 0, 'name': 'wall', 
                                'x': 400, 'y': 558,  
                                'width': 40, 'height': 40})
            self.layout.append({'id': 0, 'name': 'wall', 
                                'x': 440, 'y': 558,  
                                'width': 40, 'height': 40})
            self.layout.append({'id': 0, 'name': 'wall', 
                                'x': 320, 'y': 558,  
                                'width': 40, 'height': 40})
        if 'W' not in self.doors:
            self.layout.append({'id': 0, 'name': 'wall', 
                                'x': 3, 'y': 240,  
                                'width': 40, 'height': 40})
            self.layout.append({'id': 0, 'name': 'wall', 
                                'x': 3, 'y': 280,  
                                'width': 40, 'height': 40})
            self.layout.append({'id': 0, 'name': 'wall', 
                                'x': 3, 'y': 320,  
                                'width': 40, 'height': 40})
            
        if 'E' not in self.doors:
            self.layout.append({'id': 0, 'name': 'wall', 
                                'x': 758, 'y': 240,  
                                'width': 40, 'height': 40})
            self.layout.append({'id': 0, 'name': 'wall', 
                                'x': 758, 'y': 280,  
                                'width': 40, 'height': 40})
            self.layout.append({'id': 0, 'name': 'wall', 
                                'x': 758, 'y': 320,  
                                'width': 40, 'height': 40})

    
    def shutDoors(self):
        if not self.shut:
            for door in self.doors:
                if self.type == 'start':
                    pos = (st.DOOR_POSITIONS[door][0], st.DOOR_POSITIONS[door][1] 
                            + st.GUI_HEIGHT)
                    d = spr.Door(self.game, pos, direction=door)
                    self.shut_doors.append(d)
                else:
                    if self.game.dircheck == UP:
                        if 'N' in self.doors:
                            pos = (st.DOOR_POSITIONS['N'][0], st.DOOR_POSITIONS['N'][1] 
                                + st.GUI_HEIGHT+1)
                            d = spr.Door(self.game, pos, direction='N')
                            self.shut_doors.append(d)
                        if 'E' in self.doors:
                            pos = (st.DOOR_POSITIONS['E'][0], st.DOOR_POSITIONS['E'][1] 
                            + st.GUI_HEIGHT)
                            d = spr.Door(self.game, pos, direction='E')
                            self.shut_doors.append(d)
                        if 'W' in self.doors:
                            pos = (st.DOOR_POSITIONS['W'][0], st.DOOR_POSITIONS['W'][1] 
                                + st.GUI_HEIGHT)
                            d = spr.Door(self.game, pos, direction='W')
                            self.shut_doors.append(d)
                        if 'S' in self.doors:
                            pos = (st.DOOR_POSITIONS['S'][0], st.DOOR_POSITIONS['S'][1] 
                            + st.GUI_HEIGHT)
                            d = spr.Door(self.game, pos, direction='S')
                            self.shut_doors.append(d)
                    if self.game.dircheck == RIGHT:
                        if 'N' in self.doors:
                            pos = (st.DOOR_POSITIONS['N'][0], st.DOOR_POSITIONS['N'][1] 
                                + st.GUI_HEIGHT)
                            d = spr.Door(self.game, pos, direction='N')
                            self.shut_doors.append(d)
                        if 'E' in self.doors:
                            pos = (st.DOOR_POSITIONS['E'][0], st.DOOR_POSITIONS['E'][1] 
                            + st.GUI_HEIGHT)
                            d = spr.Door(self.game, pos, direction='E')
                            self.shut_doors.append(d)
                        if 'W' in self.doors:
                            pos = (st.DOOR_POSITIONS['W'][0]-1, st.DOOR_POSITIONS['W'][1] 
                                + st.GUI_HEIGHT)
                            d = spr.Door(self.game, pos, direction='W')
                            self.shut_doors.append(d)
                        if 'S' in self.doors:
                            pos = (st.DOOR_POSITIONS['S'][0], st.DOOR_POSITIONS['S'][1] 
                            + st.GUI_HEIGHT)
                            d = spr.Door(self.game, pos, direction='S')
                            self.shut_doors.append(d)
                    if self.game.dircheck == LEFT:
                        if 'N' in self.doors:
                            pos = (st.DOOR_POSITIONS['N'][0], st.DOOR_POSITIONS['N'][1] 
                                + st.GUI_HEIGHT)
                            d = spr.Door(self.game, pos, direction='N')
                            self.shut_doors.append(d)
                        if 'E' in self.doors:
                            pos = (st.DOOR_POSITIONS['E'][0]+1, st.DOOR_POSITIONS['E'][1] 
                            + st.GUI_HEIGHT)
                            d = spr.Door(self.game, pos, direction='E')
                            self.shut_doors.append(d)
                        if 'W' in self.doors:
                            pos = (st.DOOR_POSITIONS['W'][0], st.DOOR_POSITIONS['W'][1] 
                                + st.GUI_HEIGHT)
                            d = spr.Door(self.game, pos, direction='W')
                            self.shut_doors.append(d)
                        if 'S' in self.doors:
                            pos = (st.DOOR_POSITIONS['S'][0], st.DOOR_POSITIONS['S'][1] 
                            + st.GUI_HEIGHT)
                            d = spr.Door(self.game, pos, direction='S')
                            self.shut_doors.append(d)
                    if self.game.dircheck == DOWN:
                        
                        if 'N' in self.doors:
                            pos = (st.DOOR_POSITIONS['N'][0], st.DOOR_POSITIONS['N'][1] 
                                + st.GUI_HEIGHT)
                            d = spr.Door(self.game, pos, direction='N')
                            self.shut_doors.append(d)
                        if 'E' in self.doors:
                            pos = (st.DOOR_POSITIONS['E'][0], st.DOOR_POSITIONS['E'][1] 
                            + st.GUI_HEIGHT)
                            d = spr.Door(self.game, pos, direction='E')
                            self.shut_doors.append(d)
                        if 'W' in self.doors:
                            pos = (st.DOOR_POSITIONS['W'][0], st.DOOR_POSITIONS['W'][1] 
                                + st.GUI_HEIGHT)
                            d = spr.Door(self.game, pos, direction='W')
                            self.shut_doors.append(d)
                        if 'S' in self.doors:
                            pos = (st.DOOR_POSITIONS['S'][0], st.DOOR_POSITIONS['S'][1] 
                            + st.GUI_HEIGHT)
                            d = spr.Door(self.game, pos, direction='S')
                            self.shut_doors.append(d)
                            
            self.shut = True
        
    
    def openDoors(self):
        '''
        delets all door sprites
        '''
        if self.shut:
            for d in self.shut_doors:
                d.kill()
            self.shut = False
                   


class Dungeon:
    def __init__(self, game, size):
        self.size = vec(size)
        self.game = game
        # variables for animation
        self.last_update = 0
        self.current_frame = 0
                  
        w = int(self.size.x)
        h = int(self.size.y)
        # empty dungeon
        self.rooms = [[None for i in range(w)] for j in range(h)]
        # 1D list of rooms
        self.room_list = []

        # starting room
        self.start = [h // 2, w // 2]
        r_start = Room(self.game, 'NSWE', 'start')
        self.rooms[self.start[0]][self.start[1]] = r_start
        self.room_list.append(r_start)
        self.room_index = self.start
        
        self.room_current = self.rooms[self.room_index[0]][self.room_index[1]]
        
        self.done = False
            
        self.tileset = choice(self.game.imageLoader.tileset_names)
                
    def create(self, rng_seed): 
        start = datetime.now()
        
        if rng_seed != None:
            self.seed = rng_seed
        else:
            self.seed = randint(1000000, 9999999)
        
        st.randomizeRooms()
        
        self.build(rng_seed)

        self.closeDoors()
        # assign a distance from the start to every room
        self.floodFill()
        
        self.keyLogic()
            
        dt = datetime.now() - start
        ms = dt.seconds * 1000 + dt.microseconds / 1000.0
        print('Dungeon built in {} ms'.format(round(ms, 1)))
        
        
    def findEnd(self):
        # finds the farest room from the start
        for room in self.room_list:
            if room.dist == self.dist_longest:
                print('Endboss 2 in', room.pos)
                return room.pos
        
        
    def build(self, rng_seed):   
        # set seed for randomisation
        seed(a=rng_seed)
        
        while self.done == False:
            self.done = True
            for i in range(1, len(self.rooms) - 1):
                for j in range(1, len(self.rooms[i]) - 1):
                    room = self.rooms[i][j]
                    if room:
                        if 'N' in room.doors and self.rooms[i - 1][j] == None:
                            if i == 1:
                                r = Room(self.game, 'S')
                                self.rooms[i - 1][j] = r
                                self.room_list.append(r)
                            else:
                                # pick random door constellation
                                rng = choice(st.ROOMS['N'])
                                
                                # prevent one-sided doors
                                if 'N' in rng and self.rooms[i - 2][j]:
                                    rng = rng.replace('N', '')
                                if 'W' in rng and self.rooms[i - 1][j - 1]:
                                    rng = rng.replace('W', '')
                                if 'E' in rng and self.rooms[i - 1][j + 1]: 
                                    rng = rng.replace('E', '')
      
                                r = Room(self.game, rng)
                                self.rooms[i - 1][j] = r
                                self.room_list.append(r)
                                  
                            self.done = False
                        
                        if 'W' in room.doors and self.rooms[i][j - 1] == None:
                            if j == 1:
                                r = Room(self.game, 'E')
                                self.rooms[i][j - 1] = r
                                self.room_list.append(r)
                            else:
                                rng = choice(st.ROOMS['W'])
                                
                                if 'N' in rng and self.rooms[i - 1][j - 1]:
                                    rng = rng.replace('N', '')
                                if 'W' in rng and self.rooms[i][j - 2]: 
                                    rng = rng.replace('W', '')
                                if 'S' in rng and self.rooms[i + 1][j - 1]: 
                                    rng = rng.replace('S', '')
                                
                                r = Room(self.game, rng)
                                self.rooms[i][j - 1] = r
                                self.room_list.append(r)
                             
                            self.done = False
                        
                        if 'E' in room.doors and self.rooms[i][j + 1] == None:
                            if j == len(self.rooms) - 2:
                                r = Room(self.game, 'W')
                                self.rooms[i][j + 1] = r
                                self.room_list.append(r)
                            else:
                                rng = choice(st.ROOMS['E'])
                                
                                if 'N' in rng and self.rooms[i - 1][j + 1]:
                                    rng = rng.replace('N', '')
                                if 'E' in rng and self.rooms[i][j + 2]: 
                                    rng = rng.replace('E', '')
                                if 'S' in rng and self.rooms[i + 1][j + 1]: 
                                    rng = rng.replace('S', '')
                                
                                r = Room(self.game, rng)
                                self.rooms[i][j + 1] = r
                                self.room_list.append(r)
                            
                            self.done = False                              
                        
                        if 'S' in room.doors and self.rooms[i + 1][j] == None:
                            if i == len(self.rooms) - 2:
                                r = Room(self.game, 'N')
                                self.rooms[i + 1][j] = r
                                self.room_list.append(r)
                            else:
                                rng = choice(st.ROOMS['S'])
                                
                                if 'W' in rng and self.rooms[i + 1][j - 1]:
                                    rng = rng.replace('W', '')
                                if 'E' in rng and self.rooms[i + 1][j + 1]: 
                                    rng = rng.replace('E', '')
                                if 'S' in rng and self.rooms[i + 2][j]: 
                                    rng = rng.replace('S', '')
                                
                                r = Room(self.game, rng)
                                self.rooms[i + 1][j] = r
                                self.room_list.append(r)
                            
                            self.done = False

    
    def closeDoors(self):
        for i in range(len(self.rooms)):
            for j in range(len(self.rooms[i])):
                room = self.rooms[i][j]
                if room:
                    # set the room's position value
                    room.pos = [i, j]
                    if 'N' in room.doors and self.rooms[i - 1][j]:
                        if 'S' not in self.rooms[i - 1][j].doors:
                            room.doors = room.doors.replace('N', '')
  
                    if 'S' in room.doors and self.rooms[i + 1][j]:
                        if 'N' not in self.rooms[i + 1][j].doors:
                            room.doors = room.doors.replace('S', '')
                    
                    if 'W' in room.doors and self.rooms[i][j - 1]:
                        if 'E' not in self.rooms[i][j - 1].doors:
                            room.doors = room.doors.replace('W', '')
                            
                    if 'E' in room.doors and self.rooms[i][j + 1]:
                        if 'W' not in self.rooms[i][j + 1].doors:
                            room.doors = room.doors.replace('E', '')
                    
                    # re-build the rooms after changes
                    room.build()
                    
    
    def floodFill(self):
        cycle = 0
        starting_room = self.rooms[self.start[0]][self.start[1]]
        starting_room.dist = 0
        done = False
        while not done:
            done = True
            for i in range(1, len(self.rooms) - 1):
                for j in range(1, len(self.rooms[i]) - 1):
                    room = self.rooms[i][j]
                    
                    if room and room.dist == cycle:
                        if 'N' in room.doors and self.rooms[i - 1][j]:
                            if self.rooms[i - 1][j].dist == -1:
                                self.rooms[i - 1][j].dist = cycle + 1
                                done = False
                            
                        if 'S' in room.doors and self.rooms[i + 1][j]:
                            if self.rooms[i + 1][j].dist == -1:
                                self.rooms[i + 1][j].dist = cycle + 1
                                done = False
                        
                        if 'W' in room.doors and self.rooms[i][j - 1]:
                            if self.rooms[i][j - 1].dist == -1:
                                self.rooms[i][j - 1].dist = cycle + 1
                                done = False
                        
                        if 'E' in room.doors and self.rooms[i][j + 1]:
                            if self.rooms[i][j + 1].dist == -1:
                                self.rooms[i][j + 1].dist = cycle + 1
                                done = False
            
            cycle += 1

       
    def keyLogic(self):
        
        # find longest distance
        self.dist_longest = 0
        for room in self.room_list:
            self.dist_longest = max(self.dist_longest, room.dist)
            
        # set the farest room to endboss
        for room in self.room_list:
            if room.dist == self.dist_longest:
                print('Endboss in', room.pos)
                room.type = 'endboss'
                pos = room.pos
                room.tm_file = 'room_0.tmx'
                room.build()
                 # put boss in room
                room.layout.append({'id': 0, 'name': 'Enemy01', 
                                            'x': 150, 
                                        'y': 150, 
                                        'width': 40, 'height': 40})
                room.layout.append({'id': 0, 'name': 'Enemy01', 
                                            'x': 250, 
                                        'y': 150, 
                                        'width': 40, 'height': 40})
                room.layout.append({'id': 0, 'name': 'Enemy01', 
                                            'x': 250, 
                                        'y': 250, 
                                        'width': 40, 'height': 40})
                
                room.layout.append({'id': 0, 'name': 'Boss', 'x': 150,
                                    'y': 150, 'width': 40, 'height': 40})
                room.layout.append({'id': 0, 'name': 'Boss', 'x': 250,
                                    'y': 250, 'width': 40, 'height': 40})
                room.layout.append({'id': 0, 'name': 'Mboss', 
                                    'x': 5 * st.TILESIZE, 
                                'y': 5 * st.TILESIZE, 
                                'width': 40, 'height': 40})
                room.layout.append({'id': 0, 'name': 'Mboss', 
                                    'x': 7 * st.TILESIZE, 
                                'y': 10 * st.TILESIZE, 
                                'width': 40, 'height': 40})
                break

        
        # find the adjacent room and lock it
        room = self.rooms[pos[0]][pos[1]]     
        # find second longest distance
        dist_longest = 0
        for room in self.room_list:
            if room.type != 'endboss' and len(room.doors) == 1:
                dist_longest = max(dist_longest, room.dist)
            
        xRange = [120,160,200,240,280,320,360,400,440,480,520,560,600]
        yRange = [120,160,200,240,280,320,360,400,440,480,80,520]

        xBRange = [160,200,280,320,360,530,570]
        yBRange = [120,200,280,320,360,440,500]

        xERange = [420,130,488,240]
        yERange = [420,160,488,240]
        
        for room in self.room_list:
            Check_List = []
            Block_List = []
            Exp_List = []
        
            br = randint(3,10)
            
            er = randint(2,3)
            
            for i in range (br):
                x = choice(xBRange)
                y = choice(yBRange)
                Block_List.append((int(x),int(y)))
                x = Block_List[i][0]
                y = Block_List[i][1]
                
                room.layout.append({'id': 0, 'name': 'Block', 
                                        'x': x, 
                                    'y': y, 
                                    'width': 40, 'height': 40})

            for z in range (er):
                
                a = choice(xERange)
                b = choice(yERange)
                if (a,b) in Exp_List:
                    break
                else:
                    Exp_List.append((int(a),int(b)))              
                a = Exp_List[z][0]
                b = Exp_List[z][1]
                
                    
                room.layout.append({'id': 0, 'name': 'Explosive_crate', 
                                        'x': a, 
                                    'y': b, 
                                    'width': 36, 'height': 36})
               

                
                
            
                
                
            
        for room in self.room_list:
            if room.dist == dist_longest and room.type != 'endboss':
                room.type = 'miniboss'
                room.layout.append({'id': 0, 'name': 'Boss', 
                    'x': 150, 'y': 150, 
                    'width': 40, 'height': 40})
                room.layout.append({'id': 0, 'name': 'Boss', 
                    'x': 250, 'y': 250, 
                    'width': 40, 'height': 40})
                room.layout.append({'id': 0, 'name': 'Mboss', 
                                    'x': 5 * st.TILESIZE, 
                                'y': 5 * st.TILESIZE, 
                                'width': 40, 'height': 40})
                room.layout.append({'id': 0, 'name': 'Mboss', 
                                    'x': 7 * st.TILESIZE, 
                                'y': 10 * st.TILESIZE, 
                                'width': 40, 'height': 40})
                break

        
        Rcount = 0
        for room in self.room_list:
            Rcount = Rcount + 1
            for i in range(Rcount):
                x = choice(xRange)
                y = choice(yRange)
                Check_List.append((int(x),int(y)))
                x = Check_List[i][0]
                y = Check_List[i][1]
                if room.type != 'endboss' and room.type != 'miniboss':
                        room.layout.append({'id': 0, 'name': 'Mboss', 
                                    'x': x, 
                                'y': y, 
                                'width': 40, 'height': 40})
                        if Rcount > 2:
                            room.layout.append({'id': 0, 'name': 'Boss', 
                        'x': x+40, 'y': y+40, 
                        'width': 40, 'height': 40})
                Check_List = list(dict.fromkeys(Check_List))
                if Rcount == 4:
                    Rcount = 2

    def blitRooms(self):
        # blit a mini-map image onto the screen
        
        # room image size
        size = (6, 4)
        
        # mini map size
        w = 59
        h = 39

        self.map_img = pg.Surface((w, h), flags=pg.SRCALPHA)
        self.map_img.fill(st.BLACK)
        
        imgs = self.game.imageLoader.room_img
             
        for i in range(len(self.rooms)):
            for j in range(len(self.rooms[i])):
                room = self.rooms[i][j]
                #pos = (j * (w / self.size.x) - 1, i  * (h / self.size.y) - 1)
                pos = (j * size[0] - 1, i * size[1] - 1)
                if room:# and room.visited:
                    self.map_img.blit(room.image, pos)
                    if room.type == 'start':
                        # draw a square representing the starting room
                        self.map_img.blit(imgs[17], pos)
                else:
                    self.map_img.blit(imgs[0], pos)

        # animated red square representing the player
        now = pg.time.get_ticks()
        pos2 = (self.room_index[1] * size[0] - 1, 
                self.room_index[0] * size[1] - 1)
        player_imgs = [imgs[18], imgs[19]]
        
        if now - self.last_update > 500:
                self.last_update = now
                # change the image
                self.current_frame = (self.current_frame + 1) % len(player_imgs)
        self.map_img.blit(player_imgs[self.current_frame], pos2)
        
        scaled = (w, h)
        return pg.transform.scale(self.map_img, scaled)
        
            
            

import pygame
import random
from datetime import datetime

import Config as cfg
from Room import Room

class Dungeon:
    """This class contains all settings related to the dungeon.

    """
    def __init__(self, game, size):
        """__init__ method for Dungeon class

        Args:
            game (<class 'Integrate.Game'>): Integrate.Game class object.
            size (<class 'tuple'>): the size of dungeon in a 2 point tuple.

        """
        self.game = game
        self.size = pygame.math.Vector2(size)
        w = int(self.size.x)
        h = int(self.size.y)
        self.room_matrix = [[None for i in range(w)] for j in range(h)]   # Initializing empty rooms 2D
        self.room_list = [] # Initializing empty rooms 1D
        self.current_room_index = [h // 2, w // 2] # Starting room set to middle one

        # beginnning room contains doors in all directions
        room_start = Room(self.game, 'NSWE', 'start')
        room_start.pos = [self.current_room_index[0], self.current_room_index[1]]
        self.room_matrix[self.current_room_index[0]][self.current_room_index[1]] = room_start
        self.room_list.append(room_start)
        self.room_current = self.room_matrix[self.current_room_index[0]][self.current_room_index[1]]
        
        # variables for animation
        self.last_update = 0
        self.current_frame = 0
                  
        self.tileset = random.choice(self.game.imageLoader.tileset_file)
    
    def create(self): 
        """Dungeon class method to create the dungeon.
        
        """
        # Calculating dungeon building time
        start_time = datetime.now()
        self.build_dungeon()
        self.calculate_room_distances()
        self.place_bosses()
        self.place_blocks()
        self.place_explosions()
        time_to_build = datetime.now() - start_time
        time_to_build = time_to_build.seconds * 1000 + time_to_build.microseconds / 1000.0
        print('Dungeon built in {} ms'.format(round(time_to_build, 1)))


    def check_door_to_no_room(self, room, door, i , j):
        """Dungeon class method to check if door from current room doesnt lead to any room.

        Args:
            room (<class 'Room.Room'>): Room.Room class object.
            door (char): door to check, possible values : N, S, E or W.
            i (int): x index of room matrix.
            j (int): y index of room matrix.

        Returns:
            room_not_exists (bool): True if door leads to no room, False otherwise.

        """
        room_not_exists = False
        if door in room.doors and self.room_matrix[i][j] == None:
            room_not_exists =  True
        
        return room_not_exists


    def build_room(self, door, i, j):
        """Dungeon class method to build a room given x, y room matrix and door.

        Args:
            door (char): door to build a room from, possible values : N, S, E or W.
            i (int): x index of room matrix.
            j (int): y index of room matrix.

        """
        # Top row, Bottom row, left most column and right most column checking conditions
        boundary_check = {'N':{'is_boundary':i==1, 'door_exists':'S', 'matrix_x':i-1, 'matrix_y':j },
                          'S':{'is_boundary':i==len(self.room_matrix)-2, 'door_exists':'N', 'matrix_x':i+1, 'matrix_y':j},
                          'E':{'is_boundary':j==len(self.room_matrix)-2, 'door_exists':'W', 'matrix_x':i, 'matrix_y':j+1},
                          'W':{'is_boundary':j==1, 'door_exists':'E', 'matrix_x':i, 'matrix_y':j-1}
                          }

        # one sided doors checking conditions
        one_sided_check = { 'N':{'N':[i-2,j], 'E':[i-1,j+1],'W':[i-1,j-1]},
                            'S':{'S':[i+2,j], 'E':[i+1,j+1],'W':[i+1,j-1]},
                            'E':{'N':[i-1,j+1], 'E':[i,j+2],'S':[i+1,j+1]},
                            'W':{'N':[i-1,j-1], 'S':[i+1,j-1],'W':[i,j-2]}
                         }

        # x and y index of the room go be build from the current door
        x = boundary_check.get(door).get('matrix_x')
        y = boundary_check.get(door).get('matrix_y')

        # build a simple room with only one door 
        # if the leading room is at the boundary
        if boundary_check.get(door).get('is_boundary') == True:
            door_present = boundary_check.get(door).get('door_exists')
            this_room = Room(self.game, door_present)
            this_room.pos = [x,y]     
            self.room_matrix[x][y] = this_room
            self.room_list.append(this_room)

        # build a random design room with random door 
        # if the leading room is not at the boundary
        else:
            room_design = random.choice(cfg.ROOMS[door])
            # preventing single side doors
            door_dict = one_sided_check.get(door)
            for door_dict_door in door_dict.keys():
                xy = door_dict.get(door_dict_door)
                if door_dict_door in room_design and self.room_matrix[xy[0]][xy[1]]:
                    room_design = room_design.replace(door_dict_door, '')

            this_room = Room(self.game, room_design)
            this_room.pos = [x,y]   
            self.room_matrix[x][y] = this_room
            self.room_list.append(this_room)


    def build_dungeon(self):   
        """Dungeon class method to build the dungeon starting from the beginning room and spreading out.
        
        """
        rand_seed = random.randint(1000000, 9999999)   # Random seed value
        random.seed(a=rand_seed)
        #random.seed(a=1000)
        
        dungeon_complete = False
        while dungeon_complete == False:
            dungeon_complete = True
            # Iterating room matrix leaving one row from each side.
            for i in range(1, len(self.room_matrix) - 1):
                for j in range(1, len(self.room_matrix[i]) - 1):
                    this_room = self.room_matrix[i][j]
                    # if room is already built then check 
                    # if any doors are present not leading to any room
                    # then build those rooms
                    if not this_room == None:
                        if self.check_door_to_no_room(this_room, 'N', i-1, j) == True:
                            self.build_room('N', i ,j)
                            dungeon_complete = False
                        
                        if self.check_door_to_no_room(this_room, 'W', i, j-1) == True:
                            self.build_room('W', i ,j)
                            dungeon_complete = False
                        
                        if self.check_door_to_no_room(this_room, 'E', i, j+1) == True:
                            self.build_room('E', i ,j)
                            dungeon_complete = False                              
                        
                        if self.check_door_to_no_room(this_room, 'S', i+1, j) == True:
                            self.build_room('S', i ,j)
                            dungeon_complete = False
                

    def calculate_room_distances(self):
        """Dungeon class method to calculate distance from current room.
        
        """
        # setting distance of current room as zero
        self.room_matrix[self.current_room_index[0]][self.current_room_index[1]].dist = 0
        
        current_distance = 0
        all_distance_calculated = False
        while all_distance_calculated == False:
            all_distance_calculated = True
            # Iterating room matrix leaving one row from each side.
            for i in range(1, len(self.room_matrix) - 1):
                for j in range(1, len(self.room_matrix[i]) - 1):

                    this_room = self.room_matrix[i][j]
                    
                    # for the rooms that have distance  = current distance
                    if not this_room == None and this_room.dist == current_distance:
                        if 'N' in this_room.doors and not self.room_matrix[i - 1][j] == None:
                            # if distance not set yet (since default is -1)
                            if self.room_matrix[i - 1][j].dist == -1:
                                self.room_matrix[i - 1][j].dist = current_distance + 1
                                all_distance_calculated = False
                            
                        if 'S' in this_room.doors and not self.room_matrix[i + 1][j] == None:
                            # if distance not set yet (since default is -1)
                            if self.room_matrix[i + 1][j].dist == -1:
                                self.room_matrix[i + 1][j].dist = current_distance + 1
                                all_distance_calculated = False
                        
                        if 'W' in this_room.doors and not self.room_matrix[i][j - 1] == None:
                            # if distance not set yet (since default is -1)
                            if self.room_matrix[i][j - 1].dist == -1:
                                self.room_matrix[i][j - 1].dist = current_distance + 1
                                all_distance_calculated = False
                        
                        if 'E' in this_room.doors and not self.room_matrix[i][j + 1] == None:
                            # if distance not set yet (since default is -1)
                            if self.room_matrix[i][j + 1].dist == -1:
                                self.room_matrix[i][j + 1].dist = current_distance + 1
                                all_distance_calculated = False
            
            current_distance += 1

        # setting the dist_longest attribute for dungeon
        self.dist_longest = current_distance -1


    def place_blocks(self):
        """Dungeon class method to place blocks in all rooms.
        
        """
        x_blocks = [160,200,280,320,360,530,570]
        y_blocks = [120,200,280,320,360,440,500]

        for i in range(0, len(self.room_matrix)):
            for j in range(0, len(self.room_matrix[i])):
                block_list=[]
                this_room = self.room_matrix[i][j]
                if not this_room == None:
                    for z in range(random.randint(3,10)):
                        x = random.choice(x_blocks)
                        y = random.choice(y_blocks)
                        if (x,y) in block_list: break
                        else: block_list.append((int(x),int(y)))   
                        x = block_list[z][0]
                        y = block_list[z][1] 
                        this_room.layout.append({'id': 0, 'name': 'Block', 'x': x, 'y': y, 'width': 40, 'height': 40})

                    
    def place_explosions(self):
        """Dungeon class method to place explosions in all rooms.
        
        """
        x_explosions = [420,130,488,240]
        y_explosions = [420,160,488,240]

        for i in range(0, len(self.room_matrix)):
            for j in range(0, len(self.room_matrix[i])):
                explosion_list=[]
                this_room = self.room_matrix[i][j]
                if not this_room == None:
                    for z in range(random.randint(2,3)):
                        x = random.choice(x_explosions)
                        y = random.choice(y_explosions)
                        if (x,y) in explosion_list: break
                        else: explosion_list.append((int(x),int(y)))              
                        x = explosion_list[z][0]
                        y = explosion_list[z][1]      
                        this_room.layout.append({'id': 0, 'name': 'Explosivecrate', 'x': x, 'y': y, 'width': 36, 'height': 36})
          
       
    def place_bosses(self):
        """Dungeon class method to place bosses in relevant rooms.
        
        """

        # set the most distant room to as the endboss room
        endboss = False
        for i in range(0, len(self.room_matrix)):
            for j in range(0, len(self.room_matrix[i])):

                this_room = self.room_matrix[i][j]
                if not this_room == None and endboss == False:
               
                    if this_room.dist == self.dist_longest:
                        # rebuilding the boss room
                        this_room.type = 'endboss'
                        this_room.tm_file = 'room_0.tmx'
                        this_room.build()
                        
                        # put boss in room
                        this_room.layout.append({'id': 0, 'name': 'SwordEnemy', 'x': 150, 'y': 150, 'width': 40, 'height': 40})
                        this_room.layout.append({'id': 0, 'name': 'SwordEnemy', 'x': 250, 'y': 150, 'width': 40, 'height': 40})
                        this_room.layout.append({'id': 0, 'name': 'SwordEnemy', 'x': 250, 'y': 250, 'width': 40, 'height': 40})
                        this_room.layout.append({'id': 0, 'name': 'Boss', 'x': 150, 'y': 150, 'width': 40, 'height': 40})
                        this_room.layout.append({'id': 0, 'name': 'Boss', 'x': 250, 'y': 250, 'width': 40, 'height': 40})
                        this_room.layout.append({'id': 0, 'name': 'MiniBoss', 'x': 5 * cfg.TILESIZE, 'y': 5 * cfg.TILESIZE, 'width': 40, 'height': 40})
                        this_room.layout.append({'id': 0, 'name': 'MiniBoss', 'x': 7 * cfg.TILESIZE, 'y': 10 * cfg.TILESIZE, 'width': 40, 'height': 40})

                        self.boss_room = this_room
                        pos = self.boss_room.pos
                        
                        print('Endboss is in : ', self.boss_room.pos)
                        endboss =True

        
        # find second longest distance
        dist_2nd_longest = 0
        for i in range(0, len(self.room_matrix)):
            for j in range(0, len(self.room_matrix[i])):

                this_room = self.room_matrix[i][j]
                if not this_room == None:
                    # checking if this is not the endboss room and also only a single door room 
                    if this_room.type != 'endboss' and len(this_room.doors) == 1:
                        dist_2nd_longest = max(dist_2nd_longest, this_room.dist)


        # set the second most distant room with single door as the MiniBoss room
        MiniBoss = False
        for i in range(0, len(self.room_matrix)):
            for j in range(0, len(self.room_matrix[i])):
                this_room = self.room_matrix[i][j]
                if not this_room == None and MiniBoss == False:
                    if this_room.dist == dist_2nd_longest and this_room.type != 'endboss' and len(this_room.doors) == 1:

                        this_room.type = 'MiniBoss'
                        this_room.layout.append({'id': 0, 'name': 'Boss', 'x': 150, 'y': 150, 'width': 40, 'height': 40})
                        this_room.layout.append({'id': 0, 'name': 'Boss', 'x': 250, 'y': 250, 'width': 40, 'height': 40})
                        this_room.layout.append({'id': 0, 'name': 'MiniBoss', 'x': 5 * cfg.TILESIZE, 'y': 5 * cfg.TILESIZE, 'width': 40, 'height': 40})
                        this_room.layout.append({'id': 0, 'name': 'MiniBoss', 'x': 7 * cfg.TILESIZE, 'y': 10 * cfg.TILESIZE, 'width': 40, 'height': 40})
                        MiniBoss = True
            
        
        # setting enemies in other rooms
        xRange = [120,160,200,240,280,320,360,400,440,480,520,560,600]
        yRange = [120,160,200,240,280,320,360,400,440,480,80,520]
        Check_List = []
        
        room_count = 0
        for this_room in self.room_list:
            room_count = room_count + 1
            for i in range(room_count):
                x = random.choice(xRange)
                y = random.choice(yRange)
                Check_List.append((int(x),int(y)))
                x = Check_List[i][0]
                y = Check_List[i][1]
                if this_room.type != 'endboss' and this_room.type != 'MiniBoss':
                        this_room.layout.append({'id': 0, 'name': 'MiniBoss', 'x': x, 'y': y, 'width': 40, 'height': 40})
                        if room_count > 2:
                            this_room.layout.append({'id': 0, 'name': 'Boss', 'x': x+40, 'y': y+40, 'width': 40, 'height': 40})
                Check_List = list(dict.fromkeys(Check_List))
                if room_count == 4:
                    room_count = 2


    def render_rooms_map(self):
        """Dungeon class method to render a mini map of rooms.
        
        """
        # room image size
        size = (6, 4)
        # mini map size
        w = 59
        h = 39

        self.map_img = pygame.Surface((w, h), flags=pygame.SRCALPHA)
        self.map_img.fill(cfg.BLACK)
        
        imgs = self.game.imageLoader.room_img
             
        for i in range(len(self.room_matrix)):
            for j in range(len(self.room_matrix[i])):
                this_room = self.room_matrix[i][j]
                room_pos = (j * size[0] - 1, i * size[1] - 1)
                if not this_room == None:
                    self.map_img.blit(this_room.image, room_pos)
                    if this_room.type == 'start':
                        # draw a square representing the starting room
                        self.map_img.blit(imgs[17], room_pos)
                else:
                    self.map_img.blit(imgs[0], room_pos)

        # animated red square representing the player
        current = pygame.time.get_ticks()
        player_pos = (self.current_room_index[1] * size[0] - 1, self.current_room_index[0] * size[1] - 1)
        player_imgs = [imgs[18], imgs[19]]
        
        if current - self.last_update > 500:
            self.last_update = current
            # change the image
            self.current_frame = (self.current_frame + 1) % len(player_imgs)

        self.map_img.blit(player_imgs[self.current_frame], player_pos)
        
        scaled = (w, h)
        return pygame.transform.scale(self.map_img, scaled)
        
            
            

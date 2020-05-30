import pygame
import traceback
import os
import random
import sys
import math

from Dungeon import Dungeon
from ImageLoader import ImageLoader
from Player import Player
import Sounds as snd
import Config as cfg
from Button import Button

from effects.Effect import Effect
from effects.Explosion import Explosion
from objects.Object import Object
from objects.Wall import Wall
from objects.Block import Block
from objects.Door import Door
from objects.Explosivecrate import Explosivecrate
from bullets.PlayerProjectile import PlayerProjectile
from bullets.PlayerPistolBullet import PlayerPistolBullet
from bullets.PlayerMachinegunBullet import PlayerMachinegunBullet
from bullets.EnemyProjectile import EnemyProjectile
from bullets.EnemyBullet import EnemyBullet
from bullets.EnemyPistolBullet import EnemyPistolBullet
from bullets.EnemyMachineGunBullet import EnemyMachineGunBullet
from Inventory import Inventory
from Item import Item
from weapons.Weapon import Weapon
from weapons.Sword import Sword
from weapons.Pistol import Pistol
from weapons.MachineGun import MachineGun
from enemies.SwordEnemy import SwordEnemy
from enemies.PistolEnemy import PistolEnemy
from enemies.MachineGunEnemy import MachineGunEnemy

# load a dictionary of GameFlow.py namespace
module_dict = sys.modules[__name__].__dict__

#directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

global Dx,Dy
Dx = 5
Dy = 5

class Game:
    """This class is main Game class.

    """
    def __init__(self):
        """__init__ method for Game class.

        """
        # initialise game window, settings etc.
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        pygame.init()
        pygame.mouse.set_visible(False)
        pygame.key.set_repeat(10, cfg.KEY_DELAY)
    
        self.actual_screen = pygame.display.set_mode((cfg.S_WIDTH, cfg.S_HEIGHT))
        #self.actual_screen = pygame.display.set_mode((cfg.S_WIDTH, cfg.S_HEIGHT), pygame.FULLSCREEN)
        
        self.screen = pygame.Surface((cfg.WIDTH, cfg.HEIGHT))

        self.clock = pygame.time.Clock()
        self.running = True
        self.loaded = False
        self.dircheck = None

        # booleans for drawing the hit rects and other debug stuff
        self.debug = False
        self.draw_vectors = False
        self.show_player_stats = False
        self.caption = ''

        self.key_down = None
        self.state = 'GAME'
        self.in_transition = False

        self.loadAssets()
        self.clearcount = 0
        self.check = True
        self.timer = 0
        self.levelcleared = 1
        self.pistolpick = True
        self.machinegunpick = False
        self.lastweapon = 'MachineGun'
        self.spritecheck = []


    def keyDown(self, events, game):
        """Game class method for checking keys presses.

        Args:
            events (<Event>): key press events.
            game (Integrate.Game): Integrate.Game class object.

        """
        for event in events:
            if event.type == pygame.KEYUP:
                if event.key == cfg.KEY_RIGHT:
                    game.player.RightCheck = False
                if event.key == cfg.KEY_UP:
                    game.player.UpCheck = False
                if event.key == cfg.KEY_LEFT:
                    game.player.LeftCheck = False
                if event.key == cfg.KEY_DOWN:
                    game.player.DownCheck = False


    def transitRoom(self, game, dungeon, offset=pygame.math.Vector2(0, 0)):
        """Game class method for room transition.

        Args:
            game (Integrate.Game): Integrate.Game class object.
            dungeon (Dungeon.Dungeon): Dungeon.Dungeon object

        """
        # get the index of the next and the previous room
        index_next = dungeon.current_room_index
        index_prev = game.prev_room
        # select the rooms based on the indices
        room_prev = dungeon.room_matrix[index_prev[0]][index_prev[1]]
        room_next = dungeon.room_matrix[index_next[0]][index_next[1]]
        
        # remove all sprite from the previous room
        room_prev.object_data = []
        
        for sprite in game.all_sprites:
            if sprite != game.player and sprite not in game.item_drops:
                if hasattr(sprite, 'data'):
                    room_prev.object_data.append(sprite.data)
                sprite.kill()
        
        if room_next.visited == False:
            # if room not visited, get the object data from the initial layout
            data = room_next.layout    
            for d in data:
                try:
                    if offset == (0, 0):
                        self.create(game, d)
                    else:
                        self.create(game, d, offset)
                except Exception:
                    traceback.print_exc()
                    pass
            
            room_next.visited = True
        
        else:
            # if room already visited, get the objects from the stored data
            data = room_next.object_data    
            for d in data:
                try:
                    if offset == (0, 0):
                        self.create(game, d)
                    else:
                        self.create(game, d, offset)
                except Exception:
                    traceback.print_exc()
                    pass
        
        # set the dungeon's current room based on room index
        dungeon.room_current = dungeon.room_matrix[dungeon.current_room_index[0]][dungeon.current_room_index[1]]

        
    def create(self, game, data, offset=pygame.math.Vector2(0, cfg.GUI_HEIGHT)):
        """Game class method for room transition.

        Args:
            game (Integrate.Game): Integrate.Game class object.
            data (dict{'id', 'name', 'x', 'y', 'width', 'height'}): objects data

        """
        # takes a dictionary of sprite properties
        name = data['name']
        # capitalizing first letter
        name_1 = name[0].capitalize()
        name_2 = name[1:]
        name = name_1+name_2

        #instantiate the sprite 
        spr = module_dict[name](game, (data['x'] + offset.x, data['y'] + offset.y), (data['width'], data['height']))

        for key, value in data.items():
            try:
                setattr(spr, key, value)
            except:
                print('cant set value of {0} for {1}'.format(key, spr))
        
        if hasattr(spr, 'on_create'):
            # do initialisation stuff after ___init__()
            spr.on_create()
        
        spr.data = data


    def loadAssets(self):
        """Game class method to load all assets.

        """
        #loading assets (images, sounds)
        self.imageLoader = ImageLoader(self)
        self.soundLoader = snd.Sound()
        try:
            self.imageLoader.load_assets()
            self.soundLoader.load()
        except Exception:
            traceback.print_exc()
            self.running = False

    def new(self):
        """Game class method to start a new game.

        """
        # start a new game
        # initialise sprite groups
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.walls = pygame.sprite.LayeredUpdates() 
        self.gui = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.item_drops = pygame.sprite.LayeredUpdates()

        # instantiate dungeon
        self.dungeon = Dungeon(self, cfg.DUNGEON_SIZE)
        if self.loaded:
            self.dungeon.tileset = self.saveGame.data['tileset']
        else:
            self.dungeon.create()

        self.WSign = self.imageLoader.WarnSign
        self.WSign2 = self.imageLoader.WarnSign2

        self.inventory = Inventory(self)

        # spawn the player in the middle of the room
        self.player = Player(self, (cfg.WIDTH // 2, cfg.TILESIZE * 12))

        self.currentpistol = Pistol(self, self.player)
        self.currentmachine = MachineGun(self, self.player)
        
        if self.pistolpick == True :
            self.player.itemA = self.currentpistol
            
        elif self.machinegunpick == True:
            self.player.itemA = self.currentmachine
               

        # load settings
        if self.loaded:
            self.loadSavefile()

        # spawn the new objects (invisible) 
        self.prev_room = self.dungeon.current_room_index
        self.transitRoom(self, self.dungeon)

        # create a background image from the tileset for the current room
        self.background = self.tileRoom(self,
                          self.imageLoader.tileset,
                          self.dungeon.current_room_index)

        self.run()


    def checkFight(self, game):
        """Game class method to check distance from door and closes the doors 
           and opens them when player defeats all enemies in the room
        
        """
        room = game.dungeon.room_current
        if len(game.enemies) > 0:
            room.cleared = False
        else:
            if not room.is_doors_shut:
                room.cleared = True
                return
        
        # check if the room's doors are closed
        if room.is_doors_shut == False:
            # check player's position
            margin_x = 5 * cfg.TILESIZE_SMALL
            margin_y = 5.5 * cfg.TILESIZE_SMALL + cfg.GUI_HEIGHT
            rect = pygame.Rect((margin_x, margin_y), (cfg.WIDTH - 2 *  margin_x, cfg.HEIGHT - cfg.GUI_HEIGHT - margin_y))
            if rect.colliderect(game.player.hit_rect):
                # player is far enough in the room to shut the doors
                room.shut_doors()
                game.soundLoader.get['roomLocked'].play()
                
        else:
            if len(game.enemies) == 0:
                # if all enemies are defeated, open the doors
                room.open_doors()
                game.soundLoader.get['roomCleared'].play()
                room.cleared = True



    def get_inputs(self, game):
        """Game class method to load all assets store keyboard inputs in a key map
        
        """
        game.keys = {
                    'A': False,
                    'B': False,
                    'X': False,
                    'Y': False, 
                    'L': False,
                    'BACK': False,
                    'START': False,
                    'STICK_L_PRESSED': False,
                    'STICK_R_PRESSED': False,
                    'STICK_R': pygame.math.Vector2(0, 0),
                    'STICK_L': pygame.math.Vector2(0, 0),
                    'DPAD': pygame.math.Vector2(0, 0),
                    'DPAD_MENU': pygame.math.Vector2(0, 0)
                    }
        
        key = game.keys
        
        
        # get keyboard keys 
        get_keys = pygame.key.get_pressed()
        if get_keys[cfg.KEY_RIGHT]:
            game.player.RightCheck = True
        elif get_keys[cfg.KEY_LEFT]:
            game.player.LeftCheck = True
        if get_keys[cfg.KEY_DOWN]:
            game.player.DownCheck = True
        elif get_keys[cfg.KEY_UP]:
            game.player.UpCheck = True
            
        
        get_mkeys = pygame.mouse.get_pressed()
        
        key['A'] = get_mkeys == cfg.KEY_A or key['A']
        key['B'] = game.key_down == cfg.KEY_B or key['B']
        key['X'] = game.key_down == cfg.KEY_ENTER or key['X']
        
        key['START'] = get_keys[cfg.KEY_MENU]


    def run(self):
        """Game class method to start running infinite loop until quit.

        """
        # game loop
        self.playing = True
        while self.playing:
            #reset game screen
            self.screen = pygame.Surface((cfg.WIDTH, cfg.HEIGHT))
            self.dt = self.clock.tick(cfg.FPS) / 1000
            self.events()
            self.get_inputs(self)
            self.update()
            self.draw()


    def events(self):
        """Game class method to loop game events.

        """
        # game loop events
        self.event_list = pygame.event.get()
        for event in self.event_list:
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                # Key events
                if event.key == pygame.K_r and self.debug:
                    self.loaded = False
                    self.new()

                if event.key == pygame.K_h:
                    self.debug = not self.debug

                if event.key == pygame.K_k and self.debug:
                    # kill all enemies
                    for e in self.enemies:
                        e.hp = 0

    def screenWrap(self, player, dungeon):
        """Game class method to check if the player goes outside the screen
           if they do, set their new position based on where they went

        """
        index = list(dungeon.current_room_index)
        direction = ''
        new_pos = pygame.math.Vector2(player.hit_rect.center)
        if player.hit_rect.left < cfg.TILESIZE:
            direction = (-1, 0)
            player.vel = pygame.math.Vector2(0, 0)
            new_pos.x  = cfg.WIDTH - player.hit_rect.width - cfg.TILESIZE
            index[1] -= 1
        elif player.hit_rect.right > cfg.WIDTH - cfg.TILESIZE:
            player.vel = pygame.math.Vector2(0, 0)
            direction = (1, 0)
            new_pos.x = player.hit_rect.width + cfg.TILESIZE
            index[1] += 1
        elif player.hit_rect.top < cfg.GUI_HEIGHT + cfg.TILESIZE:
            player.vel = pygame.math.Vector2(0, 0)
            direction = (0, -1)
            new_pos.y = cfg.HEIGHT - player.hit_rect.height - cfg.TILESIZE
            index[0] -= 1
        elif player.hit_rect.bottom > cfg.HEIGHT - cfg.TILESIZE:
            player.vel = pygame.math.Vector2(0, 0)
            direction = (0, 1)
            new_pos.y = player.hit_rect.height + cfg.GUI_HEIGHT + cfg.TILESIZE
            index[0] += 1

        try:
            return direction, index, new_pos
        except Exception:
            traceback.print_exc()

    def update(self):
        """Game class method update game situation.

        """
        
        if self.pistolpick == True :
            self.player.itemA = self.currentpistol

        elif self.machinegunpick == True:
            self.player.itemA = self.currentmachine

        
        if self.debug:
            self.caption = (str(round(self.clock.get_fps(), 2)))

        else:
            self.caption = cfg.TITLE

        pygame.display.set_caption(self.caption)

        # check for key presses
        self.key_down = self.keyDown(self.event_list, self)

        if self.state == 'GAME':
            pygame.mouse.set_visible(False)
            self.all_sprites.update()
        
            self.inventory.update()
            # check for room transitions on screen exit (every frame)
            self.direction, self.new_room, self.new_pos = self.screenWrap(self.player, self.dungeon)

            if self.direction == UP:
                self.dircheck = UP
            elif self.direction == DOWN:
                self.dircheck = DOWN
            elif self.direction == LEFT:
                self.dircheck = LEFT
            elif self.direction == RIGHT:
                self.dircheck = RIGHT

            if self.new_room != self.dungeon.current_room_index:
                self.prev_room = self.dungeon.current_room_index
                self.dungeon.current_room_index = self.new_room
                self.state = 'TRANSITION'

            # When in a fight, shut the doors:
            if not self.dungeon.room_current.cleared:
                self.checkFight(self)
            
            if self.check:
                if self.dungeon.room_current.cleared:
                    a = self.clearcount
                    self.clearcount = self.clearcount + 1
                    self.spritecheck = []
                    if a + 1 == self.clearcount:
                        self.check = False
                
        elif self.state == 'MENU' or self.state == 'MENU_TRANSITION':
            pygame.mouse.set_visible(True)
            self.inventory.update()

        elif self.state == 'TRANSITION':
            #self.RoomTransition(self.new_pos, self.direction)
            # ^this went into draw()
            pass

        elif self.state == 'CUTSCENE':
            self.walls.update()

            
    def WinSit(self):
        """Game class method to check if player won then show next screen.

        """
        global Dx,Dy
        
        if self.dungeon.room_current.type == "endboss" and self.dungeon.room_current.cleared:
            pygame.mouse.set_visible(True)
            self.state = 'WIN'
            self.actual_screen.blit(self.imageLoader.WinImg,(0,0))
            self.Quitbtn = Button(400, 450, 150, 50, 'Quit', (200,20,20,0), (180,0,0,0), self.imageLoader.font1, self.imageLoader.font2)
            self.Nextbtn = Button(200, 450, 150, 50, 'Next', (200,20,20,0), (180,0,0,0), self.imageLoader.font1, self.imageLoader.font2)
            self.Quitbtn.show(self.imageLoader.WinImg)
            self.Nextbtn.show(self.imageLoader.WinImg)
            if self.Quitbtn.is_mouse_clicked():
                    pygame.quit()
                    quit()
            if self.Nextbtn.is_mouse_clicked():
                    self.levelcleared += 1
                    self.clearcount = 0
                    self.check = True
                    cfg.DUNGEON_SIZE = (Dx,Dy)
                    self.state = 'GAME'
                    self.new()
                    Dx = Dx + 1
                    Dy = Dy + 1
                    

    def GameOverr(self):
        """Game class method to check if player is dead and game is over.

        """
        global Dx,Dy
        if self.player.Dead == True:
            self.state = 'GAME OVER' 
            pygame.mouse.set_visible(True)
            self.actual_screen.blit(self.imageLoader.GameOverImg,(0,0))
            self.Quitbtn = Button(400, 450, 150, 50, 'Quit', (200,20,20,0), (180,0,0,0), self.imageLoader.font1, self.imageLoader.font2)
            self.Nextbtn = Button(200, 450, 150, 50, 'Restart', (200,20,20,0), (180,0,0,0), self.imageLoader.font1, self.imageLoader.font2)
            self.Quitbtn.show(self.imageLoader.GameOverImg)
            self.Nextbtn.show(self.imageLoader.GameOverImg)
            if self.Quitbtn.is_mouse_clicked():
                    pygame.quit()
                    quit()
            if self.Nextbtn.is_mouse_clicked():
                    self.levelcleared = 1
                    self.clearcount = 0
                    Dx = 5
                    Dy = 5
                    self.pistolpick = True
                    self.machinegunpick = False
                    self.check = True
                    cfg.DUNGEON_SIZE = (Dx,Dy)
                    self.state = 'GAME'
                    self.new()


    def draw(self):
        """Game class method to draw

        """
        if self.state != 'TRANSITION':
            # draw the background (tilemap)
            self.screen.blit(self.background, (0, cfg.GUI_HEIGHT))
            # call additional draw methods (before drawing)
            for sprite in self.all_sprites:
                if hasattr(sprite, 'draw_before'):
                    sprite.draw_before()
            # draw the sprites
            self.all_sprites.draw(self.screen)

            for sprite in self.all_sprites:
                if hasattr(sprite, 'draw_after'):
                    sprite.draw_after()

            # for machine gun with player
            if self.machinegunpick and self.player.itemA == self.currentmachine:
                if self.player.itemA.check and self.player.mana < 9.8:
                    self.WSignRect = self.WSign.get_rect()
                    self.WSignRect.center = pygame.mouse.get_pos() - pygame.math.Vector2(0,30)
                    self.screen.blit(self.WSign,self.WSignRect)
                    
                if self.player.itemA.check and self.player.mana > 9.8:
                    self.WSignRect = self.WSign2.get_rect()
                    self.WSignRect.center = pygame.mouse.get_pos()- pygame.math.Vector2(0,30)
                    self.screen.blit(self.WSign2,self.WSignRect)
                    
                if self.player.mana < 0.2:
                    self.cursor = self.imageLoader.CursorMain1
                elif self.player.mana < 1.4:
                    self.cursor = self.imageLoader.cursor[0]
                elif self.player.mana < 2.8:
                    self.cursor = self.imageLoader.cursor[1]
                elif self.player.mana < 4.2:
                    self.cursor = self.imageLoader.cursor[2]
                elif self.player.mana < 5.6:
                    self.cursor = self.imageLoader.cursor[3]
                elif self.player.mana < 7:
                    self.cursor = self.imageLoader.cursor[4]
                elif self.player.mana < 8.4:
                    self.cursor = self.imageLoader.cursor[5]
                elif self.player.mana < 9.8:
                    self.cursor = self.imageLoader.cursor[6]
                elif self.player.mana < 11.4:
                    self.cursor = self.imageLoader.cursor[7]

                self.cursorrect = self.cursor.get_rect()
                self.cursorrect.center = pygame.mouse.get_pos()
                self.screen.blit(self.cursor,self.cursorrect)

    
            else:   
                self.cursor = self.imageLoader.CursorMain1
                self.cursorrect = self.cursor.get_rect()
                self.cursorrect.center = pygame.mouse.get_pos()
                self.screen.blit(self.cursor,self.cursorrect)
        
        else:
            self.RoomTransition(self.new_pos, self.direction)
            if not self.dungeon.room_current.cleared:
                self.check = True


        # ----- DEBUG STUFF ----- #
        # draw hitboxes in debug mode
        if self.debug:
            for sprite in self.all_sprites:
                if hasattr(sprite, 'hit_rect'):
                    pygame.draw.rect(self.screen, cfg.CYAN, sprite.hit_rect, 1)
                if hasattr(sprite, 'interact_rect'):
                    pygame.draw.rect(self.screen, cfg.GREEN,
                                 sprite.interact_rect, 1)
                

        # draw the inventory
        self.drawGUI()
        self.screen = pygame.transform.scale(self.screen,(cfg.S_WIDTH, cfg.S_HEIGHT))
        self.actual_screen.blit(self.screen, (0, 0))
        self.WinSit()
        self.GameOverr()
        pygame.display.update()


    def drawGUI(self):
        """Game class method draw inventory with map.

        """
        self.inventory.map_img = self.dungeon.render_rooms_map()
        self.inventory.draw()


    def tileRoom(self, game, tileset, index):
        """Game class method render room tiles.

        """
        image = pygame.Surface((cfg.WIDTH, cfg.HEIGHT - cfg.GUI_HEIGHT))
        data = game.dungeon.room_matrix[index[0]][index[1]].tiles
  
        for i in range(len(data)):
            for j in range(len(data[i])):
                x = j * cfg.TILESIZE
                y = i * cfg.TILESIZE
                try:
                    image.blit(tileset[data[i][j]], (x, y))
                except Exception:
                    traceback.print_exc()
                    return

        return image


    def RoomTransition(self, new_pos, direction):
        """Game class method for room transition.

        Args:
            new_pos (tuple): tuple with x,y corrdinates for the new room for player
            direction (Up, DOWN, LEFT OR RIGHT): direction of start in new room

        """
        if not self.in_transition:
            # store the old background image temporarily
            self.old_background = self.background

            # blit the background and sprites to prevent flickering
            self.screen.blit(self.old_background, (0, cfg.GUI_HEIGHT))
            self.all_sprites.draw(self.screen)

            # build the new room
            self.background = self.tileRoom(self, self.imageLoader.tileset, self.dungeon.current_room_index)
            
            # scroll the new and old background
            # start positions for the new bg are based on the direction the
            # player is moving
            start_positions = {
                              UP: pygame.math.Vector2(0, - (cfg.HEIGHT - cfg.GUI_HEIGHT * 2)),
                              DOWN: pygame.math.Vector2(0, cfg.HEIGHT),
                              LEFT: pygame.math.Vector2(- cfg.WIDTH, cfg.GUI_HEIGHT),
                              RIGHT: pygame.math.Vector2(cfg.WIDTH, cfg.GUI_HEIGHT)
                              }

            self.bg_pos1 = start_positions[direction]
            # pos2 is the old bg's position that gets pushed out of the screen
            self.bg_pos2 = pygame.math.Vector2(0, cfg.GUI_HEIGHT)
            self.in_transition = True

            self.transitRoom(self, self.dungeon, self.bg_pos1)

        else:
            if self.bg_pos1 != (0, cfg.GUI_HEIGHT):
                # moves the 2 room backrounds until the new background is at (0,0)
                # PROBLEM: Only works with certain scroll speeds!

                # calculate the move vector based on the direction
                move = (pygame.math.Vector2(0, 0) - direction) * cfg.SCROLLSPEED

                # move the background surfaces
                self.bg_pos1 += move
                self.bg_pos2 += move

                if direction == UP:
                    self.bg_pos1.y = min(cfg.GUI_HEIGHT, self.bg_pos1.y)
                elif direction == DOWN:
                    self.bg_pos1.y = max(cfg.GUI_HEIGHT, self.bg_pos1.y)
                elif direction == LEFT:
                    self.bg_pos1.x = min(0, self.bg_pos1.x)
                elif direction == RIGHT:
                    self.bg_pos1.x = max(0, self.bg_pos1.x)

                # move the sprites during transition
                for sprite in self.all_sprites:
                    sprite.rect.topleft += move
                    sprite.hit_rect.topleft += move
                    sprite.pos += move

                self.screen.blit(self.old_background, self.bg_pos2)
                self.screen.blit(self.background, self.bg_pos1)
                self.all_sprites.draw(self.screen)
            
            else:
                # update the player's position
                self.player.pos = pygame.math.Vector2(new_pos)
                self.player.hit_rect.center = pygame.math.Vector2(new_pos)
                self.player.spawn_pos = pygame.math.Vector2(new_pos)
                self.player.rect.bottom = self.player.hit_rect.bottom
                
                # end transtition
                self.in_transition = False
                self.state = 'GAME'

                # blit the background and sprites to prevent flickering
                self.screen.blit(self.background, (0, cfg.GUI_HEIGHT))
                self.all_sprites.draw(self.screen)




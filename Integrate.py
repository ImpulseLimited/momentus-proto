import pygame as pg
import traceback

import sprites as spr
import functions as fn
import rooms
import cutscenes as cs
import sounds as snd
import settings as st
from Button import Button
import pdb


vec = pg.math.Vector2


#directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

global Dx,Dy
Dx = 5
Dy = 5
class Game:
    def __init__(self):
        # initialise game window, settings etc.
        pg.mixer.pre_init(44100, -16, 2, 2048)
        pg.mixer.init()
        pg.init()
        pg.mouse.set_visible(False)
        pg.key.set_repeat(10, st.KEY_DELAY)
    
        self.actual_screen = pg.display.set_mode((st.S_WIDTH, st.S_HEIGHT))
        
        self.screen = pg.Surface((st.WIDTH, st.HEIGHT))

        self.clock = pg.time.Clock()
        self.running = True
        self.loaded = False
        self.dircheck = None
        # booleans for drawing the hit rects and other debug stuff
        self.debug = False
        self.draw_vectors = False
        self.show_player_stats = False
        self.caption = ''
        #self.debug_font = pg.font.Font(st.FONT, 24)

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


    def loadAssets(self):
        #loading assets (images, sounds)
        self.imageLoader = spr.ImageLoader(self)
        self.soundLoader = snd.SoundLoader(self)
        try:
            self.imageLoader.load()
            self.soundLoader.load()
        except Exception:
            traceback.print_exc()
            self.running = False

    def new(self):
        # start a new game
        # initialise sprite groups
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.LayeredUpdates() 
        self.gui = pg.sprite.LayeredUpdates()
        self.enemies = pg.sprite.LayeredUpdates()
        self.item_drops = pg.sprite.LayeredUpdates()

        # instantiate dungeon
        self.dungeon = rooms.Dungeon(self, st.DUNGEON_SIZE)
        if self.loaded:
            self.dungeon.tileset = self.saveGame.data['tileset']
        else:
            self.dungeon.create(rng_seed=None)

        self.WSign = self.imageLoader.WarnSign
        self.WSign2 = self.imageLoader.WarnSign2

        self.inventory = spr.Inventory(self)

        # spawn the player in the middle of the room
        self.player = spr.Player(self, (st.WIDTH // 2, st.TILESIZE * 12))

        self.currentpistol = spr.PBullet(self, self.player)
        self.currentmachine = spr.MachineBullet(self, self.player)
        
        if self.pistolpick == True :
            self.player.itemA = self.currentpistol
            
        elif self.machinegunpick == True:
            self.player.itemA = self.currentmachine
               

        # load settings
        if self.loaded:
            self.loadSavefile()

        # spawn the new objects (invisible)
        self.prev_room = self.dungeon.room_index
        fn.transitRoom(self, self.dungeon)

        # create a background image from the tileset for the current room
        self.background = fn.tileRoom(self,
                          self.imageLoader.tileset_dict[self.dungeon.tileset],
                          self.dungeon.room_index)

        self.run()


    def run(self):
        # game loop
        self.playing = True
        while self.playing:
            #reset game screen
            self.screen = pg.Surface((st.WIDTH, st.HEIGHT))
            self.dt = self.clock.tick(st.FPS) / 1000
            self.events()
            fn.get_inputs(self)
            self.update()
            self.draw()


    def events(self):
        # game loop events
        self.event_list = pg.event.get()
        for event in self.event_list:
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                # Key events
                if event.key == pg.K_r and self.debug:
                    self.loaded = False
                    self.new()

                if event.key == pg.K_h:
                    self.debug = not self.debug

                if event.key == pg.K_k and self.debug:
                    # kill all enemies
                    for e in self.enemies:
                        e.hp = 0

    def update(self):
        if self.pistolpick == True :
            self.player.itemA = self.currentpistol

        elif self.machinegunpick == True:
            self.player.itemA = self.currentmachine

        
        
        if self.debug:
            self.caption = (str(round(self.clock.get_fps(), 2)))

        else:
            self.caption = st.TITLE
        pg.display.set_caption(self.caption)

        # check for key presses
        self.key_down = fn.keyDown(self.event_list, self)

        if self.state == 'GAME':
            pg.mouse.set_visible(False)
            self.all_sprites.update()
        
            self.inventory.update()
            # check for room transitions on screen exit (every frame)
            self.direction, self.new_room, self.new_pos = fn.screenWrap(
                    self.player, self.dungeon)

            if self.direction == UP:
                self.dircheck = UP
            elif self.direction == DOWN:
                self.dircheck = DOWN
            elif self.direction == LEFT:
                self.dircheck = LEFT
            elif self.direction == RIGHT:
                self.dircheck = RIGHT

            

            if self.new_room != self.dungeon.room_index:
                self.prev_room = self.dungeon.room_index
                self.dungeon.room_index = self.new_room
                self.state = 'TRANSITION'

            # When in a fight, shut the doors:
            if not self.dungeon.room_current.cleared:
                cs.checkFight(self)
            
            if self.check:
                if self.dungeon.room_current.cleared:
                    a = self.clearcount
                    self.clearcount = self.clearcount + 1
                    self.spritecheck = []
                    if a + 1 == self.clearcount:
                        self.check = False
                
        elif self.state == 'MENU' or self.state == 'MENU_TRANSITION':
            pg.mouse.set_visible(True)
            self.inventory.update()

        elif self.state == 'TRANSITION':
            #self.RoomTransition(self.new_pos, self.direction)
            # ^this went into draw()
            pass

        elif self.state == 'CUTSCENE':
            self.walls.update()

            
    def WinSit(self):
        global Dx,Dy
        
        if self.dungeon.room_current.type == "endboss" and self.dungeon.room_current.cleared:
            pg.mouse.set_visible(True)
            self.state = 'WIN'
            self.actual_screen.blit(self.imageLoader.WinImg,(0,0))
            self.Quitbtn = Button(400,450,150,50,[200,20,20], 'Quit', self.imageLoader.font1, [0,0,0], self.imageLoader.font2)
            self.Nextbtn = Button(200,450,150,50,[200,20,20], 'Next', self.imageLoader.font1, [0,0,0], self.imageLoader.font2)
            self.Quitbtn.update(self.imageLoader.WinImg)
            self.Nextbtn.update(self.imageLoader.WinImg)
            if self.Quitbtn.clicked():
                    pg.quit()
                    quit()
            if self.Nextbtn.clicked():
                    self.levelcleared += 1
                    self.clearcount = 0
                    self.check = True
                    st.DUNGEON_SIZE = (Dx,Dy)
                    self.state = 'GAME'
                    self.new()
                    Dx = Dx + 1
                    Dy = Dy + 1
                    
    def GameOverr(self):
        global Dx,Dy
        if self.player.Dead == True:
            self.state = 'GAME OVER' 
            pg.mouse.set_visible(True)
            self.actual_screen.blit(self.imageLoader.GameOverImg,(0,0))
            self.Quitbtn = Button(400,450,150,50,[200,20,20], 'Quit', self.imageLoader.font1, [0,0,0], self.imageLoader.font2)
            self.Nextbtn = Button(200,450,150,50,[200,20,20], 'Restart', self.imageLoader.font1, [0,0,0], self.imageLoader.font2)
            self.Quitbtn.update(self.imageLoader.GameOverImg)
            self.Nextbtn.update(self.imageLoader.GameOverImg)
            if self.Quitbtn.clicked():
                    pg.quit()
                    quit()
            if self.Nextbtn.clicked():
                    self.levelcleared = 1
                    self.clearcount = 0
                    Dx = 5
                    Dy = 5
                    self.pistolpick = True
                    self.machinegunpick = False
                    self.check = True
                    st.DUNGEON_SIZE = (Dx,Dy)
                    self.state = 'GAME'
                    self.new()

    def draw(self):
        if self.state != 'TRANSITION':
            # draw the background (tilemap)
            self.screen.blit(self.background, (0, st.GUI_HEIGHT))
            # call additional draw methods (before drawing)
            for sprite in self.all_sprites:
                if hasattr(sprite, 'draw_before'):
                    sprite.draw_before()
            # draw the sprites
            self.all_sprites.draw(self.screen)

            for sprite in self.all_sprites:
                if hasattr(sprite, 'draw_after'):
                    sprite.draw_after()
            if self.machinegunpick and self.player.itemA == self.currentmachine:
                if self.player.itemA.check and self.player.mana < 9.8:
                    self.WSignRect = self.WSign.get_rect()
                    self.WSignRect.center = pg.mouse.get_pos() - vec(0,30)
                    self.screen.blit(self.WSign,self.WSignRect)
                    
                if self.player.itemA.check and self.player.mana > 9.8:
                    self.WSignRect = self.WSign2.get_rect()
                    self.WSignRect.center = pg.mouse.get_pos()- vec(0,30)
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
                self.cursorrect.center = pg.mouse.get_pos()
                self.screen.blit(self.cursor,self.cursorrect)

    
            else:   
                self.cursor = self.imageLoader.CursorMain1
                self.cursorrect = self.cursor.get_rect()
                self.cursorrect.center = pg.mouse.get_pos()
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
                    pg.draw.rect(self.screen, st.CYAN, sprite.hit_rect, 1)
                if hasattr(sprite, 'interact_rect'):
                    pg.draw.rect(self.screen, st.GREEN,
                                 sprite.interact_rect, 1)
                
        # draw the inventory
        self.drawGUI()
        self.screen = pg.transform.scale(self.screen,(st.S_WIDTH, st.S_HEIGHT))
        self.actual_screen.blit(self.screen, (0, 0))
        self.WinSit()
        self.GameOverr()
        pg.display.update()

    def drawGUI(self):
        self.inventory.map_img = self.dungeon.blitRooms()
        self.inventory.draw()


    def RoomTransition(self, new_pos, direction):
        if not self.in_transition:
            # store the old background image temporarily
            self.old_background = self.background

            # blit the background and sprites to prevent flickering
            self.screen.blit(self.old_background, (0, st.GUI_HEIGHT))
            self.all_sprites.draw(self.screen)

            # build the new room
            self.background = fn.tileRoom(self,self.imageLoader.tileset_dict[self.dungeon.tileset],self.dungeon.room_index)
            # scroll the new and old background
            # start positions for the new bg are based on the direction the
            # player is moving

            start_positions = {
                              UP: vec(0, - (st.HEIGHT - st.GUI_HEIGHT * 2)),
                              DOWN: vec(0, st.HEIGHT),
                              LEFT: vec(- st.WIDTH, st.GUI_HEIGHT),
                              RIGHT: vec(st.WIDTH, st.GUI_HEIGHT)
                              }

            self.bg_pos1 = start_positions[direction]
            # pos2 is the old bg's position that gets pushed out of the screen
            self.bg_pos2 = vec(0, st.GUI_HEIGHT)
            self.in_transition = True

            fn.transitRoom(self, self.dungeon, self.bg_pos1)

        else:
            if self.bg_pos1 != (0, st.GUI_HEIGHT):
                # moves the 2 room backrounds until the new background is at (0,0)
                # PROBLEM: Only works with certain scroll speeds!

                # calculate the move vector based on the direction
                move = (vec(0, 0) - direction) * st.SCROLLSPEED

                # move the background surfaces
                self.bg_pos1 += move
                self.bg_pos2 += move

                if direction == UP:
                    self.bg_pos1.y = min(st.GUI_HEIGHT, self.bg_pos1.y)
                elif direction == DOWN:
                    self.bg_pos1.y = max(st.GUI_HEIGHT, self.bg_pos1.y)
                elif direction == LEFT:
                    self.bg_pos1.x = min(0, self.bg_pos1.x)
                elif direction == RIGHT:
                    self.bg_pos1.x = max(0, self.bg_pos1.x)

                # move the sprites during transition
                # MEMO: get the target position of the sprite somehow
                for sprite in self.all_sprites:
                    sprite.rect.topleft += move
                    sprite.hit_rect.topleft += move
                    sprite.pos += move

                self.screen.blit(self.old_background, self.bg_pos2)
                self.screen.blit(self.background, self.bg_pos1)
                self.all_sprites.draw(self.screen)
                #self.drawGUI()
            else:
                # update the player's position
                self.player.pos = vec(new_pos)
                self.player.hit_rect.center = vec(new_pos)
                self.player.spawn_pos = vec(new_pos)
                self.player.rect.bottom = self.player.hit_rect.bottom
                # end transtition
                self.in_transition = False
                self.state = 'GAME'

                # blit the background and sprites to prevent flickering
                self.screen.blit(self.background, (0, st.GUI_HEIGHT))
                self.all_sprites.draw(self.screen)




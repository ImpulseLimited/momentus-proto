import pygame
import os

import Config as cfg
from Button import Button

class Inventory(pygame.sprite.Sprite):
    """This class is class for player inventory.

    """
    def __init__(self, game):
        """__init__ method for Inventory class

        Args:
            game (Integrate.Game): Integrate.Game class object.

        """
        self.groups = game.gui
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        # if in menu then True, otherwise False
        self.menu = False

        self.size = (cfg.WIDTH, cfg.HEIGHT)
        self.start_pos = pygame.math.Vector2(0, (0 - cfg.HEIGHT + cfg.GUI_HEIGHT))
        self.pos = pygame.math.Vector2(self.start_pos)
        self.image = pygame.Surface(self.size)
        self.image.fill(cfg.BLACK)

        self.map_img = None

        # "health" string
        self.health_string = self.game.imageLoader.gui_img['health']
        self.heart_images = self.game.imageLoader.gui_img['hearts']
       
        for i in range(len(self.heart_images)):
            self.heart_images[i] = pygame.transform.scale(self.heart_images[i], 
                                  (8, 8))
        
        self.fo1 = pygame.font.Font(os.path.join(cfg.FONT_FOLDER,'slkscr.ttf'),20)
        self.fo3 = pygame.font.Font(os.path.join(cfg.FONT_FOLDER,'slkscr.ttf'),10)
        self.fo2 = pygame.font.Font(os.path.join(cfg.FONT_FOLDER,'slkscrb.ttf'),30)
        self.anim_update = 0
        self.anim_delay = 300
        self.current_frame = 0
        
        self.heart_frames = 0
        self.Quitbtn = Button(cfg.WIDTH//2, cfg.HEIGHT//2, 250, 50, 'Quit Game', (200,20,20,0), (180,0,0,0), self.fo1, self.fo2 )
        

    def update(self):
        """Inventory class method for menu transition update.

        """
        if self.game.keys['START'] and self.game.state != 'MENU_TRANSITION':
            self.menu = not self.menu

        if self.menu:
            self.game.state = 'MENU_TRANSITION'
            # sliding down animation
            if self.pos != (0, 0):
                self.pos.y += cfg.SCROLLSPEED_MENU
                self.pos.y = min(0, self.pos.y)
            else:
                self.game.state = 'MENU'
        else:
            # sliding up animation
            if self.pos != self.start_pos:
                self.game.state = 'MENU_TRANSITION'
                self.pos.y -= cfg.SCROLLSPEED_MENU
                self.pos.y = min(0, self.pos.y)
            else:
                if self.game.state != 'GAME':
                    self.game.state = 'GAME'
                    
        if self.game.state != 'GAME':
                if self.Quitbtn.is_mouse_clicked():
                    pygame.quit()
                    quit()
        

    def draw(self):
        """Inventory class method to draw inventory items.

        """
        self.image.fill(cfg.BLACK)
        # draw player health
        player = self.game.player
        
        for i in range(int(player.max_hp)):
            # calculate position
            if i < cfg.PLAYER_HP_ROW:
                pos = (6 + 10 * i, cfg.HEIGHT - 34)
            else:
                pos = (6 + 10 * (i - cfg.PLAYER_HP_ROW), cfg.HEIGHT - 24)

            # draw hearts:
            if i < int(player.hp):
                img = self.heart_images[1]
            elif i == int(player.hp):
                if player.hp % 1 == 0.25:
                    img = self.heart_images[4]
                elif player.hp % 1 == 0.5:
                    img = self.heart_images[3]
                elif player.hp % 1 == 0.75:
                    img = self.heart_images[2]
                else:
                    img = self.heart_images[5]
            else:
                img = self.heart_images[5]

            self.image.blit(img, pos)

        label = self.fo1.render('Rooms Cleared: '+ str(self.game.clearcount), True, cfg.WHITE)
        labelRect = label.get_rect()
        labelRect.center = (500,cfg.HEIGHT - 30)
        self.image.blit(label, labelRect)
        
        label2 = self.fo1.render('Level: '+ str(self.game.levelcleared), True, cfg.WHITE)
        labelRect2 = label2.get_rect()
        labelRect2.center = (700,cfg.HEIGHT - 30)
        self.image.blit(label2, labelRect2)
        
        self.image.blit(self.health_string, (25, cfg.HEIGHT - 42))
        # draw the mini map
        map_pos = (300, cfg.HEIGHT - 44)
        self.Quitbtn.show(self.image)
        self.image.blit(self.map_img, map_pos)
        self.game.screen.blit(self.image, self.pos)
            
             

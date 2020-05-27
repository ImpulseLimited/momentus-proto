import pygame

import Config as cfg

class Item:       
    """This class is for Items.

    """
    def drop(name, game, pos):
        """item class method drop an item.

        Args:
            name (str): item name..
            game (Integrate.Game) : integrate.Game object.
            pos (tuple) : 2d tuple for position.

        """
        if name in Item.__dict__:
            # instanciate the given sprite by its name
            Item.__dict__[name](game, pos)
        elif name == 'none':
            pass
        else:
            print('Can\'t drop {}.'.format(name))
            
            
    class ItemDrop(pygame.sprite.Sprite):
        """This class is for dropping an item.

        """
        def __init__(self, game, pos):
            """__init__ method for ItemDrop class

            Args:
                game (Integrate.Game): Integrate.Game class object.
                pos (tuple length 2) : position of the player (x,y).

            """
            self.game = game                    
            self.player = self.game.player
            self.pos = pygame.math.Vector2(pos)
            self.groups = self.game.all_sprites, self.game.item_drops
            self.layer = self.game.player.layer - 1
            pygame.sprite.Sprite.__init__(self)
            
            for g in self.groups:
                g.add(self, layer=self.layer)
            
            self.timer = 0
            self.duration = 6 * cfg.FPS
            
            self.alpha = iter([i for i in range(255, 0, -10)] * 3)

        def collide_hit_rect(self, one, two):
            """ItemDrop class method to check if two objects are colliding.

            """
            return one.hit_rect.colliderect(two.hit_rect)
        
        
        def update(self):
            """ItemDrop class method to update item, whether collected or time ended.

            """
            if self.collide_hit_rect(self.player, self):
                self.collect()

            if self.game.player.MoveCheck == True:
                self.timer += 1
                
            if self.timer >= self.duration:
                try:
                    alpha = next(self.alpha)
                    self.image = self.lastimage.copy()
                    self.image.fill((255, 255, 255, alpha), 
                                    special_flags=pygame.BLEND_RGBA_MULT)
                except:
                    self.kill()
            else:
                self.lastimage = self.image.copy()
        
        
        def collect(self):
            """ItemDrop class method to kill item if collected by player.

            """
            self.kill()
        
        
    class heart(ItemDrop):
        """This class is derived from ItemDrop class and 
           contains settings for a dropped heart item.

        """
        def __init__(self, game, pos):
            """__init__ method for heart class

            Args:
                game (Integrate.Game): Integrate.Game class object.
                pos (tuple length 2) : position of the player (x,y).

            """
            super().__init__(game, pos)
            self.image = self.game.imageLoader.item_img['heart']
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.hit_rect = self.rect
           
            
        def collect(self):
            """heart class method to update after heart is collected

            """
            self.player.hp += 1
            self.game.soundLoader.get['heart'].play()
            super().collect()

    class MachineGun(ItemDrop):
        """This class is derived from ItemDrop class and 
           contains settings for a dropped MachineGun item.

        """
        def __init__(self, game, pos):
            """__init__ method for MachineGun class

            Args:
                game (Integrate.Game): Integrate.Game class object.
                pos (tuple length 2) : position of the player (x,y).

            """
            super().__init__(game, pos)
            self.image = self.game.imageLoader.item_img['MachineGun']
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.hit_rect = self.rect

        def update(self):
            """MachineGun class method to update if player collides with it.

            """
            if self.collide_hit_rect(self.player, self):
                self.collect()

            
        def collect(self):
            """MachineGun class method to update after MachineGun is collected

            """
            self.game.player.mana = 0
            if self.game.pistolpick == True:
                self.game.lastweapon = 'Pistol'
            elif self.game.machinegunpick == True:
                self.game.lastweapon = 'MachineGun'

            check = self.player.pos - pygame.math.Vector2(40,40)
            
            if check.x < 50:
                check.x = 80
            elif check.x > 755:
                check.x = 730
            if check.y < 140:
                check.y = 150
            elif check.y > 555:
                check.y = 530
            
            try:
                Item.drop(self.game.lastweapon, self.game, check)
            except:
                print('error. cannot drop item', self.game.lastweapon)
            self.game.machinegunpick = True
            self.game.pistolpick = False
            self.game.soundLoader.get['heart'].play()
            super().collect()
            
    class Pistol(ItemDrop):
        """This class is derived from ItemDrop class and 
           contains settings for a dropped Pistol item.

        """
        def __init__(self, game, pos):
            """__init__ method for Pistol class

            Args:
                game (Integrate.Game): Integrate.Game class object.
                pos (tuple length 2) : position of the player (x,y).

            """
            super().__init__(game, pos)
            self.image = self.game.imageLoader.item_img['Pistol']
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.hit_rect = self.rect

        def update(self):
            """Pistol class method to update if player collides with it.

            """
            if self.collide_hit_rect(self.player, self):
                self.collect()

    
        def collect(self):
            """Pistol class method to update after MachineGun is collected

            """
            if self.game.pistolpick == True:
                self.game.lastweapon = 'Pistol'
            elif self.game.machinegunpick == True:
                self.game.lastweapon = 'MachineGun'
            check = self.player.pos - pygame.math.Vector2(40,40)
            
            if check.x < 50:
                check.x = 80
            elif check.x > 755:
                check.x = 730
            if check.y < 140:
                check.y = 150
            elif check.y > 555:
                check.y = 530
            
            try:
                Item.drop(self.game.lastweapon, self.game, check)
            except:
                print('error. cannot drop item', self.game.lastweapon)
                
            self.game.machinegunpick = False
            self.game.pistolpick = True
            self.game.soundLoader.get['heart'].play()
            super().collect()
        
         
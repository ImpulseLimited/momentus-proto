import pygame
import random

from weapons.Weapon import Weapon
from bullets.PlayerPistolBullet import PlayerPistolBullet

class Pistol(Weapon):
    """This class is derived from Weapon class and 
       contains settings for a pistol usage by a player.

    """
    def __init__(self, game, player):
        """__init__ method for Pistol class

        Args:
            game (<class 'Integrate.Game'>): Integrate.Game class object.
            player (<class 'Player.Player'>): Player.Player class object

        """
        self.type = 'Pistol'
        super().__init__(game, player)
        self.fired = False
        self.cooldown = 30
        self.hit_rect = pygame.Rect((0, 0), (int(10),int(10)))
        self.soundlist = [self.game.soundLoader.get['laserPistolShot']]
        
    def use(self):
        """Pistol class method to use the pistol. 
           Overriding base class method

        """
        super().use()
        if not self.fired and self.player.shootcheck == True:
            self.lastdir = self.player.lastdir
            PlayerPistolBullet(self.game, self, self.rect.center)
            asound = random.choice(self.soundlist)
            asound.play()
            self.fired = True
    
    def reset(self):
        """Pistol class method to reset the pistol. 

        """
        self.fired = False
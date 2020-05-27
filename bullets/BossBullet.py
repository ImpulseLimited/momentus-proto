import pygame
 
from bullets.EnemyProjectile import EnemyProjectile    

class BossBullet(EnemyProjectile):
    """This class is derived from EnemyProjectile class and 
       contains settings for a bullet projectile shot by the boss.

    """
    def __init__(self, game, enemy, pos, rotating=True):
        """__init__ method for BossBullet class

        Args:
            game (Integrate.Game): Integrate.Game class object.
            enemy (Enemy.Enemy): Enemy.Enemy class object.
            pos (tuple length 2) : position of the player (x,y).

        """
        self.image = game.imageLoader.item_img['BossBullet']           
        super().__init__(game, enemy, pos)
        
        self.speed = 3
        self.max_speed = 5
        self.damage = 2
        self.anim_speed = 100
        self.hit_rect = pygame.Rect((0, 0), (int(5),int(5)))
    

    
        
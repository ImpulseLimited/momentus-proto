import pygame

from bullets.EnemyProjectile import EnemyProjectile

class EnemyBullet(EnemyProjectile):
    """This class is derived from EnemyProjectile class and 
       contains settings for a bullet projectile shot by a enemy.

    """
    def __init__(self, game, enemy, pos, rotating=True):
        """__init__ method for EnemyBullet class

        Args:
            game (Integrate.Game): Integrate.Game class object.
            enemy (Enemy.Enemy): Enemy.Enemy class object.
            pos (tuple length 2) : position of the player (x,y).

        """
        self.image = game.imageLoader.item_img['EnemyBullet']           
        super().__init__(game, enemy, pos)
        
        self.speed = 2
        self.max_speed = 4
        self.damage = 1
        self.anim_speed = 100
        self.hit_rect = pygame.Rect((0, 0), (int(5),int(5)))
        self.destroy_timer = 0
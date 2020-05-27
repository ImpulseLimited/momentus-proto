from bullets.EnemyProjectile import EnemyProjectile

class MiniBossBullet(EnemyProjectile):
    """This class is derived from EnemyProjectile class and 
       contains settings for a bullet projectile shot by a mini boss.

    """
    def __init__(self, game, enemy, pos, rotating=True):
        """__init__ method for MiniBossBullet class

        Args:
            game (Integrate.Game): Integrate.Game class object.
            enemy (Enemy.Enemy): Enemy.Enemy class object.
            pos (tuple length 2) : position of the player (x,y).

        """
        self.image = game.imageLoader.item_img['MiniBossBullet']           
        super().__init__(game, enemy, pos)
        
        self.speed = 3
        self.max_speed = 5
        self.damage = 1.5
        self.anim_speed = 100
        
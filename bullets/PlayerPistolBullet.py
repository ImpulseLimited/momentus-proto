from bullets.PlayerProjectile import PlayerProjectile

class PlayerPistolBullet(PlayerProjectile):
    """This class is derived from PlayerProjectile class and 
       contains settings for a pistol Bullet Projectile shot by a player.

    """
    def __init__(self, game, player, pos):
        """__init__ method for PlayerPistolBullet class

        Args:
            game (Integrate.Game): Integrate.Game class object.
            player (Player.Player): Player.Player class object.
            pos (tuple length 2) : position of the player (x,y).

        """
        self.image = game.imageLoader.item_img['Pbullet']           
        super().__init__(game, player, pos)
        self.speed = 2
        self.max_speed = 4
        self.damage = 2
        self.anim_speed = 100
        self.destroy_timer = 0

    def destroy(self):
        """PlayerPistolBullet class method to destroy the bullet. 
           Overriding base class method

        """
        if self.state == 'HIT_WALL':
            if self.vel.length_squared() > 0:
                self.pos += self.vel.normalize() * 3
            self.vel *= 0
            self.kill()
        elif self.state == 'HIT_ENEMY':
            self.pos = self.enemy.pos
            self.kill()
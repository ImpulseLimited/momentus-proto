
import pygame
import math

from bullets.PlayerProjectile import PlayerProjectile

class PlayerMachinegunBullet(PlayerProjectile):
    """This class is derived from PlayerProjectile class and 
       contains settings for a machine gun bullet PlayerProjectile shot by a player.

    """
    def __init__(self, game, player, pos):
        """__init__ method for Bullet class

        Args:
            game (<class 'Integrate.Game'>): Integrate.Game class object.
            player (<class 'Player.Player'>): Player.Player class object.
            pos (tuple length 2) : position of the player (x,y).

        """
        self.image = game.imageLoader.item_img['Mbullet']           
        super().__init__(game, player, pos)
        
        self.speed = 2
        self.max_speed = 4
        self.damage = 3
        self.anim_speed = 100
        self.destroy_timer = 0
        self.hit_rect = pygame.Rect((0, 0), (int(5),int(5)))
        position = pygame.mouse.get_pos()
        Bangle = math.degrees(math.atan2(position[1]-(self.game.player.pos.y),position[0]-(self.game.player.pos.x)))
        A = self.game.player.pos.x + math.cos(math.radians(Bangle))*40
        B = self.game.player.pos.y + math.sin(math.radians(Bangle))*40
        self.bulletlst.append([math.atan2(position[1]-(self.game.player.pos.y),position[0]-(self.game.player.pos.x)),A,B])
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.hit_rect.center = self.rect.center
        
    def destroy(self):
        """PlayerMachinegunBullet class method to destroy the bullet. 
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
                 

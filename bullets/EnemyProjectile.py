import pygame
import math

from effects.Explosion import Explosion      

class EnemyProjectile(pygame.sprite.Sprite):
    """This class is base class for all bullet projectiles by the enemy.

    """
    def __init__(self, game, enemy, pos):
        """__init__ method for EnemyProjectile class

        Args:
            game (Integrate.Game): Integrate.Game class object.
            enemy (Enemy.Enemy): Enemy.Enemy class object.
            pos (tuple length 2) : position of the player (x,y).

        """
        self.group = game.all_sprites
        self.layer = enemy.layer
        pygame.sprite.Sprite.__init__(self)
        self.group.add(self, layer=self.layer)
        self.enemy = enemy
        self.game = game
        self.pos = pygame.math.Vector2(pos)
        self.Blst = []
        self.vel = pygame.math.Vector2(0, 0)       
        self.anim_update = 0
        self.current_frame = 0
        self.state = 'SHOT'
        
        # set own direction based on the direction the player sprite is facing
        self.destroy_timer = 0
        self.angle = 0
        self.dir = self.enemy.lastdir
        
        self.image = pygame.transform.rotozoom(self.image, self.enemy.angleee, 1)
        Bangle = math.degrees(math.atan2(self.game.player.pos.y-(self.enemy.pos.y),self.game.player.pos.x-(self.enemy.pos.x)))
        A = self.enemy.pos.x + math.cos(math.radians(Bangle))*35
        B = self.enemy.pos.y + math.sin(math.radians(Bangle))*35
        self.Blst.append([math.atan2(self.game.player.pos.y-(self.enemy.pos.y),self.game.player.pos.x-(self.enemy.pos.x)),A,B])
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.maskbount = self.mask.get_bounding_rects()
        self.rect.center = self.pos
        self.hit_rect = self.maskbount[0]
        self.hit_rect.center = self.rect.center

    def collide_hit_rect(self, one, two):
        """EnemyProjectile class method to check if two objects are colliding.

        """
        return one.hit_rect.colliderect(two.hit_rect)

    def update(self):
        """EnemyProjectile class method to update the projectile motion of enemy bullet and its effects.

        """
        if self.state == 'SHOT':
            # effects of hiting an explotion crate
            hits_walls = pygame.sprite.spritecollide(self, self.game.walls, False, self.collide_hit_rect)
            for wall in hits_walls:
                if wall.image == self.game.imageLoader.solid_img['crate']:
                    images = self.game.imageLoader.effects['crate_explosion']
                    Explosion(self.game, pygame.math.Vector2(self.pos), images, 80, damage = 0.2,
                              sound=self.game.soundLoader.get['explosiveTank'],
                              hit_rect=pygame.Rect(images[0].get_rect().inflate(-6, -6)))
                    wall.kill()
            
            # change the state to hits wall and later destroy bullet
            if hits_walls:
                self.state = 'HIT_WALL'

            # update the bullet velocity and position
            for bullet in self.Blst:
                velx=math.cos(bullet[0])*5
                vely=math.sin(bullet[0])*5
                if self.game.player.MoveCheck == True:
                    bullet[1]+=velx
                    bullet[2]+=vely
                for projectile in self.Blst:
                    self.acc = projectile
                    
            # cause damage to player if bullet hits them
            player = self.game.player
            if self.collide_hit_rect(player, self):
                if (player.state != 'HITSTUN'):
                    self.state = 'HIT_Player'
                    player.hp -= self.damage
                    
            # limit velocity
            if self.vel.length_squared() > self.max_speed ** 2:
                self.vel.scale_to_length(self.max_speed)

            # updates the position of the bullet.
            self.pos = (self.acc[1], self.acc[2])

        else:
            self.destroy()
        
        self.rect.center = self.pos
        self.hit_rect.center = self.rect.center

    def destroy(self):
        """EnemyProjectile class method to destroy the bullet.

        """
        if self.state == 'HIT_WALL':
            # push the arrow a bit into a wall
            if self.vel.length_squared() > 0:
                self.pos += self.vel.normalize() * 3
            self.vel *= 0
            self.kill()
        elif self.state == 'HIT_Player':
            self.pos = self.game.player.pos
            self.kill()
              
           
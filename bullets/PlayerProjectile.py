import pygame
import math

from effects.Explosion import Explosion
     
class PlayerProjectile(pygame.sprite.Sprite):
    """This class is base class for all bullet projectiles by the player.

    """
    def __init__(self, game, player, pos):
        """__init__ method for PlayerProjectile class

        Args:
            game (Integrate.Game): Integrate.Game class object.
            player (Player.Player): Player.Player class object.
            pos (tuple length 2) : position of the player (x,y).

        """
        self.group = game.all_sprites
        self.layer = 1
        pygame.sprite.Sprite.__init__(self)
        self.group.add(self, layer=self.layer)
        self.player = player
        self.game = game
        self.Blst = []
        self.vel = pygame.math.Vector2(0, 0)
        self.anim_update = 0
        self.current_frame = 0
        self.angle = 0
        self.bulletlst = []
        
        self.state = 'SHOT'
        self.pos = (0,0)
        self.dir = self.player.lastdir  # set own direction based on the direction the player sprite is facing
        
        self.image = pygame.transform.rotozoom(self.image, self.game.player.angle3, 1)
            
        position = pygame.mouse.get_pos()
        Bangle = math.degrees(math.atan2(position[1]-(self.game.player.pos.y),position[0]-(self.game.player.pos.x)))
        A = self.game.player.pos.x + math.cos(math.radians(Bangle))*35
        B = self.game.player.pos.y + math.sin(math.radians(Bangle))*35
        self.bulletlst.append([math.atan2(position[1]-(self.game.player.pos.y),position[0]-(self.game.player.pos.x)),A,B])
        self.mask = pygame.mask.from_surface(self.image)
        self.maskbount = self.mask.get_bounding_rects()
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.hit_rect = self.maskbount[0]
        self.hit_rect.center = self.rect.center


    def collide_hit_rect(self, one, two):
        """PlayerProjectile class method to check if two objects are colliding.

        """
        return one.hit_rect.colliderect(two.hit_rect)
        
        
    def update(self):
        """PlayerProjectile class method to update the PlayerProjectile motion of player bullet and its effects.

        """
        if self.state == 'SHOT':
            # effects of hiting an explotion crate
            hits_walls = pygame.sprite.spritecollide(self, self.game.walls, False, self.collide_hit_rect)
            for wall in hits_walls:
                if wall.image == self.game.imageLoader.solid_img['crate']:
                    images = self.game.imageLoader.effects['crate_explosion']
                    Explosion(self.game, pygame.math.Vector2(self.pos), images, 80, damage = 0.2,
                              sound=self.game.soundLoader.get['bomb'],
                              hit_rect=pygame.Rect(images[0].get_rect().inflate(-6, -6)))
                    wall.kill()

            # change the state to hits wall and later destroy bullet
            if hits_walls:
                self.state = 'HIT_WALL'

            # update the bullet velocity and position
            for bullet in self.bulletlst:
                velx=math.cos(bullet[0])*5
                vely=math.sin(bullet[0])*5
                if self.game.player.MoveCheck == True:
                    bullet[1]+=velx
                    bullet[2]+=vely
                for PlayerProjectile in self.bulletlst:
                    self.acc = PlayerProjectile
                    
            # cause damage to enemies if bullet hits them
            hits_enemies = pygame.sprite.spritecollide(self, self.game.enemies, False, self.collide_hit_rect)
            # change the state to hit enemies and later destroy bullet
            if hits_enemies:
                for enemy in hits_enemies:
                    enemy.hp -= self.damage
                    self.state = 'HIT_ENEMY'
                    self.enemy = enemy

            # updates the position of the bullet.
            self.pos = (self.acc[1], self.acc[2])
        
        else:
            self.destroy()
        
        self.rect.center = self.pos
        self.hit_rect.center = self.rect.center
        
        # animate the motion of bullet
        try:        
            self.animate()
        except:
            # has no animation frames
            pass
        
    
    def animate(self):
        """PlayerProjectile class method to animate the bullet PlayerProjectile.

        """
        now = pygame.time.get_ticks()
        if now - self.anim_update > self.anim_speed:
            self.anim_update = now
            self.current_frame = (self.current_frame + 1) % len(
                                  self.image_frames)
            self.image = self.image_frames[self.current_frame]
            
    
    def destroy(self):
        """PlayerProjectile class method to destroy the bullet.

        """
        self.vel *= 0
        self.kill()

      

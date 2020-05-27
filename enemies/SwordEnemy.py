import pygame
import random

import Config as cfg
from enemies.Enemy import Enemy

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class SwordEnemy(Enemy):
    """This class is derived from Enemy class and 
       contains settings for a simple enemy.

    """
    def __init__(self, game, pos, *args, **kwargs):
        """__init__ method for SwordEnemy class

        Args:
            game (Integrate.Game): Integrate.Game class object.
            pos (tuple length 2) : position of the player (x,y).

        """
        self.name = 'Enemy'
        self.image_strip = game.imageLoader.enemy_img[self.name]
        self.walk_frames = {
            UP: [self.image_strip[0][0],self.image_strip[0][1],self.image_strip[0][2],self.image_strip[0][3]],
            DOWN: [self.image_strip[1][0],self.image_strip[1][1],self.image_strip[1][2],self.image_strip[1][3]],
            LEFT: [self.image_strip[2][0],self.image_strip[2][1],self.image_strip[2][2],self.image_strip[2][3]],
            RIGHT: [self.image_strip[3][0],self.image_strip[3][1],self.image_strip[3][2],self.image_strip[3][3]]}
        self.idle_frames = {
            UP: [self.image_strip[0][0]],
            DOWN: [self.image_strip[1][0]], 
            LEFT: [self.image_strip[2][0]],
            RIGHT: [self.image_strip[3][0]]}
        super().__init__(game, pos)
        self.image = self.idle_frames[UP][0]
        self.kb_time = 1
        self.kb_intensity = 0.5
        self.hp = 12
        self.state = 'SEEK'
        self.maxSpeed = 2
        self.speed = 1
        self.anim_speed = 300
        self.drop_rates = {'none':100,'heart':50}
        self.hit_rect = pygame.Rect(0, 0, int(30), int(30))
        self.timer = 0
        self.shoot_time = 1.5 * cfg.FPS
        self.stun_timer = 0
        self.attack_update = 0
        
    def update(self):
        """SwordEnemy class method to update.

        """
        # change the drawing layer in relation to the player
        if self.hit_rect.top > self.game.player.hit_rect.top:
            for g in self.groups:
                g.change_layer(self, self.game.player.layer + 1)
        else:
            for g in self.groups:
                g.change_layer(self, self.game.player.layer - 1)
       
        # change the moving direction after a certain time
        now = pygame.time.get_ticks()
        if now - self.walk_update > 2000:
            self.walk_update = now
            self.moveTo = random.choice([LEFT, RIGHT, DOWN, UP])
            
        if self.state == 'SWORD':
            self.hit_rect = pygame.Rect(0, 0, int(2), int(2))
        else:
            self.hit_rect = pygame.Rect(0, 0, int(30), int(30))
        # calculate acceleration
        self.move()
        # add acceleration to velocity
        
        self.vel += self.acc
               
        if self.state != 'HITSTUN':
            # reset acceleration
            self.acc *= 0
             # apply friction
            self.vel *= (1 - self.friction)
    
            # cap speed at maximum
            if self.vel.length_squared() > self.maxSpeed ** 2:
                self.vel.scale_to_length(self.maxSpeed)
        
        # add velocity to position
        self.pos += self.vel
        
        # update the position
        self.rect = self.image.get_rect()
        self.hitbox = self.rect.inflate(2,2)
        self.rect.center = self.pos
        self.hitbox.center = self.pos

        if self.state != 'WALKING':
            if self.game.player.state == 'WALKING':
                self.state = 'SEEK'
            if self.game.player.state == 'IDLE':
                self.state = 'IDLE'
            if self.game.player.state == 'HITSTUN':
                self.state = 'IDLE'
        
                
            
        # collision with walls
        self.hit_rect.centerx = self.pos.x
        self.collide_with_walls(self, self.game.walls, 'x')
        self.collide_with_walls(self, self.game.enemies, 'x')
        self.hit_rect.centery = self.pos.y
        self.collide_with_walls(self, self.game.walls, 'y')
        self.collide_with_walls(self, self.game.enemies, 'y')
        if self.collide_with_walls(self, self.game.walls, 'y') or self.collide_with_walls(self, self.game.walls, 'x'):
            self.walk_update = now
            a = random.choice([LEFT, RIGHT, DOWN, UP])
            if a != self.lastdir:
                self.moveTo == a
                    
        # restrain position to stay in the room
        self.pos.x = self.clamp(self.pos.x, cfg.TILESIZE * 2, 
                              cfg.WIDTH - cfg.TILESIZE * 2)
        self.pos.y = self.clamp(self.pos.y, cfg.GUI_HEIGHT + cfg.TILESIZE * 2, 
                              cfg.HEIGHT - cfg.TILESIZE * 2)

        # position the hitbox at the bottom of the image
        self.hitbox.midbottom  = self.hit_rect.midbottom
        
            
        self.collide_with_player()
        if self.hp <= 0 and self.state != 'DYING':
            #self.destroy()
            self.vel *= 0
            self.anim_speed = 300
            self.state = 'DYING'
        
        
        self.poss = (self.game.player.pos - self.pos)
        if self.poss.length_squared() < 2000 and self.game.player.MoveCheck:
            self.state = 'SWORD'
        
        
        self.animate()  
        if self.state == 'SWORD':
            self.SwordWeapon.use()
            self.attack_update += 1
            if self.attack_update > self.SwordWeapon.cooldown:
                self.attack_update = 0
                self.SwordWeapon.reset()
        
            
            
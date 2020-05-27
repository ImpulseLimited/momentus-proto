import pygame
import random

import Config as cfg
from bullets.BossBullet import BossBullet
from enemies.Enemy import Enemy

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Boss(Enemy):
    """This class is derived from Enemy class and 
       contains settings for a Boss.

    """
    def __init__(self, game, pos, *args, **kwargs):
        """__init__ method for Boss class

        Args:
            game (Integrate.Game): Integrate.Game class object.
            pos (tuple length 2) : position of the player (x,y).

        """
        self.name = 'Boss'
        self.image_strip = game.imageLoader.enemy_img[self.name]
        self.walk_frames = {
            UP: [self.image_strip[0][0],self.image_strip[0][1],self.image_strip[0][2],self.image_strip[0][3],self.image_strip[0][4],self.image_strip[0][5]],
            DOWN: [self.image_strip[1][0],self.image_strip[1][1],self.image_strip[1][2],self.image_strip[1][3],self.image_strip[1][4],self.image_strip[1][5]],
            LEFT: [self.image_strip[2][0],self.image_strip[2][1],self.image_strip[2][2],self.image_strip[2][3],self.image_strip[2][4],self.image_strip[2][5]],
            RIGHT: [self.image_strip[3][0],self.image_strip[3][1],self.image_strip[3][2],self.image_strip[3][3], self.image_strip[3][4],self.image_strip[3][5]]}
        self.idle_frames = {
            UP: [self.image_strip[0][0]],
            DOWN: [self.image_strip[1][0]], 
            LEFT: [self.image_strip[2][0]],
            RIGHT: [self.image_strip[3][0]]}
        self.hit_image = self.idle_frames[UP][0]
        self.hit_rect = pygame.Rect((0, 0), (int(30),int(30)))
        super().__init__(game, pos)
        self.image = self.idle_frames[UP][0]
        self.state = 'WALKING'        
        self.hit_rect.center = self.rect.center
        self.damage = 0.5
        self.hp = 8
        self.drop_rates = {'none':100,'MachineGun': 20}
        # knockback stats
        self.kb_time = 1
        self.kb_intensity = 2
        self.maxSpeed = 1
        self.timer = 0
        self.shoot_time = 1*cfg.FPS
        self.stun_timer = 0

    def update(self):
        """Boss class method to update.

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
            self.moveTo = random.choice([LEFT, RIGHT, DOWN, UP, UP, UP, UP, UP, UP, LEFT, RIGHT, LEFT, RIGHT, DOWN,DOWN,DOWN,DOWN,DOWN,DOWN])
        
        # calculate acceleration
        self.move()
        if self.game.pistolpick == True:
            self.drop_rates['Pistol'] = 0
            self.drop_rates['MachineGun'] = 20
        elif self.game.machinegunpick == True:
            self.drop_rates['Pistol'] = 0
            self.drop_rates['MachineGun'] = 0
            
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
        if self.game.player.state == 'IDLE':
            self.state = 'IDLE'
        if self.game.player.state == 'WALKING':
            self.state = 'WALKING'
            
        # collision with walls
        self.hit_rect.centerx = self.pos.x
        self.collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        self.collide_with_walls(self, self.game.walls, 'y')
        if self.collide_with_walls(self, self.game.walls, 'y') or self.collide_with_walls(self, self.game.walls, 'x'):
            self.walk_update = now
            a = random.choice([LEFT, RIGHT, DOWN, UP, UP, UP, UP, UP, UP, LEFT, RIGHT, LEFT, RIGHT, DOWN,DOWN,DOWN,DOWN,DOWN,DOWN])
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
            self.anim_speed = 100
            self.state = 'DYING'
        self.animate()
        dist = self.game.player.rect.center - self.pos
        self.timer += 1
        a = random.randint(1,100)
        if a in range(1,5):
            self.state = 'FIRING'
        if self.state == 'FIRING' and self.game.player.MoveCheck == True:
            self.timer = 0
            pos = self.pos + (dist.normalize() * cfg.TILESIZE)
            BossBullet(self.game, self, pos)
            if self.timer >= self.shoot_time:
                self.state = 'WALKING'
    
    
        
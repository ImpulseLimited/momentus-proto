import pygame
import random
import math

import Config as cfg
from bullets.EnemyPistolBullet import EnemyPistolBullet
from Item import Item

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Enemy(pygame.sprite.Sprite):
    """This class is base class for all enemies.

    """
    def __init__(self, game, pos):
        """__init__ method for Enemy class

        Args:
            game (Integrate.Game): Integrate.Game class object.
            pos (tuple length 2) : position of the player (x,y).

        """
        self.game = game
        self.pos = pygame.math.Vector2(pos)
        self.groups = self.game.all_sprites, self.game.enemies
        self.layer = self.game.player.layer + 1
        pygame.sprite.Sprite.__init__(self)
        
        for g in self.groups:
            g.add(self, layer=self.layer)

        self.image = self.idle_frames[UP][0]
        
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.vel = pygame.math.Vector2(0, 0)
        self.dir = pygame.math.Vector2(DOWN)
        self.lastdir = pygame.math.Vector2(DOWN)
        self.moveTo = None
        self.acc = pygame.math.Vector2(0, 0)
        self.hit_flash = 0
        self.flash_gap = 0
        self.flash_alpha = 200
        self.friction = 0.1
        self.hp = 1
        self.damage = 0.5
        self.anim_speed = 300
        self.maxSpeed = 1
        self.drop_rates = {'none':1,'heart':0.5}
        self.state = 'IDLE'
        self.anim_update = 0
        self.walk_update = 0
        self.current_frame = 0
        self.timer = 0
        self.angle_to_player = 0
        self.shoot_time = 2 * cfg.FPS
        self.stun_timer = 0
        self.SwordEnemymove = False
        self.zig1 = False
        self.zig2 = False
        self.zig1Count = 0
        self.zig2Count = 0
        
    def move(self):
        """Enemy class method to move enemy.

        """
        # if player is moving then only enemy can move
        if self.state == 'WALKING' and self.game.player.MoveCheck == True:
            # set acceleration based on 4-way movement
            if self.moveTo == LEFT:
                self.acc.x = -1       
                self.dir = pygame.math.Vector2(LEFT)
                self.lastdir = pygame.math.Vector2(LEFT)
    
            if self.moveTo == RIGHT:
                self.acc.x = 1          
                self.dir = pygame.math.Vector2(RIGHT)
                self.lastdir = pygame.math.Vector2(RIGHT)
    
            if self.moveTo == UP:
                self.acc.y = -1
                self.dir = pygame.math.Vector2(UP)
                self.lastdir = pygame.math.Vector2(UP)
    
            if self.moveTo == DOWN:
                self.acc.y = 1
                self.dir = pygame.math.Vector2(DOWN)
                self.lastdir = pygame.math.Vector2(DOWN)
        
        elif self.state == 'SEEK' and self.game.player.MoveCheck == True:
            desired = (self.game.player.pos - self.pos)
            if desired.length_squared() > 0:
                desired = desired.normalize() * self.maxSpeed
                steer = desired - self.vel
                self.acc = steer
                if self.zig1Count < 21:
                    if self.lastdir == pygame.math.Vector2(LEFT) or self.lastdir == pygame.math.Vector2(RIGHT): 
                        self.acc = steer - pygame.math.Vector2(1,0)
                        self.acc = steer - pygame.math.Vector2(1,0)
                        self.acc = steer - pygame.math.Vector2(1,0)
                        self.acc = steer - pygame.math.Vector2(1,0)
                        self.acc = steer - pygame.math.Vector2(1,0)
                        self.acc = steer - pygame.math.Vector2(1,0)
                        self.acc = steer - pygame.math.Vector2(1,0)
                        self.acc = steer - pygame.math.Vector2(1,0)
                        self.acc = steer - pygame.math.Vector2(1,0)
                        self.acc = steer - pygame.math.Vector2(1,0)
                        
                    else:
                        self.acc = steer - pygame.math.Vector2(0,1)
                        self.acc = steer - pygame.math.Vector2(0,1)
                        self.acc = steer - pygame.math.Vector2(0,1)
                        self.acc = steer - pygame.math.Vector2(0,1)
                        self.acc = steer - pygame.math.Vector2(0,1)
                        self.acc = steer - pygame.math.Vector2(0,1)
                        self.acc = steer - pygame.math.Vector2(0,1)
                        self.acc = steer - pygame.math.Vector2(0,1)
                        self.acc = steer - pygame.math.Vector2(0,1)
                        self.acc = steer - pygame.math.Vector2(0,1)
                        
                        
                if self.zig1Count > 20 and self.zig1Count < 41:
                    if self.lastdir == pygame.math.Vector2(LEFT) or self.lastdir == pygame.math.Vector2(RIGHT):
                        self.acc = steer + pygame.math.Vector2(1,0)
                        self.acc = steer + pygame.math.Vector2(1,0)
                        self.acc = steer + pygame.math.Vector2(1,0)
                        self.acc = steer + pygame.math.Vector2(1,0)
                        self.acc = steer + pygame.math.Vector2(1,0)
                        self.acc = steer + pygame.math.Vector2(1,0)
                        self.acc = steer + pygame.math.Vector2(1,0)
                        self.acc = steer + pygame.math.Vector2(1,0)
                        self.acc = steer + pygame.math.Vector2(1,0)
                        self.acc = steer + pygame.math.Vector2(1,0)
                        
                        
                       
                    else:
                        self.acc = steer + pygame.math.Vector2(0,1)
                        self.acc = steer + pygame.math.Vector2(0,1)
                        self.acc = steer + pygame.math.Vector2(0,1)
                        self.acc = steer + pygame.math.Vector2(0,1)
                        self.acc = steer + pygame.math.Vector2(0,1)
                        self.acc = steer + pygame.math.Vector2(0,1)
                        self.acc = steer + pygame.math.Vector2(0,1)
                        self.acc = steer + pygame.math.Vector2(0,1)
                        self.acc = steer + pygame.math.Vector2(0,1)
                        self.acc = steer + pygame.math.Vector2(0,1)
                        
                    
                if self.zig1Count > 40:
                    self.zig1Count = 0
                self.zig1Count += 0.5
            
               
        elif self.state == 'HITSTUN' or self.state == 'DYING':
            # can't change acceleration when stunned
            pass

    def clamp(self, var, lower, upper):
        """Enemy class method to restrain in the room.

        Args:
            var (int): variable to restrain.
            lower (int) : lower bound.
            upper (int): upper bound.

        Returns:
            pos (int): position of the variable after applying restrain condition.

        """
        pos = max(lower, min(var, upper))
        return pos

    def collide_with_walls(self, sprite, group, dir_):
        """Enemy class method to detect collision with the walls.

        Args:
            sprite (Enemy.Enemy): Enemy object.
            group (pygame.sprite.LayeredUpdates) : sprite layers.
            dir_ (str) : direction.

        """
        if dir_ == 'x':
            hits = pygame.sprite.spritecollide(sprite, group, False, self.collide_hit_rect)
            if hits:
                # hit from left
                if hits[0].hit_rect.centerx > sprite.hit_rect.centerx:
                    sprite.pos.x = hits[0].hit_rect.left - sprite.hit_rect.w / 2
                # hit from right
                elif hits[0].hit_rect.centerx < sprite.hit_rect.centerx:
                    sprite.pos.x = hits[0].hit_rect.right + sprite.hit_rect.w / 2
                                
                sprite.vel.x = 0
                sprite.hit_rect.centerx = sprite.pos.x
                return True
                
        elif dir_ == 'y':
            hits = pygame.sprite.spritecollide(sprite, group, False, self.collide_hit_rect)
            if hits:
                # hit from top
                if hits[0].hit_rect.centery > sprite.hit_rect.centery:
                    sprite.pos.y = hits[0].hit_rect.top - sprite.hit_rect.h / 2
                # hit from bottom
                elif hits[0].hit_rect.centery < sprite.hit_rect.centery:
                    sprite.pos.y = hits[0].hit_rect.bottom + sprite.hit_rect.h / 2
                    
                sprite.vel.y = 0
                sprite.hit_rect.centery = sprite.pos.y
                return True
        return False

    def update(self):
        """Enemy class method to update.

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
        elif self.game.machinegunpick == True:
            self.drop_rates['Pistol'] = 20
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
        self.pos.x = self.clamp(self.pos.x, cfg.TILESIZE * 2, cfg.WIDTH - cfg.TILESIZE * 2)
        self.pos.y = self.clamp(self.pos.y, cfg.GUI_HEIGHT + cfg.TILESIZE * 2, cfg.HEIGHT - cfg.TILESIZE * 2)

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
        arrr = random.randint(1,100)
        if arrr in range (1,50):
            self.timer += 1
            if self.timer >= self.shoot_time and self.game.player.MoveCheck == True:
                self.state = 'FIRING'
                self.timer = 0
                pos = self.pos + (dist.normalize() * cfg.TILESIZE)
                EnemyPistolBullet(self.game, self, pos)
                self.game.soundLoader.get['laserPistolShot'].play()
                self.state = 'WALKING'
            
              
    def animate(self):
        """Enemy class method to animate.

        """
        now = pygame.time.get_ticks()
        if (self.state == 'WALKING' or self.state == 'SEEK') and self.game.player.MoveCheck == True:
            if now - self.anim_update > 500:
                self.anim_update = now
                self.current_frame = (self.current_frame + 1) % len(
                                      self.walk_frames[LEFT])
                self.image = self.walk_frames[(self.lastdir.x, 
                            self.lastdir.y)][self.current_frame]
                self.angle_to_player = math.degrees(math.atan2(self.pos.x-self.game.player.pos.x,self.pos.y-self.game.player.pos.y))
                self.angleee = self.angle_to_player
                if self.lastdir == pygame.math.Vector2(DOWN):
                    self.angle_to_player = self.angle_to_player + 180
                elif self.lastdir == pygame.math.Vector2(LEFT):
                    self.angle_to_player = self.angle_to_player - 90
                elif self.lastdir == pygame.math.Vector2(RIGHT):
                    self.angle_to_player = self.angle_to_player + 90
                else:
                    self.angle_to_player = self.angle_to_player
                
                self.image = pygame.transform.rotozoom(self.image, self.angle_to_player, 1)
                    
        elif self.state == 'HITSTUN':
            # flicker to indicate damage
            try:
                pass
            except:
                self.state = 'WALKING'
                      
        elif self.state == 'IDLE':
            self.image = self.idle_frames[(self.lastdir.x, self.lastdir.y)][0]
            self.angle_to_player = math.degrees(math.atan2(self.pos.x-self.game.player.pos.x,self.pos.y-self.game.player.pos.y))
            if self.lastdir == pygame.math.Vector2(DOWN):
                self.angle_to_player = self.angle_to_player + 180
            elif self.lastdir == pygame.math.Vector2(LEFT):
               self. angle_to_player = self.angle_to_player - 90
            elif self.lastdir == pygame.math.Vector2(RIGHT):
                self.angle_to_player = self.angle_to_player + 90
            else:
                self.angle_to_player = self.angle_to_player
            self.image = pygame.transform.rotozoom(self.image, self.angle_to_player, 1)
                
        
        elif self.state == 'DYING':
            self.destroy()
            
        elif self.state == 'SWORD':
            self.image = self.game.imageLoader.item_img['sword']

        if self.hit_flash > 0 and self.hit_flash<7:
            self.show_hit_flash()
        elif self.hit_flash >= 7 and self.hit_flash <33:
            self.hit_flash+=1
        elif self.hit_flash >= 33 and self.hit_flash <40:
            self.show_hit_flash()

    def show_hit_flash(self):
        """Enemy class method to flash on taking damage.

        """
        flash_color = (255, 255, 255, self.flash_alpha)
        self.image.fill(flash_color, None, pygame.BLEND_RGBA_MULT)
        if self.hit_flash == 39:
            self.hit_flash = 0
        else:
            self.hit_flash +=1 

    def collide_hit_rect(self, one, two):
        """Enemy class method to check if two objects are colliding.

        """
        return one.hit_rect.colliderect(two.hit_rect)
            
                            
    def collide_with_player(self):
        """Enemy class method to check if enemy is colliding with player.

        """
        keys = pygame.key.get_pressed()
        if self.state == 'DYING':
            return
        
        # detect collision with player
        player = self.game.player
        if self.collide_hit_rect(player, self):
                player.knockback(self, self.kb_time, self.kb_intensity)
                player.hp -= self.damage
            
            
    def knockback(self, other, time, intensity):
        """Enemy class method to knockback enemy.

        Args:
            other (class): the other object with which collision occured and enemy is knocked back.
            time (int) : time it takes to complete the knockback.
            internsity (int): intensity of the knockback.

        """
        if self.state != 'HITSTUN':
            self.vel *= 0
            # calculate vector from other to self
            knockdir = self.pos - other.pos
            if knockdir.length_squared() > 0:
                knockdir = knockdir.normalize()
                self.acc = knockdir * intensity
            else:
                self.acc *= 0
            self.state = 'HITSTUN'
            self.lastimage = self.image.copy()
            self.damage_alpha = iter(cfg.DAMAGE_ALPHA * time)
    
    def destroy(self):
        """Enemy class method to destroy enemy and drop if it has any items.

        """
        self.dropItem()
        self.kill()

            
    def updateData(self):
        """Enemy class method update data.

        """
        self.data['x'] = self.pos.x
        self.data['y'] = self.pos.y
        
    
    def dropItem(self):
        """Enemy class method to drop its item.

        """
        # drop an item based on the weighted probability
        if hasattr(self, 'drop_rates'):
            items = list(self.drop_rates.keys())
            weights = list(self.drop_rates.values())
    
            c = random.choices(items, weights)[0]
             
            try:
                Item.drop(c, self.game, self.pos)
            except:
                print('error. cannot drop item', c)

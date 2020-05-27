import pygame
import math

import Config as cfg

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

UP_RIGHT = (1, -1)
UP_LEFT = (-1, -1)
DOWN_RIGHT = (1, 1)
DOWN_LEFT = (-1, 1)

class Player(pygame.sprite.Sprite):
    """This class contains all settings for the player.

    """
    def __init__(self, game,  pos):
        """__init__ method for Player class

        Args:
            game (Integrate.Game): Integrate.Game class object.
            pos (tuple length 2) : position of the player (x,y).

        """
        self.group = game.all_sprites
        self.layer = 6
        pygame.sprite.Sprite.__init__(self)
        self.group.add(self, layer=self.layer)
        self.game = game
        
        # Machine Gun Walking/Attacking Animation
        if self.game.machinegunpick:
            
            self.image_stripU = self.game.imageLoader.player_img['MwalkU']
            self.image_stripD = self.game.imageLoader.player_img['MwalkD']
            self.image_stripR = self.game.imageLoader.player_img['MwalkR']
            self.image_stripL = self.game.imageLoader.player_img['MwalkL']

            self.AttackU = self.image_stripU[0]
            self.AttackD = self.image_stripD[0]
            self.AttackL = self.image_stripL[0]
            self.AttackR = self.image_stripR[0]
            
        # Pistol Walking/Attacking Animation
        elif self.game.pistolpick:
            self.image_stripU = self.game.imageLoader.player_img['PwalkU']
            self.image_stripD = self.game.imageLoader.player_img['PwalkD']
            self.image_stripR = self.game.imageLoader.player_img['PwalkR']
            self.image_stripL = self.game.imageLoader.player_img['PwalkL']

            self.AttackU = self.image_stripU[0]
            self.AttackD = self.image_stripD[0]
            self.AttackL = self.image_stripL[0]
            self.AttackR = self.image_stripR[0]
        
        # frames when walking
        self.walk_frames = {
                LEFT: [self.image_stripL[0],self.image_stripL[1],self.image_stripL[2],self.image_stripL[3],self.image_stripL[4],self.image_stripL[5]],
                RIGHT: [self.image_stripR[0],self.image_stripR[1],self.image_stripR[2],self.image_stripR[3],self.image_stripR[4],self.image_stripR[5]],
                UP: [self.image_stripU[0],self.image_stripU[1],self.image_stripU[2],self.image_stripU[3],self.image_stripU[4],self.image_stripU[5]],
                DOWN: [self.image_stripD[0],self.image_stripD[1],self.image_stripD[2],self.image_stripD[3],self.image_stripD[4],self.image_stripD[5]]
                }
        
        # frames when attacking
        self.attack_frames = {
                UP: [self.AttackU],
                RIGHT: [self.AttackR],
                LEFT: [self.AttackL],
                DOWN: [self.AttackD]
                }

        # frames when idle
        self.idle_frames = {
                LEFT: [self.image_stripL[0]],
                RIGHT: [self.image_stripR[0]],
                UP: [self.image_stripU[0]],
                DOWN: [self.image_stripD[0]]
                }


        self.image = self.idle_frames[DOWN][0]
        self.sound = self.game.soundLoader
        self.rect = self.image.get_rect()
        self.pos = pygame.math.Vector2(pos)
        self.spawn_pos = pygame.math.Vector2(pos)
        self.rect.center = pos
        self.hit_rect = pygame.Rect((0, 0), (int(10),int(10)))
        self.hit_rect.center = self.pos
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)
        self.dir = pygame.math.Vector2(DOWN)
        self.lastdir = pygame.math.Vector2(DOWN)
        self.friction = pygame.math.Vector2(0, 0)
        self.state = 'IDLE'
        self.hp = 7.0
        self.mana = 0
        self.max_mana = 11.4
        self.dashmana = 0
        self.dashmax_mana = 50
        self.max_hp = cfg.PLAYER_HP_START
        # animation frames for heart refill
        self.heart_refill_frames = 0
        self.target_health = 0     
        self.itemA = None
        self.itemB = None
        self.swordcheck = False
        self.item_using = None

        self.shootcheck = False
        self.anim_update = 0
        self.attack_update = 0
        self.current_frame = 0
        self.MoveCheck = False
        self.Dead = False
        self.manacheck = True
        self.dashcheck = False
        self.ctrlpress = False
        self.dashmanafill = True
        self.sprcolcheck = False
        self.manacount = 0
        self.UpCheck = False
        self.DownCheck = False
        self.RightCheck = False
        self.LeftCheck = False
        self.angle = 0
        self.angle2 = self.angle + 90
        # SHADOW
        self.shadow_surf = pygame.Surface((12, 6)).convert_alpha()
        self.shadow_surf.fill(cfg.TRANS)
        self.shadow_rect = self.shadow_surf.get_rect()
        pygame.draw.ellipse(self.shadow_surf, (0, 0, 0, 180), self.shadow_rect)
        
        self.timeupsound = [self.game.soundLoader.get['TimeUp01'],self.game.soundLoader.get['TimeUp02'],self.game.soundLoader.get['TimeUp03']]
        self.timeupcount = 0

        self.timedownsound = [self.game.soundLoader.get['TimeDown01'],self.game.soundLoader.get['TimeDown02'],self.game.soundLoader.get['TimeDown03']]
        self.timedowncount = 0

    def get_keys(self):
        """Player class method to get player keys pressed and set accordingly.

        """
        if self.state == 'IDLE' or self.state == 'WALKING':
            keys = self.game.keys
            move = keys['DPAD']
            self.acc = move
            if self.acc.length_squared() > 1:
                self.acc.normalize()
            self.acc *= cfg.PLAYER_ACC
            # set image's direction based on key pressed
            if self.LeftCheck:
                self.timedowncount = 0
                self.MoveCheck = True
                self.swordcheck = True
                self.shootcheck = True
                self.dir = pygame.math.Vector2(LEFT)
                self.acc = pygame.math.Vector2(LEFT)
                self.lastdir = pygame.math.Vector2(LEFT)
            if self.RightCheck:
                self.timedowncount = 0
                self.MoveCheck = True
                self.swordcheck = True
                self.shootcheck = True
                self.dir = pygame.math.Vector2(RIGHT)
                self.acc = pygame.math.Vector2(RIGHT)
                self.lastdir = pygame.math.Vector2(RIGHT)
            if self.UpCheck:
                self.timedowncount = 0
                self.MoveCheck = True
                self.swordcheck = True
                self.shootcheck = True
                self.dir = pygame.math.Vector2(UP)
                self.acc = pygame.math.Vector2(UP)
                self.lastdir = pygame.math.Vector2(UP)
            if self.DownCheck:
                self.timedowncount = 0
                self.MoveCheck = True
                self.swordcheck = True
                self.shootcheck = True
                self.dir = pygame.math.Vector2(DOWN)
                self.acc = pygame.math.Vector2(DOWN)
                self.lastdir = pygame.math.Vector2(DOWN)

            if self.UpCheck and self.RightCheck:
                self.acc = pygame.math.Vector2(UP_RIGHT)
            if self.UpCheck and self.LeftCheck:
                self.acc = pygame.math.Vector2(UP_LEFT)
            if self.DownCheck and self.RightCheck:
                self.acc = pygame.math.Vector2(DOWN_RIGHT)
            if self.DownCheck and self.LeftCheck:
                self.acc = pygame.math.Vector2(DOWN_LEFT)
                

            if self.acc.length() < 0.1:
                self.timedowncount += 1
                self.timeupcount = 0
                self.MoveCheck = False
               
                # if velocity is less than the threshold, set state to idle
                self.state = 'IDLE'
            else:
                 # set the state to walking
                 self.state = 'WALKING'
                 
            
            if keys['A']:
                if self.game.machinegunpick:
                    if self.itemA.check == False:
                        self.itemA.use()
                        self.attack_update += 1
                        if self.attack_update > self.itemA.cooldown:
                            self.attack_update = 0
                            self.itemA.reset()
                            self.shootcheck = False
                else:
                    self.itemA.use()
                    self.attack_update += 1
                    if self.attack_update > self.itemA.cooldown:
                        self.attack_update = 0
                        self.itemA.reset()
                        self.shootcheck = False
                
    def update(self):   
        """Player class method to update.

        """ 
        # if machine gun is in player hand then animate machine gun frames
        if self.game.machinegunpick:
            
            self.image_stripU = self.game.imageLoader.player_img['MwalkU']
            self.image_stripD = self.game.imageLoader.player_img['MwalkD']
            self.image_stripR = self.game.imageLoader.player_img['MwalkR']
            self.image_stripL = self.game.imageLoader.player_img['MwalkL']

            self.AttackU = self.image_stripU[0]
            self.AttackD = self.image_stripD[0]
            self.AttackL = self.image_stripL[0]
            self.AttackR = self.image_stripR[0]
            
        # if pistol is in player hand then animate pistol frames
        elif self.game.pistolpick:
            
            self.image_stripU = self.game.imageLoader.player_img['PwalkU']
            self.image_stripD = self.game.imageLoader.player_img['PwalkD']
            self.image_stripR = self.game.imageLoader.player_img['PwalkR']
            self.image_stripL = self.game.imageLoader.player_img['PwalkL']

            self.AttackU = self.image_stripU[0]
            self.AttackD = self.image_stripD[0]
            self.AttackL = self.image_stripL[0]
            self.AttackR = self.image_stripR[0]

        self.walk_frames = {
                LEFT: [self.image_stripL[0],self.image_stripL[1],self.image_stripL[2],self.image_stripL[3],self.image_stripL[4],self.image_stripL[5]],
                RIGHT: [self.image_stripR[0],self.image_stripR[1],self.image_stripR[2],self.image_stripR[3],self.image_stripR[4],self.image_stripR[5]],
                UP: [self.image_stripU[0],self.image_stripU[1],self.image_stripU[2],self.image_stripU[3],self.image_stripU[4],self.image_stripU[5]],
                DOWN: [self.image_stripD[0],self.image_stripD[1],self.image_stripD[2],self.image_stripD[3],self.image_stripD[4],self.image_stripD[5]]
                }
        
        self.attack_frames = {
                UP: [self.AttackU],
                RIGHT: [self.AttackR],
                LEFT: [self.AttackL],
                DOWN: [self.AttackD]
                }

        self.idle_frames = {
                LEFT: [self.image_stripL[0]],
                RIGHT: [self.image_stripR[0]],
                UP: [self.image_stripU[0]],
                DOWN: [self.image_stripD[0]]
                }

        # get player input
        self.get_keys()
        keys = pygame.key.get_pressed()
        # player animations
        self.animate()
        self.rect = self.image.get_rect()
        self.image = self.walk_frames[(self.lastdir.x, self.lastdir.y)][self.current_frame]
        
        # getting mouse input
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.angle = math.degrees(math.atan2(self.pos.x-mouse_x,self.pos.y-mouse_y))
        self.angle2 = self.angle + 90
        self.angle3 = self.angle
        if self.lastdir == pygame.math.Vector2(DOWN):
            self.angle = self.angle + 180
        elif self.lastdir == pygame.math.Vector2(LEFT):
            self.angle = self.angle - 90
        elif self.lastdir == pygame.math.Vector2(RIGHT):
            self.angle = self.angle + 90
        else:
            self.angle = self.angle
        
        self.image = pygame.transform.rotozoom(self.image, self.angle, 1)
        self.rect = self.image.get_rect()
        # add acceleration to velocity
        self.vel += self.acc

        # calculate friction
        self.friction *= 0
        if self.vel.length_squared() > 0:
            self.friction = pygame.math.Vector2(self.vel) * -1
            self.friction = self.friction.normalize()
            self.friction *= cfg.PLAYER_FRICTION

            # apply friction
            self.vel += self.friction
        
        
        # limit velocity
        if self.vel.length_squared() > cfg.PLAYER_MAXSPEED ** 2:
            self.vel.scale_to_length(cfg.PLAYER_MAXSPEED)        
        elif self.vel.length_squared() < 0.01:
            self.vel *= 0
              
        # add velocity to position
        self.pos += self.vel
        if self.state != 'HITSTUN':
            self.acc *= 0
        if self.game.machinegunpick:
            if self.mana > 11:
                self.manacheck = False
            if self.MoveCheck == True:
                self.manacount += 0.5
                if self.shootcheck == False:
                    self.manacheck = True
                    self.manacount = 0
                
            if self.manacount == 20:
                self.manacheck = False
                self.manacount = 0
            
            if self.manacheck == False:
                if self.MoveCheck:
                    if self.mana > 0:
                        self.mana -= 0.2
                        self.manacount = 0
                    if self.mana < 0.2:
                        self.itemA.check = False
                        self.manacheck = True
        
            
        self.hitbox = self.rect.inflate(-70,-70)
        self.rect.center = self.pos
        self.hitbox.center = self.pos
        
        self.hit_rect.centerx = self.pos.x
        a = self.collide_with_walls(self, self.game.walls, 'x')
        
        self.hit_rect.centery = self.pos.y
        b = self.collide_with_walls(self, self.game.walls, 'y')
                
        self.hitbox.midbottom = self.hit_rect.midbottom
        self.hitbox.center = self.hit_rect.center
        self.hitbox.bottom = self.hit_rect.bottom + 1
        
        self.fillHearts()
        # restrain items between 0 and max
        self.hp = max(0, min(self.hp, self.max_hp))
        if self.hp <= 0.8:
            self.destroy()


    def collide_hit_rect(self, one, two):
        """Player class method to check if two objects are colliding.

        """
        return one.hit_rect.colliderect(two.hit_rect)

    def collide_with_walls(self, sprite, group, dir_):
        """Player class method to detect collision with the walls.

        Args:
            sprite (Player.Player): Player object.
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
        
    
    def animate(self):
        """Player class method to animate.

        """
        now = pygame.time.get_ticks()

        if self.state == 'WALKING':
            if now - self.anim_update > 200:
                self.anim_update = now
                self.current_frame = (self.current_frame + 1) % len(
                                      self.walk_frames[LEFT])
                
                self.image = self.walk_frames[(self.lastdir.x, 
                                self.lastdir.y)][self.current_frame]
        
        elif self.state == 'IDLE':
            cfg.PLAYER_FRICTION = 0.5
            self.image = self.idle_frames[(self.lastdir.x, self.lastdir.y)][0]

                    
        elif self.state == 'HITSTUN':
            self.image = self.idle_frames[(self.lastdir.x, self.lastdir.y)][0]
            # flicker to indicate damage
            try:
                alpha = next(self.damage_alpha)
                self.image = self.lastimage.copy()
                self.image.fill((255, 255, 255, alpha), 
                                special_flags=pygame.BLEND_RGBA_MULT)
            except:
                self.state = 'IDLE'
           
    
    def stun(self, time):
        """Player class method to stun player.

        Args:
            time (int) : time for which player will be stun.

        """
        self.vel *= 0
        self.acc *= 0
        self.state = 'HITSTUN'
        self.lastimage = self.image.copy()
        self.damage_alpha = iter(cfg.DAMAGE_ALPHA * time)

    
    def knockback(self, other, time, intensity):
        """Player class method to knockback player.

        Args:
            other (class): the other object with which collision occured and player is knocked back.
            time (int) : time it takes to complete the knockback.
            internsity (int): intensity of the knockback.

        """
        if self.state != 'HITSTUN':
            self.vel = pygame.math.Vector2(0, 0)
            # calculate vector from other to self
            knockdir = self.pos - other.pos
            cfg.PLAYER_FRICTION = 0.1
            if knockdir.length_squared() > 0:
                knockdir = knockdir.normalize()
                self.acc = knockdir * intensity
                self.lastimage = self.image.copy()
                self.damage_alpha = iter(cfg.DAMAGE_ALPHA * time)
                self.state = 'HITSTUN'
                
                
    def fillHearts(self):
        """Player class method to fill hearts if pickup.

        """
        if self.hp < self.target_health:
            self.heart_refill_frames += 1
            if self.heart_refill_frames > cfg.FPS // 20:
                self.hp += 0.25
                self.heart_refill_frames = 0      
        else:
            self.target_health = 0
    
    def draw_before(self):
        """Player class method to draw its shadow.

        """

        # draw a shadow
        self.shadow_rect.centerx = self.hit_rect.centerx
        self.shadow_rect.bottom = self.hit_rect.bottom + 4
        self.game.screen.blit(self.shadow_surf, self.shadow_rect)
        
    def destroy(self):
        """Player class method to kill player.

        """
        self.kill()
        self.Dead = True
        

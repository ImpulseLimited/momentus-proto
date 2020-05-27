import pygame

import Config as cfg
from objects.Object import Object

class Explosivecrate(Object):
    """This class is derived from Object class and is for Explosive crates.

    """
    def __init__(self, game, pos, size, **kwargs):
        """__init__ method for Explosivecrate class

        Args:
            game (<class 'Integrate.Game'>): Integrate.Game class object.
            pos (tuple length 2) : position of the player (x,y).
            size (int) : size of the object.

        """
        super().__init__(game, pos, size)
        self.image = self.game.imageLoader.solid_img['crate']
        self.size = self.image.get_size()
        self.rect = pygame.Rect(self.pos, self.size)
        self.hit_rect = pygame.Rect((0, 0), (int(36),int(36)))
        self.hit_rect.center = self.pos

        offset = pygame.math.Vector2(4, 4)
        self.interact_rect = self.rect.inflate(offset)

        self.interact_rect.center = self.hit_rect.center
        
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)
        
        self.push_timer = 0

    def collide_hit_rect(self, one, two):
        """Explosivecrate class methid to detect collision of two objects.

        """
        return one.hit_rect.colliderect(two.hit_rect)
    
    
    def collide_with_walls_topleft(self, sprite, group, dir_):
        """Explosivecrate class methid to detect collision with walls

        Args:
            sprite (Explosivecrate.Explosivecrate): Explosive crate object.
            group (pygame.sprite.LayeredUpdates) : sprite layers.
            dir_ (str) : direction.

        """

        if dir_ == 'x':
            hits = pygame.sprite.spritecollide(sprite, group, False, self.collide_hit_rect)
            if hits:
                # hit from left
                if hits[0].hit_rect.centerx > sprite.hit_rect.centerx:
                    sprite.pos.x = hits[0].hit_rect.left - sprite.hit_rect.w
                # hit from right
                elif hits[0].hit_rect.centerx < sprite.hit_rect.centerx:
                    sprite.pos.x = hits[0].hit_rect.right
                                
                sprite.vel.x = 0
                sprite.hit_rect.left = sprite.pos.x
                return True
                
        elif dir_ == 'y':
            hits = pygame.sprite.spritecollide(sprite, group, False, self.collide_hit_rect)
            if hits:
                # hit from top
                if hits[0].hit_rect.centery > sprite.hit_rect.centery:
                    sprite.pos.y = hits[0].hit_rect.top - sprite.hit_rect.h
                # hit from bottom
                elif hits[0].hit_rect.centery < sprite.hit_rect.centery:
                    sprite.pos.y = hits[0].hit_rect.bottom
                    
                sprite.vel.y = 0
                sprite.hit_rect.top = sprite.pos.y
                return True
        return False


    def update(self):
        """Explosivecrate class method to update the crate.

        """
        player = self.game.player
        if self.interact_rect.colliderect(player.hit_rect):
            # if player pushes, move in that direction
            self.push_timer += 1
            if self.push_timer > 0.8 * cfg.FPS:
                self.acc = pygame.math.Vector2(player.dir)
                
        else:
            self.vel *= 0
            self.push_timer = 0
        
        self.vel += self.acc  
        self.acc *= 0
        self.pos += self.vel
        self.rect.center = self.pos
        self.hit_rect.center = self.pos
        
        # collision with walls
        self.hit_rect.left = self.pos.x
        self.collide_with_walls_topleft(self, self.game.walls, 'x')
        self.hit_rect.right = self.rect.right
        self.hit_rect.top = self.pos.y
        self.collide_with_walls_topleft(self, self.game.walls, 'y')
        self.hit_rect.bottom = self.rect.bottom
        self.rect.center = self.hit_rect.center
        
        self.interact_rect.center = self.hit_rect.center
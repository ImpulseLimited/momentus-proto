import pygame

from effects.Effect import Effect

class Explosion(Effect):
    """This class is derived from Effect class and 
       contains settings for a displaying an animation effect that is self destroyed.

    """
    def __init__(self, game,  pos, images, delay, **kwargs):
        """__init__ method for Explosion class

        Args:
            game (<class 'Integrate.Game'>): Integrate.Game class object.
            pos (tuple length 2): position of the player (x,y).
            images (<list>): image list from sprites.
            delay (int): delay between animation images

        """
        super().__init__(game,  pos, images, delay)
        self.damage = kwargs['damage']
        if 'hit_rect' in kwargs:
            # define custom hit rect
            self.hit_rect = kwargs['hit_rect']
        else:    
            self.hit_rect = self.image.get_rect()
        
        self.hit_rect.center = self.rect.center
        if 'sound' in kwargs:
            kwargs['sound'].play()

    def collide_hit_rect(self, one, two):
        """Explosion class method to check if two objects are colliding.

        """
        return one.hit_rect.colliderect(two.hit_rect)
            
            
    def update(self):
        """Explosion class method to update the effect.
           Overriding the base class method.

        """
        self.rect.center = self.pos
        now = pygame.time.get_ticks()  
        # destroy animation if images end    
        if self.frame == len(self.images):
            self.kill()
            self.end = True

        # display next image
        if now - self.timer > self.delay and self.end == False:
            self.timer = now
            self.image = self.images[self.frame]
            self.frame = self.frame + 1
            
        # if explosion hits player then cause damage to player
        player = self.game.player
        if self.collide_hit_rect(player, self):
            if (player.state != 'HITSTUN'):
                player.knockback(self, 1, 0.5)
                player.hp -= self.damage
                
        # if explosion hits enemies then cause damage to enemies
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False, self.collide_hit_rect)
        if hits:
            for enemy in hits:
                if enemy.state != 'HITSTUN':
                    enemy.hp -= self.damage
                    enemy.knockback(self, 1, 0.5)
                    
  
    
                
        

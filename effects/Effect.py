import pygame

class Effect(pygame.sprite.Sprite):
    """This class is base class for effects.
       Animation is played from images list and destroyed itself.

    """
    def __init__(self, game,  pos, images, delay):
        """__init__ method for Explosion class

        Args:
            game (<class 'Integrate.Game'>): Integrate.Game class object.
            pos (tuple length 2): position of the player (x,y).
            images (<list>): image list from sprites.
            delay (int): delay between animation images

        """
        self.group = game.all_sprites
        pygame.sprite.Sprite.__init__(self)
        self.layer = 0
        self.group.add(self, layer=self.layer)
        self.game = game

        self.timer = 0
        self.frame = 0
        self.images = images
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.game = game
        self.pos = pos
        self.delay = delay
        self.end = False
        
        
    def update(self):
        """Effect class method to update the effect.

        """
        self.rect.center = self.pos
        now = pygame.time.get_ticks()      
        if self.frame == len(self.images):
            self.kill()
            self.end = True
        if now - self.timer > self.delay:
            self.timer = now
            # print("Frame: " +str(self.frame))
            # print("Images: " + str(self.images))
            # print("Images and Frames: " + str(self.images[self.frame]))
            self.image = self.images[self.frame]
            self.frame = self.frame + 1
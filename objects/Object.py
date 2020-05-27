import pygame

class Object(pygame.sprite.Sprite):
    """This class is for all objects.

    """
    def __init__(self, game, pos, size):
        """__init__ method for Object class

        Args:
            game (<class 'Integrate.Game'>): Integrate.Game class object.
            pos (tuple length 2) : position of the player (x,y).
            size (int) : size of the object.

        """
        self.game = game
        self.pos = pygame.math.Vector2(pos)
        self.size = size
        self.groups = self.game.walls, self.game.all_sprites
        self.layer = 1
        pygame.sprite.Sprite.__init__(self)
        for g in self.groups:
            g.add(self, layer=self.layer)
        self.rect = pygame.Rect(self.pos, self.size)
        self.hit_rect = self.rect.copy()

    def update(self):
        """Object class method to be updated by objects if needed.

        """
        pass
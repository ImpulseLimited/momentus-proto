import pygame

from objects.Object import Object

class Wall(Object):
    """This class is derived from Object class and is for Wall objects.

    """
    def __init__(self, game, pos, size, **kwargs):
        """__init__ method for Wall class

        Args:
            game (<class 'Integrate.Game'>): Integrate.Game class object.
            pos (tuple length 2) : position of the player (x,y).
            size (int) : size of the object.

        """
        super().__init__(game, pos, size)
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        
        

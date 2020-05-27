import pygame

from objects.Object import Object

class Door(Object):
    """This class is derived from Object class and is for doors.
       It disappears if the player achieves a goal.
    
    """
    def __init__(self, game, pos,**kwargs):
        """__init__ method for Door class

        Args:
            game (<class 'Integrate.Game'>): Integrate.Game class object.
            pos (tuple length 2) : position of the player (x,y).

        """
        super().__init__(game, pos, size=(0, 0))
        self.image = self.game.imageLoader.door_image_dict[kwargs['direction']]
        self.size = self.image.get_size()
        
        self.rect = pygame.Rect(self.pos, self.size)
        self.hit_rect = self.rect.copy()
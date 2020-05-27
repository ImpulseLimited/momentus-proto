
from objects.Object import Object  

class Block(Object):
    """This class is derived from Object class and is for blocks.

    """ 
    def __init__(self, game, pos, size, **kwargs):
        """__init__ method for Block class

        Args:
            game (<class 'Integrate.Game'>): Integrate.Game class object.
            pos (tuple length 2) : position of the player (x,y).
            size (int) : size of the object.

        """
        super().__init__(game, pos, size)
        self.image = self.game.imageLoader.solid_img['block']
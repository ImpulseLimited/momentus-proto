import pygame

class Weapon(pygame.sprite.Sprite):
    """This class is base class for all attack items. All types of attack items derive this class.

    """
    def __init__(self, game, player):
        """__init__ method for Weapon class

        Args:
            game (<class 'Integrate.Game'>): Integrate.Game class object.
            player (<class 'Player.Player'>): Player.Player class object

        """
        self.group = game.all_sprites
        self.layer = player.layer
        pygame.sprite.Sprite.__init__(self)
        self.player = player
        self.game = game
        self.image = self.game.imageLoader.item_img[self.type].copy()
        self.cooldown = 20
        
    def update(self):
        """Weapon class method to update the item.

        """
        # delete sprite if fired
        if not self.player.state == 'USE_A':
            self.game.all_sprites.remove(self)
            
    
    def use(self):
        """Weapon class method to use the item.

        """
        self.image = self.game.imageLoader.item_img[self.type].copy()
        self.group.add(self, layer=self.layer)
    
        self.dir = self.player.lastdir
        self.angle = 0
        self.angle += self.player.angle2
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        
        self.hit_rect.center = self.rect.center
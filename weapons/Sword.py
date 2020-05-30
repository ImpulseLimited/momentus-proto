import pygame

from weapons.Weapon import Weapon

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Sword(Weapon):
    """This class is derived from Weapon class and 
       contains settings for a sword usage by a player.

    """
    def __init__(self, game, player):
        """__init__ method for Sword class

        Args:
            game (<class 'Integrate.Game'>): Integrate.Game class object.
            player (<class 'Player.Player'>): Player.Player class object

        """
        self.type = 'sword'
        super().__init__(game, player)
        self.cooldown = 20
        img = self.game.imageLoader.item_anims[self.type]
        img2 = self.game.imageLoader.item_anims['swordD']
        img3 = self.game.imageLoader.item_anims['swordL']
        img4 = self.game.imageLoader.item_anims['swordR']
        self.animations = {
                UP: img,
                DOWN: img2,
                LEFT: img3,
                RIGHT: img4
                }
        
        self.anim_update = 0
        self.current_frame = 0
        self.anim_speed = 80
        self.fired = False
        self.hit_rect = pygame.Rect((0, 0), (int(50),int(50)))
        self.damage = 0.2
        self.kb_time = 1
        self.kb_intensity = 0.5
        
    def collide_hit_rect(self, one, two):
        """Sword class method to check if two objects are colliding.

        """
        return one.hit_rect.colliderect(two.hit_rect)

    def update(self):
        """Sword class method to update.

        """
        if not self.player.state == 'SWORD':
            self.game.all_sprites.remove(self)

        checkplayer = self.game.player
        if collide_hit_rect(checkplayer, self):
            checkplayer.knockback(self, self.kb_time, self.kb_intensity)
            checkplayer.hp -= self.damage

    def use(self):
        """Sword class method to use the sword. 
           Overriding base class method

        """
        self.group.add(self, layer=self.layer)
        
        self.pos = self.player.pos
        self.dir = self.player.lastdir
        anim = self.animations[DOWN]
        self.image = anim[self.current_frame]
        self.image = pygame.transform.rotozoom(self.image, self.player.angle_to_player, 1)
        self.rect = self.image.get_rect()
        
        now = pygame.time.get_ticks()
        if now - self.anim_update > self.anim_speed:
            self.anim_update = now
            self.current_frame = (self.current_frame + 1) % len(anim)
        
        self.rect.center = self.pos
        self.hit_rect.center = self.rect.center
        
        if not self.fired:
            # play slash sound      
            self.game.soundLoader.get['swordSlash'].play()
            self.fired = True
            
    def reset(self):
        """Sword class method to reset the sword. 

        """
        self.fired = False
        self.current_frame = 0
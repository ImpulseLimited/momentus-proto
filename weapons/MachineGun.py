from weapons.Weapon import Weapon
from bullets.PlayerMachinegunBullet import PlayerMachinegunBullet

class MachineGun(Weapon):
    """This class is derived from Weapon class and 
       contains settings for a machine gun usage by a player.

    """
    def __init__(self, game, player):
        """__init__ method for MachineGun class

        Args:
            game (<class 'Integrate.Game'>): Integrate.Game class object.
            player (<class 'Player.Player'>): Player.Player class object

        """
        self.type = 'Mbullet'
        super().__init__(game, player)
        self.fired = False
        self.cooldown = 2
        self.check = False
        
        
    def use(self):
        """MachineGun class method to use the pistol. 
           Overriding base class method

        """
        super().use()
        if self.player.mana > 11:
                self.check = True
        if not self.fired and self.player.shootcheck == True:
            if self.player.mana < 12 and self.check == False:
                self.lastdir = self.player.lastdir
                PlayerMachinegunBullet(self.game, self, self.rect.center)
                self.player.mana += 1
                self.game.soundLoader.get['magic1'].play()
                self.fired = True

                
    def reset(self):
        """MachineGun class method to reset the pistol. 

        """
        self.fired = False
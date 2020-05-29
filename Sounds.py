import pygame
import os

import Config as cfg

class Sound:
    """This class contains all settings related to sounds.

    """
    
    def get_sound(self, filename, volume):
        """Sound class method to extract file path of sound. 

        Args:
            filename (str): filename of sound.
            volume (float): volume value.

        """
        sound = pygame.mixer.Sound(os.path.join(cfg.SOUND_FOLDER, filename))
        sound.set_volume(volume * cfg.SFX_VOL)

        return sound
        
    def load(self):     
        """Sound class method to load sound. 

        """ 
        self.get = {
                'swordSlash': self.get_sound('sword_slash.wav', 0.4),
                'heart': self.get_sound('heart.wav', 1),
                'explosiveTank': self.get_sound('gas_tank_explosion.wav', 1),
                'roomLocked': self.get_sound('room_locked.wav', 1),
                'machineGunShot': self.get_sound('machine_gun_shot.wav', 0.8),
                'roomCleared': self.get_sound('room_cleared.wav', 1),
                'laserPistolShot': self.get_sound('laser_pistol_shot.wav', 0.6),
                'TimeDown01': self.get_sound('Time_Sweep_Down_01.wav', 1),
                'TimeDown02': self.get_sound('Time_Sweep_Down_02.wav', 1),
                'TimeDown03': self.get_sound('Time_Sweep_Down_03.wav', 1),
                'TimeUp01': self.get_sound('Time_Sweep_Up_01.wav', 1),
                'TimeUp02': self.get_sound('Time_Sweep_Up_02.wav', 1),
                'TimeUp03': self.get_sound('Time_Sweep_Up_03.wav', 1)
            }
        
        
        
        
        

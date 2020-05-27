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
                'slash': self.get_sound('slash.wav', 0.4),
                'heart': self.get_sound('heart.wav', 1),
                'bomb': self.get_sound('sfx_exp_various1.wav', 1),
                'shut': self.get_sound('sfx_exp_various4.wav', 1),
                'magic1': self.get_sound('sfx_sounds_impact9.wav', 0.8),
                'magic2': self.get_sound('sfx_exp_odd1.wav', 0.8),
                'fanfare1': self.get_sound('sfx_sounds_fanfare3.wav', 1),
                'Laser01': self.get_sound('Laser_Short_01.wav', 0.6),
                'Laser02': self.get_sound('Laser_Short_02.wav', 0.6),
                'Laser03': self.get_sound('Laser_Short_03.wav', 0.7),
                'Laser04': self.get_sound('Laser_Short_04.wav', 0.8),
                'Laser05': self.get_sound('Laser_Short_05.wav', 1),
                'TimeDown01': self.get_sound('Time_Sweep_Down_01.wav', 1),
                'TimeDown02': self.get_sound('Time_Sweep_Down_02.wav', 1),
                'TimeDown03': self.get_sound('Time_Sweep_Down_03.wav', 1),
                'TimeUp01': self.get_sound('Time_Sweep_Up_01.wav', 1),
                'TimeUp02': self.get_sound('Time_Sweep_Up_02.wav', 1),
                'TimeUp03': self.get_sound('Time_Sweep_Up_03.wav', 1)
            }
        
        
        
        
        

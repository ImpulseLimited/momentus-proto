import pygame

import Config as cfg
from enemies.Enemy import Enemy


UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
        
class MiniBoss(Enemy):
    """This class is derived from Enemy class and 
       contains settings for a MiniBoss.

    """
    def __init__(self, game, pos, *args, **kwargs):
        """__init__ method for MiniBoss class

        Args:
            game (Integrate.Game): Integrate.Game class object.
            pos (tuple length 2) : position of the player (x,y).

        """
        self.name = 'MiniBoss'
        self.image_strip = game.imageLoader.enemy_img[self.name]
        self.walk_frames = {
            UP: [self.image_strip[0][0],self.image_strip[0][1],self.image_strip[0][2],self.image_strip[0][3],self.image_strip[0][4],self.image_strip[0][5]],
            DOWN: [self.image_strip[1][0],self.image_strip[1][1],self.image_strip[1][2],self.image_strip[1][3],self.image_strip[1][4],self.image_strip[1][5]],
            LEFT: [self.image_strip[2][0],self.image_strip[2][1],self.image_strip[2][2],self.image_strip[2][3],self.image_strip[2][4],self.image_strip[2][5]],
            RIGHT: [self.image_strip[3][0],self.image_strip[3][1],self.image_strip[3][2],self.image_strip[3][3], self.image_strip[3][4],self.image_strip[3][5]]}
        self.idle_frames = {
            UP: [self.image_strip[0][0]],
            DOWN: [self.image_strip[1][0]], 
            LEFT: [self.image_strip[2][0]],
            RIGHT: [self.image_strip[3][0]]}
        
        self.hit_rect = pygame.Rect(0, 0, int(30), int(30))
        super().__init__(game, pos)
        self.image = self.idle_frames[UP][0]
        self.state = 'WALKING'
        self.kb_time = 1
        self.kb_intensity = 1
        self.hp = 6
        self.maxSpeed = 0.8
        self.anim_speed = 300
        self.drop_rates = {'none':100,'Pistol': 20}
        self.timer = 0
        self.shoot_time = 1.5* cfg.FPS
        self.stun_timer = 0
        
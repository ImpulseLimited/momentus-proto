import pygame as pg
import pickle
from os import path
import traceback
from random import choice, choices, randint
import sys
import json
import math

import functions as fn
import settings as st
import cutscenes as cs
from Button import Button
vec = pg.math.Vector2

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

UP_RIGHT = (1, -1)
UP_LEFT = (-1, -1)
DOWN_RIGHT = (1, 1)
DOWN_LEFT = (-1, 1)

vecNull = vec(0, 0)
vecR = vec(RIGHT)
vecL = vec(LEFT)

PLACEHOLDER_IMG = pg.Surface((st.TILESIZE, st.TILESIZE))
PLACEHOLDER_IMG.fill(st.RED)

# load a dictionary of sprites.py namespace
module_dict = sys.modules[__name__].__dict__
  
def create(game, data, offset=vec(0, st.GUI_HEIGHT)):
    d = data
    g = game
    # takes a dictionary of sprite properties
    name = d['name'].capitalize()
    #instantiate the sprite 
    spr = module_dict[name](g, (d['x'] + offset.x, d['y'] + offset.y),
                                (d['width'], d['height']))
    for key, value in d.items():
        try:
            setattr(spr, key, value)
        except:
            print('cant set value of {0} for {1}'.format(key, spr))
    
    if hasattr(spr, 'on_create'):
        # do initialisation stuff after ___init__()
        spr.on_create()
    
    spr.data = d
                
class ImageLoader:
    '''
    A class that loads all images at the start of the game
    '''
    def __init__(self, game):
        self.game = game
        
        self.tileset_names = ['new.png']

    
    def load(self):
        
        PistolMove = fn.img_list_from_strip('Pistol-moving.png', 195, 195, 0, 6, 100)
        
        PistolLeft = []
        for i in PistolMove:
            a = pg.transform.rotate(i,90)
            PistolLeft.append(a)
        PistolRight = []
        for i in PistolMove:
            a = pg.transform.rotate(i,-90)
            PistolRight.append(a)
        PistolDown = []
        for i in PistolMove:
            a = pg.transform.rotate(i,-180)
            PistolDown.append(a)

        MachineGunMove = fn.img_list_from_strip('Machine-gun-moving.png', 195, 195, 0, 6, 100)
        
        MachineGunLeft = []
        for i in MachineGunMove:
            a = pg.transform.rotate(i,90)
            MachineGunLeft.append(a)
        MachineGunRight = []
        for i in MachineGunMove:
            a = pg.transform.rotate(i,-90)
            MachineGunRight.append(a)
        MachineGunDown = []
        for i in MachineGunMove:
            a = pg.transform.rotate(i,-180)
            MachineGunDown.append(a)
        self.CursorMain = pg.image.load(path.join(st.IMAGE_FOLDER,'Cursor.png'))
        self.CursorMain1 = pg.transform.scale(self.CursorMain, (40, 40))
        self.cursor = []
        Cursor1 = pg.image.load(path.join(st.IMAGE_FOLDER,'Cursor_1.png'))
        Cursor1 = pg.transform.scale(Cursor1, (40, 40))
        self.cursor.append(Cursor1)
        
        Cursor2 = pg.image.load(path.join(st.IMAGE_FOLDER,'Cursor_2.png'))
        Cursor2 = pg.transform.scale(Cursor2, (40, 40))
        self.cursor.append(Cursor2)
        
        Cursor3 = pg.image.load(path.join(st.IMAGE_FOLDER,'Cursor_3.png'))
        Cursor3 = pg.transform.scale(Cursor3, (40, 40))
        self.cursor.append(Cursor3)
        
        Cursor4 = pg.image.load(path.join(st.IMAGE_FOLDER,'Cursor_4.png'))
        Cursor4 = pg.transform.scale(Cursor4, (40, 40))
        self.cursor.append(Cursor4)
        
        Cursor5 = pg.image.load(path.join(st.IMAGE_FOLDER,'Cursor_5.png'))
        Cursor5 = pg.transform.scale(Cursor5, (40, 40))
        self.cursor.append(Cursor5)
        
        Cursor6 = pg.image.load(path.join(st.IMAGE_FOLDER,'Cursor_6.png'))
        Cursor6 = pg.transform.scale(Cursor6, (40, 40))
        self.cursor.append(Cursor6)
        
        Cursor7 = pg.image.load(path.join(st.IMAGE_FOLDER,'Cursor_7.png'))
        Cursor7 = pg.transform.scale(Cursor7, (40, 40))
        self.cursor.append(Cursor7)
        
        Cursor8 = pg.image.load(path.join(st.IMAGE_FOLDER,'Cursor_8.png'))
        Cursor8 = pg.transform.scale(Cursor8, (40, 40))
        self.cursor.append(Cursor8)
        
        self.player_img = {
            'PwalkU': PistolMove,
            'PwalkD': PistolDown,
            'PwalkL': PistolLeft,
            'PwalkR': PistolRight,

            'MwalkU': MachineGunMove,
            'MwalkD': MachineGunDown,
            'MwalkL': MachineGunLeft,
            'MwalkR': MachineGunRight
            }
        
        self.tileset_dict = {key: fn.tileImage(key, 40, 40) 
                                for key in self.tileset_names}
        # set the image for testing
        self.tileset_image = fn.loadImage(self.tileset_names[0], 1)
        self.solid_img ={
            'block': pg.image.load(path.join(st.IMAGE_FOLDER,'Brick1.png')),
            'crate': pg.image.load(path.join(st.IMAGE_FOLDER,'Explosive.png')),
            }

        Door1 = pg.image.load(path.join(st.IMAGE_FOLDER,'4Brick.png'))
        Door2 = pg.image.load(path.join(st.IMAGE_FOLDER,'3Brick.png'))
        
        
        
        self.door_image_dict = {
                'W': Door2,
                'N': Door1,
                'E': Door2,
                'S': Door1
                }
    
        self.WarnSign = pg.image.load(path.join(st.IMAGE_FOLDER,'warning.png'))
        self.WarnSign = pg.transform.scale(self.WarnSign, (100, 20))

        self.WarnSign2 = pg.image.load(path.join(st.IMAGE_FOLDER,'WarnSign3.png'))
        self.WarnSign2 = pg.transform.scale(self.WarnSign2, (100, 20))
        self.room_img = fn.img_list_from_strip('minimap_strip_7x5.png', 7, 5, 0, 20)
        
        self.room_image_dict = {
                                'empty': self.room_img[0],
                                'NSWE': self.room_img[1],
                                'N': self.room_img[3],
                                'E': self.room_img[4],
                                'S': self.room_img[5],
                                'W': self.room_img[6],
                                'NE': self.room_img[7],
                                'NS': self.room_img[8],
                                'NW': self.room_img[9],
                                'SE': self.room_img[10],
                                'WE': self.room_img[11],
                                'SW': self.room_img[12],
                                'NWE': self.room_img[13],
                                'NES': self.room_img[14],
                                'SWE': self.room_img[15],
                                'NWS': self.room_img[16]
                                }

        #Boss
        boss_strip = pg.image.load(path.join(st.IMAGE_FOLDER,'Boss01U.png'))
        boss_strip = pg.transform.scale(boss_strip, (40, 40))
        boss_stripD = pg.image.load(path.join(st.IMAGE_FOLDER,'Boss01D.png'))
        boss_stripD = pg.transform.scale(boss_stripD, (40, 40))
        boss_stripL = pg.image.load(path.join(st.IMAGE_FOLDER,'Boss01L.png'))
        boss_stripL = pg.transform.scale(boss_stripL, (40, 40))
        boss_stripR = pg.image.load(path.join(st.IMAGE_FOLDER,'Boss01R.png'))
        boss_stripR = pg.transform.scale(boss_stripR, (40, 40))

        #miniBoss
        Mboss_strip = pg.image.load(path.join(st.IMAGE_FOLDER,'Enemy1U.png'))
        Mboss_strip = pg.transform.scale(Mboss_strip, (40, 40))
        Mboss_stripD = pg.image.load(path.join(st.IMAGE_FOLDER,'Enemy1D.png'))
        Mboss_stripD = pg.transform.scale(Mboss_stripD, (40, 40))
        Mboss_stripL = pg.image.load(path.join(st.IMAGE_FOLDER,'Enemy1L.png'))
        Mboss_stripL = pg.transform.scale(Mboss_stripL, (40, 40))
        Mboss_stripR = pg.image.load(path.join(st.IMAGE_FOLDER,'Enemy1R.png'))
        Mboss_stripR = pg.transform.scale(Mboss_stripR, (40, 40))

        #enemy
        Enemy_strip = pg.image.load(path.join(st.IMAGE_FOLDER,'Enemy2U.png'))
        Enemy_strip = pg.transform.scale(Enemy_strip, (40, 40))
        Enemy_stripD = pg.image.load(path.join(st.IMAGE_FOLDER,'Enemy2D.png'))
        Enemy_stripD = pg.transform.scale(Enemy_stripD, (40, 40))
        Enemy_stripL = pg.image.load(path.join(st.IMAGE_FOLDER,'Enemy2L.png'))
        Enemy_stripL = pg.transform.scale(Enemy_stripL, (40, 40))
        Enemy_stripR = pg.image.load(path.join(st.IMAGE_FOLDER,'Enemy2R.png'))
        Enemy_stripR = pg.transform.scale(Enemy_stripR, (40, 40))

        Pistol_Enemy_UP = fn.img_list_from_strip('enemy pistol walk.png', 120, 120, 0, 6, 60)
        
        Pistol_Enemy_Left = []
        for i in Pistol_Enemy_UP:
            a = pg.transform.rotate(i,90)
            Pistol_Enemy_Left.append(a)
            
        Pistol_Enemy_Right = []
        for i in Pistol_Enemy_UP:
            a = pg.transform.rotate(i,-90)
            Pistol_Enemy_Right.append(a)
            
        Pistol_Enemy_Down = []
        for i in Pistol_Enemy_UP:
            a = pg.transform.rotate(i,-180)
            Pistol_Enemy_Down.append(a)

        Machine_Enemy_UP = fn.img_list_from_strip('enemy machinegun walk.png', 120, 120, 0, 6, 60)
        
        Machine_Enemy_Left = []
        for i in Machine_Enemy_UP:
            a = pg.transform.rotate(i,90)
            Machine_Enemy_Left.append(a)
            
        Machine_Enemy_Right = []
        for i in Machine_Enemy_UP:
            a = pg.transform.rotate(i,-90)
            Machine_Enemy_Right.append(a)
            
        Machine_Enemy_Down = []
        for i in Machine_Enemy_UP:
            a = pg.transform.rotate(i,-180)
            Machine_Enemy_Down.append(a)

        Sword_Enemy_UP = fn.img_list_from_strip('enemy sword run.png', 150, 150, 0, 4, 80)
        
        Sword_Enemy_Left = []
        for i in Sword_Enemy_UP:
            a = pg.transform.rotate(i,90)
            Sword_Enemy_Left.append(a)
            
        Sword_Enemy_Right = []
        for i in Sword_Enemy_UP:
            a = pg.transform.rotate(i,-90)
            Sword_Enemy_Right.append(a)
            
        Sword_Enemy_Down = []
        for i in Sword_Enemy_UP:
            a = pg.transform.rotate(i,-180)
            Sword_Enemy_Down.append(a)

        SwordSwing = fn.img_list_from_strip('enemy sword attack.png', 150, 150, 0, 8, 80)
        SwordSwingLeft = []
        for i in SwordSwing:
            a = pg.transform.rotate(i,90)
            SwordSwingLeft.append(a)
        SwordSwingRight = []
        for i in SwordSwing:
            a = pg.transform.rotate(i,-90)
            SwordSwingRight.append(a)
        SwordSwingDown = []
        for i in SwordSwing:
            a = pg.transform.rotate(i,-180)
            SwordSwingDown.append(a)
            
        self.enemy_img = {
           
            'Boss': [Machine_Enemy_UP, Machine_Enemy_Down, Machine_Enemy_Left, Machine_Enemy_Right],
        
            'Mboss':[Pistol_Enemy_UP, Pistol_Enemy_Down, Pistol_Enemy_Left, Pistol_Enemy_Right],
    
            'Enemy': [Sword_Enemy_UP, Sword_Enemy_Down, Sword_Enemy_Left, Sword_Enemy_Right]
        }

        PlasmaShot = pg.image.load(path.join(st.IMAGE_FOLDER,'plasmaShot.png'))
        BulletRed = pg.image.load(path.join(st.IMAGE_FOLDER,'bullet red.png'))
        BlueShot = pg.image.load(path.join(st.IMAGE_FOLDER,'bullet blue.png'))
        BlueShot = pg.transform.scale(BlueShot, (20, 20))
        BulletRed = pg.transform.scale(BulletRed, (20, 20))
        LaserRed = pg.image.load(path.join(st.IMAGE_FOLDER,'Laser red.png'))
        LaserBlue = pg.image.load(path.join(st.IMAGE_FOLDER,'Laser blue.png'))
        LaserBlue = pg.transform.scale(LaserBlue, (40, 40))
        LaserRed = pg.transform.scale(LaserRed, (40, 40))
        
        MACHINEShot = pg.image.load(path.join(st.IMAGE_FOLDER,'bullet blue.png'))
        EnemyBullet = pg.transform.scale(PlasmaShot, (5, 5))
        tempBullet = pg.transform.scale(PlasmaShot, (1, 1))
        PlayerBullet = pg.transform.scale(BlueShot, (6, 6))
        MACHINEBullet = pg.transform.scale(MACHINEShot, (5, 15))
        
        MbossBullet = pg.transform.scale(PlasmaShot, (20, 20))
        BossBullet = pg.transform.scale(PlasmaShot, (40, 40))
        MGun = pg.image.load(path.join(st.IMAGE_FOLDER,'MachineGun.png'))
        MGun  = pg.transform.scale(MGun, (30, 20))
        PGun = pg.image.load(path.join(st.IMAGE_FOLDER,'Pistol.png'))
        PGun = pg.transform.scale(PGun, (30, 20))
        PGun2 = pg.transform.scale(PGun, (2, 2))
        HeartP = pg.image.load(path.join(st.IMAGE_FOLDER,'Heart.png'))
        HeartP = pg.transform.scale(HeartP, (20, 16))
        MBULL = fn.img_list_from_strip('MBull.png', 16, 19, 0, 3)
        
        self.item_img = {
            'tempb' : tempBullet,
            'Pbullet': LaserBlue,
            'Mbullet': BlueShot,
            'Enemybullet' : EnemyBullet,
            'Mbossbullet' : LaserRed,
            'Bossbullet' :  BulletRed,
            'heart': HeartP,
            'MachineGun' : MGun,
            'Pistol' : PGun,
            'sword': PGun2
            }

        
        self.effects = {
            'crate_explosion': fn.img_list_from_strip(
                                    'explosion.png', 32, 32, 0, 7, 150)}
        
        self.item_anims = {
                'sword': fn.img_list_from_strip('enemy sword attack.png', 150, 150, 0, 8, 80),
                'swordD': SwordSwingDown,
                'swordL': SwordSwingLeft,
                'swordR': SwordSwingRight
                }


        self.gui_img = {
            'health': fn.loadImage('health_string.png'),
            'hearts': fn.img_list_from_strip('hearts_strip.png', 8, 8, 
                                               0, 6)}
        
        self.font = st.FONT
        self.font1 = pg.font.Font(path.join(st.IMAGE_FOLDER,'slkscr.ttf'),20)
        self.font2 = pg.font.Font(path.join(st.IMAGE_FOLDER,'slkscrb.ttf'),30)
        self.GameOverImg = pg.image.load(path.join(st.IMAGE_FOLDER,'GameOver.png'))
        self.WinImg = pg.image.load(path.join(st.IMAGE_FOLDER,'Win.png'))
        Icon1 = pg.image.load(path.join(st.IMAGE_FOLDER,'icon.png'))
        self.Icon = boss_strip = pg.transform.scale(Icon1, (20, 20))     


class Player(pg.sprite.Sprite):
    def __init__(self, game,  pos):
        self.group = game.all_sprites
        pg.sprite.Sprite.__init__(self)
        self.layer = 6
        self.group.add(self, layer=self.layer)
        self.game = game
        
        # images for animation pistol
        if self.game.machinegunpick:
            
            self.image_stripU = self.game.imageLoader.player_img['MwalkU']
            self.image_stripD = self.game.imageLoader.player_img['MwalkD']
            self.image_stripR = self.game.imageLoader.player_img['MwalkR']
            self.image_stripL = self.game.imageLoader.player_img['MwalkL']

            self.AttackU = self.image_stripU[0]
            self.AttackD = self.image_stripD[0]
            self.AttackL = self.image_stripL[0]
            self.AttackR = self.image_stripR[0]
            
        elif self.game.pistolpick:
            self.image_stripU = self.game.imageLoader.player_img['PwalkU']
            self.image_stripD = self.game.imageLoader.player_img['PwalkD']
            self.image_stripR = self.game.imageLoader.player_img['PwalkR']
            self.image_stripL = self.game.imageLoader.player_img['PwalkL']

            self.AttackU = self.image_stripU[0]
            self.AttackD = self.image_stripD[0]
            self.AttackL = self.image_stripL[0]
            self.AttackR = self.image_stripR[0]
        
        self.walk_frames = {
                LEFT: [self.image_stripL[0],self.image_stripL[1],self.image_stripL[2],self.image_stripL[3],self.image_stripL[4],self.image_stripL[5]],
                RIGHT: [self.image_stripR[0],self.image_stripR[1],self.image_stripR[2],self.image_stripR[3],self.image_stripR[4],self.image_stripR[5]],
                UP: [self.image_stripU[0],self.image_stripU[1],self.image_stripU[2],self.image_stripU[3],self.image_stripU[4],self.image_stripU[5]],
                DOWN: [self.image_stripD[0],self.image_stripD[1],self.image_stripD[2],self.image_stripD[3],self.image_stripD[4],self.image_stripD[5]]
                }
        
        self.attack_frames = {
                UP: [self.AttackU],
                RIGHT: [self.AttackR],
                LEFT: [self.AttackL],
                DOWN: [self.AttackD]
                }

        self.idle_frames = {
                LEFT: [self.image_stripL[0]],
                RIGHT: [self.image_stripR[0]],
                UP: [self.image_stripU[0]],
                DOWN: [self.image_stripD[0]]
                }


        self.image = self.idle_frames[DOWN][0]
        self.sound = self.game.soundLoader
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.spawn_pos = vec(pos)
        self.rect.center = pos
        self.hit_rect = pg.Rect((0, 0), (int(10),int(10)))
        self.hit_rect.center = self.pos
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.dir = vec(DOWN)
        self.lastdir = vec(DOWN)
        self.friction = vec(0, 0)
        self.state = 'IDLE'
        self.hp = 7.0
        self.mana = 0
        self.max_mana = 11.4
        self.dashmana = 0
        self.dashmax_mana = 50
        self.max_hp = st.PLAYER_HP_START
        # animation frames for heart refill
        self.heart_refill_frames = 0
        self.target_health = 0     
        self.itemA = None
        self.itemB = None
        self.swordcheck = False
        self.item_using = None

        self.shootcheck = False
        self.anim_update = 0
        self.attack_update = 0
        self.current_frame = 0
        self.MoveCheck = False
        self.Dead = False
        self.manacheck = True
        self.dashcheck = False
        self.ctrlpress = False
        self.dashmanafill = True
        self.sprcolcheck = False
        self.manacount = 0
        self.UpCheck = False
        self.DownCheck = False
        self.RightCheck = False
        self.LeftCheck = False
        self.angle = 0
        self.angle2 = self.angle + 90
        # SHADOW
        self.shadow_surf = pg.Surface((12, 6)).convert_alpha()
        self.shadow_surf.fill(st.TRANS)
        self.shadow_rect = self.shadow_surf.get_rect()
        pg.draw.ellipse(self.shadow_surf, (0, 0, 0, 180), self.shadow_rect)
        
        self.timeupsound = [self.game.soundLoader.snd['TimeUp01'],self.game.soundLoader.snd['TimeUp02'],
                            self.game.soundLoader.snd['TimeUp03']]
        self.timeupcount = 0

        self.timedownsound = [self.game.soundLoader.snd['TimeDown01'],self.game.soundLoader.snd['TimeDown02'],
                            self.game.soundLoader.snd['TimeDown03']]
        self.timedowncount = 0
    def get_keys(self):
        if self.state == 'IDLE' or self.state == 'WALKING':
            keys = self.game.keys
            move = keys['DPAD']
            self.acc = move
            if self.acc.length_squared() > 1:
                self.acc.normalize()
            self.acc *= st.PLAYER_ACC
            # set image's direction based on key pressed
            if self.LeftCheck:
                self.timedowncount = 0
                self.MoveCheck = True
                self.swordcheck = True
                self.shootcheck = True
                self.dir = vec(LEFT)
                self.acc = vec(LEFT)
                self.lastdir = vec(LEFT)
            if self.RightCheck:
                self.timedowncount = 0
                self.MoveCheck = True
                self.swordcheck = True
                self.shootcheck = True
                self.dir = vec(RIGHT)
                self.acc = vec(RIGHT)
                self.lastdir = vec(RIGHT)
                
            if self.UpCheck:
                self.timedowncount = 0
                self.MoveCheck = True
                self.swordcheck = True
                self.shootcheck = True
                self.dir = vec(UP)
                self.acc = vec(UP)
                self.lastdir = vec(UP)
            if self.DownCheck:
                self.timedowncount = 0
                self.MoveCheck = True
                self.swordcheck = True
                self.shootcheck = True
                self.dir = vec(DOWN)
                self.acc = vec(DOWN)
                self.lastdir = vec(DOWN)

            if self.UpCheck and self.RightCheck:
                self.acc = vec(UP_RIGHT)
            if self.UpCheck and self.LeftCheck:
                self.acc = vec(UP_LEFT)
            if self.DownCheck and self.RightCheck:
                self.acc = vec(DOWN_RIGHT)
            if self.DownCheck and self.LeftCheck:
                self.acc = vec(DOWN_LEFT)
                

            if self.acc.length() < 0.1:
                self.timedowncount += 1
                self.timeupcount = 0
                self.MoveCheck = False
               
                # if velocity is less than the threshold, set state to idle
                self.state = 'IDLE'
            else:
                 # set the state to walking
                 self.state = 'WALKING'
                 
            
            if keys['A']:
                if self.game.machinegunpick:
                    if self.itemA.check == False:
                        self.itemA.use()
                        self.attack_update += 1
                        if self.attack_update > self.itemA.cooldown:
                            self.attack_update = 0
                            self.itemA.reset()
                            self.shootcheck = False
                else:
                    self.itemA.use()
                    self.attack_update += 1
                    if self.attack_update > self.itemA.cooldown:
                        self.attack_update = 0
                        self.itemA.reset()
                        self.shootcheck = False
                
    def update(self):    
        if self.game.machinegunpick:
            
            self.image_stripU = self.game.imageLoader.player_img['MwalkU']
            self.image_stripD = self.game.imageLoader.player_img['MwalkD']
            self.image_stripR = self.game.imageLoader.player_img['MwalkR']
            self.image_stripL = self.game.imageLoader.player_img['MwalkL']

            self.AttackU = self.image_stripU[0]
            self.AttackD = self.image_stripD[0]
            self.AttackL = self.image_stripL[0]
            self.AttackR = self.image_stripR[0]
            
        elif self.game.pistolpick:
            
            self.image_stripU = self.game.imageLoader.player_img['PwalkU']
            self.image_stripD = self.game.imageLoader.player_img['PwalkD']
            self.image_stripR = self.game.imageLoader.player_img['PwalkR']
            self.image_stripL = self.game.imageLoader.player_img['PwalkL']

            self.AttackU = self.image_stripU[0]
            self.AttackD = self.image_stripD[0]
            self.AttackL = self.image_stripL[0]
            self.AttackR = self.image_stripR[0]

        self.walk_frames = {
                LEFT: [self.image_stripL[0],self.image_stripL[1],self.image_stripL[2],self.image_stripL[3],self.image_stripL[4],self.image_stripL[5]],
                RIGHT: [self.image_stripR[0],self.image_stripR[1],self.image_stripR[2],self.image_stripR[3],self.image_stripR[4],self.image_stripR[5]],
                UP: [self.image_stripU[0],self.image_stripU[1],self.image_stripU[2],self.image_stripU[3],self.image_stripU[4],self.image_stripU[5]],
                DOWN: [self.image_stripD[0],self.image_stripD[1],self.image_stripD[2],self.image_stripD[3],self.image_stripD[4],self.image_stripD[5]]
                }
        
        self.attack_frames = {
                UP: [self.AttackU],
                RIGHT: [self.AttackR],
                LEFT: [self.AttackL],
                DOWN: [self.AttackD]
                }

        self.idle_frames = {
                LEFT: [self.image_stripL[0]],
                RIGHT: [self.image_stripR[0]],
                UP: [self.image_stripU[0]],
                DOWN: [self.image_stripD[0]]
                }

        # get player input
        self.get_keys()
        keys = pg.key.get_pressed()
        # player animations
        self.animate()
        self.rect = self.image.get_rect()
        self.image = self.walk_frames[(self.lastdir.x, 
                                self.lastdir.y)][self.current_frame]
        
        mouse_x, mouse_y = pg.mouse.get_pos()
        self.angle = math.degrees(math.atan2(self.pos.x-mouse_x,self.pos.y-mouse_y))
        self.angle2 = self.angle + 90
        self.angle3 = self.angle
        if self.lastdir == vec(DOWN):
            self.angle = self.angle + 180
        elif self.lastdir == vec(LEFT):
            self.angle = self.angle - 90
        elif self.lastdir == vec(RIGHT):
            self.angle = self.angle + 90
        else:
            self.angle = self.angle
        
        self.image = pg.transform.rotozoom(self.image, self.angle, 1)
        self.rect = self.image.get_rect()
        # add acceleration to velocity
        self.vel += self.acc

        # calculate friction
        self.friction *= 0
        if self.vel.length_squared() > 0:
            self.friction = vec(self.vel) * -1
            self.friction = self.friction.normalize()
            self.friction *= st.PLAYER_FRICTION

            # apply friction
            self.vel += self.friction
        
        
        # limit velocity
        if self.vel.length_squared() > st.PLAYER_MAXSPEED ** 2:
            self.vel.scale_to_length(st.PLAYER_MAXSPEED)        
        elif self.vel.length_squared() < 0.01:
            self.vel *= 0
              
        # add velocity to position
        self.pos += self.vel
        if self.state != 'HITSTUN':
            self.acc *= 0
        if self.game.machinegunpick:
            if self.mana > 11:
                self.manacheck = False
            if self.MoveCheck == True:
                self.manacount += 0.5
                if self.shootcheck == False:
                    self.manacheck = True
                    self.manacount = 0
                
            if self.manacount == 20:
                self.manacheck = False
                self.manacount = 0
            
            if self.manacheck == False:
                if self.MoveCheck:
                    if self.mana > 0:
                        self.mana -= 0.2
                        self.manacount = 0
                    if self.mana < 0.2:
                        self.itemA.check = False
                        self.manacheck = True
        
            
        self.hitbox = self.rect.inflate(-70,-70)
        self.rect.center = self.pos
        self.hitbox.center = self.pos
        
        self.hit_rect.centerx = self.pos.x
        a = fn.collide_with_walls(self, self.game.walls, 'x')
        
        self.hit_rect.centery = self.pos.y
        b = fn.collide_with_walls(self, self.game.walls, 'y')
                
        self.hitbox.midbottom = self.hit_rect.midbottom
        self.hitbox.center = self.hit_rect.center
        self.hitbox.bottom = self.hit_rect.bottom + 1
        
        self.fillHearts()
        # restrain items between 0 and max
        self.hp = max(0, min(self.hp, self.max_hp))
        if self.hp <= 0.8:
            self.destroy()
        
    
        
        
    def animate(self):
        now = pg.time.get_ticks()

        if self.state == 'WALKING':
            if now - self.anim_update > 200:
                self.anim_update = now
                self.current_frame = (self.current_frame + 1) % len(
                                      self.walk_frames[LEFT])
                
                self.image = self.walk_frames[(self.lastdir.x, 
                                self.lastdir.y)][self.current_frame]
        
        elif self.state == 'IDLE':
            st.PLAYER_FRICTION = 0.5
            self.image = self.idle_frames[(self.lastdir.x, self.lastdir.y)][0]

                    
        elif self.state == 'HITSTUN':
            self.image = self.idle_frames[(self.lastdir.x, self.lastdir.y)][0]
            # flicker to indicate damage
            try:
                alpha = next(self.damage_alpha)
                self.image = self.lastimage.copy()
                self.image.fill((255, 255, 255, alpha), 
                                special_flags=pg.BLEND_RGBA_MULT)
            except:
                self.state = 'IDLE'
           
    
    def stun(self, time):
        self.vel *= 0
        self.acc *= 0
        self.state = 'HITSTUN'
        self.lastimage = self.image.copy()
        self.damage_alpha = iter(st.DAMAGE_ALPHA * time)

    
    def knockback(self, other, time, intensity):
        if self.state != 'HITSTUN':
            self.vel = vec(0, 0)
            # calculate vector from other to self
            knockdir = self.pos - other.pos
            st.PLAYER_FRICTION = 0.1
            if knockdir.length_squared() > 0:
                knockdir = knockdir.normalize()
                self.acc = knockdir * intensity
                self.lastimage = self.image.copy()
                self.damage_alpha = iter(st.DAMAGE_ALPHA * time)
                self.state = 'HITSTUN'
                
                
       
    def fillHearts(self):
        if self.hp < self.target_health:
            self.heart_refill_frames += 1
            if self.heart_refill_frames > st.FPS // 20:
                self.hp += 0.25
                self.heart_refill_frames = 0      
        else:
            self.target_health = 0
    
    def draw_before(self):

        # draw a shadow
        self.shadow_rect.centerx = self.hit_rect.centerx
        self.shadow_rect.bottom = self.hit_rect.bottom + 4
        self.game.screen.blit(self.shadow_surf, self.shadow_rect)
        
    def destroy(self):
        self.kill()
        self.Dead = True
        


class Solid(pg.sprite.Sprite):
    '''
    Container Class for all solid objects
    '''
    def __init__(self, game, pos, size):
        self.game = game
        self.pos = vec(pos)
        self.size = size
        self.groups = self.game.walls, self.game.all_sprites
        self.layer = 1
        pg.sprite.Sprite.__init__(self)
        for g in self.groups:
            g.add(self, layer=self.layer)
        self.rect = pg.Rect(self.pos, self.size)
        self.hit_rect = self.rect.copy()


    def update(self):
        # not used right now
        pass
        
            

class Wall(Solid):
    '''
    An invisible wall object with variable size
    '''
    def __init__(self, game, pos, size, **kwargs):
        super().__init__(game, pos, size)
        self.image = pg.Surface(size, pg.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        
        
        
class Block(Solid):
    '''
    A solid block with an image, always same size
    ''' 
    def __init__(self, game, pos, size, **kwargs):
        super().__init__(game, pos, size)
        self.image = self.game.imageLoader.solid_img['block']
        
 
class Door(Solid):
    '''
     A closed door that disappears if the player achieves a goal
    '''
    def __init__(self, game, pos,**kwargs):
        super().__init__(game, pos, size=(0, 0))
        self.image = self.game.imageLoader.door_image_dict[kwargs['direction']]
        self.size = self.image.get_size()
        
        self.rect = pg.Rect(self.pos, self.size)
        self.hit_rect = self.rect.copy()

class Explosive_crate(Solid):
    def __init__(self, game, pos, size, **kwargs):
        super().__init__(game, pos, size)
        self.image = self.game.imageLoader.solid_img['crate']
        self.size = self.image.get_size()
        self.rect = pg.Rect(self.pos, self.size)
        self.hit_rect = pg.Rect((0, 0), (int(36),int(36)))
        self.hit_rect.center = self.pos

        offset = vec(4, 4)
        self.interact_rect = self.rect.inflate(offset)

        self.interact_rect.center = self.hit_rect.center
        
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        
        self.push_timer = 0
    
    
    def update(self):
        player = self.game.player
        if self.interact_rect.colliderect(player.hit_rect):
            # if player pushes, move in that direction
            self.push_timer += 1
            if self.push_timer > 0.8 * st.FPS:
                self.acc = vec(player.dir)
                
        else:
            self.vel *= 0
            self.push_timer = 0
        
        self.vel += self.acc  
        self.acc *= 0
        self.pos += self.vel
        self.rect.center = self.pos
        self.hit_rect.center = self.pos
        
        # collision with walls
        self.hit_rect.left = self.pos.x
        fn.collide_with_walls_topleft(self, self.game.walls, 'x')
        self.hit_rect.right = self.rect.right
        self.hit_rect.top = self.pos.y
        fn.collide_with_walls_topleft(self, self.game.walls, 'y')
        self.hit_rect.bottom = self.rect.bottom
        self.rect.center = self.hit_rect.center
        
        self.interact_rect.center = self.hit_rect.center
        
# --------------- Inventory & Items -------------------------------------------

class Inventory(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.gui
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        # if in menu then True, otherwise False
        self.menu = False

        self.size = (st.WIDTH, st.HEIGHT)
        self.start_pos = vec(0, (0 - st.HEIGHT + st.GUI_HEIGHT))
        self.pos = vec(self.start_pos)
        self.image = pg.Surface(self.size)
        self.image.fill(st.BLACK)

        self.map_img = None

        # "health" string
        self.health_string = self.game.imageLoader.gui_img['health']
        self.heart_images = self.game.imageLoader.gui_img['hearts']
       
        for i in range(len(self.heart_images)):
            self.heart_images[i] = pg.transform.scale(self.heart_images[i], 
                                  (8, 8))
        
        self.fo1 = pg.font.Font(path.join(st.IMAGE_FOLDER,'slkscr.ttf'),20)
        self.fo3 = pg.font.Font(path.join(st.IMAGE_FOLDER,'slkscr.ttf'),10)
        self.fo2 = pg.font.Font(path.join(st.IMAGE_FOLDER,'slkscrb.ttf'),30)
        self.anim_update = 0
        self.anim_delay = 300
        self.current_frame = 0
        
        self.heart_frames = 0
        self.Quitbtn = Button(st.WIDTH//2,st.HEIGHT//2,250,50,[200,20,20], 'Quit Game', self.fo1, [0,0,0], self.fo2)
        
    


    def update(self):
        if self.game.keys['START'] and self.game.state != 'MENU_TRANSITION':
            self.menu = not self.menu

        if self.menu:
            self.game.state = 'MENU_TRANSITION'
            # sliding down animation
            if self.pos != (0, 0):
                self.pos.y += st.SCROLLSPEED_MENU
                self.pos.y = min(0, self.pos.y)
            else:
                self.game.state = 'MENU'
        else:
            # sliding up animation
            if self.pos != self.start_pos:
                self.game.state = 'MENU_TRANSITION'
                self.pos.y -= st.SCROLLSPEED_MENU
                self.pos.y = min(0, self.pos.y)
            else:
                if self.game.state != 'GAME':
                    self.game.state = 'GAME'
                    
        if self.game.state != 'GAME':
                if self.Quitbtn.clicked():
                    pg.quit()
                    quit()
        

    def draw(self):
        self.image.fill(st.BLACK)
        # draw player health
        player = self.game.player
        
        for i in range(int(player.max_hp)):
            # calculate position
            if i < st.PLAYER_HP_ROW:
                pos = (6 + 10 * i, st.HEIGHT - 34)
            else:
                pos = (6 + 10 * (i - st.PLAYER_HP_ROW), st.HEIGHT - 24)

            # draw hearts:
            if i < int(player.hp):
                img = self.heart_images[1]
            elif i == int(player.hp):
                if player.hp % 1 == 0.25:
                    img = self.heart_images[4]
                elif player.hp % 1 == 0.5:
                    img = self.heart_images[3]
                elif player.hp % 1 == 0.75:
                    img = self.heart_images[2]
                else:
                    img = self.heart_images[5]
            else:
                img = self.heart_images[5]

            self.image.blit(img, pos)

        label = self.fo1.render('Rooms Cleared: '+ str(self.game.clearcount), True, st.WHITE)
        labelRect = label.get_rect()
        labelRect.center = (500,st.HEIGHT - 30)
        self.image.blit(label, labelRect)
        
        label2 = self.fo1.render('Level: '+ str(self.game.levelcleared), True, st.WHITE)
        labelRect2 = label2.get_rect()
        labelRect2.center = (700,st.HEIGHT - 30)
        self.image.blit(label2, labelRect2)
        
        self.image.blit(self.health_string, (25, st.HEIGHT - 42))
        # draw the mini map
        map_pos = (300, st.HEIGHT - 44)
        self.Quitbtn.update(self.image)
        self.image.blit(self.map_img, map_pos)
        self.game.screen.blit(self.image, self.pos)
            
             
class AttackItem(pg.sprite.Sprite):
    def __init__(self, game, player):
        self.group = game.all_sprites
        self.layer = player.layer
        pg.sprite.Sprite.__init__(self)
        self.player = player
        self.game = game
        self.image = self.game.imageLoader.item_img[self.type].copy()
        self.cooldown = 20
        
    def update(self):
        # delete sprite if fired
        if not self.player.state == 'USE_A':
            self.game.all_sprites.remove(self)
            
    
    def use(self):
        self.image = self.game.imageLoader.item_img[self.type].copy()
        self.group.add(self, layer=self.layer)
        
    
        self.dir = self.player.lastdir
        self.angle = 0
        self.angle += self.player.angle2
        self.image = pg.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        
        self.hit_rect.center = self.rect.center

class Sword(AttackItem):
    def __init__(self, game, player):
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
        self.hit_rect = pg.Rect((0, 0), (int(50),int(50)))
        self.damage = 0.2
        self.kb_time = 1
        self.kb_intensity = 0.5


    def update(self):
        if not self.player.state == 'SWORD':
            self.game.all_sprites.remove(self)

        checkplayer = self.game.player
        if fn.collide_hit_rect(checkplayer, self):
            checkplayer.knockback(self, self.kb_time, self.kb_intensity)
            checkplayer.hp -= self.damage
        
    def use(self):
        self.group.add(self, layer=self.layer)
        
        self.pos = self.player.pos
        self.dir = self.player.lastdir
        anim = self.animations[DOWN]
        self.image = anim[self.current_frame]
        self.image = pg.transform.rotozoom(self.image, self.player.angle_to_player, 1)
        self.rect = self.image.get_rect()
        
        now = pg.time.get_ticks()
        if now - self.anim_update > self.anim_speed:
            self.anim_update = now
            self.current_frame = (self.current_frame + 1) % len(anim)
        
        
    
        
        self.rect.center = self.pos
        self.hit_rect.center = self.rect.center
        
        if not self.fired:
            # play slash sound      
            self.game.soundLoader.snd['slash'].play()
            self.fired = True
            
    def reset(self):
        self.fired = False
        self.current_frame = 0
        
class PBullet(AttackItem):
    def __init__(self, game, player):
        self.type = 'Pbullet'
        super().__init__(game, player)
        self.fired = False
        self.cooldown = 15
        self.hit_rect = pg.Rect((0, 0), (int(10),int(10)))
        self.soundlist = [self.game.soundLoader.snd['Laser02'],self.game.soundLoader.snd['Laser03'],
                          self.game.soundLoader.snd['Laser04'],self.game.soundLoader.snd['Laser05']]
        
    def use(self):
        super().use()
        if not self.fired and self.player.shootcheck == True:
            self.lastdir = self.player.lastdir
            Bullet(self.game, self, self.rect.center)
            asound = choice(self.soundlist)
            asound.play()
            self.fired = True
    
    def reset(self):
        self.fired = False

class MachineBullet(AttackItem):
    def __init__(self, game, player):
        self.type = 'Mbullet'
        super().__init__(game, player)
        self.fired = False
        self.cooldown = 2
        self.check = False
        
        
    def use(self):
        super().use()
        if self.player.mana > 11:
                self.check = True
        if not self.fired and self.player.shootcheck == True:
            if self.player.mana < 12 and self.check == False:
                self.lastdir = self.player.lastdir
                MacBullet(self.game, self, self.rect.center)
                self.player.mana += 1
                self.game.soundLoader.snd['magic1'].play()
                self.fired = True
    def reset(self):
        self.fired = False
        
        
class Projectile(pg.sprite.Sprite):
    def __init__(self, game, player, pos):
        self.group = game.all_sprites
        self.layer = 1
        pg.sprite.Sprite.__init__(self)
        self.group.add(self, layer=self.layer)
        self.player = player
        self.game = game
        self.Blst = []
        self.vel = vec(0, 0)
        self.anim_update = 0
        self.current_frame = 0
        self.angle = 0
        self.bulletlst = []
        
        self.state = 'SHOT'
        self.pos = (0,0)
        # set own direction based on the direction the player sprite is facing
        self.dir = self.player.lastdir
        
        self.image = pg.transform.rotozoom(self.image, self.game.player.angle3, 1)
            
        position = pg.mouse.get_pos()
        Bangle = math.degrees(math.atan2(position[1]-(self.game.player.pos.y),position[0]-(self.game.player.pos.x)))
        A = self.game.player.pos.x + math.cos(math.radians(Bangle))*35
        B = self.game.player.pos.y + math.sin(math.radians(Bangle))*35
        self.bulletlst.append([math.atan2(position[1]-(self.game.player.pos.y),position[0]-(self.game.player.pos.x)),A,B])
        self.mask = pg.mask.from_surface(self.image)
        self.maskbount = self.mask.get_bounding_rects()
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.hit_rect = self.maskbount[0]
        self.hit_rect.center = self.rect.center
        
        
    def update(self):
        if self.state == 'SHOT':
            hits_walls = pg.sprite.spritecollide(self, self.game.walls, 
                                                 False, fn.collide_hit_rect)
            for wall in hits_walls:
                if wall.image == self.game.imageLoader.solid_img['crate']:
                    images = self.game.imageLoader.effects['crate_explosion']
                    Explosion(self.game, vec(self.pos), images, 80, damage = 0.2,
                              sound=self.game.soundLoader.snd['bomb'],
                              hit_rect=pg.Rect(images[0].get_rect().inflate(-6, -6)))
                    wall.kill()

            
                
                
            if hits_walls:
                self.state = 'HIT_WALL'

            for bullet in self.bulletlst:
                velx=math.cos(bullet[0])*5
                vely=math.sin(bullet[0])*5
                if self.game.player.MoveCheck == True:
                    bullet[1]+=velx
                    bullet[2]+=vely
                for projectile in self.bulletlst:
                    self.acc = projectile
                    
            
            
            hits_enemies = pg.sprite.spritecollide(self, self.game.enemies, 
                                                   False, fn.collide_hit_rect)
            if hits_enemies:
                for enemy in hits_enemies:
                    enemy.hp -= self.damage
                    self.state = 'HIT_ENEMY'
                    self.enemy = enemy

            
             
            self.pos = (self.acc[1], self.acc[2])
        
        else:
            self.destroy()
        
        self.rect.center = self.pos
        self.hit_rect.center = self.rect.center
        
        try:        
            self.animate()
        except:
            # has no animation frames
            pass
        
    def animate(self):
        now = pg.time.get_ticks()
        if now - self.anim_update > self.anim_speed:
            self.anim_update = now
            self.current_frame = (self.current_frame + 1) % len(
                                  self.image_frames)
            self.image = self.image_frames[self.current_frame]
            
    
    def destroy(self):
        self.vel *= 0
        self.kill()

      

class Bullet(Projectile):
    def __init__(self, game, player, pos):
        self.image = game.imageLoader.item_img['Pbullet']           
        super().__init__(game, player, pos)
        
        self.speed = 2
        self.max_speed = 4
        self.damage = 2
        self.anim_speed = 100
        self.destroy_timer = 0
        #self.hit_rect = pg.Rect((0, 0), (int(30),int(30)))
    def destroy(self):
        if self.state == 'HIT_WALL':
            if self.vel.length_squared() > 0:
                self.pos += self.vel.normalize() * 3
            self.vel *= 0
            self.kill()
        elif self.state == 'HIT_ENEMY':
            self.pos = self.enemy.pos
            self.kill()

class MacBullet(Projectile):
    def __init__(self, game, player, pos):
        self.image = game.imageLoader.item_img['Mbullet']           
        super().__init__(game, player, pos)
        
        self.speed = 2
        self.max_speed = 4
        self.damage = 3
        self.anim_speed = 100
        self.destroy_timer = 0
        self.hit_rect = pg.Rect((0, 0), (int(5),int(5)))
        position = pg.mouse.get_pos()
        Bangle = math.degrees(math.atan2(position[1]-(self.game.player.pos.y),position[0]-(self.game.player.pos.x)))
        A = self.game.player.pos.x + math.cos(math.radians(Bangle))*40
        B = self.game.player.pos.y + math.sin(math.radians(Bangle))*40
        self.bulletlst.append([math.atan2(position[1]-(self.game.player.pos.y),position[0]-(self.game.player.pos.x)),A,B])
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.hit_rect.center = self.rect.center
        
    def destroy(self):
        if self.state == 'HIT_WALL':
            if self.vel.length_squared() > 0:
                self.pos += self.vel.normalize() * 3
            self.vel *= 0
            self.kill()
        elif self.state == 'HIT_ENEMY':
            self.pos = self.enemy.pos
            self.kill()
                 


            
class EnemyProjectile(pg.sprite.Sprite):
    def __init__(self, game, enemy, pos):
        self.group = game.all_sprites
        self.layer = enemy.layer
        pg.sprite.Sprite.__init__(self)
        self.group.add(self, layer=self.layer)
        self.enemy = enemy
        self.game = game
        self.pos = vec(pos)
        self.Blst = []
        self.vel = vec(0, 0)       
        self.anim_update = 0
        self.current_frame = 0
        self.state = 'SHOT'
        # set own direction based on the direction the player sprite is facing
        
        self.destroy_timer = 0
        self.angle = 0
        self.dir = self.enemy.lastdir
        
        self.image = pg.transform.rotozoom(self.image, self.enemy.angleee, 1)
        Bangle = math.degrees(math.atan2(self.game.player.pos.y-(self.enemy.pos.y),self.game.player.pos.x-(self.enemy.pos.x)))
        A = self.enemy.pos.x + math.cos(math.radians(Bangle))*35
        B = self.enemy.pos.y + math.sin(math.radians(Bangle))*35
        self.Blst.append([math.atan2(self.game.player.pos.y-(self.enemy.pos.y),self.game.player.pos.x-(self.enemy.pos.x)),A,B])
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.maskbount = self.mask.get_bounding_rects()
        self.rect.center = self.pos
        self.hit_rect = self.maskbount[0]
        self.hit_rect.center = self.rect.center
    def update(self):
        if self.state == 'SHOT':
            hits_walls = pg.sprite.spritecollide(self, self.game.walls, 
                                                 False, fn.collide_hit_rect)
            for wall in hits_walls:
                if wall.image == self.game.imageLoader.solid_img['crate']:
                    images = self.game.imageLoader.effects['crate_explosion']
                    Explosion(self.game, vec(self.pos), images, 80, damage = 0.2,
                              sound=self.game.soundLoader.snd['bomb'],
                              hit_rect=pg.Rect(images[0].get_rect().inflate(-6, -6)))
                    wall.kill()
            if hits_walls:
                self.state = 'HIT_WALL'

            for bullet in self.Blst:
                velx=math.cos(bullet[0])*5
                vely=math.sin(bullet[0])*5
                if self.game.player.MoveCheck == True:
                    bullet[1]+=velx
                    bullet[2]+=vely
                for projectile in self.Blst:
                    self.acc = projectile
                    
                
            player = self.game.player
            if fn.collide_hit_rect(player, self):
                if (player.state != 'HITSTUN'):
                    self.state = 'HIT_Player'
                    player.hp -= self.damage
                    
            # limit velocity
            if self.vel.length_squared() > self.max_speed ** 2:
                self.vel.scale_to_length(self.max_speed)

                
            self.pos = (self.acc[1], self.acc[2])

        else:
            self.destroy()
        
        self.rect.center = self.pos
        self.hit_rect.center = self.rect.center

    def destroy(self):
        if self.state == 'HIT_WALL':
            # push the arrow a bit into a wall
            if self.vel.length_squared() > 0:
                self.pos += self.vel.normalize() * 3
            self.vel *= 0
            self.kill()
        elif self.state == 'HIT_Player':
            self.pos = self.game.player.pos
            self.kill()
              
            
            
class EnemyBullet(EnemyProjectile):
    def __init__(self, game, enemy, pos, rotating=True):
        self.image = game.imageLoader.item_img['Enemybullet']           
        super().__init__(game, enemy, pos)
        
        self.speed = 2
        self.max_speed = 4
        self.damage = 1
        self.anim_speed = 100
        self.hit_rect = pg.Rect((0, 0), (int(5),int(5)))
        self.destroy_timer = 0
        

class Mbossbullet(EnemyProjectile):
    def __init__(self, game, enemy, pos, rotating=True):
        self.image = game.imageLoader.item_img['Mbossbullet']           
        super().__init__(game, enemy, pos)
        
        self.speed = 3
        self.max_speed = 5
        self.damage = 1.5
        self.anim_speed = 100
        
        
        
        
    
class Bossbullet(EnemyProjectile):
    def __init__(self, game, enemy, pos, rotating=True):
        self.image = game.imageLoader.item_img['Bossbullet']           
        super().__init__(game, enemy, pos)
        
        self.speed = 3
        self.max_speed = 5
        self.damage = 2
        self.anim_speed = 100
        self.hit_rect = pg.Rect((0, 0), (int(5),int(5)))
    

    
        
        
                
class Item:       
    def drop(name, game, pos):
        if name in Item.__dict__:
            # instanciate the given sprite by its name
            Item.__dict__[name](game, pos)
        elif name == 'none':
            pass
        else:
            print('Can\'t drop {}.'.format(name))
            
            
    class ItemDrop(pg.sprite.Sprite):
        def __init__(self, game, pos):
            self.game = game                    
            self.player = self.game.player
            self.pos = vec(pos)
            self.groups = self.game.all_sprites, self.game.item_drops
            self.layer = self.game.player.layer - 1
            pg.sprite.Sprite.__init__(self)
            
            for g in self.groups:
                g.add(self, layer=self.layer)
            
            self.timer = 0
            self.duration = 6 * st.FPS
            
            self.alpha = iter([i for i in range(255, 0, -10)] * 3)
        
        
        def update(self):
            if fn.collide_hit_rect(self.player, self):
                self.collect()

            if self.game.player.MoveCheck == True:
                self.timer += 1
                
            if self.timer >= self.duration:
                try:
                    alpha = next(self.alpha)
                    self.image = self.lastimage.copy()
                    self.image.fill((255, 255, 255, alpha), 
                                    special_flags=pg.BLEND_RGBA_MULT)
                except:
                    self.kill()
            else:
                self.lastimage = self.image.copy()
        
        
        def collect(self):
            self.kill()
        
        
    class heart(ItemDrop):
        def __init__(self, game, pos):
            super().__init__(game, pos)
            self.image = self.game.imageLoader.item_img['heart']
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.hit_rect = self.rect
           
            
        def collect(self):
            self.player.hp += 1
            self.game.soundLoader.snd['heart'].play()
            super().collect()

    class MachineGun(ItemDrop):
        def __init__(self, game, pos):
            super().__init__(game, pos)
            self.image = self.game.imageLoader.item_img['MachineGun']
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.hit_rect = self.rect

        def update(self):
            if fn.collide_hit_rect(self.player, self):
                self.collect()

            
        def collect(self):
            self.game.player.mana = 0
            if self.game.pistolpick == True:
                self.game.lastweapon = 'Pistol'
            elif self.game.machinegunpick == True:
                self.game.lastweapon = 'MachineGun'

            check = self.player.pos - vec(40,40)
            
            if check.x < 50:
                check.x = 80
            elif check.x > 755:
                check.x = 730
            if check.y < 140:
                check.y = 150
            elif check.y > 555:
                check.y = 530
            
            try:
                Item.drop(self.game.lastweapon, self.game, check)
            except:
                print('error. cannot drop item', self.game.lastweapon)
            self.game.machinegunpick = True
            self.game.pistolpick = False
            self.game.soundLoader.snd['heart'].play()
            super().collect()
            
    class Pistol(ItemDrop):
        def __init__(self, game, pos):
            super().__init__(game, pos)
            self.image = self.game.imageLoader.item_img['Pistol']
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.hit_rect = self.rect

        def update(self):
            if fn.collide_hit_rect(self.player, self):
                self.collect()

    
        def collect(self):
            if self.game.pistolpick == True:
                self.game.lastweapon = 'Pistol'
            elif self.game.machinegunpick == True:
                self.game.lastweapon = 'MachineGun'
            check = self.player.pos - vec(40,40)
            
            if check.x < 50:
                check.x = 80
            elif check.x > 755:
                check.x = 730
            if check.y < 140:
                check.y = 150
            elif check.y > 555:
                check.y = 530
            
            try:
                Item.drop(self.game.lastweapon, self.game, check)
            except:
                print('error. cannot drop item', self.game.lastweapon)
                
            self.game.machinegunpick = False
            self.game.pistolpick = True
            self.game.soundLoader.snd['heart'].play()
            super().collect()
        
            
# ----------------------- ENEMIES ---------------------------------------------
        
class Enemy(pg.sprite.Sprite):
    '''
    Container class for all basic enemies
    '''
    def __init__(self, game, pos):
        self.game = game
        self.pos = vec(pos)
        self.groups = self.game.all_sprites, self.game.enemies
        self.layer = self.game.player.layer + 1
        pg.sprite.Sprite.__init__(self)
        
        for g in self.groups:
            g.add(self, layer=self.layer)

        self.image = self.idle_frames[UP][0]
        
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.vel = vec(0, 0)
        self.dir = vec(DOWN)
        self.lastdir = vec(DOWN)
        self.moveTo = None
        self.acc = vec(0, 0)
        self.friction = 0.1
        self.hp = 1
        self.damage = 0.5
        self.anim_speed = 300
        self.maxSpeed = 1
        self.drop_rates = {'none':1,'heart':0.5}
        self.state = 'IDLE'
        self.anim_update = 0
        self.walk_update = 0
        self.current_frame = 0
        self.timer = 0
        self.angle_to_player = 0
        self.shoot_time = 2 * st.FPS
        self.stun_timer = 0
        self.SwordWeapon = Sword(self.game, self)
        self.enemy01move = False
        self.zig1 = False
        self.zig2 = False
        self.zig1Count = 0
        self.zig2Count = 0
        
    def move(self):
        if self.state == 'WALKING' and self.game.player.MoveCheck == True:
            # set acceleration based on 4-way movement
            if self.moveTo == LEFT:
                self.acc.x = -1       
                self.dir = vec(LEFT)
                self.lastdir = vec(LEFT)
    
            if self.moveTo == RIGHT:
                self.acc.x = 1          
                self.dir = vec(RIGHT)
                self.lastdir = vec(RIGHT)
    
            if self.moveTo == UP:
                self.acc.y = -1
                self.dir = vec(UP)
                self.lastdir = vec(UP)
    
            if self.moveTo == DOWN:
                self.acc.y = 1
                self.dir = vec(DOWN)
                self.lastdir = vec(DOWN)
        
        elif self.state == 'SEEK' and self.game.player.MoveCheck == True:
            desired = (self.game.player.pos - self.pos)
            if desired.length_squared() > 0:
                desired = desired.normalize() * self.maxSpeed
                steer = desired - self.vel
                self.acc = steer
                if self.zig1Count < 21:
                    if self.lastdir == vec(LEFT) or self.lastdir == vec(RIGHT): 
                        self.acc = steer - vec(1,0)
                        self.acc = steer - vec(1,0)
                        self.acc = steer - vec(1,0)
                        self.acc = steer - vec(1,0)
                        self.acc = steer - vec(1,0)
                        self.acc = steer - vec(1,0)
                        self.acc = steer - vec(1,0)
                        self.acc = steer - vec(1,0)
                        self.acc = steer - vec(1,0)
                        self.acc = steer - vec(1,0)
                        
                    else:
                        self.acc = steer - vec(0,1)
                        self.acc = steer - vec(0,1)
                        self.acc = steer - vec(0,1)
                        self.acc = steer - vec(0,1)
                        self.acc = steer - vec(0,1)
                        self.acc = steer - vec(0,1)
                        self.acc = steer - vec(0,1)
                        self.acc = steer - vec(0,1)
                        self.acc = steer - vec(0,1)
                        self.acc = steer - vec(0,1)
                        
                        
                if self.zig1Count > 20 and self.zig1Count < 41:
                    if self.lastdir == vec(LEFT) or self.lastdir == vec(RIGHT):
                        self.acc = steer + vec(1,0)
                        self.acc = steer + vec(1,0)
                        self.acc = steer + vec(1,0)
                        self.acc = steer + vec(1,0)
                        self.acc = steer + vec(1,0)
                        self.acc = steer + vec(1,0)
                        self.acc = steer + vec(1,0)
                        self.acc = steer + vec(1,0)
                        self.acc = steer + vec(1,0)
                        self.acc = steer + vec(1,0)
                        
                        
                       
                    else:
                        self.acc = steer + vec(0,1)
                        self.acc = steer + vec(0,1)
                        self.acc = steer + vec(0,1)
                        self.acc = steer + vec(0,1)
                        self.acc = steer + vec(0,1)
                        self.acc = steer + vec(0,1)
                        self.acc = steer + vec(0,1)
                        self.acc = steer + vec(0,1)
                        self.acc = steer + vec(0,1)
                        self.acc = steer + vec(0,1)
                        
                    
                if self.zig1Count > 40:
                    self.zig1Count = 0
                self.zig1Count += 0.5
            
               
        elif self.state == 'HITSTUN' or self.state == 'DYING':
            # can't change acceleration when stunned
            pass
    
        
    def update(self):
        # change the drawing layer in relation to the player
        if self.hit_rect.top > self.game.player.hit_rect.top:
            for g in self.groups:
                g.change_layer(self, self.game.player.layer + 1)
        else:
            for g in self.groups:
                g.change_layer(self, self.game.player.layer - 1)
       
        # change the moving direction after a certain time
        now = pg.time.get_ticks()
        if now - self.walk_update > 2000:
            self.walk_update = now
            self.moveTo = choice([LEFT, RIGHT, DOWN, UP, UP, UP, UP, UP, UP, LEFT, RIGHT, LEFT, RIGHT, DOWN,DOWN,DOWN,DOWN,DOWN,DOWN])
        
        # calculate acceleration
        self.move()
        if self.game.pistolpick == True:
            self.drop_rates['Pistol'] = 0
        elif self.game.machinegunpick == True:
            self.drop_rates['Pistol'] = 20
        # add acceleration to velocity
        
        self.vel += self.acc
               
        if self.state != 'HITSTUN':
            # reset acceleration
            self.acc *= 0
             # apply friction
            self.vel *= (1 - self.friction)
    
            # cap speed at maximum
            if self.vel.length_squared() > self.maxSpeed ** 2:
                self.vel.scale_to_length(self.maxSpeed)
        
        # add velocity to position
        self.pos += self.vel
        
        # update the position
        self.rect = self.image.get_rect()
        self.hitbox = self.rect.inflate(2,2)
        self.rect.center = self.pos
        self.hitbox.center = self.pos
        if self.game.player.state == 'IDLE':
            self.state = 'IDLE'
        if self.game.player.state == 'WALKING':
            self.state = 'WALKING'
            
        # collision with walls
        self.hit_rect.centerx = self.pos.x
        fn.collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        fn.collide_with_walls(self, self.game.walls, 'y')
        if fn.collide_with_walls(self, self.game.walls, 'y') or fn.collide_with_walls(self, self.game.walls, 'x'):
            self.walk_update = now
            a = choice([LEFT, RIGHT, DOWN, UP, UP, UP, UP, UP, UP, LEFT, RIGHT, LEFT, RIGHT, DOWN,DOWN,DOWN,DOWN,DOWN,DOWN])
            if a != self.lastdir:
                self.moveTo == a 
        
        # restrain position to stay in the room
        self.pos.x = fn.clamp(self.pos.x, st.TILESIZE * 2, 
                              st.WIDTH - st.TILESIZE * 2)
        self.pos.y = fn.clamp(self.pos.y, st.GUI_HEIGHT + st.TILESIZE * 2, 
                              st.HEIGHT - st.TILESIZE * 2)

        # position the hitbox at the bottom of the image
        self.hitbox.midbottom  = self.hit_rect.midbottom
        
        self.collide_with_player()
        if self.hp <= 0 and self.state != 'DYING':
            #self.destroy()
            self.vel *= 0
            self.anim_speed = 100
            self.state = 'DYING'
        self.animate()
        dist = self.game.player.rect.center - self.pos
        arrr = randint(1,100)
        if arrr in range (1,50):
            self.timer += 1
            if self.timer >= self.shoot_time and self.game.player.MoveCheck == True:
                self.state = 'FIRING'
                self.timer = 0
                pos = self.pos + (dist.normalize() * st.TILESIZE)
                Mbossbullet(self.game, self, pos)
                self.game.soundLoader.snd['Laser01'].play()
                self.state = 'WALKING'
            
            
              
    def animate(self):
        now = pg.time.get_ticks()
        if (self.state == 'WALKING' or self.state == 'SEEK') and self.game.player.MoveCheck == True:
            if now - self.anim_update > 500:
                self.anim_update = now
                self.current_frame = (self.current_frame + 1) % len(
                                      self.walk_frames[LEFT])
                self.image = self.walk_frames[(self.lastdir.x, 
                            self.lastdir.y)][self.current_frame]
                self.angle_to_player = math.degrees(math.atan2(self.pos.x-self.game.player.pos.x,self.pos.y-self.game.player.pos.y))
                self.angleee = self.angle_to_player
                if self.lastdir == vec(DOWN):
                    self.angle_to_player = self.angle_to_player + 180
                elif self.lastdir == vec(LEFT):
                    self.angle_to_player = self.angle_to_player - 90
                elif self.lastdir == vec(RIGHT):
                    self.angle_to_player = self.angle_to_player + 90
                else:
                    self.angle_to_player = self.angle_to_player
                
                self.image = pg.transform.rotozoom(self.image, self.angle_to_player, 1)
                    
        elif self.state == 'HITSTUN':
            # flicker to indicate damage
            try:
                pass
            except:
                self.state = 'WALKING'
                      
        elif self.state == 'IDLE':
            self.image = self.idle_frames[(self.lastdir.x, self.lastdir.y)][0]
            self.angle_to_player = math.degrees(math.atan2(self.pos.x-self.game.player.pos.x,self.pos.y-self.game.player.pos.y))
            if self.lastdir == vec(DOWN):
                self.angle_to_player = self.angle_to_player + 180
            elif self.lastdir == vec(LEFT):
               self. angle_to_player = self.angle_to_player - 90
            elif self.lastdir == vec(RIGHT):
                self.angle_to_player = self.angle_to_player + 90
            else:
                self.angle_to_player = self.angle_to_player
            self.image = pg.transform.rotozoom(self.image, self.angle_to_player, 1)
                
        
        elif self.state == 'DYING':
            self.destroy()
            
        elif self.state == 'SWORD':
            self.image = self.game.imageLoader.item_img['sword']
            
            
                    
    def collide_with_player(self):
        keys = pg.key.get_pressed()
        if self.state == 'DYING':
            return
        
        # detect collision with player
        player = self.game.player
        if fn.collide_hit_rect(player, self):
                player.knockback(self, self.kb_time, self.kb_intensity)
                player.hp -= self.damage
            
            
    
    def knockback(self, other, time, intensity):
        if self.state != 'HITSTUN':
            self.vel *= 0
            # calculate vector from other to self
            knockdir = self.pos - other.pos
            if knockdir.length_squared() > 0:
                knockdir = knockdir.normalize()
                self.acc = knockdir * intensity
            else:
                self.acc *= 0
            self.state = 'HITSTUN'
            self.lastimage = self.image.copy()
            self.damage_alpha = iter(st.DAMAGE_ALPHA * time)
    
    def destroy(self):
        self.dropItem()
        self.kill()

            
        
    def updateData(self):
        self.data['x'] = self.pos.x
        self.data['y'] = self.pos.y
        
    
    def dropItem(self):
        # drop an item based on the weighted probability
        if hasattr(self, 'drop_rates'):
            items = list(self.drop_rates.keys())
            weights = list(self.drop_rates.values())
    
            c = choices(items, weights)[0]
             
            try:
                Item.drop(c, self.game, self.pos)
            except:
                print('error. cannot drop item', c)

class Enemy01(Enemy):
 
    def __init__(self, game, pos, *args, **kwargs):
        self.name = 'Enemy'
        self.image_strip = game.imageLoader.enemy_img[self.name]
        self.walk_frames = {
            UP: [self.image_strip[0][0],self.image_strip[0][1],self.image_strip[0][2],self.image_strip[0][3]],
            DOWN: [self.image_strip[1][0],self.image_strip[1][1],self.image_strip[1][2],self.image_strip[1][3]],
            LEFT: [self.image_strip[2][0],self.image_strip[2][1],self.image_strip[2][2],self.image_strip[2][3]],
            RIGHT: [self.image_strip[3][0],self.image_strip[3][1],self.image_strip[3][2],self.image_strip[3][3]]}
        self.idle_frames = {
            UP: [self.image_strip[0][0]],
            DOWN: [self.image_strip[1][0]], 
            LEFT: [self.image_strip[2][0]],
            RIGHT: [self.image_strip[3][0]]}
        super().__init__(game, pos)
        self.image = self.idle_frames[UP][0]
        self.kb_time = 1
        self.kb_intensity = 0.5
        self.hp = 12
        self.state = 'SEEK'
        self.maxSpeed = 2
        self.speed = 1
        self.anim_speed = 300
        self.drop_rates = {'none':100,'heart':50}
        self.hit_rect = pg.Rect(0, 0, int(30), int(30))
        self.timer = 0
        self.shoot_time = 1.5 * st.FPS
        self.stun_timer = 0
        self.attack_update = 0
        
    def update(self):
        # change the drawing layer in relation to the player
        if self.hit_rect.top > self.game.player.hit_rect.top:
            for g in self.groups:
                g.change_layer(self, self.game.player.layer + 1)
        else:
            for g in self.groups:
                g.change_layer(self, self.game.player.layer - 1)
       
        # change the moving direction after a certain time
        now = pg.time.get_ticks()
        if now - self.walk_update > 2000:
            self.walk_update = now
            self.moveTo = choice([LEFT, RIGHT, DOWN, UP])
            
        if self.state == 'SWORD':
            self.hit_rect = pg.Rect(0, 0, int(2), int(2))
        else:
            self.hit_rect = pg.Rect(0, 0, int(30), int(30))
        # calculate acceleration
        self.move()
        # add acceleration to velocity
        
        self.vel += self.acc
               
        if self.state != 'HITSTUN':
            # reset acceleration
            self.acc *= 0
             # apply friction
            self.vel *= (1 - self.friction)
    
            # cap speed at maximum
            if self.vel.length_squared() > self.maxSpeed ** 2:
                self.vel.scale_to_length(self.maxSpeed)
        
        # add velocity to position
        self.pos += self.vel
        
        # update the position
        self.rect = self.image.get_rect()
        self.hitbox = self.rect.inflate(2,2)
        self.rect.center = self.pos
        self.hitbox.center = self.pos

        if self.state != 'WALKING':
            if self.game.player.state == 'WALKING':
                self.state = 'SEEK'
            if self.game.player.state == 'IDLE':
                self.state = 'IDLE'
            if self.game.player.state == 'HITSTUN':
                self.state = 'IDLE'
        
                
            
        # collision with walls
        self.hit_rect.centerx = self.pos.x
        fn.collide_with_walls(self, self.game.walls, 'x')
        fn.collide_with_walls(self, self.game.enemies, 'x')
        self.hit_rect.centery = self.pos.y
        fn.collide_with_walls(self, self.game.walls, 'y')
        fn.collide_with_walls(self, self.game.enemies, 'y')
        if fn.collide_with_walls(self, self.game.walls, 'y') or fn.collide_with_walls(self, self.game.walls, 'x'):
            self.walk_update = now
            a = choice([LEFT, RIGHT, DOWN, UP])
            if a != self.lastdir:
                self.moveTo == a
                    
        # restrain position to stay in the room
        self.pos.x = fn.clamp(self.pos.x, st.TILESIZE * 2, 
                              st.WIDTH - st.TILESIZE * 2)
        self.pos.y = fn.clamp(self.pos.y, st.GUI_HEIGHT + st.TILESIZE * 2, 
                              st.HEIGHT - st.TILESIZE * 2)

        # position the hitbox at the bottom of the image
        self.hitbox.midbottom  = self.hit_rect.midbottom
        
            
        self.collide_with_player()
        if self.hp <= 0 and self.state != 'DYING':
            #self.destroy()
            self.vel *= 0
            self.anim_speed = 300
            self.state = 'DYING'
        
        
        self.poss = (self.game.player.pos - self.pos)
        if self.poss.length_squared() < 2000 and self.game.player.MoveCheck:
            self.state = 'SWORD'
        
        
        self.animate()  
        if self.state == 'SWORD':
            self.SwordWeapon.use()
            self.attack_update += 1
            if self.attack_update > self.SwordWeapon.cooldown:
                self.attack_update = 0
                self.SwordWeapon.reset()
        
            
            
        
class Mboss(Enemy):
    def __init__(self, game, pos, *args, **kwargs):
        self.name = 'Mboss'
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
        
        super().__init__(game, pos)
        self.image = self.idle_frames[UP][0]
        self.state = 'WALKING'
        self.kb_time = 1
        self.kb_intensity = 1
        self.hp = 6
        self.maxSpeed = 0.8
        self.anim_speed = 300
        self.drop_rates = {'none':100,'Pistol': 20}
        self.hit_rect = pg.Rect(0, 0, int(30), 
                                int(30))
        self.timer = 0
        self.shoot_time = 1.5* st.FPS
        self.stun_timer = 0
        
class Boss(Enemy):
    def __init__(self, game, pos, *args, **kwargs):
        self.name = 'Boss'
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
        self.hit_image = self.idle_frames[UP][0]
        super().__init__(game, pos)
        self.image = self.idle_frames[UP][0]
        self.state = 'WALKING'        
        self.hit_rect = pg.Rect((0, 0), (int(30),int(30)))
        self.hit_rect.center = self.rect.center
        self.damage = 0.5
        self.hp = 8
        self.drop_rates = {'none':100,'MachineGun': 20}
        # knockback stats
        self.kb_time = 1
        self.kb_intensity = 2
        self.maxSpeed = 1
        self.timer = 0
        self.shoot_time = 1*st.FPS
        self.stun_timer = 0
    def update(self):
        # change the drawing layer in relation to the player
        if self.hit_rect.top > self.game.player.hit_rect.top:
            for g in self.groups:
                g.change_layer(self, self.game.player.layer + 1)
        else:
            for g in self.groups:
                g.change_layer(self, self.game.player.layer - 1)
       
        # change the moving direction after a certain time
        now = pg.time.get_ticks()
        if now - self.walk_update > 2000:
            self.walk_update = now
            self.moveTo = choice([LEFT, RIGHT, DOWN, UP, UP, UP, UP, UP, UP, LEFT, RIGHT, LEFT, RIGHT, DOWN,DOWN,DOWN,DOWN,DOWN,DOWN])
        
        # calculate acceleration
        self.move()
        if self.game.pistolpick == True:
            self.drop_rates['Pistol'] = 0
            self.drop_rates['MachineGun'] = 20
        elif self.game.machinegunpick == True:
            self.drop_rates['Pistol'] = 0
            self.drop_rates['MachineGun'] = 0
            
        # add acceleration to velocity
        self.vel += self.acc
               
        if self.state != 'HITSTUN':
            # reset acceleration
            self.acc *= 0
             # apply friction
            self.vel *= (1 - self.friction)
    
            # cap speed at maximum
            if self.vel.length_squared() > self.maxSpeed ** 2:
                self.vel.scale_to_length(self.maxSpeed)
        
        # add velocity to position
        self.pos += self.vel
        
        # update the position
        self.rect = self.image.get_rect()
        self.hitbox = self.rect.inflate(2,2)
        self.rect.center = self.pos
        self.hitbox.center = self.pos
        if self.game.player.state == 'IDLE':
            self.state = 'IDLE'
        if self.game.player.state == 'WALKING':
            self.state = 'WALKING'
            
        # collision with walls
        self.hit_rect.centerx = self.pos.x
        fn.collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        fn.collide_with_walls(self, self.game.walls, 'y')
        if fn.collide_with_walls(self, self.game.walls, 'y') or fn.collide_with_walls(self, self.game.walls, 'x'):
            self.walk_update = now
            a = choice([LEFT, RIGHT, DOWN, UP, UP, UP, UP, UP, UP, LEFT, RIGHT, LEFT, RIGHT, DOWN,DOWN,DOWN,DOWN,DOWN,DOWN])
            if a != self.lastdir:
                self.moveTo == a 
        
        # restrain position to stay in the room
        self.pos.x = fn.clamp(self.pos.x, st.TILESIZE * 2, 
                              st.WIDTH - st.TILESIZE * 2)
        self.pos.y = fn.clamp(self.pos.y, st.GUI_HEIGHT + st.TILESIZE * 2, 
                              st.HEIGHT - st.TILESIZE * 2)

        # position the hitbox at the bottom of the image
        self.hitbox.midbottom  = self.hit_rect.midbottom
        
        self.collide_with_player()
        if self.hp <= 0 and self.state != 'DYING':
            #self.destroy()
            self.vel *= 0
            self.anim_speed = 100
            self.state = 'DYING'
        self.animate()
        dist = self.game.player.rect.center - self.pos
        self.timer += 1
        a = randint(1,100)
        if a in range(1,5):
            self.state = 'FIRING'
        if self.state == 'FIRING' and self.game.player.MoveCheck == True:
            self.timer = 0
            pos = self.pos + (dist.normalize() * st.TILESIZE)
            Bossbullet(self.game, self, pos)
            if self.timer >= self.shoot_time:
                self.state = 'WALKING'
    
    
        
   
            
class Effect(pg.sprite.Sprite):
    '''
    Sprite that plays an animation from a given image list
    and then destroys itself
    '''
    def __init__(self, game,  pos, images, delay):
        self.group = game.all_sprites
        pg.sprite.Sprite.__init__(self)
        self.layer = 0
        self.group.add(self, layer=self.layer)
        self.game = game

        self.timer = 0
        self.frame = 0
        self.images = images
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.game = game
        self.pos = pos
        self.delay = delay
        self.end = False
        
        
    def update(self):
        self.rect.center = self.pos
        now = pg.time.get_ticks()      
        if self.frame == len(self.images):
            self.kill()
            self.end = True
        if now - self.timer > self.delay:
            self.timer = now
            self.image = self.images[self.frame]
            self.frame = self.frame + 1
            
            
    
class Explosion(Effect):
    '''
    Effect that also damages enemies or the player
    '''
    def __init__(self, game,  pos, images, delay, **kwargs):
        super().__init__(game,  pos, images, delay)
        self.damage = kwargs['damage']
        if 'hit_rect' in kwargs:
            # define custom hit rect
            self.hit_rect = kwargs['hit_rect']
        else:    
            self.hit_rect = self.image.get_rect()
        
        self.hit_rect.center = self.rect.center
        if 'sound' in kwargs:
            kwargs['sound'].play()
            
            
    def update(self):
        self.rect.center = self.pos
        now = pg.time.get_ticks()      
        if self.frame == len(self.images):
            self.kill()
            self.end = True
        if now - self.timer > self.delay:
            self.timer = now
            self.image = self.images[self.frame]
            self.frame = self.frame + 1
            
        player = self.game.player
        if fn.collide_hit_rect(player, self):
            if (player.state != 'HITSTUN'):
                player.knockback(self, 1, 0.5)
                player.hp -= self.damage
                
        # collision with enemies
        hits = pg.sprite.spritecollide(self, self.game.enemies, False, 
                                       fn.collide_hit_rect)
        if hits:
            for enemy in hits:
                if enemy.state != 'HITSTUN':
                    enemy.hp -= self.damage
                    enemy.knockback(self, 1, 0.5)
                    
  
    
                
        

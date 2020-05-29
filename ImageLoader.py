import pygame
import os
import traceback

import Config as cfg

class ImageLoader:
    """This class loads all asset images before the game begins.

    """
    def __init__(self, game):
        """__init__ method for ImageLoader class

        Args:
            game (<class 'Integrate.Game'>): Integrate.Game class object.

        """
        self.game = game
        self.tileset_file = ['tiles/wall.png', 'tiles/floor1.png', 'tiles/floor2.png']


    def create_tileset(self, filenames, size_w, size_h, alpha=False):
        """ImageLoader class method to set tiles in a room according to data.
           0 for wall
           1 for floor1
           2 for floor2

        Args:
            filenames (str): list of filenames of the tileset image.
            size_w (int): width of a tile.
            size_h (int): height of a tile.
            alpha (bool): True or False.

        Returns:
            tilset (<class 'list'> of tiles): List of tiles in a room.

        """
        tileset=[]
        for filename in filenames:

            file = os.path.join(cfg.IMAGE_FOLDER, filename)
            try:
                img = pygame.image.load(file).convert()
                if alpha:
                    color = img.get_at((0,0))
                    img.set_colorkey(color)
            except Exception:
                traceback.print_exc()
                return

            tileset.append(img)
        
        return tileset


    def load_image(self, filename, scale=1):
        """ImageLoader class method to load images.

        Args:
            filename (str): filename of the image.
            scale (int): scale of image.

        Returns:
            surface (<class 'pygame.Surface'>): pygame.Surface object.

        """
        file = os.path.join(cfg.IMAGE_FOLDER, filename)

        try:
            img = pygame.image.load(file).convert_alpha()
            new_size = (int(img.get_width() * scale), int(img.get_height() * scale))
            surface = pygame.transform.scale(img, new_size)
            return surface

        except Exception:
            traceback.print_exc()
            return     


    def extract_images_from_sprite(self, filename, width, height, startpos, number, size=cfg.TILESIZE):
        """ImageLoader class method to split sprites into multiple images.

        Args:
            filename (str): filename of the image.
            width (int): width of image.
            height (int): height of image.
            startpos (int): position where to start extracting images from sprite.
            number (int): number of images in the sprite
            size (int): single tile size

        Returns:
            images (<class 'list'> of <class 'pygame.Surface'>): list of pygame.Surface object.

        """
        file = os.path.join(cfg.IMAGE_FOLDER, filename)
        try:
            # loading the sprite
            img = pygame.image.load(file).convert_alpha()
            img_set = []

            # splitting sprite into multiple images
            for i in range(startpos, (startpos + number)):
                rect = ((i * width, 0), (width, height))
                if size != cfg.TILESIZE:
                    subimg = pygame.transform.scale(img.subsurface(rect), (size, size))
                else:
                    subimg = img.subsurface(rect)
                img_set.append(subimg)
            return img_set

        except Exception:
            traceback.print_exc()
            return

    def load_player_images(self):
        """ImageLoader class method to load all images related to player moving.

        """
        # Loading assets for player moving with pistol
        plyr_mv_up_pist_imgs = self.extract_images_from_sprite('player/Pistol-moving.png', 195, 195, 0, 6, 100)
        
        plyr_mv_left_pist_imgs = []
        for i in plyr_mv_up_pist_imgs:
            a = pygame.transform.rotozoom(i,90,1)
            plyr_mv_left_pist_imgs.append(a)

        plyr_mv_right_pist_imgs = []
        for i in plyr_mv_up_pist_imgs:
            a = pygame.transform.rotozoom(i,-90,1)
            plyr_mv_right_pist_imgs.append(a)
            
        plyr_mv_down_pist_imgs = []
        for i in plyr_mv_up_pist_imgs:
            a = pygame.transform.rotozoom(i,-180,1)
            plyr_mv_down_pist_imgs.append(a)

        # Loading assets for player moving with machine gun
        plyr_mv_up_machine_imgs = self.extract_images_from_sprite('player/Machine-gun-moving.png', 195, 195, 0, 6, 100)
        
        plyr_mv_left_machine_imgs = []
        for i in plyr_mv_up_machine_imgs:
            a = pygame.transform.rotozoom(i,90,1)
            plyr_mv_left_machine_imgs.append(a)
        plyr_mv_right_machine_imgs = []
        for i in plyr_mv_up_machine_imgs:
            a = pygame.transform.rotozoom(i,-90,1)
            plyr_mv_right_machine_imgs.append(a)
        plyr_mv_down_machine_imgs = []
        for i in plyr_mv_up_machine_imgs:
            a = pygame.transform.rotozoom(i,-180,1)
            plyr_mv_down_machine_imgs.append(a)

        # setting up player_img attribute with image lists
        self.player_img = {
            'PwalkU': plyr_mv_up_pist_imgs,
            'PwalkD': plyr_mv_down_pist_imgs,
            'PwalkL': plyr_mv_left_pist_imgs,
            'PwalkR': plyr_mv_right_pist_imgs,

            'MwalkU': plyr_mv_up_machine_imgs,
            'MwalkD': plyr_mv_down_machine_imgs,
            'MwalkL': plyr_mv_left_machine_imgs,
            'MwalkR': plyr_mv_right_machine_imgs
            }


    def load_enemy_images(self):
        """ImageLoader class method to load all images related to enemy moving.

        """
        # Loading assets for enemy moving with pistol
        enemy_mv_up_pist_imgs = self.extract_images_from_sprite('enemy/enemy pistol walk.png', 120, 120, 0, 6, 60)
        
        enemy_mv_left_pist_imgs = []
        for i in enemy_mv_up_pist_imgs:
            a = pygame.transform.rotozoom(i,90,1)
            enemy_mv_left_pist_imgs.append(a)
            
        enemy_mv_right_pist_imgs = []
        for i in enemy_mv_up_pist_imgs:
            a = pygame.transform.rotozoom(i,-90,1)
            enemy_mv_right_pist_imgs.append(a)
            
        enemy_mv_down_pist_imgs = []
        for i in enemy_mv_up_pist_imgs:
            a = pygame.transform.rotozoom(i,-180,1)
            enemy_mv_down_pist_imgs.append(a)

        # Loading assets for enemy moving with machine gun
        enemy_mv_up_machine_imgs = self.extract_images_from_sprite('enemy/enemy machinegun walk.png', 120, 120, 0, 6, 60)
        
        enemy_mv_left_machine_imgs = []
        for i in enemy_mv_up_machine_imgs:
            a = pygame.transform.rotozoom(i,90,1)
            enemy_mv_left_machine_imgs.append(a)
            
        enemy_mv_right_machine_imgs = []
        for i in enemy_mv_up_machine_imgs:
            a = pygame.transform.rotozoom(i,-90,1)
            enemy_mv_right_machine_imgs.append(a)
            
        enemy_mv_down_machine_imgs = []
        for i in enemy_mv_up_machine_imgs:
            a = pygame.transform.rotozoom(i,-180,1)
            enemy_mv_down_machine_imgs.append(a)

        # Loading assets for enemy moving with sword
        enemy_mv_up_sword_imgs = self.extract_images_from_sprite('enemy/enemy sword run.png', 150, 150, 0, 4, 80)
        
        enemy_mv_left_sword_imgs = []
        for i in enemy_mv_up_sword_imgs:
            a = pygame.transform.rotozoom(i,90,1)
            enemy_mv_left_sword_imgs.append(a)
            
        enemy_mv_right_sword_imgs = []
        for i in enemy_mv_up_sword_imgs:
            a = pygame.transform.rotozoom(i,-90,1)
            enemy_mv_right_sword_imgs.append(a)
            
        enemy_mv_down_sword_imgs = []
        for i in enemy_mv_up_sword_imgs:
            a = pygame.transform.rotozoom(i,-180,1)
            enemy_mv_down_sword_imgs.append(a)

        # Loading assets for enemy swinging sword
        enemy_swing_up_sword_imgs = self.extract_images_from_sprite('enemy/enemy sword attack.png', 150, 150, 0, 8, 80)

        enemy_swing_left_sword_imgs = []
        for i in enemy_swing_up_sword_imgs:
            a = pygame.transform.rotozoom(i,90,1)
            enemy_swing_left_sword_imgs.append(a)

        enemy_swing_right_sword_imgs = []
        for i in enemy_swing_up_sword_imgs:
            a = pygame.transform.rotozoom(i,-90,1)
            enemy_swing_right_sword_imgs.append(a)

        enemy_swing_down_sword_imgs = []
        for i in enemy_swing_up_sword_imgs:
            a = pygame.transform.rotozoom(i,-180,1)
            enemy_swing_down_sword_imgs.append(a)
            
        # setting up player_img attribute with image lists
        self.enemy_img = {
            'MachineGunEnemy': [enemy_mv_up_machine_imgs, enemy_mv_down_machine_imgs, enemy_mv_left_machine_imgs, enemy_mv_right_machine_imgs],
            'PistolEnemy':[enemy_mv_up_pist_imgs, enemy_mv_down_pist_imgs, enemy_mv_left_pist_imgs, enemy_mv_right_pist_imgs],
            'SwordEnemy': [enemy_mv_up_sword_imgs, enemy_mv_down_sword_imgs, enemy_mv_left_sword_imgs, enemy_mv_right_sword_imgs]
            }

        self.item_anims = { 'sword': enemy_swing_up_sword_imgs,
                            'swordD': enemy_swing_down_sword_imgs,
                            'swordL': enemy_swing_left_sword_imgs,
                            'swordR': enemy_swing_right_sword_imgs
                          }


    def load_bullet_images(self):
        """ImageLoader class method to load all types of bullets.

        """
        PlasmaShot = pygame.image.load(os.path.join(cfg.IMAGE_FOLDER,'bullets/plasmaShot.png'))
        BulletRed = pygame.image.load(os.path.join(cfg.IMAGE_FOLDER,'bullets/bullet red.png'))
        BlueShot = pygame.image.load(os.path.join(cfg.IMAGE_FOLDER,'bullets/bullet blue.png'))
        BlueShot = pygame.transform.scale(BlueShot, (20, 20))
        BulletRed = pygame.transform.scale(BulletRed, (20, 20))
        LaserRed = pygame.image.load(os.path.join(cfg.IMAGE_FOLDER,'bullets/Laser red.png'))
        LaserBlue = pygame.image.load(os.path.join(cfg.IMAGE_FOLDER,'bullets/Laser blue.png'))
        LaserBlue = pygame.transform.scale(LaserBlue, (40, 40))
        LaserRed = pygame.transform.scale(LaserRed, (40, 40))
        
        MACHINEShot = pygame.image.load(os.path.join(cfg.IMAGE_FOLDER,'bullets/bullet blue.png'))
        EnemyBullet = pygame.transform.scale(PlasmaShot, (5, 5))
        tempBullet = pygame.transform.scale(PlasmaShot, (1, 1))
        PlayerBullet = pygame.transform.scale(BlueShot, (6, 6))
        MACHINEBullet = pygame.transform.scale(MACHINEShot, (5, 15))
        
        EnemyPistolBullet = pygame.transform.scale(PlasmaShot, (20, 20))
        EnemyMachineGunBullet = pygame.transform.scale(PlasmaShot, (40, 40))
        MGun = pygame.image.load(os.path.join(cfg.IMAGE_FOLDER,'guns/MachineGun.png'))
        MGun  = pygame.transform.scale(MGun, (30, 20))
        PGun = pygame.image.load(os.path.join(cfg.IMAGE_FOLDER,'guns/Pistol.png'))
        PGun = pygame.transform.scale(PGun, (30, 20))
        PGun2 = pygame.transform.scale(PGun, (2, 2))
        HeartP = pygame.image.load(os.path.join(cfg.IMAGE_FOLDER,'others/Heart.png'))
        HeartP = pygame.transform.scale(HeartP, (20, 16))
        MBULL = self.extract_images_from_sprite('bullets/MBull.png', 16, 19, 0, 3)
        
        self.item_img = {
            'tempb' : tempBullet,
            'Pbullet': LaserBlue,
            'Mbullet': BlueShot,
            'EnemyBullet' : EnemyBullet,
            'EnemyPistolBullet' : LaserRed,
            'EnemyMachineGunBullet' :  BulletRed,
            'heart': HeartP,
            'MachineGun' : MGun,
            'Pistol' : PGun,
            'sword': PGun2
            }
        


    def load_cursor_images(self):
        """ImageLoader class method to load all images of cursor.

        """
        self.CursorMain = pygame.image.load(os.path.join(cfg.IMAGE_FOLDER,'others/Cursor.png'))
        self.CursorMain1 = pygame.transform.scale(self.CursorMain, (40, 40))

        cursor_image_files = [  'others/Cursor_1.png', 'others/Cursor_2.png', 'others/Cursor_3.png', 'others/Cursor_4.png',
                                'others/Cursor_5.png', 'others/Cursor_6.png', 'others/Cursor_6.png', 'others/Cursor_8.png' ]
        self.cursor = []
        for image_file in cursor_image_files:
            cursor_img = pygame.image.load(os.path.join(cfg.IMAGE_FOLDER, image_file))
            cursor_img = pygame.transform.scale(cursor_img, (40, 40))
            self.cursor.append(cursor_img)
        

    def load_door_images(self):
        """ImageLoader class method to load all images of doors.

        """
        door_NS = pygame.image.load(os.path.join(cfg.IMAGE_FOLDER,'tiles/NSdoor.png'))
        door_EW = pygame.image.load(os.path.join(cfg.IMAGE_FOLDER,'tiles/EWdoor.png'))
        
        self.door_image_dict = {'W': door_EW,
                                'N': door_NS,
                                'E': door_EW,
                                'S': door_NS}


    def load_room_images(self):
        """ImageLoader class method to load all images of rooms.

        """
        self.room_img = self.extract_images_from_sprite('others/minimap_strip_7x5.png', 7, 5, 0, 20)
        
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

    def load_other_assets(self):
        """ImageLoader class method to load all other images.

        """
        self.tileset = self.create_tileset(self.tileset_file, 40, 40)
        self.tileset_image = self.load_image(self.tileset_file[0], 1)

        self.solid_img ={ 'block': pygame.image.load(os.path.join(cfg.IMAGE_FOLDER,'tiles/box.png')),
                          'crate': pygame.image.load(os.path.join(cfg.IMAGE_FOLDER,'tiles/explosive tank.png')),
                        }
        self.solid_img['block'] = pygame.transform.scale(self.solid_img['block'], (40, 40))
        self.solid_img['crate'] = pygame.transform.scale(self.solid_img['crate'], (36, 36))

        self.effects = {'crate_explosion': self.extract_images_from_sprite('others/explosion.png', 32, 32, 0, 7, 150)}

        self.gui_img =  {'health': self.load_image('others/health_string.png'),
                         'hearts': self.extract_images_from_sprite('others/hearts_strip.png', 8, 8, 0, 6)
                        }

        self.WarnSign = pygame.image.load(os.path.join(cfg.IMAGE_FOLDER,'others/warning.png'))
        self.WarnSign = pygame.transform.scale(self.WarnSign, (100, 20))

        self.WarnSign2 = pygame.image.load(os.path.join(cfg.IMAGE_FOLDER,'others/WarnSign3.png'))
        self.WarnSign2 = pygame.transform.scale(self.WarnSign2, (100, 20))

        self.font = cfg.FONT
        self.font1 = pygame.font.Font(os.path.join(cfg.FONT_FOLDER,'slkscr.ttf'),20)
        self.font2 = pygame.font.Font(os.path.join(cfg.FONT_FOLDER,'slkscrb.ttf'),30)
        self.GameOverImg = pygame.image.load(os.path.join(cfg.IMAGE_FOLDER,'others/GameOver.png'))
        self.WinImg = pygame.image.load(os.path.join(cfg.IMAGE_FOLDER,'others/Win.png'))
        Icon1 = pygame.image.load(os.path.join(cfg.IMAGE_FOLDER,'others/icon.png'))
        self.Icon = boss_strip = pygame.transform.scale(Icon1, (20, 20))
        

    
    def load_assets(self):
        """ImageLoader class method to load all assets.

        """
        self.load_player_images()
        self.load_enemy_images()
        self.load_bullet_images()
        self.load_cursor_images()
        self.load_door_images()
        self.load_room_images()
        self.load_other_assets()
        

        

        

        

        
        


        
        
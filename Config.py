import pygame
from os import path
from random import choice

vec = pygame.math.Vector2

# GAME WINDOW CONFIGURATIONS
SCREEN_SCALE = 1
TILESIZE = 40
TILESIZE_SMALL = 20
TILES_W = 20
TILES_H = 20
GUI_MARGIN = 1
GUI_HEIGHT = 80
WIDTH = 800
HEIGHT = 600 + GUI_HEIGHT
S_WIDTH = WIDTH * SCREEN_SCALE
S_HEIGHT = HEIGHT * SCREEN_SCALE

# FILE PATHS FOR ASSSETS
FONT_FOLDER = './assets/fonts'
IMAGE_FOLDER = './assets/images'
ROOM_FOLDER = './assets/rooms'
SOUND_FOLDER = './assets/sounds'

 
# INGAME CONFIGURATIONS
DUNGEON_SIZE = (5, 5)
SCROLLSPEED = 8
SCROLLSPEED_MENU = 14
FPS = 60
FONT = path.join(FONT_FOLDER, 'slkscr.TTF')
TITLE = ('Momentus Proto')
SFX_VOL = 0.2
MU_VOL = 0.5
KEY_DELAY = 150

# PLAYER CONFIGURATIONS
PLAYER_MAXSPEED = 4
PLAYER_ACC = 0.5
PLAYER_FRICTION = 0.5
PLAYER_HIT_RECT = pygame.Rect(0, 0, int(TILESIZE * 0.8), int(TILESIZE * 0.6))
PLAYER_HP_START = 7.0
PLAYER_HP_MAX = 14.0
PLAYER_HP_ROW = 7

# ROOMS CONFIGURATIONS
ROOMS = {
    'N': ['NS', 'NS', 'NS', 'NS', 'S', 'S', 'S', 'WS', 'ES', 'SWE', 'NSW', 'NSE'],
    'W': ['WE', 'WE', 'WE', 'WE', 'E', 'E', 'E', 'ES', 'EN', 'SWE', 'NSE', 'NWE'],
    'E': ['WE', 'WE', 'WE', 'WE', 'W', 'W', 'W', 'WS', 'WN', 'SWE', 'NSW', 'NWE'],
    'S': ['NS', 'NS', 'NS', 'NS', 'N', 'N', 'N', 'WN', 'EN', 'NSE', 'NSW', 'NWE']
    }

DOOR_POSITIONS = {
    'N': (320, 3.2),
    'S': (320, 558),
    'W': (3, 240),
    'E': (758, 240)
    }


# TMX FILE CONFIGURATIONS
TILEMAP_FILES = [1, 2, 5, 8, 9, 10, 11, 12, 13, 14, 15]

# EFFECTS CONFIGURATIONS
DAMAGE_ALPHA = [i for i in range(0, 255, 15)]

# COLOR CONFIGURATIONS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
PINK = (255, 0, 255)
TRANS = (0, 0, 0, 0)
DARKGREY = (100, 100, 100)

# KEYS CONFIGURATIONS
KEY_A = (1,0,0)
KEY_B = pygame.K_LCTRL
KEY_MENU = pygame.K_ESCAPE
KEY_UP = pygame.K_w
KEY_DOWN = pygame.K_s
KEY_LEFT = pygame.K_a
KEY_RIGHT = pygame.K_d
KEY_ENTER = pygame.K_RETURN




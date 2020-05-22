import pygame as pg
from os import path
from random import choice

vec = pg.math.Vector2

# window settings and constants
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

# file paths
directory = path.join(path.dirname(__file__), '..')

FONT_FOLDER = 'fonts'
IMAGE_FOLDER = 'images'
ROOM_FOLDER = 'rooms'
SOUND_FOLDER = 'sounds'

 
# ingame settings
DUNGEON_SIZE = (5, 5)
SCROLLSPEED = 8
SCROLLSPEED_MENU = 14
FPS = 60
FONT = path.join(FONT_FOLDER, 'slkscr.TTF')
TITLE = ('Momentus Proto')

SFX_VOL = 0.2
MU_VOL = 0.5

KEY_DELAY = 150

# player settings
PLAYER_MAXSPEED = 4
PLAYER_ACC = 0.5
PLAYER_FRICTION = 0.5
PLAYER_HIT_RECT = pg.Rect(0, 0, int(TILESIZE * 0.8), int(TILESIZE * 0.6))

# player hp 
PLAYER_HP_START = 7.0
PLAYER_HP_MAX = 14.0
PLAYER_HP_ROW = 7

# possible rooms for picking
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


# list of tmx file numbers to pick from
TILEMAP_FILES = [1, 2, 5, 8, 9, 10, 11, 12, 13, 14, 15]


TM_POOL = []
def randomizeRooms():
    for i in range(DUNGEON_SIZE[0] * DUNGEON_SIZE[1]):
        TM_POOL.append(choice(TILEMAP_FILES))

# effects
DAMAGE_ALPHA = [i for i in range(0, 255, 15)]

# default colors
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



# key bindings
KEY_A = (1,0,0)
KEY_B = pg.K_LCTRL
KEY_MENU = pg.K_ESCAPE
KEY_UP = pg.K_w
KEY_DOWN = pg.K_s
KEY_LEFT = pg.K_a
KEY_RIGHT = pg.K_d
KEY_ENTER = pg.K_RETURN




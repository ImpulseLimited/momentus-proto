import pygame as pg
from os import path
import json
#import traceback
import itertools

#import functions as fn
import settings as st

vec = pg.math.Vector2

def checkFight(game):
    '''
    closes the doors and opens them when player defeats all enemies in the room
    '''
    room = game.dungeon.room_current
    if len(game.enemies) > 0:
        room.cleared = False
    else:
        if not room.shut:
            room.cleared = True
            return
    
    # check if the room's doors are closed
    if room.shut == False:
        # check player's position
        margin_x = 5 * st.TILESIZE_SMALL
        margin_y = 5.5 * st.TILESIZE_SMALL + st.GUI_HEIGHT
        rect = pg.Rect((margin_x, margin_y), (st.WIDTH - 2 *  margin_x,
                       st.HEIGHT - st.GUI_HEIGHT - margin_y))
        if rect.colliderect(game.player.hit_rect):
            # player is far enough in the room to shut the doors
            room.shutDoors()
            game.soundLoader.snd['shut'].play()
            
    else:
        if len(game.enemies) == 0:
            # if all enemies are defeated, open the doors
            room.openDoors()
            game.soundLoader.snd['fanfare1'].play()
            room.cleared = True

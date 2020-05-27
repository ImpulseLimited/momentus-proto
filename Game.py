import GameFlow
import pygame as pg
import traceback


pg.init()

if __name__ == '__main__':
    g = GameFlow.Game()
    try:
        while g.running:
            g.new()
    except Exception:
        traceback.print_exc()
    pg.quit
    


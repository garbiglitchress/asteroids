import pygame
from constants import *
class GameOverScreen():#return keys
    def __init__(self,  con_surface,screen, ast, p1):
        
        self.con_surface=con_surface
        self.screen=screen
        self.ast=ast
        self.p1=p1
    def show(self):
        self.screen.blit(self.con_surface, (SCREEN_WIDTH*.5, SCREEN_HEIGHT*.8))
        for a in self.ast:
            a.kill()
        self.p1.kill()
        
        

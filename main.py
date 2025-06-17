import pygame
from src.game import Game #import d'une classe
if __name__ == '__main__':
    pygame.init()

    game = Game() #appel de la classe
    game.run() #appel d'une fonction de la classe      
 
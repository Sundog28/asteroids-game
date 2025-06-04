# this allows us to use code from
# the open-source pygame library
# throughout this file
import pygame
from constants import *  # import all constants

def main():
    pygame.init()  # initialize pygame

    # create the game window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # game loop
    while True:
        # handle quit events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return  # exit the loop and close the game

        # fill the screen with black
        screen.fill((0, 0, 0))

        # update the display
        pygame.display.flip()

if __name__ == "__main__":
    main()

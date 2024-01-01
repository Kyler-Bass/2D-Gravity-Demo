import pygame 
import time
import random
from node import Node
from point import Point
from functions import exit_event_check, user_input



def main():

    # user input 
    GRAVITY, mass, start_ct, color = user_input()
    
    # window setup
    pygame.init()
    SCREENSIZE = (512,512)
    window = pygame.display
    screen_surface = window.set_mode(SCREENSIZE)
    window.set_caption("Gravity Demo")
    clock = pygame.time.Clock()

    # tree setup
    root = Node(color)

    # add starting points
    for i in range(start_ct):
        x = random.randint(0, SCREENSIZE[0])
        y = random.randint(0, SCREENSIZE[1])
        root.add_child(Point([x,y], mass, GRAVITY), root)

    while True:
        if exit_event_check():
            return 0
        
        # user data
        mouse_pos = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed()

        # tree update and drawing 
        root.update(mouse_pos, clicked, mass, GRAVITY, time.time())
        root.draw(screen_surface)
        root.rebuild()

        # update window and limit fps
        window.update()
        clock.tick(60)

if __name__ == "__main__":
    main()
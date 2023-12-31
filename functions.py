# standalone functions in here
import pygame

def exit_event_check():
    """Check if user clicked the (x) exit button, and what to do when they clicked it"""
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            return True

def user_input():
    print('\n')
    print("Welcome to my demo. This demo is of the effects of gravity on small objects by bigger objects.")
    print("You can give a starting amount of small objects and also click on the screen at any time to spawn one in.")
    print("You will be asked to input the parameters used to show this demonstration.")
    print("You do not have to fill in all of them, or any of them if you don't want to, they all have defaults.")
    print("Some suggestions: \n -Gravitational Constant: no lower than 0.001\n -Center Object Mass: no lower than 5x the small object mass\n -Amount of smaller objects: ~200\n")
    grav = float(input("Gravitational Constant: "))
    center_mass = float(input("Center Object Mass: "))
    small_obj_mass = float(input("Small Object Mass: "))
    small_obj_ct = int(input("Amount of Smaller Objects: "))
    small_color = input("Small Object Color: ")
    center_color = input("Center Object Color: ")
    center_pos = input("Center Object Position (x,y) from top left of screen: ")
    return grav, center_mass, small_obj_mass, small_obj_ct, small_color, center_color, center_pos
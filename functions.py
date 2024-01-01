import pygame
from node import Node

def exit_event_check():
    """Check if user clicked the (x) exit button, and what to do when they clicked it"""
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            return True


def user_input(skip=False):
    colors = {
        'white': pygame.color.Color((255,255,255)),
        'black': pygame.color.Color((0,0,0)),
        'red': pygame.color.Color((255,0,0)),
        'green': pygame.color.Color((0,255,0)),
        'blue': pygame.color.Color((0,0,255))
    }

    if not skip:
        print("\nWelcome to this 2D gravity demonstration.")
        print("You may click on the screen at any point in time to create an object.")
        print("You will be asked to input the parameters used to show this demonstration.")
        print("You do not have to fill in all of them, or any of them if you don't want to, they all have defaults.")
        print("If you do not want to fill one in, simple leave it blank and press ENTER")
    try:
        grav = input("\nGravitational Constant: ")
        obj_mass = input("Object Mass: ")
        obj_ct = input("Amount of Starting Smaller Objects: ")
        obj_color = input("Small Object Color (red, green, blue, black, white or (0-255,0-255,0-255)): ")
        if grav == "":
            grav = 0.01
        else:
            grav = float(grav)
        if obj_mass == "":
            obj_mass = 1
        else:
            obj_mass = float(obj_mass)
        if obj_ct == "":
            obj_ct = 0
        else:
            obj_ct = int(obj_ct)
        if '(' in obj_color:
            color = tuple(int(i) for i in obj_color[1:-1].split(','))
            color = pygame.color.Color(color)
        elif obj_color == "":
            color = color = pygame.color.Color((255,255,255))
        else:
            color = colors[obj_color.lower()]
            if color == 0:
                raise(ValueError)
    except:
        print("\nThere was an error with your input, please try again.")
        return user_input(skip=True)


    return grav, obj_mass, obj_ct, color
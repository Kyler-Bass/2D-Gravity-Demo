import pygame
from node import Node

def exit_event_check():
    """Check if user clicked the (x) exit button, and what to do when they clicked it"""
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            return True

def rebuild(node):
    """Rebuild the tree to reflect changes to point positions"""
    points = node.points
    root = Node(node.color)
    for point in points:
        root.add_child(point, root)
    return root 

def user_input(skip=False):
    if not skip:
        print("\nWelcome to my demo. This demo is of the effects of gravity on objects.")
        print("You can give a starting amount of small objects and also click on the screen at any time to spawn one in.")
        print("You will be asked to input the parameters used to show this demonstration.")
        print("You do not have to fill in all of them, or any of them if you don't want to, they all have defaults.")
        print("Suggestion: \n -Gravitational Constant: no lower than 0.001\n")
    try:
        grav = float(input("Gravitational Constant: "))
        obj_mass = float(input("Object Mass: "))
        obj_ct = int(input("Amount of Starting Smaller Objects: "))
        obj_color = input("Small Object Color (red, green, blue, black, white or (244,45,12)): ")
    except:
        print("\nThere was an error with your input, please try again.")
        return user_input(skip=True)

    colors = {
        'white': (255,255,255),
        'black': (0,0,0),
        'red': (255,0,0),
        'green': (0,255,0),
        'blue': (0,0,255),
        'White': (255,255,255),
        'Black': (0,0,0),
        'Red': (255,0,0),
        'Green': (0,255,0),
        'Blue': (0,0,255)
    }

    if '(' in obj_color:
        try: 
            color = tuple(int(i) for i in obj_color[1:-1].split(','))
            color = pygame.color.Color(color)
        except:
            color = pygame.color.Color((255,0,0))
    else:
        color = pygame.color.Color(colors[obj_color])
        if color == 0:
            color = pygame.color.Color((255,0,0))

    return grav, obj_mass, obj_ct, color
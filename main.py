import pygame 
from node import Node
from point import Point
from functions import exit_event_check



def main():
    pygame.init()
    window = pygame.display
    surface = window.set_mode((512,512))
    window.set_caption("Gravity Demo")
    clock = pygame.time.Clock()

    # setup root node, for testing 
    root = Node()
    root.add_child(Point([200,200], 1, 0.01), root)
    root.add_child(Point([450,450], 1, 0.01), root)
    root.add_child(Point([250,250], 10, 0.01), root)
    root.add_child(Point([400,400], 1, 0.01), root)
    root.add_child(Point([300,300], 1, 0.01), root)
    root.add_child(Point([350,350], 1, 0.01), root)


    while True:
        if exit_event_check():
            return 0
        
        surface.fill((0,0,0))
        root.set_mass()
        root.set_center_point()

        center_masses = []
        center_points = []
        for node in root.children:
            center_masses.append(node.total_mass)
            center_points.append(node.center_point)
        root.move_all(center_masses, center_points)
        root.draw(surface)
        root.remove_offscreen_points(root.size, root)
        #print(center_masses)
        #print(center_points)

        
        points = root.get_points()
        root = Node()
        for point in points:
            root.add_child(point, root)



        window.update()
        clock.tick(40)

if __name__ == "__main__":
    main()
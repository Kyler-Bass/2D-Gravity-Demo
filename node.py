import pygame 
from point import Point

class Node:
    def __init__(self, quadrant=None, parent=None, depth=None):
        if parent == None:
            self.top_left = (0,0) # where the node starts, top left of screen as (0,0)
            self.size = 512
            self.depth = 0
            # start with root node and 4 children nodes 
            self.children = [Node(0, self, self.depth), Node(1, self, self.depth), Node(2, self, self.depth), Node(3, self, self.depth)]
            self.points = []
        else:
            self.size = parent.size / 2
            if quadrant == 0:
                self.top_left = parent.top_left
            elif quadrant == 1:
                self.top_left = (parent.top_left[0] + self.size, parent.top_left[1])
            elif quadrant == 2:
                self.top_left = (parent.top_left[0], parent.top_left[1] + self.size)
            elif quadrant == 3:
                self.top_left = (parent.top_left[0] + self.size, parent.top_left[1] + self.size)
            self.children = [0,0,0,0]
            self.depth = depth + 1

        self.center_point = []
        self.total_mass = 0
        self.point_ct = 0
        self.rect = pygame.Rect(self.top_left[0], self.top_left[1], self.size, self.size)

    def check_inside(self):
        # tracking 
        Node_ct = 0
        point_ct = 0

        # recursion 
        for child in self.children: 
            if isinstance(child, Node):
                Node_ct += 1
                x,y = child.check_inside()
                Node_ct += x
                point_ct += y
            elif isinstance(child, Point):
                point_ct += 1
            elif isinstance(child, list):
                for point in child:
                    point_ct += 1
        return Node_ct, point_ct

    def add_child(self, point:Point, root):
        """Add a child point to this Node, creating more nodes if necessary"""
        # first one for x, add 0 if below, 1 if above 
        # second one for y, add 0 if below, 2 if above
        quadrant = (point.pos[0] >= self.top_left[0] + self.size/2) * 1 + (point.pos[1] >= self.top_left[1] + self.size/2) * 2
        
        if self.depth == 0:
            self.points.append(point)

        if self.children[quadrant] == 0:
            self.children[quadrant] = point
        elif isinstance(self.children[quadrant], Node):
            self.children[quadrant].add_child(point, root)
        elif isinstance(self.children[quadrant], Point):
            if self.size == 1:
                root.points.append(point.collision(self.children[quadrant], root))
            else:
                temp = Node(quadrant, self, self.depth)
                temp.add_child(self.children[quadrant], root)
                temp.add_child(point, root)
                self.children[quadrant] = temp
        elif isinstance(self.children[quadrant], list):
            self.children[quadrant].append(point)

    def draw(self, surface):
        for child in self.children:
            if isinstance(child, Node):
                child.draw(surface)
            elif isinstance(child, Point):
                pygame.draw.circle(surface, color=(255,0,0), center=child.pos, radius=1)
        pygame.draw.rect(surface, color=(255,255,255), rect=self.rect, width=1)
        if self.depth == 1:
            if self.center_point != []:
                pygame.draw.circle(surface, color=(0,255,0), center=self.center_point, radius=1)
        if self.depth == 0:
            if self.center_point != []:
                pygame.draw.circle(surface, color=(0,0,255), center=self.center_point, radius=1)

    def set_mass(self):
        total_mass = 0
        for child in self.children:
            if isinstance(child, Node):
                child.set_mass()
                total_mass += child.total_mass
            elif isinstance(child, Point):
                total_mass += child.mass
            elif isinstance(child, list):
                for point in child:
                    total_mass += point.mass

        self.total_mass = total_mass
    
    def set_center_point(self):
        xs = []
        ys = []
        masses = []
        point_ct = 0

        for child in self.children:
            if isinstance(child, Node):
                child.set_center_point()
                if child.point_ct > 0:
                    xs.append(child.center_point[0])
                    ys.append(child.center_point[1])
                    masses.append(child.total_mass)
                    point_ct += 1
            elif isinstance(child, Point):
                xs.append(child.pos[0])
                ys.append(child.pos[1])
                masses.append(child.mass)
                point_ct += 1
            elif isinstance(child, list):
                for point in child:
                    xs.append(point.pos[0])
                    ys.append(point.pos[1])
                    masses.append(point.mass)
                    point_ct += 1
        if point_ct > 0:
            total_mass = sum(masses)
            x_moments = [m * x for m,x in zip(masses,xs)]
            y_moments = [m * y for m,y in zip(masses,ys)]
            center_x = sum(x_moments) / total_mass
            center_y = sum(y_moments) / total_mass
            self.center_point = [center_x, center_y]
            self.point_ct = point_ct
            

    def move_all(self, center_masses, center_points):
        for child in self.children:
            if isinstance(child, Node):
                child.move_all(center_masses, center_points)
            elif isinstance(child, Point):
                child.move(center_masses, center_points)
            elif isinstance(child, list):
                for point in child:
                    point.move(center_masses, center_points)

    def remove_offscreen_points(self, root_size, root):
        for child in self.children:
            if isinstance(child, Node):
                child.remove_offscreen_points(root_size, root)
            elif isinstance(child, Point):
                if child.pos[0] > root_size or child.pos[1] > root_size:
                    root.points.remove(child)
                    child = 0
                    print("removed")
                elif child.pos[0] < 0 or child.pos[1] < 0:
                    root.points.remove(child)
                    child = 0
                    print("removed")


    def get_points(self):
        return self.points
        
import pygame 
from point import Point

class Node:
    def __init__(self, color, quadrant=None, parent=None, depth=None):
        if parent == None:
            self.top_left = (0,0) # where the node starts, top left of screen as (0,0)
            self.size = 512
            self.depth = 0
            self.color = color 
            # start with root node and 4 children nodes 
            self.children = [Node(self.color, 0, self, self.depth), Node(self.color, 1, self, self.depth), Node(self.color, 2, self, self.depth), Node(self.color, 3, self, self.depth)]
            self.points = []
        else:
            self.color = color
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

        self.quadrant = quadrant
        self.center_point = []
        self.total_mass = 0
        self.point_ct = 0
        self.last_add = 0
        self.rect = pygame.Rect(self.top_left[0], self.top_left[1], self.size, self.size)

    def check_inside(self):
        """Returns the total number of nodes and points in the tree"""
        # variables
        node_ct = 0
        point_ct = 0

        # count total number of nodes and points 
        for child in self.children: 
            if isinstance(child, Node):
                node_ct += 1
                x,y = child.check_inside()
                node_ct += x
                point_ct += y
            elif isinstance(child, Point):
                point_ct += 1
            elif isinstance(child, list):
                point_ct += len(child)

        return node_ct, point_ct

    def add_child(self, point:Point, root):
        """Add a child point to this Node, creating more nodes if necessary"""\
        
        """ determine the quadrant of the parent node that the point lies in
        Quadrants:
        0, 1
        2, 3
        """
        quadrant = (point.pos[0] >= self.top_left[0] + self.size/2) * 1 + (point.pos[1] >= self.top_left[1] + self.size/2) * 2

        # Add point to list of points in root node 
        if self.depth == 0:
            self.points.append(point)

        # Determine collisions and how to place point in the tree
        if self.children[quadrant] == 0:
            self.children[quadrant] = point
        elif isinstance(self.children[quadrant], Node):
            self.children[quadrant].add_child(point, root)
        elif isinstance(self.children[quadrant], Point):
            if self.size == 1:
                new_point = point.collision(self.children[quadrant], root)
                self.children[quadrant] = new_point
            else:
                temp = Node(self.color, quadrant, self, self.depth)
                temp.add_child(self.children[quadrant], root)
                temp.add_child(point, root)
                self.children[quadrant] = temp
        elif isinstance(self.children[quadrant], list):
            self.children[quadrant].append(point)

    def draw(self, surface):
        """Draws the current tree to the screen"""

        if self.depth == 0:
            # fill screen with black to remove last frame 
            surface.fill((0,0,0))

        # draw current frame 
        for child in self.children:
            if isinstance(child, Node):
                child.draw(surface)
            elif isinstance(child, Point):
                pygame.draw.circle(surface, color=self.color, center=child.pos, radius=1)
        
    def set_mass(self):
        """Set the total mass of every node in the tree"""
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
        """Set the center of gravity for every node in the tree"""
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
            

    def move_all(self, center_masses, center_points, quadrant=None):
        """Move all points that are children of this node"""

        if self.depth == 0:
            for child in self.children:
                child.move_all(center_masses, center_points, child.quadrant)
        else:
            for child in self.children:
                if isinstance(child, Node):
                    child.move_all(center_masses, center_points, quadrant)
                elif isinstance(child, Point):
                    child.move(center_masses, center_points, quadrant)
                elif isinstance(child, list):
                    for point in child:
                        point.move(center_masses, center_points, quadrant)

    def remove_offscreen_points(self, root_size, root):
        """Remove points that are offscreen from the tree"""
        for child in self.children:
            if isinstance(child, Node):
                child.remove_offscreen_points(root_size, root)
            elif isinstance(child, Point):
                if child.pos[0] > root_size or child.pos[1] > root_size:
                    root.points.remove(child)
                    child = 0
                elif child.pos[0] < 0 or child.pos[1] < 0:
                    root.points.remove(child)
                    child = 0

    def update(self, mouse_pos, clicked, mass, GRAVITY, current_time):
        """Perform updates on all points and add new ones if necessary"""

        if clicked[0] and current_time - self.last_add > 0.05:
            self.add_child(Point([mouse_pos[0], mouse_pos[1]], mass, GRAVITY), self)
            self.last_add = current_time

        self.set_mass()
        self.set_center_point()
        center_masses = []
        center_points = []
        for node in self.children:
            center_masses.append(node.total_mass)
            center_points.append(node.center_point)
        self.move_all(center_masses, center_points)
        self.remove_offscreen_points(self.size, self)
        
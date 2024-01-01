
class Point:
    def __init__(self, pos:[float,float], mass:float, gravity:float):
        self.pos = pos
        self.mass = mass
        self.X_Speed = 0
        self.Y_Speed = 0
        self.GRAVITY = gravity
        self.quadrant = None # set when adding point into the tree

    def move(self, nodes:list):
        """Apply the gravity of given points, and move this point accordingly"""
        X_Acel = 0
        Y_Acel = 0

        for node in nodes: 
            if node.center_point == []:
                continue
            
            if self.quadrant != node.quadrant:
                x_dist = node.center_point[0] - self.pos[0]
                y_dist = node.center_point[1] - self.pos[1]
                if round(y_dist) == 0 or round(x_dist) == 0:
                    continue

                X_Acel += ((self.GRAVITY * self.mass * node.total_mass) / x_dist)
                Y_Acel += ((self.GRAVITY * self.mass * node.total_mass) / y_dist)
            else: 
                # remove this object's effect on gravity so it is not pulling on itself 
                x_moment = self.pos[0] * self.mass
                y_moment = self.pos[1] * self.mass
                new_mass = node.total_mass - self.mass

                if new_mass == 0:
                    continue

                new_center_x = (node.total_x_moment - x_moment) / new_mass
                new_center_y = (node.total_y_moment - y_moment) / new_mass

                new_x_dist = new_center_x - self.pos[0]
                new_y_dist = new_center_y - self.pos[1]

                if round(new_y_dist) == 0 or round(new_x_dist) == 0:
                    continue

                X_Acel += ((self.GRAVITY * self.mass * new_mass) / new_x_dist)
                Y_Acel += ((self.GRAVITY * self.mass * new_mass) / new_y_dist)

        self.X_Speed += X_Acel
        self.Y_Speed += Y_Acel
        self.pos[0] += self.X_Speed
        self.pos[1] += self.Y_Speed

    def collision(self, point, root):
        """Combine two colliding points and place a explosion graphic where they collide"""
        root.collisions.append([point.pos[0], point.pos[1], 60])
        new_point = Point(point.pos, point.mass + self.mass, point.GRAVITY)
        new_point.X_Speed = (self.X_Speed * self.mass + point.X_Speed * point.mass) / new_point.mass
        new_point.Y_Speed = (self.Y_Speed * self.mass + point.Y_Speed * point.mass) / new_point.mass
        root.points.remove(self)
        root.points.remove(point)
        root.points.append(new_point)
        return new_point
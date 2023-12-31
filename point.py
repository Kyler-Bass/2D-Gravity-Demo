
class Point:
    def __init__(self, pos:[int,int], mass:int, gravity):
        self.pos = pos
        self.mass = mass
        self.X_Speed = 0
        self.Y_Speed = 0
        self.GRAVITY = gravity

    def move(self, center_masses, center_points, quadrant):
        """Apply the gravity of given points, and move this point accordingly"""
        X_Acel = 0
        Y_Acel = 0

        for i in range(4): 
            if center_points[i] == []:
                continue
            x_dist = center_points[i][0] - self.pos[0]
            y_dist = center_points[i][1] - self.pos[1]
            if round(y_dist) == 0 or round(x_dist) == 0:
                continue
            
            if quadrant != i:
                X_Acel += ((self.GRAVITY * self.mass * center_masses[i]) / x_dist)
                Y_Acel += ((self.GRAVITY * self.mass * center_masses[i]) / y_dist)
            else:
                X_Acel += ((self.GRAVITY * self.mass * (center_masses[i] - self.mass)) / x_dist)
                Y_Acel += ((self.GRAVITY * self.mass * (center_masses[i] - self.mass)) / y_dist)

        self.X_Speed += X_Acel
        self.Y_Speed += Y_Acel
        self.pos[0] += self.X_Speed
        self.pos[1] += self.Y_Speed

    def collision(self, point, root):
        print("Collision")
        new_point = Point(point.pos, point.mass + self.mass, point.GRAVITY)
        new_point.X_Speed = (self.X_Speed * self.mass + point.X_Speed * point.mass) / new_point.mass
        new_point.Y_Speed = (self.Y_Speed * self.mass + point.Y_Speed * point.mass) / new_point.mass
        root.points.remove(self)
        root.points.remove(point)
        root.points.append(new_point)
        return new_point
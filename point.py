import pygame 
from functions import exit_event_check

class Point:
    def __init__(self, pos:[int,int], mass:int, gravity):
        self.pos = pos
        self.mass = mass
        self.X_Speed = 0
        self.Y_Speed = 0
        self.GRAVITY = gravity

    def move(self, center_masses, center_points):
        """Apply the gravity of given points, and move this point accordingly"""
        X_Acel = 0
        Y_Acel = 0

        for i in range(4): 
            if center_points[i] == []:
                continue
            x_dist = center_points[i][0] - self.pos[0]
            y_dist = center_points[i][1] - self.pos[1]
            #print(y_dist, " : ", x_dist)
            if round(y_dist) == 0 or round(x_dist) == 0:
                continue
            if x_dist < 1: # add collisions later 
                if x_dist < 0:
                    if x_dist < -1:
                        pass
                    else:
                        x_dist = -1
                else:
                    y_dist = 1
            if y_dist < 1: # add collisions later
                if y_dist < 0:
                    if y_dist < -1:
                        pass
                    else:
                        y_dist = -1
                else:
                    y_dist = 1
                
            #print(self.GRAVITY * self.mass * center_masses[i])
            X_Acel += ((self.GRAVITY * self.mass * center_masses[i]) / x_dist)
            Y_Acel += ((self.GRAVITY * self.mass * center_masses[i]) / y_dist)

        self.X_Speed += X_Acel
        self.Y_Speed += Y_Acel
        self.pos[0] += self.X_Speed
        self.pos[1] += self.Y_Speed

        #print(X_Acel)
        #print(self.X_Speed, " : ", self.Y_Speed)


    def collision(self, point, root):
        print("Collision")
        temp = Point(point.pos, point.mass + self.mass, point.GRAVITY)
        temp.X_Speed = (self.X_Speed * self.mass + point.X_Speed * point.mass) / temp.mass
        temp.Y_Speed = (self.Y_Speed * self.mass + point.Y_Speed * point.mass) / temp.mass
        root.points.remove(self)
        root.points.remove(point)
        return temp
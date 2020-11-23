##
#   Graham Decomposition of Polygons
#   https://github.com/hugoaboud/graham-polygon-decomposition
#
#   vector.py - Linear Algebra, Vector Class
#
##

import math

class Vector:
    def __init__(self, pos, y = None):
        if (y == None):
            self.x = pos[0]
            self.y = pos[1]
        else:
            self.x = pos
            self.y = y

    def __add__(self, other):
        return Vector(self.x+other.x, self.y+other.y)

    def __sub__(self, other):
        return Vector(self.x-other.x, self.y-other.y)

    def astuple(self):
        return (int(self.x),int(self.y))

    def set(self, pos):
        self.x = pos[0]
        self.y = pos[1]

    def dist(self, other):
        return math.sqrt((other.x-self.x)*(other.x-self.x)+(other.y-self.y)*(other.y-self.y))

    def dot(self, other):
        return self.x*other.x+self.y*other.y

    def cross(self, other):
        return self.x*other.y-self.y*other.x

    def normalize(self):
        norm = math.sqrt(self.x*self.x+self.y*self.y)
        return Vector(self.x/norm,self.y/norm)

    def angle(self, other):
        return -(self.normalize().dot(other.normalize()))

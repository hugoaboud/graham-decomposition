##
#   Graham Decomposition of Polygons
#   https://github.com/hugoaboud/graham-polygon-decomposition
#
#   polygon.py - Polygon Data Structures
##

from graham_decomp.vector import Vector

# Vertex
# Item from vertices doubly-linked circular list

class Vertex:

    def __init__(self, pos):
        self.pos = Vector(pos)
        self.area = 0
        self.next = None
        self.prev = None

    def update_area(self):
        self.area = (self.prev.pos-self.pos).cross(self.next.pos-self.pos)/2

# Triangle
# Composed by 3 vertices

class Triangle:

    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

# Polygon
# Doubly-linked circular list of Vertex

class Polygon:

    def __init__(self, points):
        # Sanity check
        assert len(points) > 2
        # Create linked list of vertices
        self.vertices = [Vertex(points[0])]
        for p in range(1,len(points)):
            self.vertices.append(Vertex(points[p]))
        # Define list of reflex vertices
        self.reflexes = []
        # Reset polygon
        self.reset()

    def reset(self):
        # Relink list of vertices
        for v in range(1,len(self.vertices)):
            self.vertices[v].prev = self.vertices[v-1]
            self.vertices[v-1].next = self.vertices[v]
        self.vertices[0].prev = self.vertices[-1]
        self.vertices[-1].next = self.vertices[0]
        # Calculate polygon area
        self.area = 0
        for vertex in self.vertices:
            self.area += (vertex.prev.pos.x+vertex.pos.x) * (vertex.prev.pos.y-vertex.pos.y)
        self.area = abs(self.area)/2
        # Calculate inner areas of the vertices
        # Also populate reflex list
        self.reflexes = []
        for vertex in self.vertices:
            # vertex area
            vertex.update_area()
            # reflex vertices
            if (vertex.area < 0):
                self.reflexes.append(vertex)

    def subpolygon(self, start):
        points = []
        it = start
        while (True):
            points.append(it.pos)
            it = it.next
            if (it == start): break
        return Polygon(points)

    def print(self):
        print()
        for vertex in self.vertices:
            print(str(self.vertices.index(vertex)) + "\t" +
                  str('R' if (vertex.area < 0) else 'C') + "\t" +
                  str("%1.4f"%vertex.area) + "\t" +
                  str('X' if vertex.prev==None else self.vertices.index(vertex.prev)) + "\t" +
                  str('X' if vertex.next==None else self.vertices.index(vertex.next)))

    def print_points(self):
        print([vtx.pos.astuple() for vtx in self.vertices])

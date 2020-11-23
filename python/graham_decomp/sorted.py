##
#   Graham Decomposition of Polygons
#   https://github.com/hugoaboud/graham-polygon-decomposition
#
#   sorted.py - Binary Sorted Insertion and Search Algorithms
##

import math

# Binary Sorted Insertion, Area
# Inserts vertex into areas list, keeping a descending order

def insert_area(areas, vertex):
    s = 0
    e = len(areas)
    if (s == e):
        areas.append(vertex)
        return
    while (e-s>1):
        i = s+math.floor((e-s)/2)
        if (vertex.area >= areas[i].area): e = i
        else: s = i
    if (vertex.area >= areas[s].area):
        areas.insert(s, vertex)
    else:
        areas.insert(e, vertex)

# Binary Sorted Insertion, Graham Angle
# Inserts vertex into graham angles list, keeping an ascending order

def insert_graham(vertices, vertex, graham):
    s = 0
    e = len(vertices)
    if (s == e):
        vertices.append((vertex,graham))
        return
    while (e-s>1):
        i = s+math.floor((e-s)/2)
        if (graham <= vertices[i][1]): e = i
        else: s = i
    if (graham <= vertices[s][1]):
        vertices.insert(s, (vertex,graham))
    else:
        vertices.insert(e, (vertex,graham))

# Binary Sorted Search of Average Area
# Searches for the vertex on list with the closest area
# value to the average triangle area of the polygon

def search_avg_area(areas, total):
    s = 0
    e = len(areas)
    # calculate average of total area
    # a n-gon is composed of (n-2) triangles
    value = total/(e-2)
    # binary search of average value
    while (e-s>1):
        i = s+math.floor((e-s)/2)
        if (value <= areas[i].area): s = i
        else: e = i
    # return vertex with smaller area ratio to the average
    if (e == len(areas) or (areas[s].area/value < value/areas[e].area)):
        # additional rule:
        # if largest face is greater than average, return second largest
        if (s == 0 and areas[0].area > value):
            return areas[1]
        return areas[s]
    return areas[e]

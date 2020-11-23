##
#   Graham Decomposition of Polygons
#   https://github.com/hugoaboud/graham-polygon-decomposition
#
#   earclip.py - Average Ear Clipping Method
##

from graham_decomp import sorted
from graham_decomp.polygon import Triangle

#   Average Ear Clipping (convex only)
#   Performs an ear clipping assuming every vertex is an ear
#   and always clipping the ear with area closest to the average

def avg_ear_clipping(polygon, start = None):

    # Default start
    if (not start):
        start = polygon.vertices[0]

    # Sort vertices by area (descending)
    # Also calculate total area of polygon
    areas = [start]
    it = start
    total_area = (it.prev.pos.x+it.pos.x) * (it.prev.pos.y-it.pos.y)
    while (True):
        # Next vertex
        it = it.next
        # Reached end of polygon
        if (it == start): break
        # Binary Insertion Sort
        sorted.insert_area(areas, it)
        # Accumulate total area
        total_area += (it.prev.pos.x+it.pos.x) * (it.prev.pos.y-it.pos.y)
    total_area /= 2

    # Triangles to be returned
    triangles = []

    # Ear creation loop
    while (True):
        # Find mid-range ear
        it = sorted.search_avg_area(areas, total_area)

        # Create ear triangle
        triangles.append(Triangle(it.prev, it, it.next))

        # Relink and remove ear
        it.prev.next = it.next
        it.next.prev = it.prev
        areas.pop(areas.index(it))
        total_area -= it.area

        # Recalculate areas
        it.prev.update_area()
        it.next.update_area()

        # Reorder areas in list
        areas.pop(areas.index(it.prev))
        sorted.insert_area(areas, it.prev)
        areas.pop(areas.index(it.next))
        sorted.insert_area(areas, it.next)

        # Break if done (only 3 points left)
        if (it.next.next == it.prev):
            break

    return triangles

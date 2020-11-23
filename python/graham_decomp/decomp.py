##
#   Graham Decomposition of Polygons
#   https://github.com/hugoaboud/graham-polygon-decomposition
#
#   decomp.py - Graham Decomposition of Concave Polygons
##

from graham_decomp.earclip import avg_ear_clipping
from graham_decomp import sorted

#   Graham Decomposition
#   Recursively slice the concave polygon
#   into convex sub polygons

def graham_decomposition(polygon, pivot=None, root=None, triangulate=True, r=0):

    # If it's a convex polygon
    if (not len(polygon.reflexes)):
        if (r==0): polygon.reset()
        if (triangulate):
            triangles = avg_ear_clipping(polygon)
            polygon.reset()
            return triangles
        else:
            return [polygon]

    # Default pivot
    if (not pivot):
        pivot = polygon.reflexes[0]

    # Triangles to be created
    if (triangulate):
        triangles = []
    # Subpolygons to be created
    else:
        subpolygons = []

    # Map reflex vertices on path
    # This might seem like a duplicate of polygon.reflexes, however
    # it is necessary on recursive steps to avoind creating a whole
    # new Polygon object
    reflexes = []
    it = pivot
    while (True):
        if (it == root): break
        # Add to list
        reflexes.insert(0, it)
        # (On a linked list this is more straight-forward, just use "prev")
        it = polygon.reflexes[polygon.reflexes.index(it)-1]
        # If reached pivot (loop end) or last pivot (open end)
        if (it == pivot): break

    # While there's a pivot (reflex vertex)
    while (len(reflexes)):
        # If next is reflex, the pivot edge is invalid, so jump to next vertex
        if (pivot.next.area < 0):
            pivot = pivot.next
            continue

        # Pivot edge, to calculate next "graham angles"
        pivot_edge = pivot.next.pos-pivot.pos

        # Populate list of reflexes potentially inside
        # the next convex hull
        in_reflexes = []
        if (len(reflexes) > 1):
            # Iterate reflex vertices starting from pivot
            it = pivot
            while (True):
                # (On a linked list this is more straight-forward, just use "next")
                it = reflexes[(reflexes.index(it)+1)%len(reflexes)]
                # If reflex is above the pivot edge, map it
                reflex_diag = it.pos-pivot.pos
                if (pivot_edge.cross(reflex_diag) < 0):
                    sorted.insert_graham(in_reflexes, it, pivot_edge.angle(reflex_diag))
                # If reached pivot, break
                if (it == pivot): break

        # Scan for the next subpolygon
        # It could either be a convex polygon (if 180° or a reflex vertex reached)
        # Or a concave one, to which recursion is applied
        it = pivot
        slice = None
        convex = False
        while (slice == None):
            # Iterate vertex
            it = it.next
            # Diagonal edge from pivot to it.next
            diag = it.next.pos-pivot.pos
            # If next angle is greater than 180, or 'it' is a reflex vertex
            # close a convex hull
            if (pivot_edge.cross(diag) > 0 or it.area < 0):
                slice = it
                convex = True
                break
            # Calculate edge graham angle
            graham_angle = diag.angle(pivot_edge)
            # Remove from in_reflexes vertices that are outside the edge (it -> it.next)
            in_reflexes = [reflex for reflex in in_reflexes if ((it.next.pos - it.pos).cross(reflex[0].pos-it.pos) < 0)]
            # If a reflex was found inside the subpolygon
            # relink polygon and do recursion
            if (len(in_reflexes) and in_reflexes[0][1] < graham_angle):
                slice = in_reflexes[0][0]

        # Store to relink later
        prev = pivot.prev
        next = slice.next
        pivot_reflex = (pivot.area < 0)
        slice_reflex = (slice.area < 0)

        # Close sub-polygon
        pivot.prev = slice
        slice.next = pivot
        pivot.update_area()
        slice.update_area()

        # If it's a convex hull, close it with ear clipping
        # Todo: if single triangle, just create it
        if (convex):
            if (triangulate):
                triangles += avg_ear_clipping(polygon, pivot)
            else:
                subpolygons.append(polygon.subpolygon(pivot))
        # If it's concave,
        else:
            # Close the bridge
            it_next = it.next
            it.next = slice
            slice_prev = slice.prev
            slice.prev = it
            if (triangulate):
                triangles += avg_ear_clipping(polygon, pivot)
            else:
                subpolygons.append(polygon.subpolygon(pivot))
            it.next = it_next
            it.prev = slice
            slice.next = it
            slice.prev = slice_prev
            slice.update_area()
            it.update_area()

            # Find recursion pivot
            # slice vertex remains reflex, use it
            if (slice.area < 0):
                r_pivot = slice
            # slice vertex is now concave
            else:
                # (On a linked list this is more straight-forward, just use "prev")
                r_pivot = reflexes[reflexes.index(slice)-1]
                # If there's no reflex on the subpolygon, avoid recursion
                if (r_pivot == pivot):
                    r_pivot = None

            # recursion pivot found
            if (r_pivot):
                triangles += graham_decomposition(polygon, r_pivot, pivot, r=r+1)
            # not found, convex subpolygon ahead
            else:
                if (triangulate):
                    triangles += avg_ear_clipping(polygon, slice)
                else:
                    subpolygons.append(polygon.subpolygon(slice))

        # Relink original polygon

        pivot.prev = prev
        slice.next = next
        pivot.next = slice
        slice.prev = pivot
        pivot.update_area()
        slice.update_area()

        # Find next pivot
        # If sliced a convex subpolygon, the reflex vertices can
        # be removed from the list if they are no longer reflex
        if (convex):
            if (slice_reflex and slice.area > 0):
                reflexes.remove(slice)
                polygon.reflexes.remove(slice)
            new_pivot = reflexes[(reflexes.index(pivot)+1)%len(reflexes)]
            if (pivot_reflex and pivot.area > 0):
                reflexes.remove(pivot)
                polygon.reflexes.remove(pivot)
        # If it's concave, remove a subset of the list.
        else:
            new_pivot = reflexes[(reflexes.index(slice)+1)%len(reflexes)]
            # Remove section of reflex list (on a linked list this is way more straight-forward)
            i_pivot = reflexes.index(pivot)
            i_slice = reflexes.index(slice)
            if (i_pivot < i_slice):
                if (pivot.area < 0): i_pivot += 1
                if (slice.area > 0): i_slice += 1
                reflexes = reflexes[:i_pivot] + reflexes[i_slice:]
            else:
                if (pivot.area < 0): i_pivot += 1
                if (slice.area > 0): i_slice += 1
                reflexes = reflexes[i_slice:i_pivot]
            # Remove section of polygon reflex list (on a linked list this is way more straight-forward)
            if (r == 0 and not r_pivot):
                i_p_pivot = polygon.reflexes.index(pivot)
                i_p_slice = polygon.reflexes.index(slice)
                if (i_p_pivot < i_p_slice):
                    if (pivot.area < 0): i_p_pivot += 1
                    if (slice.area > 0): i_p_slice += 1
                    polygon.reflexes = polygon.reflexes[:i_p_pivot] + polygon.reflexes[i_p_slice:]
                else:
                    if (pivot.area < 0): i_p_pivot += 1
                    if (slice.area > 0): i_p_slice += 1
                    polygon.reflexes = polygon.reflexes[i_p_slice:i_p_pivot]

        # If reached end, save starting point
        if (new_pivot == pivot and pivot.area > 0):
            reflexes = []
        # If not, advance to next pivot
        else:
            pivot = new_pivot

    # All reflex vertices should have been removed by now,
    # just clip the remaining convex polygon
    # TODO: if single vertex, just create it

    if (triangulate):
        triangles += avg_ear_clipping(polygon, pivot)
        if (r==0): polygon.reset()
        return triangles

    subpolygons.append(polygon.subpolygon(pivot))
    if (r==0): polygon.reset()
    return subpolygons

/*
*   Graham Decomposition of Polygons
*   https://github.com/hugoaboud/graham-polygon-decomposition
*
*   v0.0.0
*
*   This is a single-header C implementation of the Graham Decomposition
*   of Polygons algorithm. The aim of the algorithm is to decompose a
*   concave polygon into convex sub-polygons.
*
*   It also features an implementation of Average Ear Clipping, an
*   algorithm to triangulate convex polygon avoiding skinny triangles
*
*   This header has a define section to allow it's use with different
*   vector/mesh libraries. A simple vector/mesh library is included
*   in a separate file, which is used by default.
*
*/


/*
    Vector Library Defines
    Replace with your prefered Vector library
*/

#include "vector.h"

#define VECTOR vector
#define DOT(A,B) (dot((A),(B)))
#define CROSS(A,B) (dot((A),(B)))

/**
*
*     POLYGON STRUCTS
*
**/

/*
  Vertex
  Node of the vertices arraylist
*/

typedef struct ghd_vertex {
  size_t i;
  VECTOR pos;
  float area;
  struct ghd_vertex* prev = NULL;
  struct ghd_vertex* next = NULL;
} ghd_vertex;

void ghd_vertex_update_area(ghd_vertex* vertex) {
  vertex->area = CROSS((vertex->prev.pos-vertex->pos),(vertex->next.pos-vertex->pos))/2;
}

/*
  Reflex
  Node of a reflex list
*/

typedef struct ghd_reflex {
  ghd_vertex* v;
  struct ghd_reflex* prev;
  struct ghd_reflex* next;
} ghd_reflex;

void ghd_reflex_list_insert(ghd_reflex* head, ghd_vertex* reflex) {
  if (head == NULL) {
    head = reflex;
    reflex->next = reflex;
    reflex->prev = reflex;
  }
  else {
    head->prev->next = reflex;
    reflex->prev = head->prev;
    reflex->next = head;
    head->prev = reflex;
  }
}

void ghd_reflex_list_insert(ghd_reflex* head, ghd_vertex* vertex) {
  ghd_reflex* reflex = (ghd_reflex*) malloc(sizeof(ghd_reflex));
  reflex->v = vertex;
  ghd_reflex_list_insert(head, reflex);
}

ghd_reflex_list_clear(ghd_vertex* head) {
  ghd_reflex* it = head;
  ghd_reflex* next;
  while (it != NULL) {
    next = it->next;
    if (it == next) next = NULL;
    free(it);
    it = next;
  }
}

/*
  Polygon
  ArrayList of vertices
  List of reflex vertices
*/

typedef struct {
  ghd_vertex* vertices; // arraylist (doubly linked)
  ghd_reflex* reflexes; // list (doubly linked)
  size_t n;
} ghd_polygon;

ghd_polygon* ghd_polygon_new(VECTOR* points, size_t n) {
  ghd_polygon* this = (ghd_polygon*) malloc(sizeof(ghd_polygon));
  // Allocate polygon vertices
  this->n = n;
  this->vertices = (ghd_vertex*) malloc(sizeof(ghd_vertex)*n);
  // Populate vertices
  for (size_t i = 0; i < n_vertices; i++) {
    this->vertices.i = i;
    this->vertices.pos = points[i];
    this->vertices.prev = &this->vertices[(i>0)?(i-1):(n-1)];
    this->vertices.next = &this->vertices[(i<(n-1))?(i+1):(0)];
  }
  // Update areas and create doubly linked list of reflex vertices
  for (size_t i = 0; i < n_vertices; i++) {
    this->vertices[i].UpdateArea();
    if (this->vertices[i].area < 0) {
      ghd_reflex_list_insert(this->reflexes, this->vertices[i]);
    }
  }
  return this;
}

// TODO: return loop vertices
size_t* ghd_polygon_perimeter(ghd_polygon* this, size_t* n_out, ghd_vertex* start) {
  return NULL;
}

void ghd_polygon_del(ghd_polygon* this) {
  // Clear vertices array
  for (int i = 0; i < n; i++) free(this->vertices[i]);
  // Clear reflex list
  ghd_reflex_list_clear(this->reflexes);
  free(this);
}

/**
*
*     OUTPUT STRUCTS
*
**/

/*
  Triangle
  indices of the vertices on the polygon
*/

typedef struct {
  size_t a;
  size_t b;
  size_t c;
} ghd_triangle;

void ghd_triangle_set(ghd_triangle* this, size_t a, size_t b, size_t c) {
  this->a = a;
  this->b = b;
  this->c = c;
}

/*
  Triangle Array
  array returned by triangulation methods
*/

typedef struct {
  ghd_triangle* array;
  size_t n;
} ghd_triangle_array;

ghd_triangle_array ghd_triangle_array_new(size_t n) {
  ghd_triangle_array this;
  this.n = n;
  this.array = (gh_triangle*) malloc(n * sizeof(gh_triangle));
  return this;
}

void ghd_triangle_array_del (ghd_triangle_array* this) {
  for (int i = 0; i < n; i++) free(this->array[i]);
  free(this);
}

ghd_triangle_array* ghd_triangle_array_ref (ghd_triangle_array array) {
  ghd_triangle_array* ref;
  ref = (ghd_triangle_array*) malloc(sizeof(ghd_triangle_array));
  ref->array = array.array;
  ref->n = array.n;
  return ref;
}

/*
  SubPolygon
  Node in SubPolygonList, containing vertices and triangles
  of the subpolygon. This is used as output of GrahamDecomposition
*/

typedef struct ghd_subpolygon {
  ghd_vertex* vertices;
  size_t n;
  ghd_triangle_array* triangles;
  struct ghd_subpolygon* next = NULL;
} ghd_subpolygon;

ghd_subpolygon* ghd_subpolygon_new(ghd_vertex* vertices, size_t n, ghd_triangle_array* triangles) {
  ghd_subpolygon* this = (ghd_subpolygon*) malloc(sizeof(ghd_subpolygon));
  this->vertices = vertices;
  this->n = n;
  this->triangles = triangles;
  return this;
}

void ghd_subpolygon_del(ghd_subpolygon* this) {
  for (int i = 0; i < n; i++) free(this->vertices[i]);
  ghd_triangle_array_del(this->triangles);
  free(this);
}

/*
  SubPolygonList Struct
  Linked list of SubPolygons
*/

typedef struct ghd_subpolygon_list {
  ghd_subpolygon* head;
  ghd_subpolygon* tail;
} ghd_subpolygon_list;

void ghd_subpolygon_list_insert(ghd_subpolygon_list* this, size_t* vertices, size_t n, TriangleArray* triangles) {
  ghd_subpolygon* sub = ghd_subpolygon_new(vertices, n, triangles);
  if (list->head == NULL)
    list->head = sub;
  else
    list->tail->next = sub;
    list->tail = sub;
}

void ghd_subpolygon_list_del(ghd_subpolygon_list* this) {
  ghd_subpolygon* it = this->head;
  ghd_subpolygon* next;
  while (it != NULL) {
    next = it->next;
    if (it == next) next = NULL;
    free(it);
    it = next;
  }
}

/*
  Area Array
  Data structure for O(log(n)) search, removal and reorder of vertices by area
  There's no buffer overflow check, so it should be used carefully
*/

typedef struct ghd_area_array {
  ghd_vertex** array; // 1D array of pointers
  size_t n;
};

ghd_area_array* ghd_area_array_new(size_t n) {
  ghd_area_array* this = (ghd_area_array*) malloc(sizeof(ghd_area_array));
  array = (ghd_vertex**) malloc(n*sizeof(ghd_vertex*));
  this->n = 0;
}

void ghd_area_array_insert(ghd_area_array* this, ghd_vertex* v) {
  this->array[this->n] = v;
  this->n++;
}

void ghd_area_array_pop(ghd_area_array* this, ghd_vertex* v) {
  v->area = 0;
  this->Sort();
  this->n--;
}

// Quicksort based on vertices area - O(log(n))
void ghd_area_array_sort(ghd_area_array* this, size_t s = 0, size_t p = -1) {
  if (p == -1) p = this->n-1;
  // buffer for quicksort swaping
  ghd_vertex* buf;
  // left/right iterators
  size_t l = s;
  size_t r = p-1;
  float pivot_area = this->array[p]->area;
  // iterate sublist
  while (r > l) {
    if (this->array[l]->area < pivot_area) l++;
    else if (this->array[r]->area > pivot_area) r--;
    else {
      buf = this->array[l];
      this->array[l] = this->array[r];
      this->array[r] = buf;
    }
  }
  // swap pivot (if necessary)
  if (this->array[l]->area > pivot_area) {
    buf = this->array[l];
    this->array[l] = this->array[p];
    this->array[p] = buf;
  }
  // recursion time!
  if (l-s > 1) Sort(s,l-1);
  if (e-l > 1) Sort(l+1,e);
}

// Binary search + additional rules - O(log(n))
ghd_vertex* ghd_area_array_search(ghd_area_array* this, float total_area) {

  // Initial start/end indexes
  size_t s = 0;
  size_t e = this->n;
  // Calculate average area
  float avg = total_area/(e-2);
  // Binary search of average area
  size_t i;
  while (e-s>1) {
    i = s+(e-s)/2;
    if (avg <= this->array[i]->area) s = i;
    else e = i;
  }
  // Return vertex with smaller area ratio to the average
  if (e == this->n || (this->array[s]->area/value < value/this->array[e]->area)) {
    // Additional rule:
    // If largest face is greater than average, return second largest
    if (s == 0 && this->array[0]->area > avg)
      return this->array[1];
    return this->array[s];
  }
  return this->array[e];
}

void ghd_area_array_del(ghd_area_array* this) {
  free(this->array);
}

/*
  Average Ear Clipping
  Returns an array of Triangles, each containing the
  indices of 3 vertices on the polygon.

  - This method will follow the path from start->start.
  - If the path is not closed it will break.
  - If the path is closed on a subpolygon loop it should work fine.
    - In this case, you can use the "n" argument to limit memory
    usage to the vertices on the loop
*/

ghd_triangle_array ghd_avg_ear_clipping(ghd_polygon* polygon, ghd_vertex* start = NULL, size_t n = 0) {

  // If no given start vertex, use polygon list head
  // Start is usually set externally when triangulating subpolygon loops
  if (start == NULL) {
    start = polygon->vertices[0];
  }

  // If number of vertices is not given, use polygon n.
  // This is used to avoid allocating memory for the whole polygon
  // when you're triangulating a subpolygon loop inside it
  // If this is set, it MUST match the number of vertices inside the loop
  if (n == 0) {
    n = polygon->n;
  }

  // Create data structure to keep vertices sorted by area
  ghd_area_array* areas = ghd_area_array_new(n);

  // Create variable to store total area of polygon
  float total_area = (start->prev->pos.x+start->pos.x)*(start->prev->pos.y-start->pos.y);

  // Populate array of areas
  // while also accumulating the total area of the polygon
  // O(n)
  ghd_area_array_insert(areas, start);
  for (ghd_vertex* it = start->next; it != start; it = it->next) {
    ghd_area_array_insert(areas, it);
    total_area += (it->prev->pos.x+it->pos.x)*(it->prev->pos.y-it->pos.y);
  }
  total_area /= 2;

  // Sort areas - O(log n)
  ghd_area_array_sort();

  // Triangle array to be returned
  // The process of ear clipping always results on (n-2) triangles
  ghd_triangle_array triangles = ghd_triangle_array_new(n-2);
  size_t triangle_i = 0;

  // Ear creation loop - O(n*log(n))
  ghd_vertex* it;
  while (true) { // - O(n)

    // Search ear with area closest to the average - O(log(n))
    it = ghd_area_array_search(areas, total_area);

    // Create ear triangle - O(1)
    triangles.array[triangle_i].a = it->prev->i;
    triangles.array[triangle_i].b = it->i;
    triangles.array[triangle_i].c = it->next->i;
    triangle_i++;

    // Clip ear (relink vertex nodes) - O(1)
    it->prev->next = it->next;
    it->next->prev = it->prev;

    // Update neighbour areas - O(1)
    ghd_vertex_update_area(it->prev);
    ghd_vertex_update_area(it->next);

    // Remove vertex from area array - O(log(n))
    // This will sort the array, including the changes to the neighbour areas
    // This will also set the vertex area to 0.
    ghd_area_array_pop(it);

    // Break if done (only 3 points left)
    if (it->next->next == it->prev):
      break
  }

  return triangles;
}

/*
  Graham Decomposition of Polygons
*/

#define GHD_OUTPUT_PERIMETERS 0
#define GHD_OUTPUT_TRIANGLES 1
#define GHD_OUTPUT_PRM_TRI 2


ghd_subpolygon_list ghd_graham_decomposition(ghd_polygon* polygon, size_t output = GHD_OUTPUT_PRM_TRI, ghd_reflex* pivot = NULL, ghd_vertex* root = NULL, size_t r = 0) {

  sub_polygon_list subpolygons;

  // If it's a convex polygon, just triangulate
  if (polygon->reflexes->head == NULL) {
    size_t* perimeter = NULL;
    size_t n = 0;
    ghd_triangle_array* triangles;
    if (output == GHD_OUTPUT_PRM_TRI || output == GHD_OUTPUT_PERIMETERS) {
      perimeter = ghd_polygon_perimeter(polygon, &n);
    }
    if (output == GHD_OUTPUT_PRM_TRI || output == GHD_OUTPUT_TRIANGLES) {
      triangles = ghd_triangle_array_ref(ghd_avg_ear_clipping(polygon));
    }
    ghd_subpolygon_list_insert(&subpolygons, vertices, n, triangles)
    return AvgEarClipping(polygon);
  }

  // Default pivot
  if (pivot == NULL)
    pivot = polygon->reflexes->head;

  // Map reflex vertices on loop
  ghd_reflex* loop_reflexes = NULL; // this list is inverted
  ghd_reflex* it = pivot;

  while (true) {
    if (it->v == root) break;
    ghd_reflex_list_insert(loop_reflexes, it);
    it = it->prev;
    if (it == pivot) break;
  }

  // Main slicing loop
  // Run while there are reflex vertices in the loop
  while (loop_reflexes != NULL) {
    // If next is reflex, jump
    if (pivot->next->area < 0) {
      pivot = pivot->next;
    }

    // Pivot edge
    VECTOR pivot_edge = DIR(pivot->v->pos, pivot->v->next->pos);

    // Populate list of reflexes potentially inside the next convex hull
    ghd_reflex* in_reflexes = NULL;
    if (loop_reflexes->next != NULL) {
      // Iterate reflex vertices starting from pivot
      it = pivot->prev;
      while (it != pivot) {
        // If reflex is above the pivot edge, map it
        VECTOR reflex_diag = DIR(pivot->v->pos, it->v->pos);
        if (CROSS(pivot_edge, reflex_diag) < 0)
          ghd_graham_array_insert()
      }
    }
  }
}

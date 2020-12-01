/*
*   Graham Decomposition of Polygons
*   https://github.com/hugoaboud/graham-polygon-decomposition
*
*   vector.h - Single-header simple ANSI-C 2D vector library
*   v0.0.0
*/

typedef struct {
    float x;
    float y;
} vector;

vector dir(vector* a, vector* b) {
  vector result;
  result.x = b->x-a->x;
  result.y = b->y-a->y;
  return result
}

vector dist(vector* a, vector* b) {
  return sqrt((b->x-a->x)*(b->x-a->x)+(b->y-a->y)*(b->y-a->y))
}

vector dot(vector* a, vector* b) {
  return a->x*b->x+a->y*b->y;
}

float cross(vector* a, vector* b) {
  return a->x*b->y-a->y*b->x;
}

float norm(vector* v) {
  return sqrt(v->x*v->x+v->y*v->y);
}

void normalize(vector* v) {
  float norm = sqrt(v->x*v->x+v->y*v->y);
  v->x /= norm;
  v->y /= norm;
}

vector normalized(vector* v) {
  float norm = sqrt(v->x*v->x+v->y*v->y)
  vector result;
  result.x = v->x/norm;
  result.y = v->y/norm;
  return result;
}

float angle(vector* a, vector* b) {
  return dot(normalized(a),normalized(b));
}

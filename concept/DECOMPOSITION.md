**DECOMPOSITION**

The decomposition algorithm proposed here tries to balance performance, implementation complexity and output quality. Quality meaning the least amount of thin angles.
It employs both divide-and-conquer and recursion strategies, with simple rules.

*ALGORITHM OVERVIEW*

The idea is to find a convex sub-polygon, defined by consecutive vertices starting on a reflex vertex, and trim it from the polygon. If another vertex is found inside this sub-polygon, a diagonal is created to it and a recursion step starts. The trimming continues until there's no reflex vertex left.

![Decomposition Overview 1](https://i.ibb.co/hXJgN70/decomp1.png)

```
- Given a polygon `P` with `n` vertices, and `m>0` reflex vertices.
- Given a vertex `v(x)` from `P`.
- Given a `pivot` reflex vertex `v(p)` such that `V(p+1)` is not reflex.
```
```
TrimConvex(T,p,n):
  - Trim sub-polygon `S_ear = [v(p+n),...,v(p)]` from `T`
  - Reevaluate reflex state of `v(p)` and `v(p+n)`
  - If `T` still has reflex vertices:
    - true: `return next reflex vertex`
    - false: `return NULL`
```
```
TrimConcave(T,p,n,i):
  - Trim sub-polygon `S_bridge = [v(p),...,v(p+n),v(i)]` from `P`
  - Trim sub-polygon `S_sub = [v(p+n),...,v(i)]` from `P`
  - `Decompose(S_sub)`
  - Reevaluate reflex state of `v(p)` and `v(i)`
  - If `T` still has reflex vertices:
    - true: `return next reflex vertex`
    - false: `return NULL`
```
```
Decompose(P):
  - Find a reflex vertex `pivot = v(p)`, so that `v(p+1)` is not reflex   
  - While `pivot != NULL`:
    - Starting on `pivot = v(p)`, for each vertex `v(p+n)`, `n>=1`:
      - If the vertex `v(p+n)` is reflex:
        - `pivot = TrimConvex(P,p,n)`
        - `continue`
      - Check if the angle `{v(p+n+1),v(p),v(p+1)} <= 180`:
        - If yes, `continue`
        - If no, `TrimConvex(P,p,p+n)`
      - Check if there's a vertex `V(i)` inside the triangle `{v(p+n+1),v(p),v(p+1)}`:
        - If no, `continue`
        - If yes, `TrimConcave(p,i)`
```

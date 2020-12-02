# Graham Decomposition of Concave Polygons

This is a set of **Python** and **C++** implementations of `Polygon Decomposition and Triangulation` algorithms.
The name `Graham` is a reference to the `Graham Scan`, which inspired the decomposition algorithm, however [I'm looking for suggestions](https://math.stackexchange.com/questions/3917943/big-ear-of-polygons-proper-nomenclature).

This is an attempt to balance performance, implementation complexity and output quality for a `convex polygon triangulation` algorithm. I've developed it for a personal project where the *skinny triangles* created by traditional Ear Clipping were a huge problem, and performance must be moderately good.

Two algorithms are proposed:
 - **Graham Decomposition**: splits a concave polygon into convex sub-polygons
 - **Average Ear Clipping**: a O(n*log(n)) implementation of Ear-Clipping, limited to convex polygons, which tries to keep the triangle areas homogeneous.

For a detailed description check the `concept` folder.

![python sandbox](http://i.ibb.co/WFvPC9Y/graham.png)

For language-specific instructions, open the `README` file on the language folder.

> *DISCLAIMER* I'm not qualified to provide formal definitions and proofs. Please feel welcome to submit fixes to everything written in here.

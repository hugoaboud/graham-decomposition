##
#   Graham Decomposition of Polygons
#   https://github.com/hugoaboud/graham-polygon-decomposition
#
#   sandbox.py - UI created with pygame to play with the algorithm
##

import pygame, sys, math, os
from pygame.locals import QUIT

from graham_decomp.vector import Vector
from graham_decomp.polygon import Polygon
from graham_decomp.decomp import graham_decomposition

#
# Shapes
#

shape = 0
shapes = []
shapes.append([(133, 188), (132, 477), (451, 505), (575, 323), (456, 104)])
shapes.append([(530, 484), (641, 415), (670, 278), (578, 126), (456, 104), (365, 197), (285, 117), (133, 150), (75, 250), (120, 366), (227, 457), (368, 381)])
shapes.append([(279, 474), (624, 524), (768, 509), (578, 126), (456, 104), (430, 100), (285, 117), (173, 174), (75, 250), (109, 406), (227, 457), (254, 467)])
shapes.append([(410, 487), (695, 98), (633, 85), (576, 76), (514, 68), (454, 66), (415, 65), (370, 65), (328, 65), (231, 65), (166, 77), (141, 114)])
shapes.append([(227, 457), (260, 280), (470, 466), (641, 415), (712, 316), (645, 125), (516, 176), (569, 345), (285, 117), (133, 150), (75, 250), (65, 408)])
shapes.append([(227, 457), (279, 347), (470, 466), (586, 336), (410, 310), (326, 218), (508, 262), (635, 347), (677, 422), (738, 310), (305, 51), (26, 269)])
shapes.append([(227, 457), (352, 477), (470, 466), (641, 415), (712, 316), (645, 125), (516, 176), (569, 345), (285, 117), (133, 150), (75, 250), (65, 408)])
shapes.append([(221, 277), (390, 327), (470, 466), (641, 415), (712, 316), (645, 125), (516, 176), (569, 345), (285, 117), (133, 150), (75, 250), (65, 408)])
shapes.append([(153, 454), (292, 465), (549, 218), (641, 415), (712, 316), (645, 125), (516, 176), (163, 371), (285, 117), (133, 150), (75, 250), (65, 408)])
shapes.append([(126, 497), (284, 546), (524, 503), (641, 415), (732, 237), (482, 312), (348, 317), (260, 270), (186, 133), (133, 150), (75, 250), (65, 408)])
shapes.append([(349, 486), (374, 308), (524, 503), (641, 415), (732, 237), (482, 312), (293, 203), (314, 138), (186, 133), (133, 150), (207, 164), (79, 210), (263, 180), (120, 271), (247, 241), (324, 455), (93, 341), (187, 454), (131, 545), (386, 563), (216, 490), (508, 530), (444, 479)])
shapes.append([(486, 319), (473, 184), (625, 246), (641, 415), (732, 237), (419, 82), (420, 402), (314, 138), (274, 192), (274, 30), (207, 164), (79, 210), (185, 216), (223, 362), (247, 241), (455, 485), (93, 341), (226, 453), (57, 409), (163, 569), (216, 490), (508, 530), (596, 270)])
shapes.append([(80, 182), (107, 269), (206, 313), (231, 564), (409, 549), (336, 482), (405, 413), (309, 381), (444, 284), (514, 396), (410, 454), (475, 510), (565, 400), (464, 241), (579, 164), (494, 21), (379, 67), (471, 138), (381, 252), (268, 225), (316, 85), (196, 65), (107, 114)])

#
# Colors
#

colors = {}
colors['BACKGROUND'] = (0, 0, 0)
colors['TRIANGLE'] = (0,128, 255)
colors['EDGE_PREV'] = (255, 128, 255)
colors['EDGE_NEXT'] = (128, 255, 255)
colors['DIAGONAL'] = (200, 200, 200)
colors['CONVEX_VERTEX'] = (255, 127, 0)
colors['REFLEX_VERTEX'] = (255, 127, 0)

#
# UI Settings
#

WINDOW_TITLE = "Graham Decomposition of Concave Polygons, the sandbox"
WINDOW_SIZE = (1024,768)
DOUBLECLICKTIME = 200

RADIUS = 10
THICC_EDGE = 2
THICC_DIAG = 1

#
# Render
#

def render(windowSurface, polygon, triangles, font):
    # background
    windowSurface.fill(colors['BACKGROUND'])

    # draw triangles
    for triangle in triangles:
        pygame.draw.polygon(windowSurface, colors['TRIANGLE'], [triangle.a.pos.astuple(), triangle.b.pos.astuple(), triangle.c.pos.astuple()], 0)
        pygame.draw.line(windowSurface, colors['DIAGONAL'], triangle.a.pos.astuple(), triangle.b.pos.astuple(), THICC_DIAG)
        pygame.draw.line(windowSurface, colors['DIAGONAL'], triangle.b.pos.astuple(), triangle.c.pos.astuple(), THICC_DIAG)
        pygame.draw.line(windowSurface, colors['DIAGONAL'], triangle.c.pos.astuple(), triangle.a.pos.astuple(), THICC_DIAG)

    ## draw polygons
    for vertex in polygon.vertices:
        vpos = vertex.pos.astuple()
        ## draw polygon edges
        if (vertex.prev):
            p = vertex.prev.pos-vertex.pos
            p = vertex.pos+Vector(p.x/2,p.y/2)
            pygame.draw.line(windowSurface, colors['EDGE_PREV'], p.astuple(), vpos, THICC_EDGE)
        if (vertex.next):
            p = vertex.next.pos-vertex.pos
            p = vertex.pos+Vector(p.x/2,p.y/2)
            pygame.draw.line(windowSurface, colors['EDGE_NEXT'], vpos, p.astuple(), THICC_EDGE)

        ## draw polygon points
        pygame.draw.ellipse(windowSurface, colors['REFLEX_VERTEX'] if (vertex.area < 0) else colors['CONVEX_VERTEX'], (vertex.pos.x-RADIUS/2, vertex.pos.y-RADIUS/2, RADIUS, RADIUS), 0)

    # draw_text
    text_surface = font.render('You can drag the points.', True, (255, 255, 255))
    windowSurface.blit(text_surface, dest=(WINDOW_SIZE[0]*3/4-50,30))
    text_surface = font.render('Left/Right: prev/next shape', True, (255, 255, 255))
    windowSurface.blit(text_surface, dest=(WINDOW_SIZE[0]*3/4-50,45))
    text_surface = font.render('R: reset triangles', True, (255, 255, 255))
    windowSurface.blit(text_surface, dest=(WINDOW_SIZE[0]*3/4-50,60))
    text_surface = font.render('S: reset shape', True, (255, 255, 255))
    windowSurface.blit(text_surface, dest=(WINDOW_SIZE[0]*3/4-50,75))
    text_surface = font.render('P: print points', True, (255, 255, 255))
    windowSurface.blit(text_surface, dest=(WINDOW_SIZE[0]*3/4-50,90))
    text_surface = font.render('D: print polygon table', True, (255, 255, 255))

    # draw the window onto the screen
    pygame.display.update()

#
# Setup
#

pygame.init()
windowSurface = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
pygame.display.set_caption(WINDOW_TITLE)
font = pygame.font.Font(pygame.font.get_default_font(), 12)

#
# Internal Variables
#

_draggin = None
polygon = Polygon(shapes[shape])
triangles = graham_decomposition(polygon)

#
# Main Loop
#

while True:

    ## I/O

    for event in pygame.event.get():

        ## Mouse

        if event.type == pygame.MOUSEBUTTONDOWN:
            click = Vector(pygame.mouse.get_pos())
            for vertex in polygon.vertices:
                if (click.dist(vertex.pos) <= RADIUS):
                    _draggin = vertex
                    break

        elif event.type == pygame.MOUSEMOTION:
            #motion = pygame.mouse.get_pos()
            if (_draggin != None):
                _draggin.pos.set(pygame.mouse.get_pos())
                polygon.reset()
                triangles = graham_decomposition(polygon)

        elif event.type == pygame.MOUSEBUTTONUP:
            if (_draggin != None): _draggin = None

        ## Keyboard

        if event.type == pygame.KEYDOWN:

            ## < d > Print Polygon Table
            if event.key  == pygame.K_d:
                os.system('cls' if os.name == 'nt' else 'clear')
                polygon.print()

            ## < p > Print points
            elif event.key  == pygame.K_p:
                os.system('cls' if os.name == 'nt' else 'clear')
                polygon.print_points()

            ## < s > Step
            elif event.key  == pygame.K_s:
                os.system('cls' if os.name == 'nt' else 'clear')
                triangles.clear()
                polygon = Polygon(shapes[shape])
                triangles = graham_decomposition(polygon)

            ## < Left Arrow > Previous shape
            elif event.key  == pygame.K_LEFT:
                os.system('cls' if os.name == 'nt' else 'clear')
                triangles.clear()
                shape = (shape-1) if (shape > 0) else (len(shapes)-1)
                polygon = Polygon(shapes[shape])
                triangles = graham_decomposition(polygon)

            ## < Right Arrow > Next shape
            elif event.key  == pygame.K_RIGHT:
                os.system('cls' if os.name == 'nt' else 'clear')
                triangles.clear()
                shape = (shape+1)%len(shapes)
                polygon = Polygon(shapes[shape])
                triangles = graham_decomposition(polygon)

            ## < r > Reset polygon
            elif event.key == pygame.K_r:
                os.system('cls' if os.name == 'nt' else 'clear')
                triangles.clear()
                polygon.reset()

        ## Window

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    ## Rendering

    render(windowSurface, polygon, triangles, font)

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *


# funcion para inicializar pygame y opengl.
def init(ancho, alto, titulo, color_fondo=[0, 0, 0, 0], far=2000, near=1):
    # init pygame
    pygame.init()
    pygame.display.set_mode((ancho, alto), OPENGL | DOUBLEBUF)
    pygame.display.set_caption(titulo)

    # init opengl
    if alto == 0:
        alto = 1
    glViewport(0, 0, ancho, alto)
    glMatrixMode(GL_PROJECTION)

    glLoadIdentity()
    # establecer tipo de proyeccion: perspectiva u ortogonal
    gluPerspective(45, float(ancho) / float(alto), near, far)
    # glOrtho(-ancho, ancho, -alto, alto, near, far)

    glMatrixMode(GL_MODELVIEW)  # magia?

    # enable gl
    glClearColor(color_fondo[0], color_fondo[1], color_fondo[2], color_fondo[3])  # setea el color de fondo

    glClearDepth(1.0)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

    glEnable(GL_BLEND)  # transparencias
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glEnable(GL_DEPTH_TEST)  # profundidad
    glDepthFunc(GL_LEQUAL)

    # Las normales se modifican al efectuar transfomaciones,
    # dicho efecto puede ser evitado con GL_RESCALE_NORMAL
    # o GL_NORMALIZE
    glEnable(GL_RESCALE_NORMAL)

    glEnable(GL_LIGHTING)  # luz
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)  # rellenar las caras de los poligonos

    # descomentar estas lineas para no renderizar las caras traseras de los poligonos
    # glEnable(GL_CULL_FACE)
    # glCullFace(GL_BACK)
    return

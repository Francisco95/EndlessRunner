# -*- coding: utf-8 -*-
from OpenGL.GL import *


class Eje:
    def __init__(self, largo):
        self.largo = largo
        self.lista = 0
        self.crear()

    def crear(self):
        self.lista = glGenLists(1)
        glNewList(self.lista, GL_COMPILE)

        glBegin(GL_LINES)
        # eje Y verde
        glColor4f(0.0, 1.0, 0.0, 1.0)
        glVertex4f(0.0, self.largo, 0.0, 1.0)
        glVertex4f(0.0, 0.0, 0.0, 1.0)
        # eje x rojo
        glColor4f(1.0, 0.0, 0.0, 1.0)
        glVertex4f(0.0, 0.0, 0.0, 1.0)
        glVertex4f(self.largo, 0.0, 0.0, 1.0)
        # eje z azul
        glColor4f(0.0, 0.0, 1.0, 1.0)
        glVertex4f(0.0, 0.0, 0.0, 1.0)
        glVertex4f(0.0, 0.0, self.largo, 1.0)
        glEnd()

        glEndList()

    def dibujar(self):
        # almaceno la matriz, para aplicar los cambios solo sobre el Eje
        glDisable(GL_LIGHTING)

        glPushMatrix()
        glCallList(self.lista)
        glPopMatrix()

        glEnable(GL_LIGHTING)

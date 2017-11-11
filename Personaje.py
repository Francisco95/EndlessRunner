import numpy as np
from .MasterOctagon import Octagon
from EndlessRunner.CC3501Utils import Vector, esfera
from OpenGL.GL import *

class Personaje:
    def __init__(self, pos=Vector(0, 0, 0), tipo="simple",
                 fi=0):
        print("inicia personaje")
        self.pos = pos
        self.tipo = tipo
        self.lista = 0
        self.angulo = 0
        self.fi = fi
        self.crear()

    def crear(self):
        if self.tipo == "simple":
            self.lista = glGenLists(1)
            glNewList(self.lista, GL_COMPILE)
            glEnable(GL_COLOR_MATERIAL)

            glBegin(GL_TRIANGLES)
            glColor3f(1.0, 1.0, 0.0)
            esfera(40)
            glEnd()

            glEndList()

    def rotation(self, delta_ang):
       self.angulo += delta_ang

    def dibujar(self):
        glPushMatrix()
        glTranslatef(self.pos.x, self.pos.y, self.pos.z)
        glRotatef(self.angulo, 1, 0, 0)  # Rotacion en torno a eje Z
        glCallList(self.lista)
        glPopMatrix()

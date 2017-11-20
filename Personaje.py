from EndlessRunner.CC3501Utils import Vector, esfera
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image as Image
import numpy as np


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

    def read_texture(self, filename):
        img = Image.open(filename)
        img_data = np.array(list(img.getdata()), np.int8)
        textID = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, textID)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.size[0], img.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
        return textID

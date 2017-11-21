from EndlessRunner.CC3501Utils import *
import numpy as np


class Octagon:
    def __init__(self, pos=Vector(0, 0, 0),
                 dimensions=(240, 20, 780), ang=0,
                 z_pos=0, tipos=None):
        self.master_fi = ang
        self.lista = 0
        self.lenx = dimensions[0]
        self.leny = dimensions[1]
        self.lenz = dimensions[2]
        self.pos = pos
        self.z_pos = z_pos
        self.tipos = self.get_tipos(tipos)
        self.crear()

    def crear(self):
        """
        crea cada uno de los 8 paralelepipedos en su correspondiente posicion,
        trasladando un paralelepipedo maestro, usa atributo type para definir
        el tipo de paralelepipedo a crear, puede ser  nulo(0), simple(1)
        o comodin (2)
        :return:
        """
        self.lista = glGenLists(1)
        glNewList(self.lista, GL_COMPILE)
        glEnable(GL_COLOR_MATERIAL)
        glBegin(GL_TRIANGLES)

        for i in range(8):
            if self.tipos[i] == 1 or self.tipos[i] == 2:  # vacio
                glColor3f(0.0, 0.1, 0.0)
                continue
            elif self.tipos[i] == 0:  # blanco
                glColor3f(1.0, 1.0, 1.0)
            elif self.tipos[i] == 3:  # amarillos, otrogan mas tiempo de vida
                glColor3f(1.0, 1.0, 0.0)
            elif self.tipos[i] == 4:  # rojos, restan tiempo de vida
                glColor3f(1.0, 0.0, 0.0)
            else: # lo demas es vacio
                continue
            self.master_parallelepiped(i)

        glEnd()
        glEndList()

    def dibujar(self):
        glPushMatrix()
        glTranslatef(self.pos.x, -150, self.pos.z)
        glRotatef(self.master_fi, 0, 0, 1)  # Rotacion en torno a eje Z
        glCallList(self.lista)
        glPopMatrix()

    def set_ang_fi(self, number):
        """
        genera el angulo fi segun el paralelepipedo que se este usando,
        number va desde 0 hasta 7.
        :param number:
        :return:
        """
        return (np.pi * 45 * number) / 180

    def master_parallelepiped(self, number):
        idx_ver = [[-1, -1, 1], [-1, 1, 1], [-1, -1, -1], [-1, 1, -1],
                   [1, -1, 1], [1, 1, 1], [1, -1, -1], [1, 1, -1]]

        idx_faces = [[1, 0, 2, 3], [5, 4, 6, 7], [4, 0, 2, 6], [5, 1, 3, 7],
                     [3, 7, 6, 2], [1, 5, 4, 0]]

        # la idea es generar el paralelepipedo maestro segun set_displacement_pos,
        # y luego agregar la posicion maestra.

        for face in idx_faces:
            v1, v2, v3, v4 = self.individual_rect(idx_ver, face, number)
            cuadrilatero(v1, v2, v3, v4)

    def individual_rect(self, idx_ver, face, number):
        vectors = []
        for i in face:
            # face_idx.append(idx_ver[i])
            coef = idx_ver[i]
            v_i = Vector(coef[0] * self.lenx / 2,
                         coef[1] * self.leny / 2,
                         coef[2] * self.lenz / 2)
            v_i = self.set_rotation_fi(self.set_displacement_pos() + v_i,
                                       number)
            vectors.append(v_i)
        # v1, v2, v3, v4 = self.rotate_front(vectors[0], vectors[1], vectors[2], vectors[3], ang=0)
        return vectors[0], vectors[1], vectors[2], vectors[3]

    def set_rotation_fi(self, vector, number):
        return rotarFi(vector, self.set_ang_fi(number))

    def set_displacement_pos(self):
        """
        retorna la posicion del paralelepipedo maestro c/r a la posicion maestra
        :return:
        """
        return Vector(0, -(self.lenx / 2) * np.tan(np.pi * 67.5 / 180), self.z_pos / 2)

    @staticmethod
    def get_tipos(tipos):
        if tipos is None:
            tipos = [1, 1, 1, 1, 1, 1, 1, 1]
        return tipos

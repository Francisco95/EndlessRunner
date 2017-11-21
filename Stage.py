import numpy as np
from EndlessRunner.MasterOctagon import Octagon
from EndlessRunner.CC3501Utils import Vector
from OpenGL.GL import *
from EndlessRunner.map1 import map1


class Stage:
    def __init__(self, master_pos=Vector(0, 0, 0),
                 dimensions=(240, 20, 780), ang=0,
                 number=6):
        self.number = number
        self.master_pos = master_pos
        self.dimensions = dimensions
        self.ang = ang
        self.octagons = []
        self.pregenerated = False
        self.preg_counter = 0
        self.generate_first_octagons(Vector(0, 0, 0))

    def create_octagon(self, index_pos, offset, tipo):
        oct = Octagon(pos=self.set_pos(index_pos, offset),
                      dimensions=self.dimensions,
                      ang=self.ang, z_pos=0,
                      tipos=tipo)
        return oct

    def generate_first_octagons(self, offset):

        if self.pregenerated:
            tipo0 = map1[self.preg_counter]
            self.preg_counter += 1
            tipo1 = map1[self.preg_counter]
            self.preg_counter += 1

        else:
            tipo0 = [0, 0, 0, 0, 0, 0, 0, 0]
            tipo1 = [3, 3, 3, 3, 3, 3, 3, 3]

        tipos = [tipo0, tipo1, self.randon_types(),
                 self.randon_types(), self.randon_types(),
                 self.randon_types()]

        for i in range(self.number):
            oct = Octagon(pos=self.set_pos(i, offset),
                          dimensions=self.dimensions,
                          ang=self.ang, z_pos=0,
                          tipos=tipos[i])
            self.octagons.append(oct)

    def more_octagons(self):
        tipo_add = self.randon_types()
        oct = self.create_octagon(1, self.octagons[-1].pos,
                                  tipo_add)
        self.octagons.append(oct)

    def delete_octagons(self):
        glDeleteLists(self.octagons[0].lista, 1)
        self.octagons.pop(0)

    def update_config(self, cam_pos_z):
        if self.octagons[0].pos.z - cam_pos_z < - 450:
            print("eliminacion a :", self.octagons[0].pos.z - cam_pos_z)
        # if self.octagons[0].pos.z < cam_pos_z - 300:
            self.delete_octagons()
            self.more_octagons()

    def modify_pos(self, desp: Vector):
        for oct in self.octagons:
            oct.pos += desp

    def modify_fi(self, ang):
        self.ang = (self.ang + ang + 360) % 360
        for oct in self.octagons:
            oct.master_fi = self.ang
        # print("nuevo master fi = ", self.octagons[0].master_fi)

    def dibujar(self):
        for oct in self.octagons:
            oct.dibujar()

    def set_pos(self, i, offset):
        return self.master_pos + \
               Vector(0, 0, self.dimensions[2] * i) + \
               offset

    def randon_types(self):
        """
        genera un arreglo de los tipos de paralelepipedos a crear
        :return:
        """
        if not self.pregenerated: # no hay pregenerado
            tipos = [int(i) for i in np.random.exponential(1, size=8)]
        else: # si hay pregenerado
            if self.preg_counter < len(map1): #toma los tipos del mapa
                tipos = map1[self.preg_counter] # aumenta el contador
            else:
                tipos = [0, 0, 0, 0, 0, 0, 0, 0] # despues agrega escena plana
            self.preg_counter += 1

        return tipos

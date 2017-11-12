import numpy as np
from EndlessRunner.MasterOctagon import Octagon
from EndlessRunner.CC3501Utils import Vector
from OpenGL.GL import *


class Stage:
    def __init__(self, master_pos=Vector(0, 0, 0),
                 dimensions=(240, 20, 780), ang=0,
                 number=6):
        self.number=number
        self.master_pos = master_pos
        self.dimensions = dimensions
        self.ang = ang
        self.octagons = self.create_octagons(Vector(0, 0, 0),
                                             first=True)

    def create_octagons(self, offset, first=False):

        octagons = []
        if first:
            print("first")
            oct = Octagon(pos=self.set_pos(0, offset),
                          dimensions=self.dimensions,
                          ang=self.ang, z_pos=0,
                          tipos=[0, 0, 0, 0, 0, 0, 0, 0])
            octagons.append(oct)

            oct = Octagon(pos=self.set_pos(1, offset),
                          dimensions=self.dimensions,
                          ang=self.ang, z_pos=0,
                          tipos=[3, 3, 3, 3, 0, 3, 3, 3])
            octagons.append(oct)

            for i in range(self.number - 2):
                oct = Octagon(pos=self.set_pos((i + 2), offset),
                              dimensions=self.dimensions,
                              ang=self.ang, z_pos=0,
                              tipos=self.randon_types())
                octagons.append(oct)

        else:
            for i in range(self.number):
                oct = Octagon(pos=self.set_pos(i, offset),
                              dimensions=self.dimensions,
                              ang=self.ang, z_pos=0,
                              tipos=self.randon_types())
                octagons.append(oct)

        return octagons

    def more_octagons(self):
        self.octagons += self.create_octagons(self.octagons[-1].pos)

    def delete_octagons(self):
        glDeleteLists(self.octagons[0].lista, 1)
        self.octagons.pop(0)

    def update_config(self, cam_pos_z):
        if self.octagons[0].pos.z < cam_pos_z - 300:
            self.delete_octagons()

        if len(self.octagons) < self.number:
            self.more_octagons()

    def modify_pos(self, desp: Vector):
        for oct in self.octagons:
            oct.pos += desp

    def modify_fi(self, ang):
        self.ang += ang
        for oct in self.octagons:
            oct.master_fi += ang

    def dibujar(self):
        for oct in self.octagons:
            oct.dibujar()

    def set_pos(self, i, offset):
        return self.master_pos + \
               Vector(0, 0, self.dimensions[2] * i) + \
               offset

    def randon_types(self):
        return [int(i) for i in np.random.exponential(1, size=10)]

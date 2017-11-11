from EndlessRunner.CC3501Utils import Vector
from OpenGL.GL import *
from EndlessRunner.Stage import Stage
from EndlessRunner.Personaje import Personaje
from EndlessRunner.MasterOctagon import Octagon
import numpy as np


class Interactions(Personaje, Stage):
    def __init__(self, cam_pos: Vector, pj_pos=Vector(0, -90, 300),
                 master_pos=Vector(0, 0, 0),
                 dimensions_block=(240, 20, 780), number=6,
                 speed=10):
        self.cam_pos = cam_pos
        Personaje.__init__()
        Stage.__init__(dimensions=dimensions_block,
                       number=number)
        self.pos += pj_pos
        Stage.modify_pos(master_pos)
        self.can_jump = True
        self.speed = speed
        self.gravity = int(self.speed / 5)  # eje y esta invertido
        self.speed_jump = -self.set_vertical_speed()
        self.height_jump = self.set_heght_jump()
        self.instant=1


    def get_number_of_instants(self):
        return round(self.dimensions[2] / self.speed)

    def set_vertical_speed(self):
        return round(self.get_number_of_instants() / 2) * self.gravity

    def set_height_jump(self):
        return self.speed_jump ** 2 / (2 * self.gravity)

    def speed_while_jump(self, instant):
        return self.speed_jump + self.gravity * instant

    def position_while_jump(self, instant):
        return self.pos + Vector(0, self.speed_while_jump(instant)*instant, 0)

    def jump_empty_space(self):
        if self.can_jump:
            self.pos = self.position_while_jump(self.instant)
            self.instant += 1
            self.can_jump = True

        if self.instant > self.get_number_of_instants():
            self.instant = 0
            self.can_jump = False

    def fall(self):
        """
        El movimiento se detiene y el personaje empieza a caer,
        se pierde la partida, el personaje no puede saltar
        :return:
        """
        self.pos += Vector(0, 5, 2)
        self.can_jump = False


    @staticmethod
    def get_lower_block(octagon: Octagon):
        number = octagon.master_fi * 180 / (np.pi * 45)
        return octagon.tipos[number]

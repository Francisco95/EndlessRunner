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
        self.master_pos = master_pos
        self.pj_pos = pj_pos
        Personaje.__init__(self)
        Stage.__init__(self, dimensions=dimensions_block,
                       number=number)
        self.pos += pj_pos
        Stage.modify_pos(self, self.master_pos)
        self.can_jump = False
        self.right = False
        self.left = False
        self.side = False
        self.speed = speed
        self.instants = self.get_number_of_instants()
        print(self.instants)
        self.instant = 1
        self.gravity = self.get_gravity(20, 60)
        self.times = self.discrete_time(20, 60)

    def get_number_of_instants(self):
        return round(self.dimensions[2] / self.speed)

    def time_free_fall(self, speed_jump, height_jump):
        """
        calcula el tiempo de vuelo del personaje al saltar
        hasta una altura fija con una velocidad inicial fija
        :param height_jump:
        :return:
        """
        return np.sqrt(-2 * height_jump / self.gravity)

    def discrete_time(self, speed_jump, height_jump):
        """
        discretiza el tiempo real para la visualizacion segun
        el numero de instantes
        :return:
        """
        times = []
        for i in range(self.instants):
            times.append((self.time_free_fall(speed_jump, height_jump)
                          * 2 * (i + 1)) / self.instants)
        print(times)

        return times

    def get_gravity(self, speed_jump, height_jump):
        """
        en base a una velocidad y una altura calcula la gravedad
        necesaria
        :param speed_jump:
        :param height_jump:
        :return:
        """
        return -(speed_jump ** 2) / (2 * height_jump)

    def height_jump(self, speed_jump, time):
        return speed_jump * time + (self.gravity * time ** 2) / 2

    def upgrade_vertica_pos(self, speed_jump, instant=None,
                            jump=True):
        if instant is None:
            instant = self.instant
        self.pos += Vector(0, self.height_jump(speed_jump,
                                                self.times[instant - 1]),
                           0)
        self.pos += Vector(0, -self.height_jump(speed_jump,
                                               self.times[instant]),
                           0)
        # por alguna razon, el personaje baja mas de lo debido en el ultimo salto,
        # con esta condicion se corrige dicho error pero es una solucion parche
        if self.pos.y > self.pj_pos.y and jump:
            self.pos = self.pj_pos

    def jump(self, speed_jump):
        if self.can_jump:
            if self.instant < self.instants:
                self.upgrade_vertica_pos(speed_jump)
                self.instant += 1

        if self.instant >= self.instants:
            self.instant = 1
            self.can_jump = False

    def upgrade_fall(self):
        self.pos += Vector(0,
                           self.height_jump(0,
                                            0.5*(self.instant-1)),
                           0)

        self.pos += Vector(0,
                           -self.height_jump(0,
                                             0.5*self.instant),
                           0)

    def fall(self, oct: Octagon):
        """
        El movimiento se detiene y el personaje empieza a caer,
        se pierde la partida, el personaje no puede saltar
        :return:
        """
        muerte = False
        if -oct.lenz / 2 < oct.pos.z - self.pos.z - 80 < oct.lenz / 2 and \
                not self.can_jump:
            # print("cumplo primera condicion")
            if self.get_type_lower_block(oct) == 1 or \
                            self.get_type_lower_block(oct) == 2:
                print("cumplo segunda condicion")
                print("pos anterio:", self.pos.y)
                self.upgrade_fall()
                print("nueva pos: ", self.pos.y)
                self.instant += 1
                self.can_jump = False

        if self.instant >= self.instants:
            self.instant = 1
            muerte = True

        return muerte

    def is_falling(self):
        oct = self.octagons[1]
        return self.fall(oct)

    def move_to_sides(self, speed_jump, left=False, right=False):
        if left:
            ang = -self.discrete_rotatio()
        elif right:
            ang = self.discrete_rotatio()

        else:
            ang = 0

        if self.side:
            if self.instant < self.instants:
                print("modifico la rotacion segun Delta_ang: ", ang)
                self.upgrade_vertica_pos(speed_jump)
                Stage.modify_fi(self, 100*ang)
                self.instant += 1
                self.right = False
                self.left = False

        if self.instant >= self.instants:
            self.instant = 1
            self.side = False
            self.right = False
            self.left = False

    def discrete_rotatio(self):
        full_ang = (np.pi * 67.5) / 180
        return full_ang / self.instants

    @staticmethod
    def get_type_lower_block(octagon: Octagon):
        number = int(octagon.master_fi * 180 / (np.pi * 45))
        lower = number + 4
        if lower > 7:
            lower -= 80

        print(lower)
        return octagon.tipos[lower]

    def mov_sceneario(self):
        return Stage.modify_pos(self.speed)

    def draw(self):
        Stage.dibujar(self)
        Personaje.dibujar(self)



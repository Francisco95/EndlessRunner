from EndlessRunner.CC3501Utils import Vector
from OpenGL.GL import *
from EndlessRunner.Stage import Stage
from EndlessRunner.Personaje import Personaje
from EndlessRunner.MasterOctagon import Octagon
import numpy as np


class Interactions(Personaje, Stage):
    def __init__(self, cam_pos: Vector, pj_pos=Vector(0, -90, 300),
                 master_pos=Vector(0, 0, -400),
                 dimensions_block=(240, 20, 780), number=6,
                 speed=50, speed_jump=60):
        self.cam_pos = cam_pos
        self.master_pos = master_pos
        Personaje.__init__(self)
        Stage.__init__(self, dimensions=dimensions_block,
                       number=number)
        self.pj_pos = pj_pos
        self.pos += pj_pos
        print("posicion del pj: ", self.pos.y)
        Stage.modify_pos(self, self.master_pos)
        self.falling = False  # esta cayendo, permite bloquear otras acciones
        self.jumping = False  # esta saltando, permite bloquear otras acciones
        self.spinning = False  # esta rotando, permite bloquear otras acciones
        self.left = False
        self.right = False
        self.speed = speed  # velocidad de desplazamiento
        self.speed_jump = speed_jump  # velocidad del salto
        self.height_j = 70  # altura del salto
        self.instants = self.get_number_of_instants()
        self.instant = 1  # define un contador de instantes
        self.gravity = self.get_gravity()
        self.time_jump = self.time()

    def get_number_of_instants(self):
        return round((self.dimensions[2] + 40) / self.speed)

    def get_gravity(self):
        """
        en base a una velocidad y una altura calcula la gravedad
        necesaria
        :param speed_jump:
        :param height_jump:
        :return:
        """
        return -(self.speed_jump ** 2) / (2 * self.height_j)

    def height_jump(self, time, speed_jump=None):
        if speed_jump is None:
            speed_jump = self.speed_jump
        return speed_jump * time + (self.gravity * time ** 2) / 2

    def vertical_position(self, time, speed=None):
        if speed is None:
            speed = self.speed_jump
        r = -self.pj_pos.y + speed * time + (self.gravity * time ** 2) / 2
        # print("estoy actualizando posicion")
        # print("antes, y=", self.pos.y, ", ahora y=", r)
        return r

    def max_height(self, speed):
        """
        dada una velocidad vertical, calculada la gravedad del sistema, obtiene
        la altura maxima que alcanzara.
        :param speed: velocidad vertical
        :return:
        """
        return speed ** 2 / (2 * self.gravity)

    def time(self):
        max_time = np.sqrt(-2 * self.height_j / self.gravity)
        times = []
        for i in range(self.instants):
            times.append(max_time * 2 * (i + 1) / self.instants)

        return times

    def upgrade_vertica_pos(self, type_jump: str):
        """
        actualiza la posicion vertical
        :param type_jump:
        :return:
        """
        next_time = self.time_jump[self.instant]
        if type_jump is "jump":
            print("actualizo segun jump")
            speed_jump = self.speed_jump

        elif type_jump is "small_jump":
            speed_jump = self.speed_jump / 2

        elif type_jump is "fall":
            speed_jump = 0

        else:
            speed_jump = 0
            raise ValueError('type_jump invalido')

        self.pos = Vector(0, -self.vertical_position(next_time, speed=speed_jump),
                          300)
        # self.pos += Vector(0, self.height_jump(prev_time, speed_jump=speed_jump), 0)
        # self.pos += Vector(0, -self.height_jump(next_time, speed_jump=speed_jump), 0)
        # por alguna razon, el personaje baja mas de lo debido en el ultimo
        # salto, con esta condicion se corrige dicho error pero es una
        # solucion parche
        if self.pos.y > self.pj_pos.y and type_jump is not "fall":
            self.pos = self.pj_pos

    def fall_condition(self, oct: Octagon):
        """
        El movimiento se detiene y el personaje empieza a caer,
        se pierde la partida, el personaje no puede saltar
        :return:
        """
        aux_cond_type = False
        aux_cond_pos = False
        lower_type = self.get_type_lower_block(oct)
        if lower_type == 1 or lower_type == 2:
            aux_cond_type = True

        xfloor, yfloor, zfloor = oct.set_displacement_pos().cartesianas()
        if abs(oct.pos.z - self.pos.z) < oct.lenz / 2 + 150:
        # if -oct.lenz / 2 < oct.pos.z - self.pos.z < oct.lenz / 2:
            # verificaremos que la posicion vertical este en el piso
            # print("delta pos: ", abs(-yfloor - self.pos.y))
            if abs(-yfloor - self.pos.y) < 200:
                aux_cond_pos = True

        if abs(-yfloor - self.pos.y) < 198.5: #mas abajo del piso siempre se cumple
            aux_cond_pos = True
            aux_cond_type = True

        aux_cond_counter = True if self.instant < self.instants else False

        return [not self.jumping, not self.spinning, aux_cond_type, aux_cond_pos,
                aux_cond_counter]

    def jump_conditions(self):
        aux_cond_counter = True if self.instant < self.instants else False
        return [not self.falling, self.jumping, not self.spinning, aux_cond_counter]

    def spin_conditions(self):
        aux_cond_counter = True if self.instant < self.instants else False
        return [not self.falling, not self.jumping, self.spinning, aux_cond_counter,
                (self.right and not self.left) or (not self.right and self.left)]

    def jump(self):
        # print("estoy en jump")
        if all(self.jump_conditions()):
            print("salto")
            print("instat = ", self.instant)
            self.upgrade_vertica_pos("jump")
            self.instant += 1

        if self.instant >= self.instants \
                and not self.falling and not self.spinning:
            print("termina el salto")
            self.instant = 1
            self.jumping = False

    def fall(self):
        oct = self.octagons[1]
        run = True
        if all(self.fall_condition(oct)):  # cumple todas las condiciones de caida
            print("me caigo")
            self.upgrade_vertica_pos("fall")
            self.instant += 1
            self.falling = True  # esto permitira bloquear otras acciones

        if self.instant >= self.instants \
                and not self.jumping \
                and not self.spinning:  # luego de cierto tiempo "muere"
            self.falling = False
            self.muerte = True
            run = False
            # aqui debemos generar la muerte

        return run

    def spin(self):
        if self.left and not self.right:
            ang = -self.discrete_rotation()
        elif self.right and not self.left:
            ang = self.discrete_rotation()

        if all(self.spin_conditions()):
            # print("modifico la rotacion segun Delta_ang: ", 4 * ang * 180 / np.pi)
            # print("instant = ", self.instant)
            self.upgrade_vertica_pos("small_jump")
            Stage.modify_fi(self, ang)
            self.instant += 1

        if self.instant >= int(self.instants / 2) + 1 \
                and not self.jumping and not self.falling:
            self.instant = 1
            # Stage.modify_fi(self, 45)
            # print("nuevo master fi = ", self.ang)
            self.spinning = False
            self.right = False
            self.left = False

    def add_time_conditions(self, oct):
        """
                El movimiento se detiene y el personaje empieza a caer,
                se pierde la partida, el personaje no puede saltar
                :return:
                """
        aux_cond_type = False
        aux_cond_pos = False
        lower_type = self.get_type_lower_block(oct)
        if lower_type >= 3:
            # print("lower tipe es comodin")
            aux_cond_type = True

        xfloor, yfloor, zfloor = oct.set_displacement_pos().cartesianas()
        if abs(oct.pos.z - self.pos.z) < oct.lenz / 2 + 150:
            # if -oct.lenz / 2 < oct.pos.z - self.pos.z < oct.lenz / 2:
            # verificaremos que la posicion vertical este en el piso
            # print("delta pos: ", abs(-yfloor - self.pos.y))
            if abs(-yfloor - self.pos.y) < 210:
                aux_cond_pos = True

        return [not self.jumping, not self.spinning, not self.falling,
                aux_cond_type, aux_cond_pos]

    def add_time(self):
        oct = self.octagons[1]
        get_more_time = False
        # print("add_time jumping: ", self.jumping)
        # print("add_time spinning: ", self.spinning)
        # print("add_time falling: ", self.falling)
        if all(self.add_time_conditions(oct)):
            print("agrego tiempo")
            get_more_time = True

        return get_more_time

    def discrete_rotation(self):
        full_ang = 45 / int(self.instants / 2)
        return full_ang

    @staticmethod
    def get_type_lower_block(octagon: Octagon):
        number = round(octagon.master_fi / 45)
        if number > 0:
            number -= 8
        lower = -int(number) + 4
        if lower > 7:
            lower -= 8
        # print(lower, " tipo=", octagon.tipos[lower])
        return octagon.tipos[lower]

    def mov_sceneario(self):
        return Stage.modify_pos(self, Vector(0, 0, -self.speed))

    def draw(self):
        Stage.dibujar(self)
        Personaje.dibujar(self)



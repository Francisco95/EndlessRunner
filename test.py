from EndlessRunner.initializers import *
from EndlessRunner.Eje import *
from EndlessRunner.CC3501Utils import *
import pygame.locals as lcl
import numpy as np
from EndlessRunner.Stage import *
from EndlessRunner.Personaje import Personaje
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'  # centrar pantalla


def main():
    # inicializar
    ancho = 800
    alto = 600
    init(ancho, alto, "ejemplo aux")

    # crear objetos
    clock = pygame.time.Clock()

    # camara
    camPos = Vector(0.0, -0.1, -100.0)
    camAt = Vector(0, 0, 0)

    # luz
    light = GL_LIGHT0
    # l_position = Vector(1000.0, 0.0, 500.0)
    l_position = Vector(0.0, 2.0, -130.0)

    # crear una luz coherente con su color base
    l_diffuse = [1.0, 1.0, 1.0, 1.0]
    l_ambient = [i / 5.0 for i in l_diffuse]
    l_specular = l_diffuse

    l_position = [0.0, 1.0, -2.0, 0.0]

    # otros valores estandar
    l_constant_attenuation = 0.0
    l_linear_attenuation = 0.0
    l_quadratic_attenuation = 0.0

    l_spot_cutoff = 180.0
    l_spot_direction = Vector(0.0, -1.0, -0.5)  # direccion
    l_spot_exponent = 0.0
    eje = Eje(400.0)  # R,G,B = X,Y,Z
    master_pos = Vector(0, 0, camPos.z)
    s = Stage()
    s.modify_pos(master_pos)
    pj = Personaje()
    print((s.dimensions[0] / 2) * np.tan(np.pi * 67.5 / 180))
    pj.pos += Vector(0, 90, 300)
    # variables de tiempo
    fps = 30
    dt = 1.0 / fps

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(60, ancho / alto, 1, 3000)

    glMatrixMode(GL_MODELVIEW)

    run = True
    while run:
        desp = Vector(0, 0, 0)
        delta_fi = 0
        ang = 0
        # manejo de eventos
        for event in pygame.event.get():
            if event.type == lcl.QUIT:
                run = False

        # obtener teclas presionadas
        pressed = pygame.key.get_pressed()
        if pressed[lcl.K_w] or pressed[lcl.K_UP]:
            desp = Vector(0, 0, 10)
            delta_fi = 2
        if pressed[lcl.K_s] or pressed[lcl.K_DOWN]:
            desp = Vector(0, 0, -10)
            delta_fi = -2
        if pressed[lcl.K_SPACE]:
            ang = np.pi * 40 / 180

        if pressed[lcl.K_d]:
            camPos += Vector(0, 0, -1)

        if pressed[lcl.K_a]:
            camPos += Vector(0, 0, 1)

        pj.rotation(delta_fi)
        s.modify_fi(ang)
        s.modify_pos(desp)
        s.update_config(camPos.z)
        # Limpiar buffers
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # dibujar objetos
        eje.dibujar()
        s.dibujar()
        pj.dibujar()
        # oct.dibujar(index, master_pos)
        # oct2.dibujar(index+1, master_pos + Vector(0, 0, oct.lenz/2))
        # oct2.dibujar(index+2, master_pos + Vector(0, 0, oct.lenz))

        # camara
        glLoadIdentity()
        gluLookAt(camPos.x, camPos.y, camPos.z,  # posicion
                  camAt.x, camAt.y, camAt.z,  # mirando hacia
                  0.0, 0.0, 1.0)  # inclinacion
        # luz
        glLightfv(light, GL_POSITION, l_position)
        glLightfv(light, GL_AMBIENT, l_ambient)
        glLightfv(light, GL_SPECULAR, l_specular)
        glLightfv(light, GL_DIFFUSE, l_diffuse)
        glLightf(light, GL_CONSTANT_ATTENUATION, l_constant_attenuation)
        glLightf(light, GL_LINEAR_ATTENUATION, l_linear_attenuation)
        glLightf(light, GL_QUADRATIC_ATTENUATION, l_quadratic_attenuation)
        glLightf(light, GL_SPOT_CUTOFF, l_spot_cutoff)
        glLightfv(light, GL_SPOT_DIRECTION, l_spot_direction.cartesianas())
        glLightf(light, GL_SPOT_EXPONENT, l_spot_exponent)

        glEnable(light)

        pygame.display.flip()  # cambiar imagen
        clock.tick(fps)  # esperar 1/fps segundos

    pygame.quit()
    return


main()
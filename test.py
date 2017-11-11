from .initializers import *
from .Eje import *
from tarea3.CC3501Utils import *
import pygame.locals as lcl
import numpy as np
from .Stage import *
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'  # centrar pantalla

def dibujar(master_pos, master_fi, listas):
    glPushMatrix()
    glTranslatef(master_pos.x, -150, master_pos.z)
    glRotatef(master_fi, 0, 0, 1)  # Rotacion en torno a eje Z
    glCallLists(listas)
    glPopMatrix()

def main():
    # inicializar
    ancho = 800
    alto = 600
    init(ancho, alto, "ejemplo aux")

    # crear objetos
    clock = pygame.time.Clock()

    # camara
    camPos = Vector(0.0, -0.1, -1000.0)
    camAt = Vector(0, 40, 0)

    # luz
    light = GL_LIGHT0
    # l_position = Vector(1000.0, 0.0, 500.0)
    l_position = Vector(0.0, 1000.0, 500.0)

    # crear una luz coherente con su color base
    l_diffuse = [1.0, 1.0, 1.0, 1.0]
    l_ambient = [i / 5.0 for i in l_diffuse]
    l_specular = l_diffuse

    l_position = [1.0, 1.0, 1.0, 0.0]
    l_ambient = [0.0, 0.0, 0.0, 1.0]
    l_diffuse = [1.0, 1.0, 1.0, 1.0]
    l_specular = [1.0, 1.0, 1.0, 1.0]

    # otros valores estandar
    l_constant_attenuation = 0.0
    l_linear_attenuation = 0.0
    l_quadratic_attenuation = 0.0

    l_spot_cutoff = 180.0
    l_spot_direction = Vector(-1.0, 0.0, -0.5)  # direccion
    l_spot_exponent = 0.0
    index = glGenLists(3)
    eje = Eje(400.0)  # R,G,B = X,Y,Z
    master_pos = Vector(0, 0, 0)
    s = Stage()
    # variables de tiempo
    fps = 30
    dt = 1.0 / fps

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(100, ancho / alto, 1, 3000)

    glMatrixMode(GL_MODELVIEW)

    run = True
    while run:
        desp = Vector(0, 0, 0)
        ang = 0
        # manejo de eventos
        for event in pygame.event.get():
            if event.type == lcl.QUIT:
                run = False

        # obtener teclas presionadas
        pressed = pygame.key.get_pressed()
        if pressed[lcl.K_w] or pressed[lcl.K_UP]:
            desp = Vector(0, 0, 50)
        if pressed[lcl.K_s] or pressed[lcl.K_DOWN]:
            desp = Vector(0, 0, -50)
        if pressed[lcl.K_SPACE]:
            ang = np.pi * 40 / 180

        s.modify_fi(ang)
        s.modify_pos(desp)
        s.update_config(camPos.z)
        # Limpiar buffers
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # dibujar objetos
        eje.dibujar()
        s.dibujar()
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
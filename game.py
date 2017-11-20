from EndlessRunner.initializers import *
from EndlessRunner.Eje import *
import pygame.locals as lcl
from EndlessRunner.Stage import *
from EndlessRunner.Interactions import Interactions
from EndlessRunner.textos import Tiempo, InitScreen, DeathScreen
from EndlessRunner.texto import draw_text_box
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PIL import Image as Image
from EndlessRunner.CC3501Utils import cuadrilatero
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'  # centrar pantalla


def drawText(value, x, y, windowHeight, windowWidth, step=18):
    """Draw the given text at given 2D position in window
    """
    glMatrixMode(GL_PROJECTION)
    # For some reason the GL_PROJECTION_MATRIX is overflowing with a single push!
    # glPushMatrix()
    matrix = glGetDouble(GL_PROJECTION_MATRIX)

    glLoadIdentity()
    glOrtho(0.0, windowHeight or 32, 0.0, windowWidth or 32, -1.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2i(x, y)
    lines = 0
    ##	import pdb
    ##	pdb.set_trace()
    for character in value:
        if character == '\n':
            glRasterPos2i(x, y - (lines * 18))
        else:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(character));
    glPopMatrix();
    glMatrixMode(GL_PROJECTION)
    # For some reason the GL_PROJECTION_MATRIX is overflowing with a single push!
    # glPopMatrix();
    glLoadMatrixd(matrix)  # should have un-decorated alias for this...

    glMatrixMode(GL_MODELVIEW)

def main():
    # inicializar
    ancho = 800
    alto = 600
    init(ancho, alto, "ejemplo aux")  # inicializa pygame, opengl
    glutInit()  # inicializa glut

    # crear objetos
    clock = pygame.time.Clock()

    # camara
    camPos = Vector(0.0, -0.1, -100.0)
    camAt = Vector(0, 0, 0)

    # luz
    light = GL_LIGHT0
    l_position = [0.0, 1.0, -2.0, 0.0]

    # crear una luz coherente con su color base
    l_diffuse = [1.0, 1.0, 1.0, 1.0]
    l_ambient = [i / 5.0 for i in l_diffuse]
    l_specular = l_diffuse

    # otros valores estandar
    l_constant_attenuation = 0.0
    l_linear_attenuation = 0.0
    l_quadratic_attenuation = 0.0

    l_spot_cutoff = 180.0
    l_spot_direction = Vector(0.0, -1.0, -0.5)  # direccion
    l_spot_exponent = 0.0

    eje = Eje(400.0)  # R,G,B = X,Y,Z
    obj = Interactions(camPos, pj_pos=Vector(0, 90, 300),
                       master_pos=Vector(0, 0, camPos.z))
    print("el numero de instants=", obj.instants)
    text = Tiempo(Vector(30, -26.5, 0))
    text.game_time = 20
    scr1 = InitScreen(ancho, alto)  # init screen
    scr2 = DeathScreen(ancho, alto) # death screen

    # variables de tiempo
    fps = 30
    dt = 1.0 / fps

    # glMatrixMode(GL_PROJECTION)
    # glLoadIdentity()
    #
    # gluPerspective(100, ancho / alto, 1, 3000)
    #
    # glMatrixMode(GL_MODELVIEW)
    run = True
    pause = False
    start = False
    death = False
    while run:
        desp = Vector(0, 0, 0)
        delta_fi = -4
        ang = 0
        # manejo de eventos
        if not pause and start:
            run = obj.fall()

        for event in pygame.event.get():
            if event.type == lcl.QUIT:
                run = False

            if event.type == lcl.KEYDOWN:
                if event.key == lcl.K_p:
                    print("pauso")
                    pause = True if not pause else False

                # acciones de control, recordar quitarlas!!
                if event.key == lcl.K_q:
                    camPos += Vector(0, 0, -20)

                if event.key == lcl.K_e:
                    camPos += Vector(0, 0, 20)

                if event.key == lcl.K_RETURN and not death:
                    start = True

                if (event.key == lcl.K_UP or event.key == lcl.K_DOWN) \
                        and not start and not death:
                    scr1.mode = "normal" if scr1.mode is "endless" else "endless"

                if event.key == lcl.K_UP and not start and death:
                    if scr2.option is "retry":
                        scr2.option = "exit"
                    elif scr2.option is "change_mode":
                        scr2.option = "retry"
                    elif scr2.option is "exit":
                        scr2.option = "change_mode"

                if event.key == lcl.K_DOWN and not start and death:
                    if scr2.option is "retry":
                        scr2.option = "change_mode"
                    elif scr2.option is "change_mode":
                        scr2.option = "exit"
                    elif scr2.option is "exit":
                        scr2.option = "retry"

                if event.key == lcl.K_RETURN and not start and death \
                        and scr2.option is "retry":
                    print("reseteo")
                    obj = Interactions(camPos, pj_pos=Vector(0, 90, 300),
                                       master_pos=Vector(0, 0, camPos.z))
                    text.game_time = 20
                    death = False
                    start = True

                if event.key == lcl.K_RETURN and not start and death \
                        and scr2.option is "exit":
                    run = False

                if event.key == lcl.K_RETURN and not start and death \
                        and scr2.option is "change_mode":
                    start = False
                    death = False
                    obj = Interactions(camPos, pj_pos=Vector(0, 90, 300),
                                       master_pos=Vector(0, 0, camPos.z))
                    text.game_time = 20

        # obtener teclas presionadas
        pressed = pygame.key.get_pressed()
        # las acciones de caer, saltar o rotar bloquean a las otras acciones:
        if not obj.falling and not obj.jumping and not obj.spinning:
            if pressed[lcl.K_SPACE] and not pressed[lcl.K_d] \
                    and not pressed[lcl.K_a]:
                obj.jumping = True
            if pressed[lcl.K_d] and not pressed[lcl.K_SPACE] \
                    and not pressed[lcl.K_a]:
                obj.right = True
                obj.left = False
                obj.spinning = True
            if pressed[lcl.K_a] and not pressed[lcl.K_SPACE] \
                    and not pressed[lcl.K_d]:
                obj.right = False
                obj.left = True
                obj.spinning = True

        if not pause and start:  # si no esta pausado el juego
            obj.spin()
            obj.jump()
            obj.rotation(delta_fi)
            obj.modify_pos(Vector(0, 0, -obj.speed))
            obj.update_config(camPos.z)
            if obj.add_time():
                print("agrego tiempo")
                print("antes tenia: ", text.game_time, " segundos")
                text.game_time += 1/4
                print("ahora tengo: ", text.game_time, " segundos")

        # Limpiar buffers
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # dibujar objetos
        if obj.pos.y > 150:  # has muerto
            start = False
            death = True
            scr2.main_info(text.session_time)
            scr2.options()

        if start:
            eje.dibujar()
            obj.draw()
            texto = text.get_time_text(clock)
            text.dibujar(texto)

        if not start and not death:
            scr1.main_title()
            scr1.instructions()
            scr1.game_mode()
        # glColor3f(0, 0, 0)
        # drawText('hello world', ancho - 100, alto - 20, ancho, alto)

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
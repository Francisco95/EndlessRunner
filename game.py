from EndlessRunner.initializers import *
from EndlessRunner.Eje import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import os
from EndlessRunner.key_interactions import *

os.environ['SDL_VIDEO_CENTERED'] = '1'  # centrar pantalla


def main():
    # inicializar
    ancho = 800
    alto = 600
    init(ancho, alto, "ENDLESS RUNNER")  # inicializa pygame, opengl
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
    text = Tiempo(Vector(30, -26.5, 0))
    text.game_time = 20
    text.crear()
    scr1 = InitScreen(ancho, alto)  # init screen
    scr2 = DeathScreen(ancho, alto) # death screen
    scr3 = VictoryScree(ancho, alto)  # victory screen

    # variables de tiempo
    fps = 30
    dt = 1.0 / fps

    pg.mixer.init(11025)
    pg.mixer.music.load("sounds/Electrical-of-cosmic.mp3")
    pg.mixer.music.set_volume(0.4)
    pg.mixer.music.play(-1)
    menu1 = pg.mixer.Sound("sounds/sfx_menu_move3.wav")
    menu2 = pg.mixer.Sound("sounds/sfx_menu_select2.wav")
    long_jump = pg.mixer.Sound("sounds/sfx_movement_jump16.wav")
    short_jump = pg.mixer.Sound("sounds/sfx_movement_jump8.wav")
    die = pg.mixer.Sound("sounds/sfx_sounds_falling7.wav")
    win = pg.mixer.Sound("sounds/Ta-Da.wav")
    pause = pg.mixer.Sound("sounds/sfx_sounds_pause1_in.wav")
    more_time = pg.mixer.Sound("sounds/sfx_movement_portal1.wav")
    less_time = pg.mixer.Sound("sounds/sfx_movement_portal3.wav")
    sounds = [menu1, menu2, long_jump, short_jump, win, pause,
              more_time, less_time]
    run = True
    pause = False
    start = False
    death = False
    win = False
    while run:
        delta_fi = -4

        # manejo de eventos
        if not pause and start:
            run = obj.fall()

        for event in pygame.event.get():
            obj, scr1, scr2, scr3, text, list_return = event_press(event, camPos,
                                                                   scr1, scr2,
                                                                   scr3, obj, text,
                                                                   pause, death,
                                                                   start, run, win,
                                                                   sounds)
        start = list_return[0]
        death = list_return[1]
        run = list_return[2]
        pause = list_return[3]
        win = list_return[4]

        # obtener teclas presionadas
        pressed = pygame.key.get_pressed()
        obj = pressed_keys(pressed, obj, sounds)
        if not pause:
            if start:
                if not win:
                    if not death and obj.preg_counter < len(map1):
                        print(obj.preg_counter, len(map1))
                        obj.spin()
                        obj.jump()
                        obj.rotation(delta_fi)
                        obj.modify_pos(Vector(0, 0, -obj.speed))
                        obj.update_config(camPos.z)
                        obj.accelerate()
                        if obj.add_time():
                            obj.lost_soud = True
                            text.game_time += 1 / 2
                            if obj.add_sound:
                                more_time.play(0)
                                obj.add_sound = False

                        elif obj.rest_time():
                            obj.add_sound = True
                            text.game_time -= 1 / 2
                            if obj.lost_soud:
                                less_time.play(0)
                                obj.lost_soud = False

                        else:
                            obj.add_sound = True
                            obj.lost_soud = True

        if obj.falling and obj.fall_sound:
            die.play(0)
            pg.time.wait(50)
            obj.fall_sound = False
            # die.set_volume(0)
        # Limpiar buffers
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # dibujar objetos
        if obj.pos.y > 150:  # has muerto
            start = False
            death = True
            scr2.main_info(text.session_time)
            scr2.options()

        elif death and not start and not win:
            scr2.main_info(text.session_time)
            scr2.options()

        elif obj.pregenerated is True:
            if obj.preg_counter == len(map1):
                win = True
                start = False
                death = True
                scr3.remaining_time = text.session_time

        if start:
            obj.draw()
            if not pause:
                texto = text.get_time_text(clock)
            text.dibujar(texto)

            if text.game_time <= 0.1:
                death = True
                start = False

        if not start and not death and not win:
            scr1.main_title()
            scr1.instructions()
            scr1.game_mode()

        if not start and win:
            scr3.main_info()
            scr3.options()

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
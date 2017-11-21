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


def pressed_keys(pressed, obj: Interactions):
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

    return obj


def event_press(event, camPos, scr1: InitScreen,
                scr2: DeathScreen, obj: Interactions,
                text: Tiempo, pause, death, start, run):

    if event.type == lcl.QUIT:
        run = False

    if event.type == lcl.KEYDOWN:
        if event.key == lcl.K_ESCAPE:
            run = False

        if event.key == lcl.K_p:
            pause = True if not pause else False

        # acciones de control, recordar quitarlas!!
        if event.key == lcl.K_q:
            camPos += Vector(0, 0, -20)

        if event.key == lcl.K_e:
            camPos += Vector(0, 0, 20)

        if event.key == lcl.K_UP and not start and not death:
            if scr1.mode is "normal":
                scr1.mode = "about_game"
            elif scr1.mode is "endless":
                scr1.mode = "normal"
            elif scr1.mode is "about_game":
                scr1.mode = "endless"

        elif event.key == lcl.K_DOWN and not start and not death:
            if scr1.mode is "normal":
                scr1.mode = "endless"
            elif scr1.mode is "endless":
                scr1.mode = "about_game"
            elif scr1.mode is "about_game":
                scr1.mode = "normal"

        if event.key == lcl.K_UP and not start and death:
            if scr2.option is "retry":
                scr2.option = "exit"
            elif scr2.option is "change_mode":
                scr2.option = "retry"
            elif scr2.option is "exit":
                scr2.option = "change_mode"

        elif event.key == lcl.K_DOWN and not start and death:
            if scr2.option is "retry":
                scr2.option = "change_mode"
            elif scr2.option is "change_mode":
                scr2.option = "exit"
            elif scr2.option is "exit":
                scr2.option = "retry"

        if event.key == lcl.K_RETURN and not death and not start \
                and scr1.mode is "endless":  # start endless mode
            start = True

        elif event.key == lcl.K_RETURN and not death and not start \
                and scr1.mode is "about_game":  # about the game
            #no implementado
            run = False
            print("::::::::::")
            print("esto no fue implementado :(")
            print("::::::::::")

        elif event.key == lcl.K_RETURN and not death and not start \
                and scr1.mode is "normal":  # normal mode
            #no implementado
            run = False
            print("::::::::::")
            print("el modo normal de juego, con mapas pre-creados no fue"
                  "implementado :(")
            print("::::::::::")

        elif event.key == lcl.K_RETURN and not start and death \
                and scr2.option is "retry":  # reset
            obj = Interactions(camPos, pj_pos=Vector(0, 90, 300),
                               master_pos=Vector(0, 0, camPos.z))
            text.game_time = 10
            death = False
            start = True

        elif event.key == lcl.K_RETURN and not start and death \
                and scr2.option is "exit":  # exit
            run = False

        elif event.key == lcl.K_RETURN and not start and death \
                and scr2.option is "change_mode":  # return main menu
            start = False
            death = False
            obj = Interactions(camPos, pj_pos=Vector(0, 90, 300),
                               master_pos=Vector(0, 0, camPos.z))
            text.game_time = 10

    list_return = [start, death, run, pause]
    return obj, scr1, scr2, text, list_return

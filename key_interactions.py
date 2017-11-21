import pygame.locals as lcl
from EndlessRunner.Stage import *
from EndlessRunner.Interactions import Interactions
from EndlessRunner.textos import Tiempo, InitScreen, DeathScreen, VictoryScree
import pygame as pg


def pressed_keys(pressed, obj: Interactions, sounds):
    if not obj.falling and not obj.jumping and not obj.spinning:
        if pressed[lcl.K_SPACE] and not pressed[lcl.K_d] \
                and not pressed[lcl.K_a]:

            sounds[2].play(0)
            obj.jumping = True
        if pressed[lcl.K_d] and not pressed[lcl.K_SPACE] \
                and not pressed[lcl.K_a]:
            sounds[3].play(0)
            obj.right = True
            obj.left = False
            obj.spinning = True
        if pressed[lcl.K_a] and not pressed[lcl.K_SPACE] \
                and not pressed[lcl.K_d]:
            sounds[3].play(0)
            obj.right = False
            obj.left = True
            obj.spinning = True

    return obj


def event_press(event, camPos, scr1: InitScreen,
                scr2: DeathScreen, scr3: VictoryScree, obj: Interactions,
                text: Tiempo, pause, death, start, run, win, sounds):
    if event.type == lcl.QUIT:
        run = False

    if event.type == lcl.KEYDOWN:
        if event.key == lcl.K_ESCAPE:
            run = False

        if event.key == lcl.K_p:
            sounds[5].play(0)
            pause = True if not pause else False

        if event.key == lcl.K_UP and not start and not death and not win:
            if scr1.mode is "normal":
                sounds[0].play(0)
                pg.time.wait(150)
                scr1.mode = "about_game"
            elif scr1.mode is "endless":
                scr1.mode = "normal"
                sounds[0].play(0)
                pg.time.wait(150)
            elif scr1.mode is "about_game":
                scr1.mode = "endless"
                sounds[0].play(0)
                pg.time.wait(150)

        elif event.key == lcl.K_DOWN and not start and not death and not win:
            if scr1.mode is "normal":
                sounds[0].play(0)
                pg.time.wait(150)
                scr1.mode = "endless"
            elif scr1.mode is "endless":
                sounds[0].play(0)
                pg.time.wait(150)
                scr1.mode = "about_game"
            elif scr1.mode is "about_game":
                sounds[0].play(0)
                pg.time.wait(150)
                scr1.mode = "normal"

        if event.key == lcl.K_UP and not start and death and not win:
            if scr2.option is "retry":
                sounds[0].play(0)
                pg.time.wait(150)
                scr2.option = "exit"
            elif scr2.option is "change_mode":
                sounds[0].play(0)
                pg.time.wait(150)
                scr2.option = "retry"
            elif scr2.option is "exit":
                sounds[0].play(0)
                pg.time.wait(150)
                scr2.option = "change_mode"

        elif event.key == lcl.K_DOWN and not start and death and not win:
            if scr2.option is "retry":
                sounds[0].play(0)
                pg.time.wait(150)
                scr2.option = "change_mode"
            elif scr2.option is "change_mode":
                sounds[0].play(0)
                pg.time.wait(150)
                scr2.option = "exit"
            elif scr2.option is "exit":
                sounds[0].play(0)
                pg.time.wait(150)
                scr2.option = "retry"

        if event.key == lcl.K_UP and not start and win:
            if scr3.option is "continue":
                sounds[0].play(0)
                pg.time.wait(150)
                scr3.option = "exit"
            elif scr3.option is "retry":
                sounds[0].play(0)
                pg.time.wait(150)
                scr3.option = "continue"
            elif scr3.option is "change_mode":
                sounds[0].play(0)
                pg.time.wait(150)
                scr3.option = "retry"
            elif scr3.option is "exit":
                sounds[0].play(0)
                pg.time.wait(150)
                scr3.option = "change_mode"

        elif event.key == lcl.K_DOWN and not start and win:
            if scr3.option is "continue":
                sounds[0].play(0)
                pg.time.wait(150)
                scr3.option = "retry"
            elif scr3.option is "retry":
                sounds[0].play(0)
                pg.time.wait(150)
                scr3.option = "change_mode"
            elif scr3.option is "change_mode":
                sounds[0].play(0)
                pg.time.wait(150)
                scr3.option = "exit"
            elif scr3.option is "exit":
                sounds[0].play(0)
                pg.time.wait(150)
                scr3.option = "continue"

        if event.key == lcl.K_RETURN and not death and not start \
                and scr1.mode is "endless" and not win:  # start endless mode
            print("presiono enter en endless")
            sounds[1].play(0)
            pg.time.wait(150)
            start = True

        elif event.key == lcl.K_RETURN and not death and not start \
                and scr1.mode is "about_game":  # about the game
            # no implementado
            sounds[1].play(0)
            pg.time.wait(150)
            run = False
            print("::::::::::")
            print("esto no fue implementado :(")
            print("::::::::::")

        elif event.key == lcl.K_RETURN and not death and not start \
                and scr1.mode is "normal" and not win:  # normal mode
            # no implementado
            # run = False
            # print("::::::::::")
            # print("el modo normal de juego, con mapas pre-creados no fue"
            #       "implementado :(")
            # print("::::::::::")
            sounds[1].play(0)
            pg.time.wait(150)
            print("presiono enter en normal")
            obj.pregenerated = True
            obj.preg_counter = 0
            obj.octagons = []
            obj.generate_first_octagons(Vector(0, 0, 0))
            start = True

        elif event.key == lcl.K_RETURN and not start and death \
                and ((scr2.option is "retry" and not win)
                     or scr3.option is "retry"):  # reset
            sounds[1].play(0)
            pg.time.wait(150)
            print("presiono enter en retry")
            if obj.pregenerated:
                obj = Interactions(camPos, pj_pos=Vector(0, 90, 300),
                                   master_pos=Vector(0, 0, camPos.z))
                obj.pregenerated = True
                obj.preg_counter = 0
                obj.octagons = []
                obj.generate_first_octagons(Vector(0, 0, 0))
            else:
                obj = Interactions(camPos, pj_pos=Vector(0, 90, 300),
                                   master_pos=Vector(0, 0, camPos.z))
            scr2.option = "retry"
            scr3.option = "continue"
            text.game_time = 20
            death = False
            start = True
            win = False

        elif event.key == lcl.K_RETURN and not start and death \
                and ((scr2.option is "exit" and not win)
                     or scr3.option is "exit"):
            #
            # exit
            sounds[1].play(0)
            pg.time.wait(150)
            run = False

        elif event.key == lcl.K_RETURN and not start and death \
                and ((scr2.option is "change_mode" and not win)
                     or scr3.option is "change_mode"):
            print("presiono enter en change mode")
            start = False
            death = False
            win = False
            sounds[1].play(0)
            pg.time.wait(150)
            obj = Interactions(camPos, pj_pos=Vector(0, 90, 300),
                               master_pos=Vector(0, 0, camPos.z))
            text.game_time = 20
            scr2.option = "retry"
            scr3.option = "continue"

        elif event.key == lcl.K_RETURN and not start and death \
                and win and scr3.option is "continue":
            sounds[1].play(0)
            pg.time.wait(150)
            print("presiono continue")
            # solo un mapa implementado :/, te envia al menu princial
            start = False
            death = False
            win = False
            pause = False
            obj = Interactions(camPos, pj_pos=Vector(0, 90, 300),
                               master_pos=Vector(0, 0, camPos.z))
            text.game_time = 20
            scr2.option = "retry"
            scr3.option = "continue"

    list_return = [start, death, run, pause, win]
    return obj, scr1, scr2, scr3, text, list_return

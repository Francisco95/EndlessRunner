from EndlessRunner.CC3501Utils import *
import pygame.locals as lcl
import pygame
from OpenGL.GL import *
from OpenGL.GLUT import *


def drawTextwithglut(value, x, y):

    glRasterPos2i(x, y)
    lines = 0
    ##	import pdb
    ##	pdb.set_trace()
    for character in value:
        if character == '\n':
            glRasterPos2i(x, y - (lines * 18))
        else:
            glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(character))

def draw_text_box(pos, width, text, color=(255, 255, 255, 0),
                  fondo=(255, 0, 0, 0)):
    tamanno = int(width / 2)
    font = pygame.font.Font(None, tamanno)
    text_surface = font.render(text, True, color, fondo)
    text_width = text_surface.get_width()
    text_height = text_surface.get_height()
    x = pos[0] + (width - text_width) / 2
    y = pos[1] + (width - text_height) / 2
    position = (x, y)
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    glRasterPos2d(*position)
    glDrawPixels(text_surface.get_width(), text_surface.get_height(),
                 GL_RGBA, GL_UNSIGNED_BYTE, text_data)


def drawText(value, x, y, windowHeight, windowWidth, withglut=True, width_text=100,
             color=(255, 255, 255, 0)):
    """
    Draw the given text at given 2D position in window.
    Funcion extraida de stackoverflow

    :param value:
    :param x:
    :param y:
    :param windowHeight:
    :param windowWidth:
    :param step:
    :return:
    """
    glMatrixMode(GL_PROJECTION)
    matrix = glGetDouble(GL_PROJECTION_MATRIX)

    glLoadIdentity()
    glOrtho(0.0, windowHeight or 32, 0.0, windowWidth or 32, -1.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    if withglut:
        drawTextwithglut(value, x, y)
    else:
        draw_text_box([x, y], width_text, value, color=color,
                      fondo=(0, 0, 0, 0))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glLoadMatrixd(matrix)  # should have un-decorated alias for this...

    glMatrixMode(GL_MODELVIEW)


class Tiempo:
    def __init__(self, pos: Vector, tiempo=0,
                 width_window=800, height_window=600,
                 width_text=144, height_text=32):
        self.pos = pos
        self.tiempo = tiempo
        self.lista = 0
        self.width_wind = width_window
        self.height_wind = height_window
        self.width_txt = width_text
        self.height_txt = height_text
        self.game_time = 0
        self.session_time = 0
        self.crear()

    def crear(self):
        self.lista = glGenLists(1)
        glNewList(self.lista, GL_COMPILE)
        glEnable(GL_COLOR_MATERIAL)
        glBegin(GL_TRIANGLES)
        if self.game_time > 15:
            glColor4f(0.0, 0.0, 0.0, 0.7)
        elif 8 < self.game_time <= 15:
            glColor4f(1.0, 1.0, 0.0, 0.7)
        else:
            glColor4f(0.8, 0.0, 0.0, 0.7)

        p1 = self.pos + Vector(-21, -4, 0)
        p2 = self.pos + Vector(21, -4, 0)
        p3 = self.pos + Vector(21, 4, 0)
        p4 = self.pos + Vector(-21, 4, 0)
        cuadrilatero(p1, p2, p3, p4)
        glEnd()
        glEndList()

    def dibujar(self, texto):

        if 14 < self.game_time < 16 \
                or 7 < self.game_time < 9:
            self.crear()

        glPushMatrix()
        glTranslatef(self.pos.x, self.pos.y, self.pos.z)
        # glRotatef(self.angulo, 0, 0, 1)  # Rotacion en torno a eje Z
        glCallList(self.lista)
        glPopMatrix()

        glColor3f(1, 1, 1)
        drawText(texto, self.width_wind - self.width_txt,
                 self.height_wind - self.height_txt, self.width_wind,
                 self.height_wind)

    def get_time_text(self, clock):
        delay = clock.get_time() * 10 ** (-3)
        self.session_time += delay #mantiene registro del timpo de juego
        self.game_time = self.game_time - delay

        if int(round(self.game_time, 2) * 100 - round(self.game_time, 1) * 100) == 0:
            text = str(round(self.game_time, 2)) + "0. secs"

        else:
            text = str(round(self.game_time, 2)) + ". secs"

        return text


class InitScreen:
    def __init__(self, width_window, height_window):
        self.width_wind = width_window
        self.height_wind = height_window
        self.time = 0
        self.mode = "endless"

    def main_title(self):
        drawText("ENDLESS RUNNER", self.width_wind / 2 - 85,
                 self.height_wind / 2 + 110,
                 self.width_wind, self.height_wind, withglut=False,
                 width_text=self.width_wind / 4)

    def instructions(self):
        offsety = - 100
        offsetx = + 220

        drawText("Instructions:",
                 self.width_wind / 2 - 85 + offsetx,
                 self.height_wind / 2 + 140 + offsety,
                 self.width_wind, self.height_wind, withglut=False,
                 width_text=self.width_wind / 6)

        drawText("Use A or D to rotate",
                 self.width_wind / 2 - 55 + offsetx,
                 self.height_wind / 2 + 90 + offsety,
                 self.width_wind, self.height_wind, withglut=False,
                 width_text=self.width_wind / 8.5)

        drawText("Use SPACE to jump",
                 self.width_wind / 2 - 55 + offsetx,
                 self.height_wind / 2 + 50 + offsety,
                 self.width_wind, self.height_wind, withglut=False,
                 width_text=self.width_wind / 8.5)

        drawText("Use P to Pause",
                 self.width_wind / 2 - 89 + offsetx,
                 self.height_wind / 2 + 10 + offsety,
                 self.width_wind, self.height_wind, withglut=False,
                 width_text=self.width_wind / 8.5)

        drawText("Use Esc to Quit",
                 self.width_wind / 2 - 86 + offsetx,
                 self.height_wind / 2 - 30 + offsety,
                 self.width_wind, self.height_wind, withglut=False,
                 width_text=self.width_wind / 8.5)

        drawText("Use UP or DOWN to",
                 self.width_wind / 2 - 55 + offsetx,
                 self.height_wind / 2 - 70 + offsety,
                 self.width_wind, self.height_wind, withglut=False,
                 width_text=self.width_wind / 8.5)

        drawText("change game mode",
                 self.width_wind / 2 - 50 + offsetx,
                 self.height_wind / 2 - 103 + offsety,
                 self.width_wind, self.height_wind, withglut=False,
                 width_text=self.width_wind / 8.5)

        drawText("Press ENTER to",
                 self.width_wind / 2 - 77 + offsetx,
                 self.height_wind / 2 - 143 + offsety,
                 self.width_wind, self.height_wind, withglut=False,
                 width_text=self.width_wind / 8)

        drawText("choose Game mode",
                 self.width_wind / 2 - 43 + offsetx,
                 self.height_wind / 2 - 176 + offsety,
                 self.width_wind, self.height_wind, withglut=False,
                 width_text=self.width_wind / 8)

    def normal_mode(self, offsetx, offsety, color=(255, 255, 255, 0)):
        drawText("Normal Run",
                 self.width_wind / 2 - 78 + offsetx,
                 self.height_wind / 2 + 90 + offsety,
                 self.width_wind, self.height_wind, withglut=False,
                 width_text=self.width_wind / 8, color=color)

    def endless_mode(self, offsetx, offsety, color=(255, 255, 255, 0)):
        drawText("Endless Run",
                 self.width_wind / 2 - 74 + offsetx,
                 self.height_wind / 2 + 40 + offsety,
                 self.width_wind, self.height_wind, withglut=False,
                 width_text=self.width_wind / 8, color=color)

    def normal_mode_disabled(self, offsetx, offsety,color=(255, 255, 255, 0)):
        drawText("Normal Run (disabled)",
                 self.width_wind / 2 - 48 + offsetx,
                 self.height_wind / 2 + 90 + offsety,
                 self.width_wind, self.height_wind, withglut=False,
                 width_text=self.width_wind / 8, color=color)

    def draw(self, text, offsetx, offsety, ratio_width, withglut=False,
             color=(255, 255, 255, 0)):
        drawText(text, self.width_wind / 2 + offsetx,
                 self.height_wind / 2 + offsety,
                 self.width_wind, self.height_wind, withglut=withglut,
                 width_text=self.width_wind / ratio_width, color=color)

    def game_mode(self):
        offsety = - 100
        offsetx = - 200
        delay = 30
        self.time = (self.time + 1 + delay) % delay
        drawText("MENU:",
                 self.width_wind / 2 - 85 + offsetx,
                 self.height_wind / 2 + 140 + offsety,
                 self.width_wind, self.height_wind, withglut=False,
                 width_text=self.width_wind / 6)
        if self.mode is "normal":
            if 0 < self.time < delay - 10:
                self.normal_mode(offsetx, offsety, color=(255, 0, 0, 0))
                # self.normal_mode_disabled(offsetx, offsety, color=(255, 0, 0, 0))
            self.endless_mode(offsetx, offsety)
            self.draw("About game", -78 + offsetx, -10 + offsety, 8)

        if self.mode is "endless":
            if 0 < self.time < delay - 10:
                self.endless_mode(offsetx, offsety, color=(255, 0, 0, 0))
            self.normal_mode(offsetx, offsety)
            # self.normal_mode_disabled(offsetx, offsety)
            self.draw("About game", -78 + offsetx, -10 + offsety, 8)

        if self.mode is "about_game":
            if 0 < self.time < delay - 10:
                self.draw("About game", -78 + offsetx, -10 + offsety,
                          8, color=(255, 0, 0, 0))
            self.normal_mode(offsetx, offsety)
            # self.normal_mode_disabled(offsetx, offsety)
            self.endless_mode(offsetx, offsety)



class DeathScreen:
    def __init__(self, width_window, height_window):
        self.width_wind = width_window
        self.height_wind = height_window
        self.mode = "endless"
        self.option = "retry"
        self.time = 0
        self.best = 0

    def main_info(self, progression):
        offsetx = 200
        offsety = -50
        if self.mode is "endless":
            drawText("GAME OVER", self.width_wind / 2 - 115,
                     self.height_wind / 2 + 110,
                     self.width_wind, self.height_wind, withglut=False,
                     width_text=self.width_wind / 4)
            ur_time = "YOUR TIME: {} secs.".format(round(progression, 2))
            if round(progression, 2) > self.best:
                self.best = round(progression, 2)
            best_time = "BEST TIME: {} secs.".format(self.best)
            drawText(ur_time, self.width_wind / 2 - 55 - offsetx,
                     self.height_wind / 2 + 110 + offsety,
                     self.width_wind, self.height_wind, withglut=False,
                     width_text=self.width_wind / 10)

            drawText(best_time, self.width_wind / 2 - 55 + offsetx,
                     self.height_wind / 2 + 110 + offsety,
                     self.width_wind, self.height_wind, withglut=False,
                     width_text=self.width_wind / 10)

        elif self.mode is "normal":
            self.draw("GAME OVER", -115, 110, 4)
            ur_time = "YOUR TIME: {} secs.".format(round(progression, 2))
            self.draw(ur_time, -55 - offsetx, 110 + offsety, 10)

    def options(self):
        offsetx = 0
        offsety = -150
        delay = 30
        self.time = (self.time + 1 + delay) % delay

        if self.option is "retry":
            if 0 < self.time < delay - 10:
                self.draw("RETRY", -55 + offsetx, 80 + offsety, 10, color=(255, 0,
                                                                           0, 0))
            self.draw("CHANGE MODE", -55 + offsetx, 40 + offsety, 10)
            self.draw("EXIT", -55 + offsetx, offsety, 10)

        if self.option is "change_mode":
            if 0 < self.time < delay - 10:
                self.draw("CHANGE MODE", -55 + offsetx,
                          40 + offsety, 10, color=(255, 0, 0, 0))
            self.draw("RETRY", -55 + offsetx, 80 + offsety, 10)
            self.draw("EXIT", -55 + offsetx, offsety, 10)

        if self.option is "exit":
            if 0 < self.time < delay - 10:
                self.draw("EXIT", -55 + offsetx, offsety, 10, color=(255, 0, 0, 0))
            self.draw("CHANGE MODE", -55 + offsetx, 40 + offsety, 10)
            self.draw("RETRY", -55 + offsetx, 80 + offsety, 10)


    def draw(self, text, offsetx, offsety, ratio_width, withglut=False,
             color=(255, 255, 255, 0)):
        drawText(text, self.width_wind / 2 + offsetx,
                 self.height_wind / 2 + offsety,
                 self.width_wind, self.height_wind, withglut=withglut,
                 width_text=self.width_wind / ratio_width, color=color)


class VictoryScree:
    def __init__(self, width_window, height_window):
        self.width_wind = width_window
        self.height_wind = height_window
        self.mode = "normal"
        self.option = "continue"
        self.lvl = 1
        self.remaining_time = 0
        self.best_time_map1 = 0
        self.time = 0

    def draw(self, text, offsetx, offsety, ratio_width, withglut=False,
             color=(255, 255, 255, 0)):
        drawText(text, self.width_wind / 2 + offsetx,
                 self.height_wind / 2 + offsety,
                 self.width_wind, self.height_wind, withglut=withglut,
                 width_text=self.width_wind / ratio_width, color=color)

    def main_info(self):
        offsetx = 200
        offsety = -50
        if self.mode is "normal":
            info = "LEVEL {} COMPLETE!".format(1 if self.lvl == 1 else 2)
            drawText(info, self.width_wind / 2 - 115,
                     self.height_wind / 2 + 110,
                     self.width_wind, self.height_wind, withglut=False,
                     width_text=self.width_wind / 4)
            ur_time = "REMAINIGN TIME: {} secs.".format(round(self.remaining_time,
                                                              2))
            if self.lvl == 1 \
                    and round(self.remaining_time, 2) > self.best_time_map1:
                self.best_time_map1 = round(self.remaining_time, 2)

            best_time_map1 = "BEST TIME: {} secs.".format(self.best_time_map1)
            self.draw(ur_time, 10 - offsetx, 140 + offsety, 10)

            if self.lvl == 1:
                self.draw(best_time_map1, -30 - offsetx, 100 + offsety, 10)

    def options(self):
        offsetx = 0
        offsety = -150
        delay = 30
        self.time = (self.time + 1 + delay) % delay

        if self.option is "continue":
            if 0 < self.time < delay - 10:
                self.draw("CONTINUE", -55 + offsetx, 80 + offsety, 10, color=(255, 0,
                                                                           0, 0))
            self.draw("RETRY", -55 + offsetx, 40 + offsety, 10)
            self.draw("CHANGE MODE", -55 + offsetx, offsety, 10)
            self.draw("EXIT", -55 + offsetx, -40 + offsety, 10)

        if self.option is "retry":
            if 0 < self.time < delay - 10:
                self.draw("RETRY", -55 + offsetx, 40 + offsety, 10, color=(255, 0,
                                                                           0, 0))
            self.draw("CONTINUE", -55 + offsetx, 80 + offsety, 10)
            self.draw("CHANGE MODE", -55 + offsetx, 0 + offsety, 10)
            self.draw("EXIT", -55 + offsetx, - 40 + offsety, 10)

        if self.option is "change_mode":
            if 0 < self.time < delay - 10:
                self.draw("CHANGE MODE", -55 + offsetx,
                          0 + offsety, 10, color=(255, 0, 0, 0))
            self.draw("CONTINUE", -55 + offsetx, 80 + offsety, 10)
            self.draw("RETRY", -55 + offsetx, 40 + offsety, 10)
            self.draw("EXIT", -55 + offsetx, - 40 + offsety, 10)

        if self.option is "exit":
            if 0 < self.time < delay - 10:
                self.draw("EXIT", -55 + offsetx, -40 + offsety, 10, color=(255, 0,
                                                                           0, 0))
            self.draw("CONTINUE", -55 + offsetx, 80 + offsety, 10)
            self.draw("CHANGE MODE", -55 + offsetx, 0 + offsety, 10)
            self.draw("RETRY", -55 + offsetx, 40 + offsety, 10)

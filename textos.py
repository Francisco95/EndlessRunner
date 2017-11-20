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
            glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(character))

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


def drawText(value, x, y, windowHeight, windowWidth, withglut=True, width_text=100):
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
    # For some reason the GL_PROJECTION_MATRIX is overflowing with a single push!
    # glPushMatrix()
    matrix = glGetDouble(GL_PROJECTION_MATRIX)

    glLoadIdentity()
    glOrtho(0.0, windowHeight or 32, 0.0, windowWidth or 32, -1.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    # glRasterPos2i(x, y)
    # lines = 0
    # ##	import pdb
    # ##	pdb.set_trace()
    # for character in value:
    #     if character == '\n':
    #         glRasterPos2i(x, y - (lines * 18))
    #     else:
    #         glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(character))
    if withglut:
        drawTextwithglut(value, x, y)
    else:
        draw_text_box([x, y], width_text, value, color=(255, 255, 255, 0),
                      fondo=(0, 0, 0, 0))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    # For some reason the GL_PROJECTION_MATRIX is overflowing with a single push!
    # glPopMatrix();
    glLoadMatrixd(matrix)  # should have un-decorated alias for this...

    glMatrixMode(GL_MODELVIEW)


class Tiempo:
    def __init__(self, pos: Vector, tiempo=0,
                 width_window=800, height_window=600,
                 width_text=134, height_text=27):
        self.pos = pos
        self.tiempo = tiempo
        self.lista = 0
        self.width_wind = width_window
        self.height_wind = height_window
        self.width_txt = width_text
        self.height_txt = height_text
        self.game_time = 0
        self.crear()

    def crear(self):
        self.lista = glGenLists(1)
        glNewList(self.lista, GL_COMPILE)
        glEnable(GL_COLOR_MATERIAL)
        glBegin(GL_TRIANGLES)
        glColor4f(0.0, 0.0, 0.0, 0.7)
        p1 = self.pos + Vector(-19, -3.5, 0)
        p2 = self.pos + Vector(19, -3.5, 0)
        p3 = self.pos + Vector(19, 3.5, 0)
        p4 = self.pos + Vector(-19, 3.5, 0)
        cuadrilatero(p1, p2, p3, p4)
        glEnd()
        glEndList()

    def dibujar(self, texto):
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
        delay = clock.get_time()
        self.game_time = self.game_time - delay * 10 ** (-3)

        if int(round(self.game_time, 2) * 100 - round(self.game_time, 1) * 100) == 0:
            text = str(round(self.game_time, 2)) + "0. secs"

        else:
            text = str(round(self.game_time, 2)) + ". secs"

        return text


class InitScreen:
    def __init__(self, width_window, height_window):
        self.width_wind = width_window
        self.height_wind = height_window

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

    def game_mode(self, mode="endless"):
        offsety = - 100
        offsetx = - 200

        drawText("Game Mode:",
                 self.width_wind / 2 - 85 + offsetx,
                 self.height_wind / 2 + 140 + offsety,
                 self.width_wind, self.height_wind, withglut=False,
                 width_text=self.width_wind / 6)
        if mode is "normal":
            drawText("Normal Run",
                    self.width_wind / 2 - 78 + offsetx,
                    self.height_wind / 2 + 90 + offsety,
                    self.width_wind, self.height_wind, withglut=False,
                    width_text=self.width_wind / 8)

        if mode is "endless":
            drawText("Endless Run",
                    self.width_wind / 2 - 74 + offsetx,
                    self.height_wind / 2 + 40 + offsety,
                    self.width_wind, self.height_wind, withglut=False,
                    width_text=self.width_wind / 8)

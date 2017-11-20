from OpenGL.GL import *
from OpenGL.GLUT import *
import pygame


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


def draw_text_circle(pos, radius, text, color=(255, 255, 255, 0),
                  fondo=(255, 0, 0, 0)):
    tamanno = int(2.5 * radius)
    font = pygame.font.Font(None, tamanno)
    text_surface = font.render(text, True, color, fondo)
    text_width = text_surface.get_width()
    text_height = text_surface.get_height()
    x = pos[0] - radius + (2*radius - text_width) / 2
    y = pos[1] + radius + (2*radius - text_height) / 2
    position = (x, y)
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    glRasterPos3d(*position)
    glDrawPixels(text_surface.get_width(), text_surface.get_height(),
                 GL_RGBA, GL_UNSIGNED_BYTE, text_data)


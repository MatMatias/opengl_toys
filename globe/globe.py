from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
from math import *
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import png

# Some api in the chain is translating the keystrokes to this octal string
# so instead of saying: ESCAPE = 27, we use the following.
ESCAPE = b"\033"

# Number of the glut window.
window = 0

# Rotations for cube.
xrot = yrot = zrot = 0.0
dx = 0.1
dy = 0
dz = 0


def LoadTextures():
    global texture
    texture = [glGenTextures(1)]

    glBindTexture(GL_TEXTURE_2D, texture[0])
    reader = png.Reader(filename="globe/map.png")
    w, h, pixels, metadata = reader.read_flat()
    if metadata["alpha"]:
        mode = GL_RGBA
    else:
        mode = GL_RGB
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexImage2D(
        GL_TEXTURE_2D, 0, mode, w, h, 0, mode, GL_UNSIGNED_BYTE, pixels.tolist()
    )
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)


def InitGL(Width, Height):
    LoadTextures()
    glEnable(GL_TEXTURE_2D)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45.0, float(Width) / float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glTranslatef(0, 0, -5)


def ReSizeGLScene(Width, Height):
    if Height == 0:
        Height = 1
    glViewport(0, 0, Width, Height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width) / float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)


phi0 = 0
phin = 2 * pi

theta0 = -pi / 2
thetan = pi / 2

n = 50

dphi = (phin - phi0) / n
dtheta = (thetan - theta0) / n


def esphere():
    glRotatef(1, 0, 1, 0)
    radius = 1

    phi = phi0
    for i in range(0, n + 1):
        glBegin(GL_TRIANGLE_STRIP)
        theta = theta0
        for j in range(0, n + 1):
            x = radius * cos(theta) * cos(phi)
            y = -radius * sin(theta)
            z = -radius * cos(theta) * sin(phi)

            x_2 = radius * cos(theta) * cos(phi + dphi)
            y_2 = -radius * sin(theta)
            z_2 = -radius * cos(theta) * sin(phi + dphi)

            glTexCoord2f(i / (n - 1), j / (n - 1))
            glVertex3f(x, y, z)
            glTexCoord2f((i + 1) / (n - 1), j / (n - 1))
            glVertex3f(x_2, y_2, z_2)

            theta += dtheta
        glEnd()
        phi += dphi


def DrawGLScene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    esphere()
    glutSwapBuffers()


def keyPressed(tecla, *_):
    if tecla == ESCAPE:
        glutLeaveMainLoop()


def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(0, 0)
    glutCreateWindow("Globe")
    glutDisplayFunc(DrawGLScene)
    glutIdleFunc(DrawGLScene)
    glutReshapeFunc(ReSizeGLScene)
    glutKeyboardFunc(keyPressed)
    InitGL(640, 480)
    glutMainLoop()


main()

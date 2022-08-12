from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from math import *
import math
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import png

quadro = 0


def calculaNormalFace(v0, v1, v2):
    x = 0
    y = 1
    z = 2
    U = (v2[x] - v0[x], v2[y] - v0[y], v2[z] - v0[z])
    V = (v1[x] - v0[x], v1[y] - v0[y], v1[z] - v0[z])
    N = (
        (U[y] * V[z] - U[z] * V[y]),
        (U[z] * V[x] - U[x] * V[z]),
        (U[x] * V[y] - U[y] * V[x]),
    )
    NLength = sqrt(N[x] * N[x] + N[y] * N[y] + N[z] * N[z])
    return (N[x] / NLength, N[y] / NLength, N[z] / NLength)


def desenha():
    global quadro
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glPushMatrix()
    # glRotatef(quadro,0.0,1.0,0.0)
    glRotatef(90.0 + quadro, 1.0, 0.0, 0.0)
    raio = 0.7
    n = 6
    glBegin(GL_TRIANGLES)

    for i in range(0, n):  # Faces
        # glColor3fv(cores[(i)%len(cores)]) #comentar cores
        v0 = [0, 0, -1]
        a = (i / n) * 2 * math.pi
        x = raio * math.cos(a)
        y = raio * math.sin(a)
        v1 = [x, y, 0]
        a = ((i + 1) / n) * 2 * math.pi
        x = raio * math.cos(a)
        y = raio * math.sin(a)
        v2 = [x, y, 0]

        glNormal3fv(calculaNormalFace(v0, v1, v2))

        glVertex3fv(v0)
        glVertex3fv(v1)
        glVertex3fv(v2)

    glEnd()

    glBegin(GL_TRIANGLE_FAN)
    # glColor3f(0.3,0.3,0.3) #comentar cores
    glNormal3f(0, 0, 1.0)
    glVertex3f(0.0, 0.0, 0.0)
    for i in range(0, n + 1):
        a = (i / n) * 2 * math.pi
        x = raio * math.cos(a)
        y = raio * math.sin(a)
        glVertex3f(x, y, 0.0)

    glEnd()

    glutSwapBuffers()
    quadro += 1
    glPopMatrix()


def timer(i):
    glutPostRedisplay()
    glutTimerFunc(50, timer, 1)


def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, float(w) / float(h), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    gluLookAt(10, 0, 0, 0, 0, 0, 0, 1, 0)


def init():
    mat_ambient = (0.4, 0.0, 0.0, 1.0)
    mat_diffuse = (1.0, 0.0, 0.0, 1.0)
    mat_specular = (1.0, 0.5, 0.5, 1.0)
    mat_shininess = (50,)
    light_position = (10, 0, 0)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    #    glShadeModel(GL_FLAT)
    glShadeModel(GL_SMOOTH)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialfv(GL_FRONT, GL_SHININESS, mat_shininess)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_MULTISAMPLE)


# PROGRAMA PRINCIPAL
glutInit(sys.argv)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH | GLUT_MULTISAMPLE)
glutInitWindowSize(800, 600)
glutCreateWindow("Illuminated Pyramid")
glutReshapeFunc(reshape)
glutDisplayFunc(desenha)
glEnable(GL_MULTISAMPLE)
glEnable(GL_DEPTH_TEST)
# glClearColor(0.,0.,0.,1.)
gluPerspective(45, 800.0 / 600.0, 0.1, 100)
glTranslatef(0.0, 0.0, -10.0)
glutTimerFunc(50, timer, 1)
init()
glutMainLoop()

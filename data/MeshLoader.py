from OpenGL.GL import *
from OpenGL.GLU import *
import sys
from PyQt6.QtWidgets import *
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtCore import *

import math
import numpy as np

mat_spec = [1, 1, 1, 1]
mat_diff = [1.0, 0.7, 0.3, 1]
mat_ambi = [0, 0, 0, 0]
mat_shin = [120]

lit_spec = [1, 1, 1, 1]
lit_diff = [1, 1, 1, 1]
lit_ambi = [0, 0, 0, 1]

light_pos = [1, 1, 0.1, 1]

def LightSet():
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_spec)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diff)
    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambi)
    glMaterialfv(GL_FRONT, GL_SHININESS, mat_shin)

    glLightfv(GL_LIGHT0, GL_SPECULAR, lit_spec)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lit_diff)
    glLightfv(GL_LIGHT0, GL_AMBIENT, lit_ambi)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

def LightPositioning() :
    glLightfv(GL_LIGHT0, GL_POSITION, light_pos)




def drawPlane():
    n, w = 100, 500
    # n: 체스판 한면의 정점수, w: 체스판 한면의 길이
   
    d = w / (n-1) # 인접한 두 정점 사이의 간격

    #  체스판 그리기
    glNormal3f(0, 1, 0)
    glBegin(GL_QUADS)
    for i in range(n):
        for j in range(n):
            if (i+j)%2 == 0:
                startX = -w/2 + i*d
                startZ = -w/2 + j*d
                glVertex3f(startX, 0, startZ)
                glVertex3f(startX, 0, startZ+d)
                glVertex3f(startX+d, 0, startZ+d)
                glVertex3f(startX+d, 0, startZ)
    glEnd()

class MeshLoader:
    def __init__(self):
        self.nV = 0 # 정점의 개수
        self.nF = 0 # 면의 개수
        self.vertexBuffer = None # 정점 버퍼
        self.idxBuffer = None # 면을 구성하는 정점 인덱스 버퍼
        self.list = None

    def loadData(self, filename, negateNormal = False):
        with open(filename, 'rt') as inputfile:
            self.nV = int(next(inputfile))
            
            self.vertexBuffer = np.zeros(shape = (self.nV*3, ), dtype=float)
            ### 정점 별 법선벡터 저장을 위한 공간 준비
            self.normalBuffer = np.zeros(shape = (self.nV*3, ), dtype=float)

            for i in range(self.nV):
                verts = next(inputfile).split()
                self.vertexBuffer[i*3:i*3+3] = verts[0:3]
            
            coordMin = self.vertexBuffer.min()
            coordMax = self.vertexBuffer.max()
            scale = max([coordMin, coordMax], key=abs)
            self.vertexBuffer /= scale

            self.nF = int(next(inputfile))
            self.idxBuffer = np.zeros(shape=(self.nF*3, ), dtype=int)

            
            for i in range(self.nF):
                idx = next(inputfile).split()
                self.idxBuffer[i*3: i*3+3] = idx[1:4]
                index = self.idxBuffer[i*3: i*3+3]
                p0 = self.vertexBuffer[index[0]*3: index[0]*3 + 3]
                p1 = self.vertexBuffer[index[1]*3: index[1]*3 + 3]
                p2 = self.vertexBuffer[index[2]*3: index[2]*3 + 3]
                u = p1-p0
                v = p2-p0
                N = np.cross(u, v)
                self.normalBuffer[index[0]*3: index[0]*3 + 3] += N
                self.normalBuffer[index[1]*3: index[1]*3 + 3] += N
                self.normalBuffer[index[2]*3: index[2]*3 + 3] += N
            
            for i in range(self.nV):
                N = self.normalBuffer[i*3: i*3 + 3]                
                norm = np.linalg.norm(N)
                N = N/norm
                if negateNormal:
                    N = -N
                self.normalBuffer[i*3: i*3 + 3] = N


    def draw(self):
        glBegin(GL_TRIANGLES)
        for i in range(self.nF):
            verts = self.idxBuffer[i*3: i*3+3]
            glNormal3fv( self.normalBuffer[verts[0]*3 : verts[0]*3 +3] )
            glVertex3fv( self.vertexBuffer[verts[0]*3 : verts[0]*3 +3] )
            glNormal3fv( self.normalBuffer[verts[1]*3 : verts[1]*3 +3] )
            glVertex3fv( self.vertexBuffer[verts[1]*3 : verts[1]*3 +3] )
            glNormal3fv( self.normalBuffer[verts[2]*3 : verts[2]*3 +3] )
            glVertex3fv( self.vertexBuffer[verts[2]*3 : verts[2]*3 +3] )
        glEnd()



    def make_displayList(self):
        self.list = glGenLists(1)
        glNewList(self.list, GL_COMPILE)
        self.draw()
        glEndList()

    def draw_list(self):
        glCallList(self.list)

class MyGLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
       
    def initializeGL(self):
        self.meshLoader1 = MeshLoader() # 메시 로더 생성
        self.meshLoader1.loadData('./sphere.txt', negateNormal=True)
        self.meshLoader1.make_displayList()

        self.meshLoader2 = MeshLoader() # 메시 로더 생성
        self.meshLoader2.loadData('./cube.txt')
        self.meshLoader2.make_displayList()

        glClearColor(0.0, 0.0, 0.0, 1.0)
        glEnable(GL_NORMALIZE)
        glEnable(GL_DEPTH_TEST)

        self.planeList = glGenLists(1)
        glNewList(self.planeList, GL_COMPILE)
        # 그리기 코드
        drawPlane()
        glEndList()

        LightSet()
        

    def resizeGL(self, width, height):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60, width/height, 0.01, 100)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        LightPositioning()
        gluLookAt(0,4,4, 0,1,0, 0,1,0)

        glCallList(self.planeList)
     
        glEnable(GL_LIGHTING)
        self.meshLoader1.draw_list()
        glTranslatef(3,1,0)
        self.meshLoader2.draw_list()
        glDisable(GL_LIGHTING)


class MyWindow(QMainWindow):
    def __init__(self, title=''):
        QMainWindow.__init__(self)
        self.setWindowTitle(title)
        self.glWidget = MyGLWidget()
        self.setCentralWidget(self.glWidget)

def main(argv = []):
    app = QApplication(argv)
    window = MyWindow('메시 읽기')
    window.setFixedSize(1200, 600)
    window.show()
    app.exec()

if __name__ == '__main__':
    main(sys.argv)

import math
import time
import os
import yaml

MASS = -1 # kg
BI_WIDTH = -1 # m
BI_HEIGHT = -1  
GRAVITY = -1 # m/s2

TORS_DAMP = 0.04
LIN_DAMP = 0.04

# Get parent directory name
here = os.path.dirname(os.path.realpath(__file__))
CONFIG_FILE_NAME = here+'\config.yaml'

def readConfigFile():

    global CONFIG_FILE_NAME 
    global BI_WIDTH
    global BI_HEIGHT
    global MASS
    global GRAVITY
    with open(CONFIG_FILE_NAME, 'r') as file:
        cfg = yaml.load(file)
    BI_HEIGHT     = cfg['main']['bi_height']*0.01 # convert to meters
    BI_WIDTH     = cfg['main']['bi_width']*0.01
    MASS         = cfg['main']['bi_mass']
    GRAVITY      = cfg['main']['gravity'] 
 

class BiCopter():


    def __init__(self, x, y, theta=0):
        
        readConfigFile()

        self.x = x
        self.y = y
        self.theta = theta
        self.vx = 0.0
        self.vy = 0.0
        self.w = 0.0

        # Input forces
        self.F1 = 0.0
        self.F2 = 0.0

        # BiCopter Dimensions
        self.m = MASS
        self.L = BI_WIDTH
        self.h = BI_HEIGHT
        self.I = self.m/12 * (self.L**2 + self.h**2)

        self.lastTime = time.time()


    """
    physics()
        Call as fast as possible
        Robust to different timeSteps
    """
    def physics(self):

        # Calculate accelerations
        ax = -1/self.m*math.sin(self.theta)*(self.F1+self.F2) - LIN_DAMP/self.m * self.vx
        ay = 1/self.m*math.cos(self.theta)*(self.F1+self.F2) - GRAVITY - LIN_DAMP/self.m * self.vy
        # print("ay: ",ay)
        alpha = self.L/(2*self.I) * (self.F2-self.F1) - TORS_DAMP/self.I * self.w
        # print("alpha: ", alpha)

        # Calculate timeStep
        curTime = time.time()
        timeStep = curTime - self.lastTime
        # print("TimeStep: ", timeStep)
        self.lastTime = curTime

        # Update position
        self.x += self.vx*timeStep + 0.5*ax*timeStep**2
        self.y += self.vy*timeStep + 0.5*ay*timeStep**2
        self.theta += self.w*timeStep + 0.5*alpha*timeStep**2

        # Update velocities
        self.vx += ax*timeStep
        self.vy += ay*timeStep
        self.w += alpha*timeStep


        # Ground force
        if self.y < 0:
            if self.vy < 0:
                self.vy = -0.5*self.vy
            self.y = 0

    def groundForce(self):
        sin = math.sin(theta)
        cos = math.cos(theta)

        x3,y3 = self.x + self.L/2*cos, self.y - self.L/2*sin # lower right
        x4,y4 = self.x - self.L/2*cos, self.y + self.L/2*sin # lower left       

        x1,y1 = x4 - self.h*sin, y4 - self.h*cos #true_x - self.bi_w/2, true_y-self.bi_h # Upper left
        x2,y2 = x3 - self.h*sin, y3 - self.h*cos

        if y1 < 0:
            y1 = 0


    def updateForces(self, F1, F2):
        self.F1 = F1
        self.F2 = F2

    def getPos(self):
        return (self.x, self.y, self.theta)

    def getVel(self):
        return (self.vx, self.vy, self.w)

    def setStartTime(self):
        self.lastTime = time.time()



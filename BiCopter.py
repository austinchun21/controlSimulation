
import math
import time


MASS = 0.1 
BI_WIDTH = 0.25 # cm
BI_HEIGHT = 0.05 
GRAVITY = 9.81

# x = x, y, theta, vx, vy, w
# x. = vx, vy, w, vx., vy., w.
# Ax + Bu = x.
 

class BiCopter():


	def __init__(self, x, y, theta=0):
		# self.pos = [x,y,theta, 0,0,0]
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
		self.I = self.L*self.h/12 * (self.L**2 + self.h**2)

		self.lastTime = time.time()


	"""
	physics()
		Call as fast as possible
		Robust to different timeSteps
	"""
	def physics(self):

		# Calculate accelerations
		ax = -1/self.m*math.sin(self.theta)*(self.F1+self.F2)
		ay = 1/self.m*math.cos(self.theta)*(self.F1+self.F2) - self.m*GRAVITY
		alpha = self.L/(2*self.I) * (self.F2-self.F1)

		# Calculate timeStep
		curTime = time.time()
		timeStep = curTime - self.lastTime
		self.lastTime = curTime

		# Update position
		self.x = self.x + self.vx*timeStep + 0.5*ax*timeStep**2
		self.y = self.y + self.vy*timeStep + 0.5*ay*timeStep**2
		self.theta = self.theta + self.w*timeStep + 0.5*alpha*timeStep**2

		# Update velocities
		self.vx = self.vx + ax*timeStep
		self.vy = self.vy + ay*timeStep
		self.w = self.w + alpha*timeStep


	def updateForces(self, F1, F2):
		self.F1 = F1
		self.F2 = F2

	def getPos(self):
		return (self.x, self.y, self.theta)

	def getVel(self):
		return (self.vx, self.vy, self.w)

	def setStartTime(self):
		self.lastTime = time.time()



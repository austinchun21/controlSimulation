
import math
import time


MASS = 1
BI_WIDTH = 1 #0.25 # m
BI_HEIGHT = 0.2 #0.05 
GRAVITY = 1009.81

TORS_DAMP = 0.04
LIN_DAMP = 0.04


 

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
		self.I = self.m * self.L*self.h/12 * (self.L**2 + self.h**2)

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
		print("TimeStep: ", timeStep)
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


	def updateForces(self, F1, F2):
		self.F1 = F1
		self.F2 = F2

	def getPos(self):
		return (self.x, self.y, self.theta)

	def getVel(self):
		return (self.vx, self.vy, self.w)

	def setStartTime(self):
		self.lastTime = time.time()



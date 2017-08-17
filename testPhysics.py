##################
## testPhysics.py
##      Simple control of biCopter in screen
##
##      Austin Chun
##      Aug 2017
##################

import math
import time
from gui.gui import GUI

timeStep = 0.01
GRAVITY = 9.81
MASS = 1
GROUND_HEIGHT = 50

class BiCopter():

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.x = 0
        self.y = 0
        self.vx = 0
        self.vy = 0



    def updatePos(self, fx, fy, tau):
        self.x = self.x + self.vx*timeStep + 0.5*fx*timeStep**2
        self.y = self.y + self.vy*timeStep + 0.5*MASS*(fy-GRAVITY)*timeStep**2

        if self.y < 0:
            self.y = 0



def main():
    g = GUI()
    bi = BiCopter(25, 5)

    while True:
        if g.quitFlag:
            g.tk.destroy()
            break
        if not g.startFlag:
            g.tk.update_idletasks()
            g.tk.update()
            time.sleep(0.01)
            continue


        x = g.bi_x
        y = g.bi_y - 1
        g.animateBi(x, y, 0)
        print("test")
        print("{},{}".format(g.bi_x,g.bi_y))
        g.tk.update_idletasks()
        g.tk.update()
        time.sleep(0.03)
        # break




if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('')
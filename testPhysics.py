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
from BiCopter import BiCopter

timeStep = 0.01
GRAVITY = 9.81
MASS = 1
GROUND_HEIGHT = 50

def main():
    g = GUI()

    bi = BiCopter(0.0,0.0,0.0)

    i = 0


    F1 = 1.0*bi.m*GRAVITY #+ 0.01math.sin(i/180.0)
    F2 = F1

    while True:
        if g.quitFlag:
            g.tk.destroy()
            break
        if not g.startFlag:
            g.tk.update_idletasks()
            g.tk.update()
            time.sleep(0.01)
            bi.setStartTime() # Continuously set start time until you actually start
            continue



        bi.updateForces(F1, F2)
        bi.physics()

        pos = bi.getPos()

        g.animateBi(pos[0], pos[1], pos[2])
        print("{},{},{}".format(pos[0], pos[1], pos[2]))
        g.tk.update_idletasks()
        g.tk.update()
        # time.sleep(0.01)



        i += 1

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('')
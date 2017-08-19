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

GRAVITY = 1009.81

def main():
    g = GUI()

    bi = BiCopter(0.0,0.0,0.0)

    i = 0


    F1 = 0.9*bi.m*GRAVITY #+ 0.01math.sin(i/180.0)
    F2 = F1


    veryStart = 0

    while True:
        if g.quitFlag:
            g.tk.destroy()
            break
        if not g.startFlag:
            g.tk.update_idletasks()
            g.tk.update()
            time.sleep(0.01)
            bi.setStartTime() # Continuously set start time until you actually start
            veryStart = time.time()
            continue

        # Wait 5 seconds
        if time.time() - veryStart > 2:
            # print("Thruster ERROR")
            F1 = 0.51*bi.m*GRAVITY
            F2 = F1 #.0001*bi.m*GRAVITY
            if time.time() - veryStart > 5:
                F1 = 0
                F2 = 0

        else:
            F1 = F1*0.999
            F2 = F2*0.999

        bi.updateForces(F1, F2)
        bi.physics()

        pos = bi.getPos()
        g.animateBi(pos[0], pos[1], pos[2], bi.F1, bi.F2, bi.m, GRAVITY)
        # print("{},{},{}".format(pos[0], pos[1], pos[2]))



        g.tk.update_idletasks()
        g.tk.update()
        time.sleep(0.001)


        # print("i: ",i)
        i += 1

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('')
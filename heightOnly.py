##################
## Pcontrol.py
##         P control for Z height
##         
##         Austin Chun
##         Aug 2017
###################


import math
import time
from gui.gui import GUI
from BiCopter import BiCopter

g = 9.81

des_height = 2 # meters

Kp = 0.1
Ki = 0.001

sum_e = 0

def Pcontrol(bi):
    global sum_e
    pos = bi.getPos()

    e = des_height-pos[1]
    sum_e += e


    F1 = 0.5*bi.m*g + Kp*e #+ Ki*sum_e
    F2 = F1

    print("e: %.3f, sum_e: %.3f,  Force: %.3f" % (e, sum_e, F1/(0.5*bi.m*g)))
    return F1, F2


def polePlace(bi):
    y = bi.getPos()[1]
    vy = bi.getVel()[1]

    K = [300, 54.98]

    return K[0]*y + K[1]*vy

def feedback(bi):
    Kr = 300
    r = des_height * Kr

    Ku = polePlace(bi)
    F = r - Ku + 0.5*bi.m*g

    return F, F

def main():
    global des_height

    gui = GUI()
    # gui.drawDest()
    bi = BiCopter(0.0,0.0,0.0)
    i = 0

    F1 = 0
    F2 = 0

    while True:
        if gui.quitFlag:
            gui.tk.destroy()
            break
        if not gui.startFlag:
            # gui.startFlag = True
            gui.tk.update_idletasks()
            gui.tk.update()
            time.sleep(0.01)
            bi.setStartTime() # Continuously set start time until you actually start
            veryStart = time.time()
            continue



        # F1, F2 = Pcontrol(bi)
        F1, F2 = feedback(bi)

        bi.updateForces(F1, F2) 
        bi.physics() # Updates position

        pos = bi.getPos()
        gui.animateBi(pos[0], pos[1], pos[2], bi.F1, bi.F2, bi.m, g)
        gui.drawDest()
        des_height = gui.des_height

        # Update GUI
        gui.tk.update_idletasks()
        gui.tk.update()
        time.sleep(0.001)


        # print("i: ",i)
        i += 1



if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('')
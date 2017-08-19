##################
## gui.py
##      Simple animation to display Bicopter simulation
##
##      Austin Chun
##      Aug 2017
##################


from tkinter import *
import time
import random
import math
import yaml
import os

# Configuration variables
GROUND_HEIGHT = -1 # pixels
WINDOW_WIDTH = -1
WINDOW_HEIGHT = -1
BI_WIDTH = -1
BI_HEIGHT = -1

# Get parent directory name
here = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
CONFIG_FILE_NAME = here+'\config.yaml'

def readConfigFile():
    global GROUND_HEIGHT
    global WINDOW_WIDTH 
    global WINDOW_HEIGHT
    global BI_WIDTH
    global BI_HEIGHT
    global CONFIG_FILE_NAME 
    with open(CONFIG_FILE_NAME, 'r') as file:
        cfg = yaml.load(file)

    GROUND_HEIGHT = cfg['main']['ground_height']
    WINDOW_HEIGHT = cfg['main']['window_height']
    WINDOW_WIDTH  = cfg['main']['window_width'] 
    BI_WIDTH = cfg['main']['bi_width']
    BI_HEIGHT = cfg['main']['bi_height']


class GUI():

    def __init__(self):

        global GROUND_HEIGHT
        global WINDOW_WIDTH 
        global WINDOW_HEIGHT
        global BI_HEIGHT
        global BI_WIDTH

        # Load configuration
        readConfigFile()

        self.width = WINDOW_WIDTH
        self.height = WINDOW_HEIGHT
        self.bi_w = BI_WIDTH
        self.bi_h = BI_HEIGHT

        self.startFlag = False
        self.quitFlag = False

        # Initialize window
        self.tk = Tk()
        self.w = Canvas(self.tk, width=self.width, height=self.height)
        self.tk.title("BiCopter Simulation")
        self.w.pack()

        # Buttons
        self.start = Button(self.tk, text="Start", command=self.startCall)
        self.start.pack()
        self.pause = Button(self.tk, text="Pause", command=self.pauseCall)
        self.pause.pack()
        self.quit = Button(self.tk, text="Quit", command=self.quitCall)
        self.quit.pack()

        # Draw ground
        ground = self.height-GROUND_HEIGHT
        self.w.create_rectangle(0,ground, self.width, self.height, fill='black')

        # Draw BiCopter
        midScreen = self.width/2.0
        x1,y1 = midScreen - self.bi_w/2, ground-self.bi_h
        x2,y2 = midScreen + self.bi_w/2, ground-self.bi_h
        x3,y3 = midScreen + self.bi_w/2, ground
        x4,y4 = midScreen - self.bi_w/2, ground
        self.bi = self.w.create_polygon(x1,y1,x2,y2,x3,y3,x4,y4, fill='blue')

        self.thrustL = self.w.create_line(x4,y4,x4,y4, fill='red')
        self.thrustR = self.w.create_line(x3,y3,x3,y3, fill='red')


        # self.bi = self.w.create_rectangle(midScreen - self.bi_w/2, ground-self.bi_h,
        #                                 midScreen + self.bi_w/2, ground, fill='blue')


        # Set biCopter coordinates
        # Define 0,0 to be center on the ground
        self.origin = [midScreen, ground]
        self.bi_x = 0
        self.bi_y = 0 # Define origin of BiCopter to be bottom middle
        self.bi_theta = 0

        self.w.pack()

        self.tk.update()

    def startCall(self):
        if not self.startFlag:
            self.startFlag = True
    def pauseCall(self):
        if self.startFlag:
            self.startFlag = False
    def quitCall(self):
        print("Quit")
        self.quitFlag = True


    """
    x: position in defined reference frame
    y: position in defined reference fram
    theta: in radians
    """
    def animateBi(self, x, y, theta, F1, F2, m, g):
        # Convert to SCREEN coordinate system
        true_x = x + self.width/2
        true_y = -y + self.height - GROUND_HEIGHT 

        # theta = math.radians(theta)
        sin = math.sin(theta)
        cos = math.cos(theta)

        x3,y3 = true_x + self.bi_w/2*cos, true_y - self.bi_w/2*sin # lower right
        x4,y4 = true_x - self.bi_w/2*cos, true_y + self.bi_w/2*sin # lower left       

        x1,y1 = x4 - self.bi_h*sin, y4 - self.bi_h*cos #true_x - self.bi_w/2, true_y-self.bi_h # Upper left
        x2,y2 = x3 - self.bi_h*sin, y3 - self.bi_h*cos #true_x + self.bi_w/2, true_y-self.bi_h # upper right
        

        # print("Coords: ", self.w.coords(self.bi))

        # Update the coords of the bicopter in the GUI
        self.w.coords(self.bi, x1,y1,x2,y2,x3,y3,x4,y4)

        # Update thrusters
        tL_val = F1/(m*g) * 50
        tR_val = F1/(m*g) * 50

        tL_endx, tL_endy = x4+tL_val*sin , y4+tL_val*cos
        tR_endx, tR_endy = x3+tR_val*sin , y3+tR_val*cos

        self.w.coords(self.thrustL, x4,y4, tL_endx, tL_endy)
        self.w.coords(self.thrustR, x3,y3, tR_endx, tR_endy)



        # Save new coordss
        self.bi_x = x
        self.bi_y = y
        self.bi_theta = theta


def main():
    g = GUI()

    i = 0
    while(True):
        if g.quitFlag:
            g.tk.destroy()
            break
        if not g.startFlag:
            g.tk.update_idletasks()
            g.tk.update()
            time.sleep(0.01)
            continue

        g.animateBi(0,i,2*i/180) # [pixles(cm), radians]
        i += 1
        # coords = g.w.coords(g.bi)
        # print(coords)
        # coords[1] += -1
        # g.w.coords(g.bi, coords)



        g.tk.update_idletasks()
        g.tk.update()
        time.sleep(0.03)

    print("Closed GUI")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('')

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
        self.bi = self.w.create_rectangle(midScreen - self.bi_w/2, ground-self.bi_h,
                                        midScreen + self.bi_w/2, ground, fill='blue')

        # Set biCopter coordinates
        # Define 0,0 to be center on the ground
        self.bi_x = 0
        self.bi_y = 0 # ground - self.bi_h
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


    def animateBi(self, x, y, theta):
        print("{},{}".format(x-self.bi_x, y-self.bi_y))
        self.w.move(self.bi, x-self.bi_x, y-self.bi_y)
        self.bi_x = x
        self.bi_y = y

# g = GUI()

# while(True):
#     if g.quitFlag:
#         g.tk.destroy()
#         break
#     if not g.startFlag:
#         g.tk.update_idletasks()
#         g.tk.update()
#         time.sleep(0.01)
#         continue

#     g.animateBi(0,0,0)
#     g.tk.update_idletasks()
#     g.tk.update()
#     time.sleep(0.03)

# print("Closed GUI")


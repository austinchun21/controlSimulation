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
        x1,y1 = midScreen - self.bi_w/2, ground-self.bi_h
        x2,y2 = midScreen + self.bi_w/2, ground-self.bi_h
        x3,y3 = midScreen + self.bi_w/2, ground
        x4,y4 = midScreen - self.bi_w/2, ground
        self.bi = self.w.create_polygon(x1,y1,x2,y2,x3,y3,x4,y4, fill='blue')


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


    def animateBi(self, x, y, theta):
        # print("{},{}".format(x-self.bi_x, y-self.bi_y))
        
        # Calculate difference
        # dx = x-self.bi_x
        # dy = y-self.bi_y

        true_x = x + self.width/2
        true_y = -y + self.height - GROUND_HEIGHT 

        x1,y1 = true_x - self.bi_w/2, true_y-self.bi_h
        x2,y2 = true_x + self.bi_w/2, true_y-self.bi_h
        x3,y3 = true_x + self.bi_w/2, true_y
        x4,y4 = true_x - self.bi_w/2, true_y        

        print("Coords: ", self.w.coords(self.bi))

        self.w.coords(self.bi, x1,y1,x2,y2,x3,y3,x4,y4)

        # self.w.coords(self.bi, [true_x-self.bi_w/2, true_y-self.bi_h, 
        #                         true_x+self.bi_w/2, true_y])
        # self.w.move(self.bi, dx, -dy) # negative dy because define up to be positive
        self.bi_x = x
        self.bi_y = y


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

        g.animateBi(i,i,0)
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

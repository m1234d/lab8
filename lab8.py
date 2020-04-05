import math
import copy
import numpy as np
from tkinter import *

def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
Canvas.create_circle = _create_circle

def makeGrid():
   
    grid = np.zeros([28, 16])
    
    grid[6:10, 8:12] = 1
    grid[16:20, 10:14] = 2
    grid[12:16, 4:6] = 3
    grid[12:14, 2:4] = 3
    
    newGrid = np.zeros([28, 16])
    bufferSize = 1
    for theta1 in range(0, 16):
        for theta2 in range(0, 28):
            newGrid[theta2, theta1] = grid[theta2, theta1]
            for tt1 in range(-bufferSize, bufferSize+1, 1):
                for tt2 in range(-bufferSize, bufferSize+1, 1):
                    newT2 = min(theta2+tt2, 27)
                    newT1 = min(theta1+tt1, 15)
                    newT2 = max(newT2, 0)
                    newT1 = max(newT1, 0)
                    if grid[newT2, newT1] != 0:
                        if newGrid[theta2, theta1] == 0:
                            newGrid[theta2, theta1] = 4


    configSpace = getConfigSpace(newGrid)
    return newGrid, configSpace

def drawGrid(grid, configSpace, t1, t2, r1, r2, p):
    runDrawing(grid, configSpace, t1=t1, t2=t2, r1=r1, r2=r2, p=p)
    
def getConfigSpace(grid):
    configSpace = np.zeros([360, 180])
    for theta1 in range(0, 180):
        for theta2 in range(0, 360):
            x = 14 + 2*3.75*math.cos(math.radians(theta1)) + 2*2.5*math.cos(math.radians(theta2+theta1))
            y = 0 + 2*3.75*math.sin(math.radians(theta1)) + 2*2.5*math.sin(math.radians(theta2+theta1))
            gridx = math.floor(x)
            gridy = math.floor(y)
            if (x>=0 and y>=0):
                configSpace[theta2, theta1] = grid[gridx, gridy]
    
    return configSpace 
    

def draw(canvas, width, height, grid, configSpace, t1, t2, r1, r2, p):
    # drawing grid
    width = 25
    yoffset = 50
    offset2 = 25
    for i in range(0, grid.shape[0]):
        for j in range(0, grid.shape[1]):
            x = width*i+20
            y = width*(grid.shape[1]-j) + offset2
            if grid[i][j] == 1:
                canvas.create_rectangle(x,y,x+width,y+width, fill="red")
            elif grid[i][j] == 2:
                canvas.create_rectangle(x,y,x+width,y+width, fill="blue")
            elif grid[i][j] == 3:
                canvas.create_rectangle(x,y,x+width,y+width, fill="orange")
            elif grid[i][j] ==4:
                canvas.create_rectangle(x,y,x+width,y+width, fill="green")
            else:
                canvas.create_rectangle(x,y,x+width,y+width, fill="white")
            
    for y in range(0, grid.shape[1]+1, 2):
        canvas.create_text(10, width*(grid.shape[1]-y)+yoffset, text=int(y/2)) 
    for x in range(0, grid.shape[0]+1, 2):
        canvas.create_text(20+width*x, 10+width*grid.shape[1]+yoffset, text=int(int((x-(grid.shape[0]/2)))/2)) 
        
    # drawing configuration space
    
    width = 2
    xoffset = 800
    for i in range(0, configSpace.shape[0]): #360
        for j in range(0, configSpace.shape[1]): #180
            y = width*((configSpace.shape[0]-i+180)%360)+yoffset
            x = width*j+xoffset
            if configSpace[i][j] == 1:
                canvas.create_rectangle(x,y,x+width,y+width, fill="red", outline="red")
            elif configSpace[i][j] == 2:
                canvas.create_rectangle(x,y,x+width,y+width, fill="blue", outline="blue")
            elif configSpace[i][j] == 3:
                canvas.create_rectangle(x,y,x+width,y+width, fill="orange", outline="orange")
            elif configSpace[i][j] ==4:
                canvas.create_rectangle(x,y,x+width,y+width, fill="green", outline="green")
            else:
                canvas.create_rectangle(x,y,x+width,y+width, fill="white", outline="white")
            if (i==270 and j == 0):
                canvas.create_text(x-15, y, text=i-360)
            if (i==180 and j == 0):
                canvas.create_text(x-15, y, text=i)
            if (i==181 and j == 0):
                canvas.create_text(x-15, y, text=-(i-1))
            if (i==90 and j == 0):
                canvas.create_text(x-15, y, text=i)
            if (i==0 and j == 0):
                canvas.create_text(x-15, y, text=i) 
                canvas.create_text(x-40, y, text="θ2", font=('arial', 18, 'bold'))
            if (i==181 and j == 0):
                canvas.create_text(x, y+15, text=j) 
            if (i==181 and j == 90):
                canvas.create_text(x, y+15, text=j) 
                canvas.create_text(x, y+40, text="θ1", font=('arial', 18, 'bold'))
            if (i==181 and j == 179):
                canvas.create_text(x, y+15, text=j+1)  
    # drawing box
    print(t1, t2, r1, r2)
    lastP1, lastP2 = None, None
    
    canvas.create_circle(r1*width+xoffset, yoffset+180*width-r2*width, 20, fill="red")
    canvas.create_text(r1*width+xoffset, yoffset+180*width-r2*width, text="        " + str(0), font=('arial', 18, 'bold'))

    for i in range(len(t1)-1):
        canvas.create_circle(t1[i]*width+xoffset, yoffset+180*width-t2[i]*width, 20, fill="orange")
        canvas.create_text(t1[i]*width+xoffset, yoffset+180*width-t2[i]*width, text="        " + str(i+1), font=('arial', 18, 'bold'))
    canvas.create_circle(t1[-1]*width+xoffset, yoffset+180*width-t2[-1]*width, 20, fill="green")
    canvas.create_text(t1[-1]*width+xoffset, yoffset+180*width-t2[-1]*width, text="        " + str(3), font=('arial', 18, 'bold'))

    for pp in p:
        p1, p2 = pp[0], pp[1]
        canvas.create_circle(p1*width+xoffset, yoffset+180*width-p2*width, 5, fill="purple", outline="")
        if lastP1 != None:
            canvas.create_line(lastP1*width+xoffset, yoffset+180*width-lastP2*width, p1*width+xoffset, yoffset+180*width-p2*width, fill="purple")
        lastP1, lastP2 = p1, p2
    
    canvas.create_rectangle(xoffset, yoffset, xoffset+width*180, width*360+yoffset, outline="black")
    

            
    
def runDrawing(grid, configSpace, width=(14*50+20) + 60 + 360+100, height=720+50+50, t1=None, t2=None, r1=None, r2=None, p=None):
    root = Tk()
    canvas = Canvas(root, width=width, height=height)
    canvas.pack()
    draw(canvas, width, height, grid, configSpace, t1, t2, r1, r2, p)
    root.mainloop()
    print("bye!")

if __name__ == "__main__":
    grid, configSpace = makeGrid()
    drawGrid(grid, configSpace)


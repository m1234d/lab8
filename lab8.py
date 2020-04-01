import math
import copy
import numpy as np
from tkinter import *


def makeGrid():
   
    grid = np.zeros([14, 8])
    
    grid[3:5, 4:6] = 1
    grid[8:10, 5:7] = 2
    grid[6:8, 2] = 3
    grid[6, 1] = 3

    configSpace =getConfigSpace(grid)
    runDrawing(grid, configSpace)

    
def getConfigSpace(grid):
    configSpace = np.zeros([360, 180])
    for theta1 in range(0, 180):
        for theta2 in range(0, 360):
            x = 7 + 3.75*math.cos(math.radians(theta1)) + 2.5*math.cos(math.radians(theta2+theta1))
            y = 0 + 3.75*math.sin(math.radians(theta1)) + 2.5*math.sin(math.radians(theta2+theta1))
            gridx = math.floor(x)
            gridy = math.floor(y)
            if (x>=0 and y>=0):
                configSpace[theta2, theta1] = grid[gridx, gridy]
    return configSpace
    
    

def draw(canvas, width, height, grid, configSpace):
    # drawing grid
    width = 50
    yoffset = 50
    for i in range(0, grid.shape[0]):
        for j in range(0, grid.shape[1]):
            x = width*i+20
            y = width*(grid.shape[1]-j)
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
            
    for y in range(0, grid.shape[1]+1):
        canvas.create_text(10, width*(grid.shape[1]-y)+yoffset, text=y) 
    for x in range(0, grid.shape[0]+1):
        canvas.create_text(20+width*x, 10+width*grid.shape[1]+yoffset, text=int(x-(grid.shape[0]/2))) 
        
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
    canvas.create_rectangle(xoffset, yoffset, xoffset+width*180, width*360+yoffset, outline="black")
    

            
    
def runDrawing(grid, configSpace, width=(14*50+20) + 60 + 360+100, height=720+50+50):
    root = Tk()
    canvas = Canvas(root, width=width, height=height)
    canvas.pack()
    draw(canvas, width, height, grid, configSpace)
    root.mainloop()
    print("bye!")
    
makeGrid()


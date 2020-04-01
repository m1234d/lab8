import time
from arm import AcrobotEnv
import sys
import math
import copy
import numpy as np

def inverseKinematics(l1, l2, x, y):
    t2 = math.acos((x**2 + y**2 - l1**2 - l2**2) / (2*l1*l2))
    t1 = math.atan2(y, x) - math.asin(l2*math.sin(t2)/ math.sqrt(x**2 + y**2))
    return t1, t2

if __name__ == '__main__':

    arm = AcrobotEnv() # set up an instance of the arm class
    
    timeStep = 0.02 # sec
    timeForEachMove = 5 # sec
    stepsForEachMove = round(timeForEachMove/timeStep)

    # Make configuration space
    # Insert you code or calls to functions here

    # Get three waypoints from the user
    Ax = int(input("Type Ax: "))
    Ay = int(input("Type Ay: "))
    Bx = int(input("Type Bx: "))
    By = int(input("Type By: "))
    Cx = int(input("Type Cx: "))
    Cy = int(input("Type Cy: "))

    arm.Ax = Ax*0.0254; # Simulaiton is in SI units
    arm.Ay = Ay*0.0254; # Simulaiton is in SI units
    arm.Bx = Bx*0.0254; # Simulaiton is in SI units
    arm.By = By*0.0254; # Simulaiton is in SI units
    arm.Cx = Cx*0.0254; # Simulaiton is in SI units
    arm.Cy = Cy*0.0254; # Simulaiton is in SI units
    
    l1 = 3.75*0.0254
    l2 = 2.5*0.0254
    # Plan a path
    # Insert your code or calls to functions here
    numberOfWaypoints = 10 # Change this based on your path
    
    state = arm.reset() # start simulation
    Kp1 = .15
    Kd1 = 1.5
    Kp2 = .32
    Kd2 = 1.0
    m1 = .02785
    m2 = 0.005
    m3 = .00005
    g = 9.8
    fix = 0
    prevCurt1 = 0
    for waypoint in range(3):
        if waypoint == 0:
            x, y = arm.Ax, arm.Ay
        elif waypoint == 1:
            x, y = arm.Bx, arm.By
        else:
            x, y = arm.Cx, arm.Cy
        # Get current waypoint
        t1, t2 = inverseKinematics(l1, l2, x, y)
        print(x, y, math.degrees(t1), math.degrees(t2))
        for timeStep in range(stepsForEachMove):
            
            print(timeStep*0.02)
            tic = time.perf_counter()

            # Control arm to reach this waypoint
            # [cos1 sin1 cos2 sin2 t1dot t2dot]
            curt1 = math.atan2(state[1], state[0]) - (math.pi/2)
            if abs(curt1 - t1) > 2*math.pi:
                fix = 2*math.pi
            else:
                fix = 0
            curt1 = curt1 + fix
            curt2 = math.atan2(state[3], state[2])
            f1 = -((l1*math.cos(curt1) + (l2/2) * math.cos(curt1 + curt2)) * m3*g + (l1/2)*math.cos(curt1)*m1*g)
            f2 = -(l2/2)*math.cos(curt1 + curt2)*m2*g
            print(curt1 - t1, curt2 - t2, f1, f2)
            actionHere1 = Kp1*(curt1 - t1) + Kd1*state[4] + f1 # N torque # Change this based on your controller
            actionHere2 = Kp2*(curt2 - t2) + Kd2*state[5] + f2
            arm.render() # Update rendering
            state, reward, terminal , __ = arm.step(actionHere1, actionHere2)
        
    print("Done")
    input("Press Enter to close...")
    arm.close()

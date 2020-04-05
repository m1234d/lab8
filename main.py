import time
from arm import AcrobotEnv
import sys
import math
import copy
import numpy as np
import lab8
import path

def inverseKinematics(l1, l2, x, y):
    try:
        t2 = math.acos((x**2 + y**2 - l1**2 - l2**2) / (2*l1*l2))
        t22 = -t2
        t1 = math.atan2(y, x) - math.asin(l2*math.sin(t2)/ math.sqrt(x**2 + y**2))
        t12 = math.atan2(y, x) - math.asin(l2*math.sin(t22)/math.sqrt(x**2 + y**2))
        if t1 < 0:
            return t12, t22
        return t1, t2
    except:
        print("Illegal point")
        sys.exit()

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
    Kp1 = 4.5
    Kd1 = 5.5
    Kp2 = 8.8
    Kd2 = 25.0
    Kf = 0
    m1 = .02785
    m2 = 0.005
    m3 = .00005
    g = 9.8
    fix = 0
    prevCurt1 = 0
    x0, y0 = 6.25*0.0254, 0
    eps = 0.05
    fullPath = []
    points1 = []
    points2 = []
    for waypoint in range(3):
        if waypoint == 0:
            x, y = arm.Ax, arm.Ay
        elif waypoint == 1:
            x, y = arm.Bx, arm.By
        else:
            x, y = arm.Cx, arm.Cy
        # Get current waypointi
        r1, r2 = inverseKinematics(l1, l2, x0, y0)
        t1, t2 = inverseKinematics(l1, l2, x, y)
        t1d, t2d, r1d, r2d = math.degrees(t1), math.degrees(t2), math.degrees(r1), math.degrees(r2)
        grid, configSpace = lab8.makeGrid()
        if waypoint == 0:
            r1og = r1d
            r2og = r2d
        try:
            p = path.main(configSpace, (r1d, r2d), (t1d, t2d))
        except:
            sys.exit()
        fullPath = fullPath + p
        x0, y0 = x, y
        points1.append(t1d)
        points2.append(t2d)

    lab8.drawGrid(grid, configSpace, points1, points2, r1og, r2og, fullPath)

    x0, y0 = 6.25*0.0254, 0
    for waypoint in range(3):
        waitCount = 0
        if waypoint == 0:
            x, y = arm.Ax, arm.Ay
        elif waypoint == 1:
            x, y = arm.Bx, arm.By
        else:
            x, y = arm.Cx, arm.Cy
        # Get current waypointi
        r1, r2 = inverseKinematics(l1, l2, x0, y0)
        t1, t2 = inverseKinematics(l1, l2, x, y)
        t1d, t2d, r1d, r2d = math.degrees(t1), math.degrees(t2), math.degrees(r1), math.degrees(r2)
        grid, configSpace = lab8.makeGrid()
        p = path.main(configSpace, (r1d, r2d), (t1d, t2d))
        p = p[1:]
        pointIndex = 0
        prevAction1 = 0
        if len(p) > 4:
            eps = 0.1
        else:
            eps = 0.05
        for timeStep in range(stepsForEachMove):
            tt = p[pointIndex]
            t1, t2 = math.radians(tt[0]), math.radians(tt[1])
            print(timeStep*0.02)
            tic = time.perf_counter()

            # Control arm to reach this waypoint
            # [cos1 sin1 cos2 sin2 t1dot t2dot]
            curt1 = math.atan2(state[1], state[0])
            if abs(curt1 - t1) > 2*math.pi:
                fix = 2*math.pi
            else:
                fix = 0
            curt1 = curt1 + fix
            curt2 = math.atan2(state[3], state[2])
            if abs(curt2 - t2) > 2*math.pi:
                fix = 2*math.pi
            else:
                fix = 0
            curt2 = curt2 + fix
            f1 = -((l1*math.cos(curt1) + (l2/2) * math.cos(curt1 + curt2)) * m3*g + (l1/2)*math.cos(curt1)*m1*g)
            f2 = -(l2/2)*math.cos(curt1 + curt2)*m2*g
            err = curt1 - t1
            err2 = curt2 - t2
            thr = .15
            thr2 = .05
            if err > thr:
                err = thr
            elif err < -thr:
                err = -thr

            if err2 > thr2:
                err2 = thr2
            elif err2 < -thr2:
                err2 = -thr2

            actionHere1 = Kp1*err + Kd1*state[4] + f1 # N torque # Change this based on your controller
            actionHere2 = Kp2*(curt2 - t2) + Kd2*state[5] + f2 + Kf*((state[4]-prevAction1))
            prevAction1 = state[4]
            arm.render() # Update rendering
            state, reward, terminal , __ = arm.step(actionHere1, actionHere2)
            if abs(curt1 - t1) < eps/2:
                if abs(curt2 - t2) < eps/2:
                    pointIndex = pointIndex + 1
                    if pointIndex >= len(p):
                        pointIndex = pointIndex - 1
                        if abs(curt1-t1) < eps/3 and abs(curt2-t2) < eps/3:
                            waitCount += 1
                            if waitCount >= 20:
                                break

        x0, y0 = x, y
    print("Done")
    input("Press Enter to close...")
    arm.close()

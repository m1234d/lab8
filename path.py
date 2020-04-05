import heapq
import math
import numpy as np

class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]

possibleMoves = ["Up", "Down", "Left","Right"]
jump = 20
def makeMove(state,action,grid):
    (t1, t2) = state
    lenX = len(grid[0])
    lenY = len(grid)

    if action == "Left":
        t1 = t1 - 1

    if action == "Right":
        t1 = t1 + 1
    
    if action == "Up":
        t2 = (((t2 + 1) + 180) % 360) - 180

    if action == "Down":
        t2 = (((t2 - 1) + 180) % 360) - 180
   
    if 0 <= t1 and t1 < lenX:
        if grid[t2][t1] == 0:
            return (t1, t2)
    
    return None


def expandNode(grid,state):
    states = []
    for action in possibleMoves:
        nextState = makeMove(state,action,grid)
        if nextState != None:
            states += [(nextState,action)]
    return states

def heuristic(cur,final):
    (x,y) = cur
    (x1,y1) = final
    return abs(x-x1) + abs(y-y1)

def a_star_search(grid, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()
        if current == goal:
            return make_path(came_from,goal,start)
        for (next,action) in expandNode(grid,current):
            c = came_from[current]
            if c == None:
                new_cost = cost_so_far[current] + 1
            else:
                _, prev_action = c
                if prev_action == action:
                    new_cost = cost_so_far[current] + 1
                else:
                    new_cost = cost_so_far[current] + 10
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                frontier.put(next, priority)
                came_from[next] = (current,action)
    print("No path found.")
    return None

def make_path(came_from,goal,start):
    path = []
    curr = goal
    while came_from[curr] != None:
        (prev,action) = came_from[curr]
        path.insert(0,action)
        curr = prev
    return path

def get_points(start, path):
    points = [start]
    count = 0
    lastP = path[0]
    for i in range(len(path)):
        p = path[i]
        last = points[-1]
        if i != len(path)-1 and lastP == p:
            count += 1
        else:
            if i == len(path)-1 and lastP == p:
                count += 1
            if lastP == "Up":
                points.append((last[0], (((last[1]+count) + 180)  % 360) - 180))
            elif lastP == "Down":
                points.append((last[0], (((last[1]-count) + 180) % 360) - 180))
            elif lastP == "Left":
                points.append((last[0]-count, last[1]))
            elif lastP == "Right":
                points.append((last[0]+count, last[1]))
            lastP = p
            count = 1
    return points


def main(grid, start, end):
    start = (int(start[0]), ((int(start[1]) + 180) % 360) - 180)
    end = (int(end[0]), ((int(end[1]) + 180) % 360) - 180)
    # start = (y, x, 'South')
    path = a_star_search(grid, start, end)
    points = get_points(start, path)
    #for i in range(len(points)):
    #    points[i] = (points[i][1], points[i][0], points[i][2]*math.pi/180)
    return points

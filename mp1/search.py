# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Kelvin Ma (kelvinm2@illinois.edu) on 01/24/2021

"""
This is the main entry point for MP1. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
# Search should return the path.
# The path should be a list of tuples in the form (row, col) that correspond
# to the positions of the path taken by your search algorithm.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,astar,astar_multi,fast)


# Feel free to use the code below as you wish
# Initialize it with a list/tuple of objectives
# Call compute_mst_weight to get the weight of the MST with those objectives
# TODO: hint, you probably want to cache the MST value for sets of objectives you've already computed...
from collections import deque
import heapq, operator, copy

class MST:
    def __init__(self, objectives):
        self.elements = {key: None for key in objectives}

        # TODO: implement some distance between two objectives 
        # ... either compute the shortest path between them, or just use the manhattan distance between the objectives
        self.distances   = {
                (i, j): abs(i[0] - j[0]) + abs(i[1] - j[1])
                for i, j in self.cross(objectives)
            }
        
    # Prim's algorithm adds edges to the MST in sorted order as long as they don't create a cycle
    def compute_mst_weight(self):
        weight      = 0
        for distance, i, j in sorted((self.distances[(i, j)], i, j) for (i, j) in self.distances):
            if self.unify(i, j):
                weight += distance
        return weight

    # helper checks the root of a node, in the process flatten the path to the root
    def resolve(self, key):
        path = []
        root = key 
        while self.elements[root] is not None:
            path.append(root)
            root = self.elements[root]
        for key in path:
            self.elements[key] = root
        return root
    
    # helper checks if the two elements have the same root they are part of the same tree
    # otherwise set the root of one to the other, connecting the trees
    def unify(self, a, b):
        ra = self.resolve(a) 
        rb = self.resolve(b)
        if ra == rb:
            return False 
        else:
            self.elements[rb] = ra
            return True

    # helper that gets all pairs i,j for a list of keys
    def cross(self, keys):
        return (x for y in (((i, j) for j in keys if i < j) for i in keys) for x in y)

def bfs(maze):
    """
    Runs BFS for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    flag = False
    visited = []
    parent = {}
    to_return = []
    q = deque()
    cur = maze.start
    q.append(cur)
    while(q):
        cur = q.popleft()
        visited.append(cur)
        for neigbours in maze.neighbors(cur[0], cur[1]) :
            if (neigbours in visited or neigbours in q) :
                continue
            else:
                q.append(neigbours)
                parent[neigbours] = cur
            if(maze.__getitem__(neigbours) == maze.legend.waypoint): 
                to_return.insert(0, neigbours)
                cur_parent=parent[neigbours]
                while(cur_parent in parent):
                    to_return.insert(0, cur_parent)
                    cur_parent = parent[cur_parent]
                to_return.insert(0, maze.start)
                flag = True
                break
        if (flag):
            break
    return to_return

# def insert_element():

def manhattan_d(x,y):
    return abs(x[0]-y[0]) + abs(x[1]-y[1])

def backtrace(parent, start, end): # helper function to travese back a correct path
    path = [end]
    
    while path[-1] != start:
        path.append(parent[path[-1]])
    path.reverse()
    return path


"""
return true if cur_state is a longer path and visited
"""
def longer_visited(cur_state, visited_state):
    longer = True
    visited = False
    for each_state in visited_state:
        if (each_state[1] == cur_state[1]):
            visited = True #visited
            if cur_state[0] < each_state[0]:
                longer = False #visited and shorter path found
                break
    return visited&longer #not visited

def astar_single(maze):
    """
    Runs A star for part 2 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    heap=[]
    g = {} #distance to startpoint
    visited = []
    visited_state=[]
    parent = {}
    to_return = []
    start = maze.start
    end = maze.waypoints[0]
    g[start] = 0
    f_start = g[start] + manhattan_d(start,end)
    start_state = (f_start, start)# state=(f,(x,y))
    heapq.heappush(heap, start_state)
    while (1): 
        cur_state = heapq.heappop(heap)
        cur_point = cur_state[1]
        if (cur_point == end):#reaches end
            break
        for each_neibour in maze.neighbors(cur_point[0], cur_point[1]):
            g_neighbour = g[cur_point] + 1
            f_cur = g_neighbour + manhattan_d(each_neibour, end)
            neibour_state = (f_cur, (each_neibour))
            if (longer_visited(neibour_state, visited_state)):
                continue
            g[each_neibour] = g_neighbour
            heapq.heappush(heap, neibour_state)
            visited_state.append(neibour_state)
            parent[neibour_state] = cur_state

    to_return.insert(0, end)
    cur_parent_state=parent[cur_state]
    while(cur_parent_state in parent):
        to_return.insert(0, cur_parent_state[1])
        cur_parent_state = parent[cur_parent_state]
    to_return.insert(0, maze.start) 
    return to_return

"""
helper function to find the next nearest waypoint
"""
def find_nearest(cur, waypoints):
    min = waypoints[0]
    for each_point in waypoints:
        if (((abs(cur[0] - each_point[0]) + abs(cur[1] - each_point[1])) < (abs(cur[0] - min[0]) + abs(cur[1] - min[1])))):
            min = each_point
    return min

def astar_corner(maze): return []



#helper functions for a star multi
def heuristic(start, goals):
    nearest = find_nearest(start, goals)
    tree=MST(goals)
    return manhattan_d(start, nearest) + tree.compute_mst_weight()

def longer_path(cur_state, visited_states):
#state = (f, ((x,y), remaining goals))
    for each_state in visited_states:
        if (each_state[1] == cur_state[1]):
            if cur_state[0] < each_state[0]:
                return False
    return True

def state_visited(cur_state, visited_states):
#state = (f, ((x,y), remaining goals))
    for each_state in visited_states:
        if (each_state[1] == cur_state[1]):
            return True
    return False

"""
delete cur_point from goals
return the resule
"""
def delete_goal(goals, cur_point):
    to_return = []
    for each_goal in goals:
        if (each_goal == cur_point):
            continue
        to_return.append(each_goal)
    return tuple(to_return)

def traceback(parent, cur_state):
    to_return = []
    to_return.insert(0, cur_state[1][0])
    cur_parent_state=parent[cur_state]
    while(cur_parent_state in parent):
        to_return.insert(0, cur_parent_state[1][0])
        cur_parent_state = parent[cur_parent_state]
    return to_return

def astar_multiple(maze):
    """
    Runs A star for part 4 of the assignment in the case where there are
    multiple objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # H(x,y,remaining_goals) = distance(x,y, closest_goal) + MST(remaining_goals)
    heap=[]
    visited = []
    visited_state=[]
    parent={}
    g = {} #distance to startpoint
    to_return = []
    goals = maze.waypoints
    start = maze.start
    start_h = heuristic(start, goals)
    g[start] = 0
    start_f = start_h
    start_state = (start_f, (start, goals))
    heapq.heappush(heap, start_state)
    while(1):
        #state = (f, ((x,y), remaining goals))
        cur_state = heapq.heappop(heap)
        cur_point = cur_state[1][0]
        print(cur_point)
        visited.append(cur_point)
        if (cur_point in goals):#reaches an waypoint
            goals = delete_goal(goals, cur_point)
            if (len(goals) == 0):
                break
        for each_neibour in maze.neighbors(cur_point[0], cur_point[1]):
            g_neighbour = g[cur_point] + 1
            f_cur = g_neighbour + heuristic(each_neibour, goals)
            neibour_state = (f_cur, (each_neibour, goals))
            if (state_visited(neibour_state, visited_state) and longer_path(neibour_state, visited_state)):
                continue
            g[each_neibour] = g_neighbour
            heapq.heappush(heap, neibour_state)
            visited_state.append(neibour_state)
            parent[neibour_state] = cur_state
    
    to_return = traceback(parent, cur_state)
    to_return.insert(0, maze.start)
    return to_return

def fast(maze):
    """
    Runs suboptimal search algorithm for part 5.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # H(x,y,remaining_goals) = distance(x,y, closest_goal) + MST(remaining_goals)
    remaining_waypoints = list(maze.waypoints)
    cur_start = maze.start
    cur_nearest = find_nearest(cur_start, remaining_waypoints)
    tree = MST(remaining_waypoints)
    cur_weight = tree.compute_mst_weight()
    f = {} #total cost {coor : total cost}
    g = {} #distance to startpoint
    g[cur_start] = 0
    f[cur_start] = g[cur_start] + abs(cur_start[0] - cur_nearest[0]) + abs(cur_start[1] - cur_nearest[1]) + cur_weight
    to_return = []
    while(1):
        visited = []
        cur_parent_map = {}
        cur_link = []
        while (1): 
            cur = min(f.items(), key=operator.itemgetter(1))[0]
            f.pop(cur)
            visited.append(cur)
            if (cur in remaining_waypoints):
                break
            for neigbours in maze.neighbors(cur[0], cur[1]):
                if (neigbours in visited):
                    continue
                else:
                    g[neigbours] = g[cur] + 1
                    f[neigbours] = g[neigbours] + cur_weight + abs(neigbours[0] - cur_nearest[0]) + abs(neigbours[1] - cur_nearest[1])
                    cur_parent_map[neigbours] = cur
        cur_link.insert(0, cur)
        cur_parent=cur_parent_map[cur]
        while(cur_parent in cur_parent_map):
            cur_link.insert(0, cur_parent)
            cur_parent = cur_parent_map[cur_parent]
        to_return += cur_link
        remaining_waypoints.remove(cur)
        if (len(remaining_waypoints) == 0):
            break        
        cur_start = cur
        cur_nearest = find_nearest(cur_start, remaining_waypoints)
        tree = MST(remaining_waypoints)
        cur_weight = tree.compute_mst_weight()
        f = {} #total cost {coor : total cost}
        f[cur_start] = g[cur_start] + abs(cur_start[0] - cur_nearest[0]) + abs(cur_start[1] - cur_nearest[1]) + cur_weight
    to_return.insert(0, maze.start)
    return to_return
    
            

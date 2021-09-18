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

import queue

import heapq


class MST:
    def __init__(self, objectives):
        self.elements = {key: None for key in objectives}
       

        # TODO: implement some distance between two objectives 
        # ... either compute the shortest path between them, or just use the manhattan distance between the objectives
        # for i, j in self.cross(objectives):
        #     print (i,j)
        # try:
        #     self.distances   = {
        #         (i, j): manhattanD(objectives[i], objectives[j]) # changed DISTANCE to manhanttanD
        #         for i, j in self.cross(objectives)
        #     }
        # except TypeError:
        #     print('1')

        self.distances   = {
                (i, j): manhattanD(i, j) # changed DISTANCE to manhanttanD
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

def backtrace(parent, start, end): # helper function to travese back a correct path
    path = [end]
    
    while path[-1] != start:
        path.append(parent[path[-1]])
    path.reverse()
    return path

def manhattanD(a,b): #helper function to get manhattan distance
    distance = abs(a[0] - b[0]) + abs(a[1] - b[1])
    return distance

def findshortest(a, objectives): ## bugged
    
   
    c = manhattanD(a, objectives[0])
    
    t = objectives[0]
    for ob in objectives:
        
        b = manhattanD(ob, a)
        
        if c > b:
            c = b
            t = ob
    return t,c   # calculate the closest waypoint and it distance to point(a)

def findshortest_1(a, objectives): 
    
   
    c = manhattanD(a, objectives[0])
    
    t = objectives[0]
    for ob in objectives:
        
        b = manhattanD(ob, a)
        
        if c > b:
            c = b
            t = ob
    return t,c   # calculate the closest waypoint and it distance to point(a)

def bfs(maze):
    """
    Runs BFS for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    toReturn = []
    st = maze.start
    q = []
    visited = []
    q.append(st)
    parent = {}
    if st == maze.waypoints[0]:
        toReturn.append(st)
        return toReturn
    while q:
        tmp = q.pop(0)
        if tmp == maze.waypoints[0]:
            return backtrace(parent, st, maze.waypoints[0])
        for i in maze.neighbors(tmp[0], tmp[1]):
            if i not in visited:
                parent[i] = tmp
                q.append(i)
                visited.append(i)
    return []

def astar_single(maze):
    """
    Runs A star for part 2 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    st = maze.start
    q = []
    visited = []
    visited.append(st)
    heapq.heappush(q, (manhattanD(st, maze.waypoints[0]), st))
    parent = {}
    while q:
        tmp = heapq.heappop(q)
        if tmp[1] == maze.waypoints[0]: # is tmp in waypoints
            return backtrace(parent, st, tmp[1]) # if in, then tmp[2].remove(tmp[1])
        for i in maze.neighbors(tmp[1][0], tmp[1][1]):
            if i not in visited: # (i, tmp[2])
                parent[i] = tmp[1]
                tuple = ((manhattanD(i, maze.waypoints[0]) + len(backtrace(parent, st, tmp[1]))), i) # switch my heuristic
                heapq.heappush(q,tuple)
                visited.append(i)
    return []


def astar_multiple(maze):
    """
    Runs A star for part 4 of the assignment in the case where there are
    multiple objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    
    """
    NOW GOAL IS TO COME UP A NEW VISITED LIST THAT ALLOWS DUPLICATED VISITS

    """
    # start with new state definition
    start_position = maze.start
    start_objectives = maze.waypoints
    start_MST = MST(maze.waypoints)
    start_h = start_MST.compute_mst_weight()
    shortpoint, shortdist = findshortest(start_position, start_objectives)
    start_f = start_h + shortdist
    start_state = (start_position, start_objectives)
    start_node = (start_f, start_state)
    heap = []
    heapq.heappush(heap, start_node)
    parent = {} # empty dictionary
    visited = set()
    visited.add(start_state)
    print(heap)
    while heap:
        current_node = heapq.heappop(heap)
        current_state = current_node[1] #state = ((x,y), list)
        saved_current_list = current_state[1]
        saved_state = current_state
        if current_state[0] in current_state[1]: # if we have searched into a waypoint then remove
            current_goal_list = []
            for o in current_state[1]:
                current_goal_list.append(o)
            current_goal_list.remove(current_state[0])
            tmp_tuples = ()
            for i in current_goal_list:
                tmp_tuples += (i,)
            current_state = (current_state[0], tmp_tuples)
        if not current_state[1]:
            tmp_list = backtrace(parent, start_state, saved_state)
            toreturn = []  
            for i in tmp_list:
                toreturn.append(i[0])
            return toreturn
        for neighbor in maze.neighbors(current_state[0][0], current_state[0][1]):
            neighbor_state = (neighbor, current_state[1])
            if neighbor_state not in visited:
                parent[neighbor_state] = (current_state[0], saved_current_list)
                neighbor_h = MST_heurist(maze, start_state, neighbor_state)
                back_len =  len(backtrace(parent, start_state, neighbor_state)) - 1
                neighbor_f = neighbor_h + back_len
                neighbor_node = (neighbor_f, neighbor_state)
                heapq.heappush(heap, neighbor_node)
                visited.add(neighbor_state)

     
                
def fast(maze):
    """
    Runs suboptimal search algorithm for part 5.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # p = []
    # objectives = maze.waypoints
    # st = maze.start
    # objlist = []
    # for o in objectives:
    #     objlist.append(o)
    # a = st
    # while objlist:
    #     shortpoint, distance = findshortest_1(st,objlist)
    #     a = shortpoint
    #     objlist.remove(shortpoint)
    #     tmppath = astar_s(maze, st, shortpoint)
    #     st = shortpoint
    #     tmppath.remove(tmppath[-1])
    #     p.extend(tmppath)
    # p.append(a)
    # return p
    start_position = maze.start
    start_objectives = maze.waypoints
    start_MST = MST(maze.waypoints)
    start_h = start_MST.compute_mst_weight()
    shortpoint, shortdist = findshortest(start_position, start_objectives)
    start_f = start_h + shortdist
    start_state = (start_position, start_objectives)
    start_node = (start_f, start_state)
    heap = []
    heapq.heappush(heap, start_node)
    # end of heap initialize
    parent = {} # empty dictionary
    visited = set()
    visited.add(start_state)
    while heap:
        current_node = heapq.heappop(heap)
        current_state = current_node[1] #state = ((x,y), list)
        saved_current_list = current_state[1]
        saved_state = current_state
        if current_state[0] in current_state[1]: # if we have searched into a waypoint then remove
            current_goal_list = []
            for o in current_state[1]:
                current_goal_list.append(o)
            current_goal_list.remove(current_state[0])
            tmp_tuples = ()
            for i in current_goal_list:
                tmp_tuples += (i,)
            current_state = (current_state[0], tmp_tuples)
        if not current_state[1]:
            tmp_list = backtrace(parent, start_state, saved_state)
            toreturn = []  
            for i in tmp_list:
                toreturn.append(i[0])
            return toreturn
        for neighbor in maze.neighbors(current_state[0][0], current_state[0][1]):
            neighbor_state = (neighbor, current_state[1])
            if neighbor_state not in visited:
                parent[neighbor_state] = (current_state[0], saved_current_list)
                neighbor_h = MST_heurist_1(maze, start_state, neighbor_state)
                back_len =  len(backtrace(parent, start_state, neighbor_state)) - 1
                neighbor_f = neighbor_h + back_len
                neighbor_node = (neighbor_f, neighbor_state)
                heapq.heappush(heap, neighbor_node)
                visited.add(neighbor_state)

    
def MST_heurist(maze,start_state, current_state): #((x,y),objectlist) tuple[0] current point, tuple[1] objectivelist to be reached
    MT= MST(current_state[1])
    g = MT.compute_mst_weight()
    
    
    shortobj, dist = findshortest(current_state[0], current_state[1])
    

    h = dist + g
    return h
def MST_heurist_1(maze,start_state, current_state): #((x,y),objectlist) tuple[0] current point, tuple[1] objectivelist to be reached
    MT= MST(current_state[1])
    g = MT.compute_mst_weight()
    h = g * 3
    shortobj, dist = findshortest_1(current_state[0], current_state[1])
    h = dist + h
    return h
def bfs_1(maze, start, end):
    """
    Runs BFS for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    toReturn = []
    st = start
    q = []
    visited = []
    q.append(st)
    parent = {}
    if st == end:
        toReturn.append(st)
        return toReturn
    while q:
        tmp = q.pop(0)
        if tmp == end:
            return backtrace(parent, st, end)
        for i in maze.neighbors(tmp[0], tmp[1]):
            if i not in visited:
                parent[i] = tmp
                q.append(i)
                visited.append(i)
    return []


def astar_s(maze, start, end):  # helper function to get greedy search
    """
    Runs A star for part 2 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # openlist = []
    # closedlist = []
    # parent = {}
    # end = maze.waypoints[0]
    # heapq.heappush(maze.start, manhattanD(maze.start, end)) #  f for start point
    # # g distance is calculated by len(backtrace(parent, maze.start, q[0]))
    # while openlist:
    #     q = heapq.heappop(openlist)
        
    #     if q[0] == maze.waypoints[0]:
    #         return backtrace(parent, maze.start, end)
    #     else:
    #         neighbors = maze.neighbors(q[0][0], q[0][1])
    #         for item in neighbors:
    #             if item in visited:
    #                if 
    #             else:

    
    q = []
    visited = []
    visited.append(start)
    heapq.heappush(q, (manhattanD(start, end), start))
    parent = {}
    while q:
        tmp = heapq.heappop(q)
        saved = tmp[1]
        if tmp[1] == end:
            return backtrace(parent, start, saved)
        for i in maze.neighbors(tmp[1][0], tmp[1][1]):
            if i not in visited:
                parent[i] = tmp[1]
                tuple = ((manhattanD(i, end) + len(backtrace(parent, start, tmp[1]))), i)
                heapq.heappush(q,tuple)
                visited.append(i)
                saved = i
    return []

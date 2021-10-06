# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018

"""
This file contains search functions.
"""
# Search should return the path and the number of states explored.
# The path should be a list of tuples in the form (alpha, beta, gamma) that correspond
# to the positions of the path taken by your search algorithm.
# Number of states explored should be a number.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs)
# You may need to slight change your previous search functions in MP1 since this is 3-d maze

from collections import deque
from heapq import heappop, heappush


def search(maze, searchMethod):
    return {
        "bfs": bfs,
    }.get(searchMethod, [])(maze)


'''
traceback parent
'''


def traceback(parent,end,start):
    toreturn = []
    cur = end
    while not(cur == start):
        toreturn.insert(0,cur)
        cur = parent.get(cur,0)
        if cur == 0:
            break
    toreturn.insert(0,start)
    return toreturn


def bfs(maze, ispart1=False):
    # Write your code here
    """
    This function returns optimal path in a list, which contains start and objective.
    If no path found, return None.

    Args:
        maze: Maze instance from maze.py
        ispart1: pass this variable when you use functions such as getNeighbors and isObjective. DO NOT MODIFY THIS
    """
    q = []
    visited = []
    parent = {}
    start = maze.getStart()
    q.append(start)
    visited.append(start)
    while q:
        cur = q.pop(0)
        if maze.isObjective(cur[0], cur[1], cur[2], ispart1):
            return traceback(parent,cur,start)
        neighbours = maze.getNeighbors(cur[0], cur[1], cur[2], ispart1)
        for each in neighbours:
            if each in visited:
                continue
            else:
                q.append(each)
                visited.append(each)
                parent[each] = cur
    return None
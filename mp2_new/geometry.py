# geometry.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by James Gao (jamesjg2@illinois.edu) on 9/03/2021
# Inspired by work done by Jongdeog Lee (jlee700@illinois.edu)

"""
This file contains geometry functions necessary for solving problems in MP2
"""

import math
import numpy as np
from alien import Alien

"""
helper funct to calculate the shortest distance between a point and a line
"""


def point_line(x, y, x1, y1, x2, y2):
    A = x - x1
    B = y - y1
    C = x2 - x1
    D = y2 - y1
    dot = A * C + B * D
    len_sq = C * C + D * D
    param = -1
    if len_sq != 0:
        param = dot / len_sq

    if param < 0:
        xx = x1
        yy = y1
    elif param > 1:
        xx = x2
        yy = y2
    else:
        xx = x1 + param * C
        yy = y1 + param * D

    dx = x - xx
    dy = y - yy
    return math.sqrt(dx * dx + dy * dy)


def ccw(A, B, C):
    return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])


def does_alien_touch_wall_single_line(head, tail, wall, g, r):
    # True if intersect
    A = head
    B = tail
    C = (wall[0], wall[1])
    D = (wall[2], wall[3])
    if ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D):
        return True

    d_min = g / math.sqrt(2) + r
    x = head[0]
    y = head[1]
    x1 = wall[0]
    y1 = wall[1]
    x2 = wall[2]
    y2 = wall[3]
    head_d = point_line(x, y, x1, y1, x2, y2)
    x = tail[0]
    y = tail[1]
    tail_d = point_line(x, y, x1, y1, x2, y2)

    x = wall[0]
    y = wall[1]
    x1 = head[0]
    y1 = head[1]
    x2 = tail[0]
    y2 = tail[1]
    wall1_d = point_line(x, y, x1, y1, x2, y2)
    x = wall[2]
    y = wall[3]
    wall2_d = point_line(x, y, x1, y1, x2, y2)

    d = min(head_d, tail_d, wall1_d, wall2_d)

    if d < d_min or np.isclose(d, d_min):
        return True

    return False


def does_alien_touch_wall_single_circle(pos, r, g, wall):
    d_min = g / math.sqrt(2) + r
    x = pos[0]
    y = pos[1]

    x1 = wall[0]
    y1 = wall[1]
    x2 = wall[2]
    y2 = wall[3]
    d = point_line(x, y, x1, y1, x2, y2)

    if d < d_min or np.isclose(d, d_min):
        return True

    return False


"""
helper func to determine if touching single wall
"""


def does_alien_touch_wall_single(alien, wall, granularity):
    # check if circle
    pos = alien.get_centroid()
    r = alien.get_width()
    if alien.is_circle():
        return does_alien_touch_wall_single_circle(pos, r, granularity, wall)
    else:
        head_tail = alien.get_head_and_tail()
        head = head_tail[0]
        tail = head_tail[1]
        return does_alien_touch_wall_single_line(head, tail, wall, granularity, r)


def does_alien_touch_wall(alien, walls, granularity):
    """Determine whether the alien touches a wall

        Args:
            alien (Alien): Instance of Alien class that will be navigating our map
            walls (list): List of endpoints of line segments that comprise the walls in the maze in the format [(startx, starty, endx, endx), ...]
            granularity (int): The granularity of the map

        Return:
            True if touched, False if not
    """
    for each_wall in walls:
        if does_alien_touch_wall_single(alien, each_wall, granularity):
            return True
    return False


"""
helper function to check circle for goal
"""


def does_alien_touch_goal_single_circle(pos, r, goal):
    d = math.sqrt((pos[0] - goal[0]) ** 2 + (pos[1] - goal[1]) ** 2) - goal[2]
    if d < r or np.isclose(d, r):
        return True
    return False


"""
helper function to check rect for goal
"""


def does_alien_touch_goal_single_rect(alien, goal):
    r = goal[2]
    pos = alien.get_centroid()
    half_l = alien.get_length() / 2
    half_w = alien.get_width()
    head_tail = alien.get_head_and_tail()
    if head_tail[0][0] == head_tail[1][0]:
        # vertical
        upper = pos[1] - half_l
        lower = pos[1] + half_l
        left = pos[0] - half_w - r
        right = pos[0] + half_w + r
        if upper < goal[1] < lower \
                and (left < goal[0] < right or np.isclose(left, goal[0]) or np.isclose(right, goal[0])):
            return True
    else:
        # horizontal
        upper = pos[1] - half_w - r
        lower = pos[1] + half_w + r
        left = pos[0] - half_l
        right = pos[0] + half_l
        if left < goal[0] < right \
                and (upper < goal[1] < lower or np.isclose(upper, goal[1]) or np.isclose(lower, goal[1])):
            return True
    # goal touches rect

    # if close enough then return true

    return False


'''
helper function to check for single goal touching
'''


def does_alien_touch_goal_single(alien, goal):
    pos = alien.get_centroid()
    if alien.is_circle():
        r = alien.get_width()
        return does_alien_touch_goal_single_circle(pos, r, goal)
    else:
        r = alien.get_width()
        head_tail = alien.get_head_and_tail()
        return does_alien_touch_goal_single_circle(head_tail[0], r, goal) \
               or does_alien_touch_goal_single_circle(head_tail[1], r, goal) \
               or does_alien_touch_goal_single_rect(alien, goal)


def does_alien_touch_goal(alien, goals):
    """Determine whether the alien touches a goal

        Args:
            alien (Alien): Instance of Alien class that will be navigating our map
            goals (list): x, y coordinate and radius of goals in the format [(x, y, r), ...]. There can be multiple goals

        Return:
            True if a goal is touched, False if not.
    """
    for each_goal in goals:
        if does_alien_touch_goal_single(alien, each_goal):
            return True
    return False


"""
helper function to check if the current circle is outside of window
"""


def check_circle(window, pos, r):
    # check for upper boundary
    if pos[1] - r < 0 or np.isclose(pos[1] - r, 0):
        return False
    # check for lower boundary
    if pos[1] + r > window[1] or np.isclose(pos[1] + r, window[1]):
        return False
    # check for left boundary
    if pos[0] - r < 0 or np.isclose(pos[0] - r, 0):
        return False
    # check for right boundary
    if pos[0] + r > window[0] or np.isclose(pos[0] + r, window[0]):
        return False
    return True


def is_alien_within_window(alien, window, granularity):
    """Determine whether the alien stays within the window

        Args:
            alien (Alien): Alien instance
            window (tuple): (width, height) of the window
            granularity (int): The granularity of the map
    """
    if alien.is_circle():
        pos = alien.get_centroid()
        r = alien.get_width() + granularity / math.sqrt(2)
        return check_circle(window, pos, r)

    else:
        r = alien.get_width() + granularity / math.sqrt(2)
        head_tail = alien.get_head_and_tail()
        head = head_tail[0]
        tail = head_tail[1]
        return check_circle(window, head, r) and check_circle(window, tail, r)


if __name__ == '__main__':
    # Walls, goals, and aliens taken from Test1 map
    walls = [(0, 100, 100, 100),
             (0, 140, 100, 140),
             (100, 100, 140, 110),
             (100, 140, 140, 130),
             (140, 110, 175, 70),
             (140, 130, 200, 130),
             (200, 130, 200, 10),
             (200, 10, 140, 10),
             (175, 70, 140, 70),
             (140, 70, 130, 55),
             (140, 10, 130, 25),
             (130, 55, 90, 55),
             (130, 25, 90, 25),
             (90, 55, 90, 25)]
    goals = [(110, 40, 10)]
    window = (220, 200)


    def test_helper(alien: Alien, position, truths):
        alien.set_alien_pos(position)
        config = alien.get_config()

        touch_wall_result = does_alien_touch_wall(alien, walls, 0)
        touch_goal_result = does_alien_touch_goal(alien, goals)
        in_window_result = is_alien_within_window(alien, window, 0)

        assert touch_wall_result == truths[
            0], f'does_alien_touch_wall(alien, walls) with alien config {config} returns {touch_wall_result}, expected: {truths[0]}'
        assert touch_goal_result == truths[
            1], f'does_alien_touch_goal(alien, goals) with alien config {config} returns {touch_goal_result}, expected: {truths[1]}'
        assert in_window_result == truths[
            2], f'is_alien_within_window(alien, window) with alien config {config} returns {in_window_result}, expected: {truths[2]}'


    # Initialize Aliens and perform simple sanity check.
    alien_ball = Alien((30, 120), [40, 0, 40], [11, 25, 11], ('Horizontal', 'Ball', 'Vertical'), 'Ball', window)
    test_helper(alien_ball, alien_ball.get_centroid(), (False, False, True))

    alien_horz = Alien((30, 120), [40, 0, 40], [11, 25, 11], ('Horizontal', 'Ball', 'Vertical'), 'Horizontal', window)
    test_helper(alien_horz, alien_horz.get_centroid(), (False, False, True))

    alien_vert = Alien((30, 120), [40, 0, 40], [11, 25, 11], ('Horizontal', 'Ball', 'Vertical'), 'Vertical', window)
    test_helper(alien_vert, alien_vert.get_centroid(), (True, False, True))

    edge_horz_alien = Alien((50, 100), [100, 0, 100], [11, 25, 11], ('Horizontal', 'Ball', 'Vertical'), 'Horizontal',
                            window)
    edge_vert_alien = Alien((200, 70), [120, 0, 120], [11, 25, 11], ('Horizontal', 'Ball', 'Vertical'), 'Vertical',
                            window)

    alien_positions = [
        # Sanity Check
        (0, 100),

        # Testing window boundary checks
        (25.6, 25.6),
        (25.5, 25.5),
        (194.4, 174.4),
        (194.5, 174.5),

        # Testing wall collisions
        (30, 112),
        (30, 113),
        (30, 105.5),
        (30, 105.6),  # Very close edge case
        (30, 135),
        (140, 120),
        (187.5, 70),  # Another very close corner case, right on corner

        # Testing goal collisions
        (110, 40),
        (145.5, 40),  # Horizontal tangent to goal
        (110, 62.5),  # ball tangent to goal

        # Test parallel line oblong line segment and wall
        (50, 100),
        (200, 100),
        (205.5, 100)  # Out of bounds
    ]

    # Truths are a list of tuples that we will compare to function calls in the form (does_alien_touch_wall, does_alien_touch_goal, is_alien_within_window)
    alien_ball_truths = [
        (True, False, False),
        (False, False, True),
        (False, False, True),
        (False, False, True),
        (False, False, True),
        (True, False, True),
        (False, False, True),
        (True, False, True),
        (True, False, True),
        (True, False, True),
        (True, False, True),
        (True, False, True),
        (False, True, True),
        (False, False, True),
        (True, True, True),
        (True, False, True),
        (True, False, True),
        (True, False, True)
    ]
    alien_horz_truths = [
        (True, False, False),
        (False, False, True),
        (False, False, False),
        (False, False, True),
        (False, False, False),
        (False, False, True),
        (False, False, True),
        (True, False, True),
        (False, False, True),
        (True, False, True),
        (False, False, True),
        (True, False, True),
        (True, True, True),
        (False, True, True),
        (True, False, True),
        (True, False, True),
        (True, False, False),
        (True, False, False)
    ]
    alien_vert_truths = [
        (True, False, False),
        (False, False, True),
        (False, False, False),
        (False, False, True),
        (False, False, False),
        (True, False, True),
        (True, False, True),
        (True, False, True),
        (True, False, True),
        (True, False, True),
        (True, False, True),
        (False, False, True),
        (True, True, True),
        (False, False, True),
        (True, True, True),
        (True, False, True),
        (True, False, True),
        (True, False, True)
    ]

    for i in range(len(alien_positions)):
        test_helper(alien_ball, alien_positions[i], alien_ball_truths[i])
        test_helper(alien_horz, alien_positions[i], alien_horz_truths[i])
        test_helper(alien_vert, alien_positions[i], alien_vert_truths[i])

    # Edge case coincide line endpoints
    test_helper(edge_horz_alien, edge_horz_alien.get_centroid(), (True, False, False))
    test_helper(edge_horz_alien, (110, 55), (True, True, True))
    test_helper(edge_vert_alien, edge_vert_alien.get_centroid(), (True, False, True))

    print("Geometry tests passed\n")

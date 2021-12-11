import numpy as np
import utils


class Agent:
    def __init__(self, actions, Ne=40, C=40, gamma=0.7):
        # HINT: You should be utilizing all of these
        self.s = None
        self.points = None
        self._train = None
        self.a = None
        self.actions = actions
        self.Ne = Ne  # used in exploration function
        self.C = C
        self.gamma = gamma
        self.reset()
        # Create the Q Table to work with
        self.Q = utils.create_q_table()
        self.N = utils.create_q_table()

    def train(self):
        self._train = True

    def eval(self):
        self._train = False

    # At the end of training save the trained model
    def save_model(self, model_path):
        utils.save(model_path, self.Q)
        utils.save(model_path.replace('.npy', '_N.npy'), self.N)

    # Load the trained model for evaluation
    def load_model(self, model_path):
        self.Q = utils.load(model_path)

    def reset(self):
        # HINT: These variables should be used for bookkeeping to store information across time-steps
        # For example, how do we know when a food pellet has been eaten if all we get from the environment
        # is the current number of points? In addition, Q-updates requires knowledge of the previously taken
        # state and action, in addition to the current state from the environment. Use these variables
        # to store this kind of information.
        self.points = 0
        self.s = None
        self.a = None

    def getMaxQ(self, food_dir_x, food_dir_y, adjoining_wall_x, adjoining_wall_y, adjoining_body_top,
                adjoining_body_bottom, adjoining_body_left, adjoining_body_right):
        max_Q = -99999999
        max_action = 0
        for action in self.actions:
            cur_Q = self.Q[food_dir_x][food_dir_y][adjoining_wall_x][adjoining_wall_y][adjoining_body_top][
                adjoining_body_bottom][adjoining_body_left][adjoining_body_right][action]
            if max_Q < cur_Q:
                max_Q = cur_Q
                max_action = action
        return max_Q

    def act(self, environment, points, dead):
        '''
        :param environment: a list of [snake_head_x, snake_head_y, snake_body, food_x, food_y] to be converted to a state.
        All of these are just numbers, except for snake_body, which is a list of (x,y) positions
        :param points: float, the current points from environment
        :param dead: boolean, if the snake is dead
        :return: chosen action between utils.UP, utils.DOWN, utils.LEFT, utils.RIGHT

        Tip: you need to discretize the environment to the state space defined on the webpage first
        (Note that [adjoining_wall_x=0, adjoining_wall_y=0] is also the case when snake runs out of the playable board)
        '''
        # TODO: write your function here
        (n_fdx, n_fdy, n_awx, n_awy, n_abt, n_abb, n_abl, n_abr) = self.generate_state(environment)

        if self._train and self.a is not None and self.s is not None:
            if dead:
                reward = -1
            elif points != self.points:
                reward = 1
            else:
                reward = -0.1

            maxQ = self.getMaxQ(n_fdx, n_fdy, n_awx, n_awy, n_abt, n_abb, n_abl, n_abr)

            fdx, fdy, awx, awy, abt, abb, abl, abr = self.s

            lr = self.C / (self.C + self.N[fdx][fdy][awx][awy][abt][abb][abl][abr][self.a])
            self.Q[fdx][fdy][awx][awy][abt][abb][abl][abr][self.a] \
                += lr * (reward + self.gamma * maxQ - self.Q[fdx][fdy][awx][awy][abt][abb][abl][abr][self.a])

        if not dead:
            self.s = (n_fdx, n_fdy, n_awx, n_awy, n_abt, n_abb, n_abl, n_abr)
            self.points = points
        else:
            self.reset()
            return 0

        best = -99999
        action = 0
        for each_action in self.actions:
            N_Table = self.N[n_fdx][n_fdy][n_awx][n_awy][n_abt][n_abb][n_abl][n_abr][each_action]
            if self.Ne <= N_Table:
                Q_table = self.Q[n_fdx][n_fdy][n_awx][n_awy][n_abt][n_abb][n_abl][n_abr][each_action]
                if Q_table >= best:
                    best = Q_table
                    action = each_action
            else:
                if best <= 1:
                    best = 1
                    action = each_action
        self.N[n_fdx][n_fdy][n_awx][n_awy][n_abt][n_abb][n_abl][n_abr][action] += 1

        self.a = action

        return action

    def generate_state(self, environment):
        # TODO: Implement this helper function that generates a state given an environment
        snake_head_x, snake_head_y, snake_body, food_x, food_y = environment
        grid_size = utils.GRID_SIZE

        # check for food
        if snake_head_x == food_x:
            food_dir_x = 0
        elif snake_head_x > food_x:
            food_dir_x = 1
        else:
            food_dir_x = 2

        if snake_head_y == food_y:
            food_dir_y = 0
        elif snake_head_y > food_y:
            food_dir_y = 1
        else:
            food_dir_y = 2

        # check for adjoining walls
        if snake_head_x == grid_size:
            adjoining_wall_x = 1
        elif snake_head_x == 12 * grid_size:
            adjoining_wall_x = 2
        else:
            adjoining_wall_x = 0

        if snake_head_y == grid_size:
            adjoining_wall_y = 1
        elif snake_head_y == 12 * grid_size:
            adjoining_wall_y = 2
        else:
            adjoining_wall_y = 0

        # check for body
        adjoining_body_top = 0
        adjoining_body_bottom = 0
        adjoining_body_left = 0
        adjoining_body_right = 0
        for i in snake_body:
            if i[0] == snake_head_x and i[1] == snake_head_y - grid_size:
                adjoining_body_top = 1
            if i[0] == snake_head_x and i[1] == snake_head_y + grid_size:
                adjoining_body_bottom = 1
            if i[1] == snake_head_y and i[0] == snake_head_x - grid_size:
                adjoining_body_left = 1
            if i[1] == snake_head_y and i[0] == snake_head_x + grid_size:
                adjoining_body_right = 1

        return food_dir_x, food_dir_y, adjoining_wall_x, adjoining_wall_y, adjoining_body_top, adjoining_body_bottom, adjoining_body_left, adjoining_body_right

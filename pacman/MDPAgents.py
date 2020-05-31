# api.py
# parsons/15-nov-2017
#
# Version 6
#
# With acknowledgements to Jiaming Ke, who was the first to report the
# bug in corners and to spot the bug in the motion model.
#
# An API for use with the PacMan AI projects from:
#
# http://ai.berkeley.edu/
#
# This provides a simple way of controlling the way that Pacman moves
# and senses its world, to permit exercises with limited sensing
# ability and nondeterminism in sensing and action.
#
# As required by the licensing agreement for the PacMan AI we have:
#
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

# The code here was written by Simon Parsons, based on examples from
# the PacMan AI projects.

from pacman import Directions
from game import Agent
import api


# map generation which includes map_negative and map_reward to assign
# utility to every position in the map.
class gridworld(Agent):
    # assign parameters of different positions and the number of iteration.
    def __init__(self):
        self.weight_wall = -20
        self.weight_food = 5
        self.weight_capsule = 10
        self.weight_ghost = -20
        self.weight_blank = 0
        self.trans_prob = 0.8
        self.re_map = -0.05
        self.n_re_map = 0.05
        self.food_iter_num = 20
        self.ghost_iter_num = 15
        self.gamma = 0.8

    # generating a map which is dominated by ghost
    def map_negative(self, state, size):
        weight_negative = {}
        (map_x, map_y) = size
        ghost = api.ghosts(state)
        for i in range(map_x + 1):
            for j in range(map_y + 1):
                if (i, j) in ghost:
                    weight_negative[(i, j)] = self.weight_ghost
                else:
                    weight_negative[(i, j)] = self.weight_blank
        return weight_negative

    # assign each point according to the element of it.
    def map_reward(self, state, size):
        weight_reward = {}
        (map_x, map_y) = size
        wall = api.walls(state)
        food = api.food(state)
        ghost = api.ghosts(state)
        capsule = api.capsules(state)
        for i in range(map_x + 1):
            for j in range(map_y + 1):
                if (i, j) in food:
                    weight_reward[(i, j)] = self.weight_food
                elif (i, j) in capsule:
                    weight_reward[(i, j)] = self.weight_capsule
                elif (i, j) in wall:
                    weight_reward[(i, j)] = self.weight_wall
                elif (i, j) in ghost:
                    weight_reward[(i, j)] = self.weight_blank
                else:
                    weight_reward[(i, j)] = self.weight_blank
        return weight_reward

    # get the height of the map
    def find_h(self, corners):
        height = 0
        for i in range(len(corners)):
            if corners[i][1] > height:
                height = corners[i][1]
        return height

    # get the width if teh map
    def find_w(self, corners):
        width = 0
        for i in range(len(corners)):
            if corners[i][0] > width:
                width = corners[i][0]
        return width

        # sum up maps
    def map_sum(self, dict1, dict2, size):
        score = {}
        for i in range(size[0] + 1):
            for j in range(size[1] + 1):
                score[(i, j)] = dict1[(i, j)] + dict2[(i, j)]
        return score

    # get the value of each position in the map
    def map_valuegeneration(self, state, size):
        utility_re = []
        utility_ne = []
        (boundary_x, boundary_y) = size
        corner = api.corners(state)
        wall = api.walls(state)
        food = api.food(state)
        ghost = api.ghosts(state)
        corner_x = self.find_w(corner)
        corner_y = self.find_h(corner)
        map_po = self.map_reward(state, (boundary_x, boundary_y))
        map_ne = self.map_negative(state, (boundary_x, boundary_y))

    # allocate action value in the position map
        for k in range(self.food_iter_num):
            for j in range(1, boundary_y):
                for i in range(1, boundary_x):
                    if (i, j) not in wall and (i, j) not in food:
                        if (i-1, j) in wall:
                            factor_re_west = map_po[(i, j)]
                        else:
                            factor_re_west = map_po[(i-1, j)]
                        if (i+1, j) in wall:
                            factor_re_east = map_po[(i, j)]
                        else:
                            factor_re_east = map_po[(i+1, j)]
                        if (i, j+1) in wall:
                            factor_re_north = map_po[(i, j)]
                        else:
                            factor_re_north = map_po[(i, j+1)]
                        if (i, j-1) in wall:
                            factor_re_south = map_po[(i, j)]
                        else:
                            factor_re_south = map_po[(i, j-1)]
                        utility_re_west = self.trans_prob * factor_re_west + 0.5*(1-self.trans_prob) * factor_re_north + 0.5*(1-self.trans_prob) * factor_re_south
                        utility_re_east = self.trans_prob * factor_re_east + 0.5*(1-self.trans_prob) * factor_re_north + 0.5*(1-self.trans_prob) * factor_re_south
                        utility_re_north = self.trans_prob * factor_re_north + 0.5*(1-self.trans_prob) * factor_re_west + 0.5*(1-self.trans_prob) * factor_re_east
                        utility_re_south = self.trans_prob * factor_re_south + 0.5*(1-self.trans_prob) * factor_re_west + 0.5*(1-self.trans_prob) * factor_re_east
                        # allocate utility value of each position in positive map
                        utility_re.append(self.n_re_map + self.gamma * utility_re_west)
                        utility_re.append(self.n_re_map + self.gamma * utility_re_east)
                        utility_re.append(self.n_re_map + self.gamma * utility_re_north)
                        utility_re.append(self.n_re_map + self.gamma * utility_re_south)
                        map_po[(i, j)] = max(utility_re)
                        utility_re[:] = []

        # allocate value in negative map
        for k in range(len(ghost)):
            for count in range(self.ghost_iter_num):
                for j in range(int(ghost[k][1]-3), int(ghost[k][1]+4)):
                    for i in range(int(ghost[k][0]-3), int(ghost[k][0]+4)):
                        if (i, j) not in wall and 0 < i < corner_x and 0 < j < corner_y and (i, j) not in ghost:
                            if (i-1, j) in wall:
                                factor_ne_west = map_ne[(i, j)]
                            else:
                                factor_ne_west = map_ne[(i-1, j)]
                            if (i+1, j) in wall:
                                factor_ne_east = map_ne[(i, j)]
                            else:
                                factor_ne_east = map_ne[(i+1, j)]
                            if (i, j+1) in wall:
                                factor_ne_north = map_ne[(i, j)]
                            else:
                                factor_ne_north = map_ne[(i, j+1)]
                            if (i, j-1) in wall:
                                factor_ne_south = map_ne[(i, j)]
                            else:
                                factor_ne_south = map_ne[(i, j-1)]
                            utility_ne_north = self.trans_prob * factor_ne_north + 0.5*(1-self.trans_prob) * factor_ne_west+0.5*(1-self.trans_prob) * factor_ne_east
                            utility_ne_south = self.trans_prob * factor_ne_south + 0.5*(1-self.trans_prob) * factor_ne_west+0.5*(1-self.trans_prob) * factor_ne_east
                            utility_ne_west = self.trans_prob * factor_ne_west + 0.5*(1-self.trans_prob) * factor_ne_north+0.5*(1-self.trans_prob) * factor_ne_south
                            utility_ne_east = self.trans_prob * factor_ne_east + 0.5*(1-self.trans_prob) * factor_ne_north+0.5*(1-self.trans_prob) * factor_ne_south
                            utility_ne.append(self.re_map + self.gamma * utility_ne_north)
                            utility_ne.append(self.re_map + self.gamma * utility_ne_south)
                            utility_ne.append(self.re_map + self.gamma * utility_ne_west)
                            utility_ne.append(self.re_map + self.gamma * utility_ne_east)
                            map_ne[(i, j)] = min(utility_ne)
                            utility_ne[:] = []
        # sum up two maps together
            map_value = self.map_sum(map_ne, map_po, (boundary_x, boundary_y))
        # print 'map positive'
        # print map_po
        # print 'map negative'
        # print map_ne
        # print 'map_value'
        # print map_value
        return map_value


# main function
class MDPAgent(Agent):
    #   get action based on MDP
    def getAction(self, state):
        value_list = []
        legal = api.legalActions(state)	
        corner = api.corners(state)
        pacman = api.whereAmI(state)
        pacman_x = pacman[0]
        pacman_y = pacman[1]
        legal_width = corner[3][0]
        legal_height = corner[3][1]
        # policy iteration and evaluation
        # get the value of four directions and select the direction corresponding to
        # the maximum value as Pacman's decision.
        map_effect = gridworld().map_valuegeneration(state, (legal_width, legal_height))
        value_list.append(map_effect[(pacman_x-1, pacman_y)])
        value_list.append(map_effect[(pacman_x+1, pacman_y)])
        value_list.append(map_effect[(pacman_x, pacman_y + 1)])
        value_list.append(map_effect[(pacman_x, pacman_y - 1)])
        max_value = value_list.index(max(value_list))
        # print 'map_effect'
        # print map_effect
        # print 'value_list'
        # print value_list
        # print 'max_value'
        # print max_value
        if max_value == 0:
            return api.makeMove(Directions.WEST, legal)
        if max_value == 1:
            return api.makeMove(Directions.EAST, legal)
        if max_value == 2:
            return api.makeMove(Directions.NORTH, legal)
        if max_value == 3:
            return api.makeMove(Directions.SOUTH, legal)

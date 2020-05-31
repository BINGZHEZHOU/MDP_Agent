# sampleAgents.py
# parsons/07-oct-2017
#
# Version 1.1
#
# Some simple agents to work with the PacMan AI projects from:
#
# http://ai.berkeley.edu/
#
# These use a simple API that allow us to control Pacman's interaction with
# the environment adding a layer on top of the AI Berkeley code.
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

# The agents here are extensions written by Simon Parsons, based on the code in
# pacmanAgents.py

from pacman import Directions
from game import Agent
import api
import random
import game
import util

# RandomAgent
#
# A very simple agent. Just makes a random pick every time that it is
# asked for an action.
class RandomAgent(Agent):

    def getAction(self, state):
        # Get the actions we can try, and remove "STOP" if that is one of them.
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        # Random choice between the legal options.
        return api.makeMove(random.choice(legal), legal)

# RandomishAgent
#
# A tiny bit more sophisticated. Having picked a direction, keep going
# until that direction is no longer possible. Then make a random
# choice.
class MyAgent(Agent):

    # Constructor
    #
    # Create a variable to hold the last action
    def __init__(self):
        self.last = Directions.STOP
        self.facing = Directions.WEST

    def getAction(self, state):
        Reward, pacman = self.get_reward(state)
        legal = api.legalActions(state)
        pick = random.choice(legal)
        self.facing = pick
        print 'pick:'
        print pick
        print 'Reward dict:'
        print Reward
        print 'Position:'
        print pacman
        print 'map amount:'
        print len(Reward)
        return api.makeMove(pick, legal)

    def maps(self, state):
        # Returns the coordinates of available positions that Pacman can move to
        mapList = []
        wallGrid = state.getWalls()
        width = wallGrid.width
        height = wallGrid.height
        for i in range(width):
            for j in range(height):
                if wallGrid[i][j] == False:
                    mapList.append((i, j))

        dict_maps = {}
        for i in range(len(mapList)):
            key = mapList[i]
            dict2 = {key: 1}
            dict_maps.update(dict2)
        return dict_maps

    def get_reward(self, state):
        Reward = self.maps(state)
        pacman = api.whereAmI(state)
        return Reward, pacman


# SensingAgent
#
# Doesn't move, but reports sensory data available to Pacman
class SensingAgent(Agent):

    def getAction(self, state):

        # Demonstrates the information that Pacman can access about the state
        # of the game.

        # What are the current moves available
        legal = api.legalActions(state)
        print "Legal moves: ", legal

        # Where is Pacman?
        pacman = api.whereAmI(state)
        print "Pacman position: ", pacman

        # Where are the ghosts?
        print "Ghost positions:"
        theGhosts = api.ghosts(state)
        for i in range(len(theGhosts)):
            print theGhosts[i]

        # How far away are the ghosts?
        print "Distance to ghosts:"
        for i in range(len(theGhosts)):
            print util.manhattanDistance(pacman,theGhosts[i])

        # Where are the capsules?
        print "Capsule locations:"
        print api.capsules(state)
        
        # Where is the food?
        print "Food locations: "
        print api.food(state)

        # Where are the walls?
        print "Wall locations: "
        print api.walls(state)
        
        # getAction has to return a move. Here we pass "STOP" to the
        # API to ask Pacman to stay where they are.
        return api.makeMove(Directions.STOP, legal)

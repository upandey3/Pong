# coding: utf-8
from Constants import *
from math import floor
from random import randint

class QLearningAgent:

    def __init__(self, end_x, GUI=False, n=12, paddleCount=12, actions=3):
        self.unscale = lambda x: x/500 # function for adjusting size for display
        self.GUI = GUI
        self.board_size = pow(n, 2)
        self.paddle_pos_count = paddleCount
        self.actionCount = actions
        self.N = self.board_size*self.paddle_pos_count*2*3 + 1  # number of states
        self.end_x = end_x
        #Q, a table of action values indexed by state and action, initially zero
        self.Q = {} #[[0]*self.actionCount for i in range(self.N)]
        self.Q["end"] = [-1, -1, -1]
        #Nsa , a table of frequencies for state–action pairs, initially zero
        self.Nsa = {} #[[0]*self.actionCount for i in range(self.N)]
        self.Ne = 5

    #Private, do NOT discretize
    # Gets the action with the highest score (idx, score)
    def get_max_Q_action(self, s):
        maxIdx, maxVal = randint(0, 2), 0
        if s not in self.Q or self.Q[s] == [0, 0, 0]:
            self.Q[s] = [0, 0, 0]
            return maxIdx, maxVal
        for idx, val in enumerate(self.Q[s]):
            if val > maxVal:
                maxIdx, maxVal = idx, val
        return maxIdx, maxVal

    # Private
    def explorationFunction(self, u, n):
        if n < self.Ne:
            return self.Ne - n
        return u

    # Public
    # Return an action with max exploration value
    def getMaxActionwithF(self, s):
        s = self.discretizeState(s)
        if s not in self.Q:
            self.Q[s] = [0,0,0]
        if s not in self.Nsa:
            self.Nsa[s] = [0,0,0]
        maxA = 0; maxVal = 0
        val = self.Q[s]
        for a in range(self.actionCount):
            val = self.explorationFunction(self.Q[s][a], self.Nsa[s][a])
            if val > maxVal:
                maxVal = val
                maxA = a
        return maxA

    # Public
    def updateQ(self, alpha, gamma, s_pr, s, a_pr, r):
        s = self.discretizeState(s)
        s_pr = self.discretizeState(s_pr)
        if s_pr not in self.Q:
            self.Q[s_pr] = [0, 0, 0]
        if s not in self.Q:
            self.Q[s] = [0, 0, 0]
        if r == -1:
            return
        else:
            idx, maxQ = self.get_max_Q_action(s)
            val1 = self.Q[s_pr][a_pr]
            n = self.Nsa[s_pr][a_pr]
            # alpha = 1/(1+ self.Nsa[s_pr][a_pr])
            self.Q[s_pr][a_pr] += alpha*(self.Nsa[s_pr][a_pr])*(r + (gamma * maxQ) - self.Q[s_pr][a_pr])
            val2 = self.Q[s_pr][a_pr]
            diff = val2 - val1

        # print()
        # for i, v in self.Q.items():
        #     print(i, ':', v)
        # print()
    # Public
    def incrementNsa(self, s, a):
        s = self.discretizeState(s)
        if s not in self.Nsa:
            self.Nsa[s] = [0, 0, 0]
        self.Nsa[s][a] += 1


    """ Discretizing function """
    """
    Add one special state for all cases when the ball has passed your paddle (ball_x > 1).
    This special state needn't differentiate among any of the other variables listed above,
    i.e., as long as ball_x > 1, the game will always be in this state, regardless of the ball's
    velocity or the paddle's location. This is the only state with a reward of -1.
    """
    def discretizeState(self, s):
        if self.GUI:
            s = map(self.unscale, s)

        ball_x, ball_y, vel_x, vel_y, paddle_y = s

        # Terminal state
        if ball_x > self.end_x:
            return "end"

        #discretize ball position
        ball_x = floor(ball_x * (12))
        ball_y = floor(ball_y * (12))
        #discretize velocities
        vel_x = -1 if vel_x < 0 else 1
        vel_y = -1 if vel_y < 0 else 1
        if abs(vel_y) < 0.015:
            vel_y = 0

        # discretize paddle position
        if paddle_y == 1 - paddle_height:
            paddle_y = 11
        else:
            paddle_y = floor(12 * paddle_y / (1 - paddle_height))

        return (ball_x, ball_y, vel_x, vel_y, paddle_y)


if __name__  == "__main__":
    q = QLearningAgent()
    print(q.N)
    print(q.discretizeState((0.5, 0.5, 0.015, 0.005, 0.5-(paddle_height/2))))

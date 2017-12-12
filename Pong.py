from QLearning import QLearningAgent
from Constants import *
from random import randint
import pygame

class Pong:

    def __init__(self, GUI=False, state=init_state):
        self.adj = (lambda x: x*500) if GUI else (lambda x: x*1) # function for adjusting size for display
        self.initialState = state
        self.state = map(self.adj, state) #(ball_x, ball_y, velocity_x, velocity_y, paddle_y)
        self.BounceCount = [0]
        self.GUI = GUI
        self.actions = [self.adj(paddle_step), -self.adj(paddle_step), 0]
        self.start_x, self.end_x = 0, self.adj(d_w) # start and end x coordinates for ball
        self.agent = QLearningAgent(self.adj, self.end_x, GUI)
        self.alpha = 0.9 # learning rate
        self.gamma = 0.3 # discount factor : short-sighted .... far-sighted
        self.trainCount = 2000
    def guiInit(self):
        pygame.init()
        window = (int(self.adj(d_w)), int(self.adj(d_h)))
        screen = pygame.display.set_mode(window)
        pygame.display.set_caption('Pong')
        clock = pygame.time.Clock()
        return screen, clock

    def play(self):
        screen = None
        start = True
        if self.GUI:
            screen, clock = self.guiInit()

        stop = False
        while True:
            if self.GUI and len(self.BounceCount) > self.trainCount:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        stop = True
                        break
                    # if event.type == pygame.KEYDOWN:
                    #     if event.key == pygame.K_UP:
                    #         self.updatePaddleY(-1 * self.adj(paddle_step))
                    #     if event.key == pygame.K_DOWN:
                    #         self.updatePaddleY(self.adj(paddle_step))

                # print(event)
            if stop: break

            # Get an action using exploration function
            max_a = self.agent.getMaxActionwithF(list(self.state))
            s_prev = list(self.state)
            # print(self.state)

            # # Perform action and get reward
            step = self.actions[max_a]
            self.updatePaddleY(step)
            r = self.updateBallCoord()
            if r == -1:
                self.startGame(screen)
                continue

            self.agent.incrementNsa(list(s_prev), max_a)
            self.agent.updateQ(self.alpha, self.gamma, list(s_prev), list(self.state), max_a, r)

            if self.GUI and len(self.BounceCount) > self.trainCount:
                #Refresh Screen
                screen.fill(white)
                self.drawLeftWall(screen)
                self.updateRightPaddle(screen)
                self.drawBall(screen)

                pygame.display.update()
                clock.tick(60)

        # print(self.BounceCount)

        if self.GUI: pygame.quit()

    def startGame(self, screen):
        bounces = self.BounceCount[-1]
        average = sum(self.BounceCount)/len(self.BounceCount)
        if len(self.BounceCount) % 2000 == 0:
            print ("Avg: ", average, ", bounces: ", bounces, ", max : ", max(self.BounceCount), ", games: ", len(self.BounceCount))
        self.BounceCount.append(0)
        self.state = map(self.adj, self.initialState) #(ball_x, ball_y, velocity_x, velocity_y, paddle_y)

        if self.GUI and len(self.BounceCount) > self.trainCount:
            screen.fill(white)
            self.drawLeftWall(screen)
            self.updateRightPaddle(screen)
            self.drawBall(screen)
            pygame.time.wait(500)

    # Return reward
    def updateBallCoord(self):
        # print(self.state)
        reward = 0
        #Update Y-Coordinate
        ball_y = self.state[1] + self.state[3]
        if ball_y < 0:
            self.state[1] = abs(ball_y)
            self.state[3] = abs(self.state[3])
            return reward
        elif ball_y > self.adj(d_h):
            self.state[1] = self.adj(2) - ball_y
            self.state[3] = -self.state[3]
            return reward
        self.state[1] = ball_y #+ self.state[3]

        #Update X-Coordinate
        ball_x = self.state[0] + self.state[2]
        if ball_x < 0:
            self.state[0] = abs(ball_x)
            self.state[2] = abs(self.state[2])
        elif ball_x > self.end_x:
            paddle_y = self.state[4]
            paddle_y_end = paddle_y + self.adj(paddle_height) + 4
            if ball_y >= paddle_y and ball_y < paddle_y_end: # Paddle hit
                U = self.adj(randint(-15, 15)/1000.0)
                V = self.adj(randint(-30, 30)/1000.0)
                self.state[0] = 2 * self.end_x - ball_x
                self.state[2] = -self.state[2] + U # velocity_x
                self.state[3] = -self.state[3] + V # velocity_y
                self.BounceCount[-1] += 1
                reward = 1

            else: # Paddle missed
                return -1
        else:
            self.state[0] = ball_x  #+ self.state[2]

        if abs(self.state[2]) <= self.adj(0.03): #velocity_x
            self.state[2] = self.adj(0.04) * (-1 if self.state[0] < 0 else 1)
        if abs(self.state[2]) >= self.adj(1):
            self.state[2] = self.adj(0.99) * (-1 if self.state[0] < 0 else 1)
        if abs(self.state[3]) >= self.adj(1): #velocity_y
            self.state[3] = self.adj(0.99) * (-1 if self.state[1] < 0 else 1)

        self.state[0] = round(self.state[0], 2)
        self.state[1] = round(self.state[1], 2)
        self.state[2] = round(self.state[2], 2)
        self.state[3] = round(self.state[3], 2)
        return reward

    def updatePaddleY(self, increment):
        if self.state[4] + increment < 0:
            self.state[4] = 0
        elif self.state[4] + increment + self.adj(paddle_height) > self.adj(d_h):
            self.state[4] = self.adj(d_h)-self.adj(paddle_height)
        else:
            self.state[4] += increment
        self.state[4] = round(self.state[4], 2)

    def drawBall(self, screen):
        pos = (int(self.state[0]), int(self.state[1]))
        pygame.draw.circle(screen, red, pos, 4)

    def drawLeftWall(self, screen):
        pygame.draw.rect(screen, black, [0, 0, wall_width, self.adj(d_h)])

    def updateRightPaddle(self, screen, paddle_y=None):
        if not paddle_y:
            paddle_y = self.state[4]
        pygame.draw.rect(screen, black, [self.end_x-wall_width, paddle_y, wall_width, self.adj(paddle_height)])


p = Pong()
p.play()

import pygame
from random import randint

black = (0,0,0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
paddle_height = 0.2
init_state = (0.5, 0.5, 0.015, 0.005, 0.5-(paddle_height/2))
wall_width = 10
d_h, d_w = 1, 1 # display height and width
paddle_step = 0.04

class Pong:

    def __init__(self, GUI=False, state=init_state):
        self.adj = (lambda x: x*500) if GUI else (lambda x: x*1) # function for adjusting size for display
        self.initialState = state
        self.state = map(self.adj, state) #(ball_x, ball_y, velocity_x, velocity_y, paddle_y)
        self.state[0] += wall_width
        self.BounceCount = [0]
        self.GUI = GUI
        self.actions = [self.adj(paddle_step), -self.adj(paddle_step), 0]
        self.start_x, self.end_x = wall_width, self.adj(d_w) + wall_width # start and end x coordinates for ball


    def play(self):
        screen = None
        if self.GUI:
            pygame.init()
            window = (int(self.adj(d_w)+(2*wall_width)), int(self.adj(d_h)))
            screen = pygame.display.set_mode(window)
            pygame.display.set_caption('Pong')
            clock = pygame.time.Clock()
        crashed = True
        stop = False
        while True:
            if crashed:
                self.startGame(screen)
                crashed = False

            if self.GUI:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        stop = True
                        break
                    # if event.type == pygame.KEYDOWN:
                    #     if event.key == pygame.K_UP:
                    #         self.updatePaddleY(-1 * self.adj(paddle_step))
                    #     if event.key == pygame.K_DOWN:
                    #         self.updatePaddleY(self.adj(paddle_step))

                print(event)
            # else:
            i = randint(0,2)
            step = self.actions[i]
            self.updatePaddleY(step)

            if stop: break
            crashed = self.updateBallCoord()

            if self.GUI:
                #Refresh Screen
                screen.fill(white)
                self.drawLeftWall(screen)
                self.updateRightPaddle(screen)
                self.drawBall(screen)

                pygame.display.update()
                clock.tick(30)

        bounces = self.BounceCount[:-1]
        average = sum(bounces)/len(bounces)
        print("The average number of bounces was ", average)
        print(self.BounceCount)

        if self.GUI: pygame.quit()

    def startGame(self, screen):
        print("The number of bounces was", self.BounceCount[-1])
        self.BounceCount.append(0)
        self.state = map(self.adj, self.initialState) #(ball_x, ball_y, velocity_x, velocity_y, paddle_y)
        self.state[0] += wall_width

        if self.GUI:
            screen.fill(white)
            self.drawLeftWall(screen)
            self.updateRightPaddle(screen)
            self.drawBall(screen)
            pygame.time.wait(500)

    def updateBallCoord(self):
        #Update Y-Coordinate
        new_y = self.state[1] + self.state[3]
        if new_y <= 0:
            self.state[1] = -new_y
            self.state[3] = -self.state[3]
            return False

        elif new_y >= self.adj(d_h):
            self.state[1] = self.adj(2) - new_y
            self.state[3] = -self.state[3]
            return False
        else:
            self.state[1] = new_y

        #Update X-Coordinate
        new_x = self.state[0] + self.state[2]
        if new_x <= self.start_x:
            self.state[0] = -new_x
            self.state[2] = -self.state[2]
        elif new_x > self.end_x:
            paddle_y = self.state[4]
            paddle_y_end = paddle_y + self.adj(paddle_height) + 4
            if new_y >= paddle_y and new_y <= paddle_y_end: # Paddle hit
                U = self.adj(randint(-15, 15)/1000.0)
                V = self.adj(randint(-30, 30)/1000.0)
                self.state[0] = 2 * self.end_x - new_x
                self.state[2] = -self.state[2] + U# velocity_x
                self.state[3] = -self.state[3] + V# velocity_y
                self.BounceCount[-1] += 1

            else: # Paddle missed
                return True
        else:
            self.state[0] = new_x

        if abs(self.state[2]) <= self.adj(0.03): #velocity_x
            self.state[2] = self.adj(0.04) * (-1 if self.state[0] < 0 else 1)
        if abs(self.state[2]) >= self.adj(1):
            self.state[2] = self.adj(0.09) * (-1 if self.state[0] < 0 else 1)
        if abs(self.state[3]) >= self.adj(1): #velocity_y
            self.state[3] = self.adj(0.09) * (-1 if self.state[1] < 0 else 1)
        return False


    def updatePaddleY(self, increment):
        if self.state[4] + increment < 0:
            self.state[4] = 0
        elif self.state[4] + increment + self.adj(paddle_height) > self.adj(d_h):
            self.state[4] = self.adj(d_h)-self.adj(paddle_height)
        else:
            self.state[4] += increment

    def drawBall(self, screen):
        pos = (int(self.state[0]), int(self.state[1]))
        pygame.draw.circle(screen, red, pos, 4)

    def drawLeftWall(self, screen):
        pygame.draw.rect(screen, black, [0, 0, wall_width, self.adj(d_h)])

    def updateRightPaddle(self, screen, paddle_y=None):
        if not paddle_y:
            paddle_y = self.state[4]
        pygame.draw.rect(screen, black, [self.end_x, paddle_y, wall_width, self.adj(paddle_height)])


p = Pong(True)
p.play()

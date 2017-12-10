import pygame
from random import randint

adj = lambda x: x*500 # function for adjusting size for display
black = (0,0,0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
paddle_height = 0.2
init_state = (0.5, 0.5, 0.015, 0.005, 0.5-(paddle_height/2))
wall_width = 20
d_h, d_w = 1, 1 # display height and width
start_x, end_x = wall_width, adj(d_w) + wall_width # start and end x coordinates for ball
paddle_step = 0.04

class Pong:

    def __init__(self, state=init_state):
        self.initialState = state
        self.state = map(adj, state) #(ball_x, ball_y, velocity_x, velocity_y, paddle_y)
        self.state[0] += 20
        # self.actions = {nothing, paddle_y += 0.04, paddle_y -= 0.04}
        # self.rewards =
        # self.termination
        pygame.init()
        # print(start_x, end_x)

    def play(self):
        window = (adj(d_w)+(2*wall_width), adj(d_h))
        screen = pygame.display.set_mode(window)
        pygame.display.set_caption('Pong')
        clock = pygame.time.Clock()
        crashed = True

        while True:
            if crashed:
                self.startGame(screen)
                crashed = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.updatePaddleY(-1 * adj(paddle_step))
                    if event.key == pygame.K_DOWN:
                        self.updatePaddleY(adj(paddle_step))

                print(event)

            crashed = self.updateBallCoord()
            #Refresh Screen
            screen.fill(white)
            self.drawLeftWall(screen)
            self.updateRightPaddle(screen)
            self.drawBall(screen)


            pygame.display.update()
            clock.tick(30)
        pygame.quit()

    def startGame(self, screen):
        self.state = map(adj, self.initialState) #(ball_x, ball_y, velocity_x, velocity_y, paddle_y)
        screen.fill(white)
        self.drawLeftWall(screen)
        self.updateRightPaddle(screen)
        self.drawBall(screen)

    def updateBallCoord(self):
        """
Increment ball_x by velocity_x and ball_y by velocity_y.
Bounce:
If ball_y < 0 (the ball is off the top of the screen), assign ball_y = -ball_y and velocity_y = -velocity_y.
If ball_y > 1 (the ball is off the bottom of the screen), let ball_y = 2 - ball_y and velocity_y = -velocity_y.
If ball_x < 0 (the ball is off the left edge of the screen), assign ball_x = -ball_x and velocity_x = -velocity_x.
If moving the ball to the new coordinates resulted in the ball bouncing off the paddle, handle the ball's
bounce by assigning ball_x = 2 * paddle_x - ball_x. Furthermore, when the ball bounces off a paddle,
randomize the velocities slightly by using the equation velocity_x = -velocity_x + U and
velocity_y = velocity_y + V, where U is chosen uniformly on [-0.015, 0.015] and V is chosen
uniformly on [-0.03, 0.03]. As specified above, make sure that all |velocity_x| > 0.03."""

        #Update Y-Coordinate
        new_y = self.state[1] + self.state[3]
        if new_y <= 0:
            self.state[1] = -new_y
            self.state[3] = -self.state[3]
            return False
        elif new_y> adj(d_h):
            self.state[1] = 2 - new_y
            self.state[3] = -self.state[3]
            return False
        else:
            self.state[1] = new_y

        #Update X-Coordinate
        new_x = self.state[0] + self.state[2]
        if new_x <= start_x:
            # print(new_x, start_x)
            self.state[0] = -new_x
            self.state[2] = -self.state[2]
        elif new_x > end_x:
            paddle_y = self.state[4]
            paddle_y_end = paddle_y + adj(paddle_height)
            if new_y >= paddle_y and new_y <= paddle_y_end: # Paddle hit
                U = randint(-15, 16)/1000.0
                V = randint(-30, 31)/1000.0
                self.state[0] = 2 * end_x - new_x
                self.state[2] = -self.state[2] + U# velocity_x
                self.state[3] = -self.state[3] + V# velocity_y
            else: # Paddle missed
                return True
        else:
            self.state[0] = new_x

        return False


    def updatePaddleY(self, increment):
        if self.state[4] + increment < 0:
            self.state[4] = 0
        elif self.state[4] + increment + adj(paddle_height) > adj(d_h):
            self.state[4] = adj(d_h)-adj(paddle_height)
        else:
            self.state[4] += increment

    def drawBall(self, screen):
        pos = (int(self.state[0]), int(self.state[1]))
        pygame.draw.circle(screen, red, pos, 4)

    def drawLeftWall(self, screen):
        pygame.draw.rect(screen, black, [0, 0, wall_width, adj(d_h)])

    def updateRightPaddle(self, screen, paddle_y=None):
        if not paddle_y:
            paddle_y = self.state[4]
        pygame.draw.rect(screen, black, [end_x, paddle_y, wall_width, adj(paddle_height)])


p = Pong()
p.play()

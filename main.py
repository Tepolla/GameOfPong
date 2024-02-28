import pygame
import sys
import random
import math

################################ Global variables ################################
#region

# Border items
borderTop = 0
borderLeft = 0
borderBottom = 700  # Screen height
borderRight = 1000  # Screen width

# Paddle items
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 90
PADDLE_MOVEMENT_DISTANCE = 10

# Player items
P1Score = 0
P2Score = 0
P1PaddleY = borderBottom / 2 - PADDLE_HEIGHT / 2
P2PaddleY = borderBottom / 2 - PADDLE_HEIGHT / 2

# Ball items
ballX = borderRight // 2
ballY = borderBottom // 2
ballSpeed = 5
ballRadius = 10
ballSpeedX = 0  # Initialize with a default value
ballSpeedY = 0  # Initialize with a default value

# Frame rate control
FPS = 60

#endregion
################################ Global variables ################################

################################ Paddle mechanics ################################
#region

def Paddle(state, y):
    if y + PADDLE_HEIGHT >= borderBottom and state == 1:
        return 0
    elif y <= borderTop and state == -1:
        return 0
    else:
        return PADDLE_MOVEMENT_DISTANCE * state

#endregion
################################ Paddle mechanics ################################

################################ P1 & P2 paddle mechanics ################################
#region

def P1PaddleMove(state):
    global P1PaddleY
    P1PaddleY += Paddle(state, P1PaddleY)

def P2PaddleMove(state):
    global P2PaddleY
    P2PaddleY += Paddle(state, P2PaddleY)

#endregion
################################ P1 & P2 paddle mechanics ################################

################################ Ball mechanics ################################
#region

def reset_ball():
    global ballX, ballY, ballSpeedX, ballSpeedY
    ballX = borderRight // 2
    ballY = borderBottom // 2
    angle = random.choice([random.randint(-45, 45), random.randint(135, 225)])
    angle_radians = math.radians(angle)
    ballSpeedX = ballSpeed * math.cos(angle_radians)
    ballSpeedY = ballSpeed * math.sin(angle_radians)

def move_ball():
    global ballX, ballY, P1Score, P2Score, ballSpeedX, ballSpeedY

    ballX += ballSpeedX
    ballY += ballSpeedY

    # Collision with top and bottom borders
    if ballY - ballRadius <= borderTop or ballY + ballRadius >= borderBottom:
        ballY -= ballSpeedY
        ballSpeedY *= -1

    # Collision with paddles
    if ballX - ballRadius <= PADDLE_WIDTH and P1PaddleY <= ballY <= P1PaddleY + PADDLE_HEIGHT:
        ballX += ballSpeedX
        ballSpeedX *= -1
    elif ballX + ballRadius >= borderRight - PADDLE_WIDTH and P2PaddleY <= ballY <= P2PaddleY + PADDLE_HEIGHT:
        ballX -= ballSpeedX
        ballSpeedX *= -1

    # Scoring
    if ballX <= borderLeft:
        P2Score += 1
        reset_ball()
    elif ballX >= borderRight:
        P1Score += 1
        reset_ball()



#endregion
################################ Ball mechanics ################################

################################ User controlled mechanics ################################
#region

def getUserInput():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        P1PaddleMove(-1)
    if keys[pygame.K_s]:
        P1PaddleMove(1)
    if keys[pygame.K_UP]:
        P2PaddleMove(-1)
    if keys[pygame.K_DOWN]:
        P2PaddleMove(1)

#endregion
################################ User controlled mechanics ################################

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((borderRight, borderBottom))
pygame.display.set_caption("Pong Game")
clock = pygame.time.Clock()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Get input for user 1 and 2
    getUserInput()

    # Move the ball
    move_ball()

    # Draw everything
    screen.fill((0, 0, 0))  # Clear screen with black color
    pygame.draw.rect(screen, (255, 255, 255), (0, P1PaddleY, PADDLE_WIDTH, PADDLE_HEIGHT))  # Player 1 paddle
    pygame.draw.rect(screen, (255, 255, 255), (borderRight - PADDLE_WIDTH, P2PaddleY, PADDLE_WIDTH, PADDLE_HEIGHT))  # Player 2 paddle
    pygame.draw.circle(screen, (255, 255, 255), (int(ballX), int(ballY)), ballRadius)  # Ball

    # Update screen
    pygame.display.flip()

    # FPS control
    clock.tick(FPS)

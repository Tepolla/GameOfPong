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
ballSpeed = 0
startingSpeed = 5  # change for greater starting speed
speedChange = 1  # change for greater change in speed
ballRadius = 10
ballSpeedX = 0
ballSpeedY = 0

# Frame rate control
FPS = 60

################################ Global variables ################################
#endregion



################################ Paddle mechanics ################################
#region

def Paddle(state, y):
    if y + PADDLE_HEIGHT >= borderBottom and state == 1:
        return 0
    elif y <= borderTop and state == -1:
        return 0
    else:
        return PADDLE_MOVEMENT_DISTANCE * state

################################ Paddle mechanics ################################
#endregion



################################ P1 & P2 paddle mechanics ################################
#region

def P1PaddleMove(state):
    global P1PaddleY
    P1PaddleY += Paddle(state, P1PaddleY)

def P2PaddleMove(state):
    global P2PaddleY
    P2PaddleY += Paddle(state, P2PaddleY)

################################ P1 & P2 paddle mechanics ################################
#endregion



################################ User controlled mechanics ################################
#region

def getUser1Input():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        P1PaddleMove(-1)
    if keys[pygame.K_s]:
        P1PaddleMove(1)

def getUser2Input():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        P2PaddleMove(-1)
    if keys[pygame.K_DOWN]:
        P2PaddleMove(1)

################################ User controlled mechanics ################################
#endregion



################################ Ball mechanics ################################
#region

# Resets ball
def reset_ball():
    global ballX, ballY, ballSpeedX, ballSpeedY, ballSpeed

    # Resets ball speed to starting speed
    ballSpeed = startingSpeed

    # Calculates ball's X, Y position
    ballX = borderRight // 2
    ballY = borderBottom // 2

    # Generates random ball direction & calculates X, Y speed
    angle = random.choice([random.randint(-45, 45), random.randint(135, 225)])
    angle_radians = math.radians(angle)
    ballSpeedX = ballSpeed * math.cos(angle_radians)
    ballSpeedY = ballSpeed * math.sin(angle_radians)

# Determines how ball motion will behave
def ballMove():
    global ballX, ballY, ballSpeedX, ballSpeedY, P1Score, P2Score, ballRadius, ballSpeed, P1PaddleY, P2PaddleY, borderBottom, borderRight

    # Calculate proposed new position
    newBallX = ballX + ballSpeedX
    newBallY = ballY + ballSpeedY

    # Ensure the ball does not go out of bounds vertically
    if newBallY - ballRadius <= 0 or newBallY + ballRadius >= borderBottom:
        ballSpeedY = -ballSpeedY  # Reverse vertical speed
        newBallY = ballY  # Revert Y to previous position to avoid sticking to the boundary

    # Collision detection and speed adjustment for left paddle
    if newBallX - ballRadius < PADDLE_WIDTH and P1PaddleY < ballY < P1PaddleY + PADDLE_HEIGHT:
        # Calculate the new angle based on where the ball hits the paddle
        ballSpeedX = -ballSpeedX
        newBallX = PADDLE_WIDTH + ballRadius  # Ensure the ball bounces off correctly

        # Increase the ball speed and recalculate speed components
        ballSpeed += speedChange
        angle_radians = math.atan2(ballSpeedY, ballSpeedX)
        ballSpeedX = abs(ballSpeed * math.cos(angle_radians))  # Ensure ballSpeedX is positive
        ballSpeedY = ballSpeed * math.sin(angle_radians)

    # Collision detection and speed adjustment for right paddle
    elif newBallX + ballRadius > borderRight - PADDLE_WIDTH and P2PaddleY < ballY < P2PaddleY + PADDLE_HEIGHT:
        ballSpeedX = -ballSpeedX
        newBallX = borderRight - PADDLE_WIDTH - ballRadius  # Ensure the ball bounces off correctly

        # Increase the ball speed and recalculate speed components
        ballSpeed += speedChange
        angle_radians = math.atan2(ballSpeedY, ballSpeedX)
        ballSpeedX = -abs(ballSpeed * math.cos(angle_radians))  # Ensure ballSpeedX is negative for leftward movement
        ballSpeedY = ballSpeed * math.sin(angle_radians)

    # Update the ball's position
    ballX, ballY = newBallX, newBallY

    # Scoring mechanism
    if ballX < 0:  # Ball is out of bounds on the left
        P2Score += 1
        reset_ball()  # Reset the ball to the center
    elif ballX > borderRight:  # Ball is out of bounds on the right
        P1Score += 1
        reset_ball()  # Reset the ball to the center


################################ Ball mechanics ################################
#endregion



################################ NPC mechanics ################################
#region

def Npc1():
    global P1PaddleY
    # Center of the paddle
    paddleCenter = (P1PaddleY + 1) + (PADDLE_HEIGHT - 1) / 2
    # Move paddle up if the ball is above the center of the paddle
    if ballY < paddleCenter - PADDLE_MOVEMENT_DISTANCE:
        P1PaddleMove(-1)
    # Move paddle down if the ball is below the center of the paddle
    elif ballY > paddleCenter + PADDLE_MOVEMENT_DISTANCE:
        P1PaddleMove(1)

def Npc2():
    global P2PaddleY
    # Center of the paddle
    paddleCenter = (P2PaddleY + 1) + (PADDLE_HEIGHT - 1) / 2
    # Move paddle up if the ball is above the center of the paddle
    if ballY < paddleCenter - PADDLE_MOVEMENT_DISTANCE:
        P2PaddleMove(-1)
    # Move paddle down if the ball is below the center of the paddle
    elif ballY > paddleCenter + PADDLE_MOVEMENT_DISTANCE:
        P2PaddleMove(1)

################################ NPC mechanics ################################
#endregion



################################ Draw Method ################################
#region

def draw():
    # print(f"Drawing ball at ({ballX}, {ballY})")  # Debugging print statement

    screen.fill((0, 0, 0))  # Clear screen with black color
    pygame.draw.rect(screen, (255, 255, 255), (0, P1PaddleY, PADDLE_WIDTH, PADDLE_HEIGHT))  # Player 1 paddle
    pygame.draw.rect(screen, (255, 255, 255), (borderRight - PADDLE_WIDTH, P2PaddleY, PADDLE_WIDTH, PADDLE_HEIGHT))  # Player 2 paddle
    pygame.draw.circle(screen, (255, 255, 255), (ballX, ballY), ballRadius)  # Ball

    # Scoreboard
    font = pygame.font.SysFont("Arial", 30)
    score_text = font.render(f"Score: {P1Score} | {P2Score}", True, (255, 255, 255))
    text_rect = score_text.get_rect(center=(borderRight / 2, 30))
    screen.blit(score_text, text_rect)

    pygame.display.flip()


################################ Draw Method ################################
#endregion



################################ Game Method ################################
#region

def game():
    global ballX, ballY
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    getUser1Input() # Enables user one to play with 'w' & 's' keys
    # getUser2Input() # Enables user two to play with arrow keys

    Npc1()  # Enables Npc one to play (left paddle)
    Npc2()  # Enables Npc two to play (right paddle)

    ballMove()

################################ Game Method ################################
#endregion



# Initialize ball direction
reset_ball()

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((borderRight, borderBottom))
pygame.display.set_caption("Pong Game")
clock = pygame.time.Clock()


# Main game loop
while True:
    game()  # Update game logic
    draw()  # Draw the current game state
    clock.tick(FPS)  # Maintain the game's framerate
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
ballSpeed = 3
ballRadius = 10
ballSpeedX = 0  # Initialize with a default value
ballSpeedY = 0  # Initialize with a default value

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

def reset_ball():
    global ballX, ballY, ballSpeedX, ballSpeedY, ballSpeed

    ballSpeed = 5
    ballX = borderRight // 2
    ballY = borderBottom // 2
    angle = random.choice([random.randint(-45, 45), random.randint(135, 225)])
    angle_radians = math.radians(angle)
    ballSpeedX = ballSpeed * math.cos(angle_radians)
    ballSpeedY = ballSpeed * math.sin(angle_radians)


def ballMove():
    global ballX, ballY, ballSpeedX, ballSpeedY, P1Score, P2Score, ballRadius, ballSpeed

    # Move the ball by its current speed
    ballX += ballSpeedX
    ballY += ballSpeedY

    # Collision with top and bottom
    if ballY - ballRadius <= 0 or ballY + ballRadius >= borderBottom:
        ballSpeedY = -ballSpeedY

    # Collision with left paddle
    if ballX - ballRadius <= PADDLE_WIDTH and P1PaddleY < ballY < P1PaddleY + PADDLE_HEIGHT:
        ballSpeedX = -ballSpeedX
        ballSpeed += 1  # Increase the ball speed
        # Recalculate speed components to reflect the new speed
        angle_radians = math.atan2(ballSpeedY, ballSpeedX)
        ballSpeedX = ballSpeed * math.cos(angle_radians)
        ballSpeedY = ballSpeed * math.sin(angle_radians)

    # Collision with right paddle
    elif ballX + ballRadius >= borderRight - PADDLE_WIDTH and P2PaddleY < ballY < P2PaddleY + PADDLE_HEIGHT:
        ballSpeedX = -ballSpeedX
        ballSpeed += 1  # Increase the ball speed
        # Recalculate speed components to reflect the new speed
        angle_radians = math.atan2(ballSpeedY, ballSpeedX)
        ballSpeedX = ballSpeed * math.cos(angle_radians)
        ballSpeedY = ballSpeed * math.sin(angle_radians)

    # Scoring
    if ballX < 0:  # Player 2 scores
        P2Score += 1
        reset_ball()  # Reset the ball to the center

    if ballX > borderRight:  # Player 1 scores
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

    Npc1()
    Npc2()

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


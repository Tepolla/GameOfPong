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

################################ User controlled mechanics ################################
#endregion



################################ Draw Method ################################
#region

def draw():
    screen.fill((0, 0, 0))  # Clear screen with black color
    pygame.draw.rect(screen, (255, 255, 255), (0, P1PaddleY, PADDLE_WIDTH, PADDLE_HEIGHT))  # Player 1 paddle
    pygame.draw.rect(screen, (255, 255, 255), (borderRight - PADDLE_WIDTH, P2PaddleY, PADDLE_WIDTH, PADDLE_HEIGHT))  # Player 2 paddle

    # Scoreboard
    font = pygame.font.SysFont("Arial", 30)  # You can change "Arial" to any available font and 30 to your desired size
    score_text = font.render(f"Score: {P1Score} | {P2Score}", True, (255, 255, 255))
    text_rect = score_text.get_rect(center=(borderRight / 2, 30))  # Adjust the Y value to move it up or down
    screen.blit(score_text, text_rect)

    pygame.display.flip()

################################ Draw Method ################################
#endregion



################################ Game Method ################################
#region

def game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    getUserInput()
    draw()

################################ Game Method ################################
#endregion



# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((borderRight, borderBottom))
pygame.display.set_caption("Pong Game")
clock = pygame.time.Clock()

# Main game loop
while True:
    game()
    clock.tick(FPS)

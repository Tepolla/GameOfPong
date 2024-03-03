import pygame
import sys

################################ Global variables ################################

# Border items
borderTop = 0
borderLeft = 0
borderBottom = 700 # Height of the screen
borderRight = 1000 # Width of the screen

# Paddle items
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 90
PADDLE_MOVEMENT_DISTANCE = 10

# Player1 items
P1Score = 0
P1PaddleX = borderLeft + 10 # borderLeft isn't needed, it just helps make the code look neater
P1PaddleY = borderBottom / 2

# Player2 items
P2Score = 0
P2PaddleX = borderRight - 10
P2PaddleY = borderBottom / 2

# Ball items
ballX = 0
ballY = 0
ballDir = 0
ballSpeed = 0

# Frame rate control
FPS = 60

################################ Global variables ################################



################################ Paddle mechanics ################################

def Paddle(state, y):
    # REMEMBER, (0, 0) IS LOCATED AT THE TOP LEFT OF THE CREATED WINDOW
    # THEREFORE INCREASING Y POSITION MOVES ENTITY DOWN AND DECREASING, UP

    # Prevents paddle from going below the screen
    if (y + PADDLE_HEIGHT) >= borderBottom and state == -1:
        return 0
    # Prevents paddle from going above the screen
    elif y <= borderTop and state == 1:
        return 0
    #
    else:
        # Moves paddle up
        if state == 1:
            return -PADDLE_MOVEMENT_DISTANCE
        # Moves paddle down
        elif state == -1:
            return PADDLE_MOVEMENT_DISTANCE
        # Doesn't move paddle if state is 0 (no directional input)
        else:
            return 0


################################ Paddle mechanics ################################



################################ P1 paddle mechanics ################################

def P1PaddleMove(state):
    global P1PaddleY
    P1PaddleY += Paddle(state, P1PaddleY)

################################ P1 paddle mechanics ################################



################################ User controlled mechanics ################################

def getUserInput():
    keys = pygame.key.get_pressed()

    # Player 1 controls
    if keys[pygame.K_w]:
        P1PaddleMove(1)  # Move up
    if keys[pygame.K_s]:
        P1PaddleMove(-1)  # Move down

# Future: Add Player 2 controls here


################################ User controlled mechanics ################################



# Initialize Pygame
pygame.init()

# Setting the width and height of the screen
screen = pygame.display.set_mode((borderRight, borderBottom))
pygame.display.set_caption("Pong Game")

# Clock object to control the frame rate
clock = pygame.time.Clock()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Get user input
    getUserInput()

    # Draw everything here
    screen.fill((0, 0, 0))  # Clear screen with black color

    # Draw Player 1 paddle
    pygame.draw.rect(screen, (255, 255, 255), (P1PaddleX, P1PaddleY, PADDLE_WIDTH, PADDLE_HEIGHT))

    # Update screen
    pygame.display.flip()

    # FPS control to make movements smoother
    clock.tick(FPS)
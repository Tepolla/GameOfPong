This code outlines a basic Pong game created with Pygame, that can be played by players or an NPC. The objective is to prevent the ball from passing one's paddle, while trying to get it past the opponent's paddle.

Content Table:
**Global Variables**
Defines the screen dimensions, paddle dimensions and movement, initial player scores, ball position and speed settings, and the frame rate.

**Paddle Mechanics**
Contains a function to calculate paddle movement while ensuring the paddle does not move out of the screen bounds.

**Player Paddle Mechanics**
Provides functions to move the player paddles up or down based on player input or NPC behavior.

**User-Controlled Mechanics**
Captures user input to control paddle movement with keyboard keys.

**Ball Mechanics**
Includes functions to reset the ball to the center of the screen, calculate its movement, handle collisions with paddles and screen borders, and update scores when the ball goes out of bounds.

**NPC Mechanics**
Defines simple AI behavior for controlling paddles automatically, aiming to keep the paddle aligned with the ball.

**Draw Method**
Handles all the drawing operations to render the game state on the screen, including paddles, ball, and score display.

**Game Method**
Manages the game loop, processing events, updating game state, and drawing the updated state each frame.

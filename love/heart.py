import pygame
import sys 
import random


# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Heart Game")


screen.fill((135, 206, 250))  # Fill the screen with light blue color




# Define Play Again button properties
play_again_button_rect = pygame.Rect(screen_width // 2 - 100, 150, 200, 50)
play_again_button_color = (0, 255, 0)
play_again_text_color = (255, 255, 255)
font = pygame.font.Font(None, 36)



# Load and resize heart image
heart_image = pygame.image.load("OIP.png")
heart_image = pygame.transform.scale(heart_image, (30, 30))  # Resize heart image
heart_rect = heart_image.get_rect()

# Load image for obstacle
obstacle_image = pygame.image.load("danger.png")
obstacle_width = 50
obstacle_height = 50

# Scale the obstacle image to fit the obstacle rectangle
obstacle_image = pygame.transform.scale(obstacle_image, (obstacle_width, obstacle_height))

# Create a green surface for the obstacle boxes
obstacle_surface = pygame.Surface((obstacle_width, obstacle_height))
obstacle_surface.fill((0, 255, 0))  # Fill with green color

# Number of obstacles to generate
num_obstacles = 10

# Generate random obstacle rectangles
obstacles = []
for _ in range(num_obstacles):
    x = random.randint(0, screen_width - obstacle_width)
    y = random.randint(0, screen_height - obstacle_height)
    obstacles.append(pygame.Rect(x, y, obstacle_width, obstacle_height))

# Initial position of the hearts
left_heart_x = screen_width // 4
left_heart_y = screen_height // 2

right_heart_x = 3 * screen_width // 4
right_heart_y = screen_height // 2

# Movement speed of the hearts
speed = 0.05

# Flag for game over
game_over = False

# Flag for joining hearts
hearts_joined = False

# Define font for message
font = pygame.font.Font(None, 36)

# Function to display message and ask for play again
def display_message():
    message = font.render("Congratulations! Hearts joined!", True, (255, 0, 0))
    screen.blit(message, (screen_width // 2 - message.get_width() // 2, 50))

    play_again_message = font.render("Press R to play again or Q to quit", True, (0, 0, 255))
    screen.blit(play_again_message, (screen_width // 2 - play_again_message.get_width() // 2, 100))

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                # Reset game if 'R' key is pressed
                game_over = False
                hearts_joined = False
                left_heart_x = screen_width // 4
                left_heart_y = screen_height // 2
                right_heart_x = 3 * screen_width // 4
                right_heart_y = screen_height // 2
            elif event.key == pygame.K_q:
                # Quit if 'Q' key is pressed
                running = False

        # Check for mouse click events
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the user clicked on the "Play Again" button
            if play_again_button_rect.collidepoint(event.pos) and game_over:
                game_over = False
                hearts_joined = False
                left_heart_x = screen_width // 4
                left_heart_y = screen_height // 2
                right_heart_x = 3 * screen_width // 4
                right_heart_y = screen_height // 2

    # Check for user input to move the hearts (right heart controlled by arrow keys)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        right_heart_x -= speed
    if keys[pygame.K_RIGHT]:
        right_heart_x += speed
    if keys[pygame.K_UP]:
        right_heart_y -= speed
    if keys[pygame.K_DOWN]:
        right_heart_y += speed

    # Update the position of the right heart
    right_heart_rect = heart_rect.move(right_heart_x, right_heart_y)

    # Left heart moves towards the right heart while avoiding obstacles
    if left_heart_x < right_heart_x:
        left_heart_x += speed
    elif left_heart_y != right_heart_y:
        if left_heart_y < right_heart_y:
            left_heart_y += speed
        else:
            left_heart_y -= speed

    # Update the position of the left heart
    left_heart_rect = heart_rect.move(left_heart_x, left_heart_y)

    # Collision detection with obstacles for both hearts
    for obstacle in obstacles:
        if left_heart_rect.colliderect(obstacle):
            # If left heart collides with obstacle, stop it
            left_heart_x, left_heart_y = left_heart_rect.center
        if right_heart_rect.colliderect(obstacle):
            # If right heart collides with obstacle, stop it
            right_heart_x, right_heart_y = right_heart_rect.center

    # Collision detection between hearts
    if left_heart_rect.colliderect(right_heart_rect):
        game_over = True
        hearts_joined = True

    # Clear the screen
    screen.fill((255, 255, 255))

    # Draw the hearts
    screen.blit(heart_image, left_heart_rect)
    screen.blit(heart_image, right_heart_rect)

    # Draw obstacle images on green surface
    for obstacle in obstacles:
        screen.blit(obstacle_surface, obstacle)
        screen.blit(obstacle_image, obstacle)

    # If hearts join, display congratulatory message
    if hearts_joined:
        display_message()
        pygame.draw.rect(screen, play_again_button_color, play_again_button_rect)
        play_again_text = font.render("Play Again", True, play_again_text_color)
        screen.blit(play_again_text, (screen_width // 2 - play_again_text.get_width() // 2, 165))

    # Update the display
    pygame.display.flip()

    

    
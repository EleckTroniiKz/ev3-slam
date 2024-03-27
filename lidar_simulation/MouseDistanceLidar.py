import pygame
import math

"""
    Dieser Code liest auch ein bild ein. Wichtig ist es WEIßER HINTERGRUND und SCHWARZE HINDERNISSE.
    Wenn man leertaste clickt, dann wird ein Strahl geschossen und die Distanz zum nächsten Hindernis wird ausgegeben.
    Der Punkt der angeschossen wurde wird rot markiert.
    In der Mitte ist ein Roboter, dieser gibt an in welche Richtung der Strahl geschossen wird.
    ABER WICHTIG: Der STRAHL wird immer von der MAUS POSITION geschossen, in die Richtung des Winkels.
"""


# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 800, 600
SPEED = 2
ROTATION_SPEED = 2

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill((255, 255, 255))

background = pygame.image.load('./LidarSimulation/images/field_one.png')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
screen.blit(background, (0, 0) )
# Define the box
box = pygame.image.load('./LidarSimulation/images/turret.png')  # Create a surface  # Fill it with white
box = pygame.transform.rotate(box, -90)
box_rect = box.get_rect()  # Get the rect of the surface
box_rect.center = (WIDTH // 2, HEIGHT // 2)  # Position the rect

OBSTACLE = (0,0,0)

def distance_to_obstacle(point, angle, distance):
    dx = math.cos(math.radians(angle))
    dy = math.sin(math.radians(angle))

    # Start at the point
    x, y = point

    # Step along the line until we hit a boundary, an obstacle, or the maximum distance
    for _ in range(int(distance)):
        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            # Get the color of the pixel at the current coordinates, ignoring the alpha value
            color = screen.get_at((int(x), int(y)))[:3]
            # Check if the color is close to black
            if color == OBSTACLE:
                break
        else:
            return math.hypot(x - point[0], y - point[1]), (x, y)
        x += dx
        y += dy

    # Return the distance from the point to the boundary or the obstacle
    return math.hypot(x - point[0], y - point[1]), (x, y)

def shoot_ray(angle, pos):
    # Calculate the direction of the ray 
    return distance_to_obstacle(pos, angle, 800)



# Set up the clock
clock = pygame.time.Clock()

# Set the initial angle
angle = 0

# Game loop
running = True
while running:
    # Cap the frame rate to 60 FPS
    clock.tick(60)

    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get the current keys pressed
    keys = pygame.key.get_pressed()

    pos = None

    if keys[pygame.K_a]:
        angle += ROTATION_SPEED
    if keys[pygame.K_d]:
        angle -= ROTATION_SPEED

    if keys[pygame.K_SPACE]:
        distance, pos = shoot_ray(angle, pygame.mouse.get_pos())
        print(f"Angle: {angle}, Distance: {distance}")

    
    # Rotate the box
    rotated_box = pygame.transform.rotate(box, -angle)
    rotated_box_rect = rotated_box.get_rect(center=box_rect.center)


    # Redraw the screen
    screen.blit(background, (0, 0))
    # Draw the box
    screen.blit(rotated_box, rotated_box_rect.topleft)

    if pos is not None:
        pygame.draw.circle(screen, (255, 0, 0), pos, 5)

    # Flip the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
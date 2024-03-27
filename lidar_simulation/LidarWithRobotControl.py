import pygame
import math

"""
    Dieser Code ist wie MouseDistanceLidar. Aber hier steuern wir einen Roboter. Dieser wird per Tastatur mit w nach vorne geschickt und mit s nach hinten.
    A und D rotieren den Roboter. Wenn man leertaste clickt, wird ein ray geschossen. 
    Da wo der Ray auf ein Hindernis trifft, wird ein roter Punkt gesetzt.
    Die Länge des Rays ist aktuell bei 800 gesetzt. Wenn der Ray auf kein Hindernis und nicht auf die Wand trifft, ist der Rote punkt in der Mitte der Map.
    Bei der Map auch darauf achten, dass der Hintergrund weiß ist und die Hindernisse schwarz.
    Wenn der Ray kürzer als 800 sein soll, dann macht einfach Strg+F und Replaced 800 mit eurer gewünschten Länge.
"""

class Robot:

    def __init__(self):
        self.x = 0
        self.y = 0
        self.angle = 0
    
    def turnRight(self, degrees):
        self.angle -= degrees

    def turnLeft(self, degrees):
        self.angle += degrees

    def moveForward(self, speed):
        self.x += speed * math.cos(math.radians(self.angle))
        self.y -= speed * math.sin(math.radians(self.angle))
    
    def moveBackward(self, speed):
        self.x -= speed * math.cos(math.radians(self.angle))
        self.y += speed * math.sin(math.radians(self.angle))

    def shootLidar(self, screen, point):
        dx = math.cos(math.radians(-self.angle))
        dy = math.sin(math.radians(-self.angle))

        # Start at the point
        x, y = point

        collided = False
        # Step along the line until we hit a boundary, an obstacle, or the maximum distance
        for _ in range(int(800)):
            if 0 <= x < screen.get_width() and 0 <= y < screen.get_height():
                # Get the color of the pixel at the current coordinates, ignoring the alpha value
                color = screen.get_at((int(x), int(y)))[:3]
                # Check if the color is close to black
                if color == (0,0,0):
                    collided = True
                    break
            else:
                return math.hypot(x - point[0], y - point[1]), (x, y)
            x += dx
            y += dy
        if not collided:
            return 800, (screen.get_width()/2, screen.get_height()/2)
        # Return the distance from the point to the boundary or the obstacle
        return math.hypot(x - point[0], y - point[1]), (x, y)
    
    def getPos(self):
        return (self.x, self.y)
    
    def getAngle(self):
        return self.angle
                                      
class Visualize:

    def __init__(self, width=800, height=600, ticks=30):
        pygame.init()
        self.WIDTH, self.HEIGHT = width, height
        self.SPEED = 2
        self.ROTATION_SPEED = 2
        self.OBSTACLE = (0,0,0)
        self.clock = pygame.time.Clock()
        self.clock.tick(ticks)
        self.running = True

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.screen.fill((255, 255, 255))

        self.background = pygame.image.load('./LidarSimulation/images/field_one.png') # change field path to your field
        self.background = pygame.transform.scale(self.background, (self.WIDTH, self.HEIGHT))
        self.screen.blit(self.background, (0, 0))

        self.robotImage = pygame.image.load('./LidarSimulation/images/turret.png')
        self.robotImage = pygame.transform.scale(self.robotImage, (50, 50))
        self.robotImage = pygame.transform.rotate(self.robotImage, -90)
        self.robot_rect = self.robotImage.get_rect()
        self.robot_rect.center = (self.WIDTH // 2, self.HEIGHT // 2)
        self.robot = Robot()

        self.robotForward = False
        self.robotBackward = False
        self.robotLeft = False
        self.robotRight = False
        self.robotScan = False

        self.lastPosition = (0, 0)
        self.lastCalculatedDistance = 0
    
    def get_last_position_and_distance(self):
        return self.lastPosition, self.lastCalculatedDistance

    def check_press_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and not self.robotForward:
                    self.robotForward = True
                    self.robot.moveForward(25) # Pixel 
                elif event.key == pygame.K_s and not self.robotBackward:
                    self.robotBackward = True
                    self.robot.moveBackward(25)
                elif event.key == pygame.K_a and not self.robotLeft:
                    self.robotLeft = True
                    self.robot.turnLeft(45) # Degrees
                elif event.key == pygame.K_d and not self.robotRight:
                    self.robotRight = True
                    self.robot.turnRight(45)
                elif event.key == pygame.K_SPACE and not self.robotScan:
                    self.robotScan = True
                    self.lastCalculatedDistance, self.lastPosition = self.robot.shootLidar(self.screen, self.robot.getPos())

                    print(self.robot.getPos())
                    print(self.robotImage.get_rect().topleft)
                    print(f"Angle: {self.robot.getAngle()}, Distance: {self.lastCalculatedDistance}")
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.robotForward = False
                elif event.key == pygame.K_s:
                    self.robotBackward = False
                elif event.key == pygame.K_a:
                    self.robotLeft = False
                elif event.key == pygame.K_d:
                    self.robotRight = False
                elif event.key == pygame.K_SPACE:
                    self.robotScan = False
        
    def update_screen(self):        
        self.robotImage.get_rect().center = self.robot.getPos()
        rotated_robot = pygame.transform.rotate(self.robotImage, self.robot.getAngle())
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(rotated_robot, self.robot.getPos())
        
        pygame.draw.circle(self.screen, (255, 0, 0), self.lastPosition, 5)
        pygame.display.flip()
    
    def game_loop(self):
        while self.running:
            self.check_press_events()
            self.update_screen()
        pygame.quit()

vis = Visualize()
vis.game_loop()
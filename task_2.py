import math
import random
import sys

import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600                          # Declaring the Constants
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ROBOT_RADIUS = 20
PILLAR_WIDTH = 200
PILLAR_HEIGHT = 300
PILLAR_TOP_LEFT = (SCREEN_WIDTH // 2 - PILLAR_WIDTH // 2, SCREEN_HEIGHT // 2 - PILLAR_HEIGHT // 2)
TARGET_RADIUS = 10
TARGET_COLOR = (255, 255, 0)
MOVEMENT_SPEED = 2

class Robot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move_towards(self, target, pillar):
        dx = target.x - self.x
        dy = target.y - self.y

        # Check for collision with the pillar
        if dx != 0 and dy != 0:
            # Diagonal movement
            new_x = self.x + math.copysign(MOVEMENT_SPEED, dx)
            new_y = self.y + math.copysign(MOVEMENT_SPEED, dy)
            new_rect = pygame.Rect(new_x - ROBOT_RADIUS, new_y - ROBOT_RADIUS, ROBOT_RADIUS * 2, ROBOT_RADIUS * 2)
            if not new_rect.colliderect(pillar.rect):
                # Move diagonally only if there's no collision
                self.x = new_x
                self.y = new_y
            elif abs(dx) > abs(dy):
                # Move only along the x-axis if the absolute value of dx is greater
                self.x += math.copysign(MOVEMENT_SPEED, dx)
            else:
                # Move only along the y-axis if the absolute value of dy is greater
                self.y += math.copysign(MOVEMENT_SPEED, dy)
        else:
            # Move along the axis where there's no obstacle
            self.x += math.copysign(MOVEMENT_SPEED, dx)
            self.y += math.copysign(MOVEMENT_SPEED, dy)

class Pillar:
    def __init__(self, top_left, width, height):
        self.top_left = top_left
        self.width = width
        self.height = height
        self.rect = pygame.Rect(top_left[0], top_left[1], width, height)

    def draw(self, screen):
        pygame.draw.rect(screen, RED, (self.top_left[0], self.top_left[1], self.width, self.height))

    def center(self):
        return (self.top_left[0] + self.width // 2, self.top_left[1] + self.height // 2)

def handle_button_click(mouse_pos):
    if 670 <= mouse_pos[0] <= 770 and 10 <= mouse_pos[1] <= 50:
        return True
    return False

def draw_restart_button(screen):
    pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(670, 10, 100, 40))
    font = pygame.font.SysFont(None, 30)
    text = font.render("Restart", True, (0, 0, 0))
    screen.blit(text, (680, 20))

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Robot Navigation")
    clock = pygame.time.Clock()  # Create a clock object

    start_x = random.choice([random.randint(0, SCREEN_WIDTH // 2 - ROBOT_RADIUS),                 # initialising position for the robot outside the pillar
                             random.randint(SCREEN_WIDTH // 2 + PILLAR_WIDTH + ROBOT_RADIUS, SCREEN_WIDTH)])
    start_y = random.randint(0, SCREEN_HEIGHT)
    robot = Robot(start_x, start_y)

    pillar = Pillar(PILLAR_TOP_LEFT, PILLAR_WIDTH, PILLAR_HEIGHT)                                 # Creating a pillar

    # Calculate center of the pillar
    center_x, center_y = pillar.center()

    # Move the robot halfway towards the center along both axes in each move
    target_x = center_x
    target_y = center_y
    target = Robot(target_x, target_y)

    # Flag to track if the robot reached the center
    reached_center = False

    # Main loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if reached_center and handle_button_click(mouse_pos):
                    start_x = random.choice([random.randint(0, SCREEN_WIDTH // 2 - ROBOT_RADIUS),
                                             random.randint(SCREEN_WIDTH // 2 + PILLAR_WIDTH + ROBOT_RADIUS, SCREEN_WIDTH)])
                    start_y = random.randint(0, SCREEN_HEIGHT)
                    robot = Robot(start_x, start_y)
                    center_x, center_y = pillar.center()
                    target_x = center_x
                    target_y = center_y
                    target = Robot(target_x, target_y)
                    reached_center = False

        # Clear the screen
        screen.fill(WHITE)

        # Draw the pillar
        pillar.draw(screen)

        # Draw the robot
        pygame.draw.circle(screen, BLUE, (int(robot.x), int(robot.y)), ROBOT_RADIUS)

        # Draw restart button if the robot reached the center
        if reached_center:
            draw_restart_button(screen)

        # Move the robot towards the center
        robot.move_towards(target, pillar)

        # Check if the robot reached the target
        if (abs(robot.x - target.x) < MOVEMENT_SPEED and abs(robot.y - target.y) < MOVEMENT_SPEED):
            reached_center = True

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(30)

    # Event handling to keep the window open until closed
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    main()

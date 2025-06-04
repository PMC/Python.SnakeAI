import pygame
import sys
import random
import time

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
GRID_SIZE = 25
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 10  # Snake speed (frames per second)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
DARK_GREEN = (0, 100, 0)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        # Start with a snake of length 3 in the middle of the screen
        x = GRID_WIDTH // 2
        y = GRID_HEIGHT // 2
        self.body = [(x, y), (x - 1, y), (x - 2, y)]
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.grow_pending = False

    def update(self):
        # Update direction from next_direction but don't allow reversing directly into itself
        if self.next_direction != (-self.direction[0], -self.direction[1]):
            self.direction = self.next_direction

        # Calculate new head position
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = ((head_x + dx) % GRID_WIDTH, (head_y + dy) % GRID_HEIGHT)

        # Check if snake collides with itself
        if new_head in self.body:
            return False

        # Add the new head to the body
        self.body.insert(0, new_head)

        # If no growth pending, remove tail
        if not self.grow_pending:
            self.body.pop()

        else:
            self.grow_pending = False

        return True

    def change_direction(self, direction):
        # Only allow changes that aren't directly opposite to current movement
        dx, dy = direction
        current_dx, current_dy = self.direction

        if (dx != -current_dx or dy != -current_dy) and (dx != 0 or dy != 0):
            self.next_direction = direction

    def grow(self):
        # Mark that we should grow on the next update
        self.grow_pending = True

    def get_head_position(self):
        return self.body[0]

    def draw(self, surface):
        for i, (x, y) in enumerate(self.body):
            color = (
                GREEN if i == 0 else DARK_GREEN
            )  # Different colors for head and body
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)  # Border


class Apple:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()

    def randomize_position(self, snake_body=None):
        if snake_body is None:
            snake_body = []

        # Generate a position that doesn't overlap with the snake's body
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            self.position = (x, y)
            if snake_body.count((x, y)) == 0:
                break

    def draw(self, surface):
        rect = pygame.Rect(
            self.position[0] * GRID_SIZE,
            self.position[1] * GRID_SIZE,
            GRID_SIZE,
            GRID_SIZE,
        )
        pygame.draw.rect(surface, self.color, rect)


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake Game - WASD Controls")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24)

        self.snake = Snake()
        self.apple = Apple()
        self.score = 0

    def draw_grid(self):
        # Draw grid lines for better visibility
        for x in range(0, WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, (50, 50, 50), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, (50, 50, 50), (0, y), (WIDTH, y))

    def draw_score(self):
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

    def run(self):
        # Main game loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    # WASD controls
                    if event.key == pygame.K_w:
                        self.snake.change_direction(UP)
                    elif event.key == pygame.K_s:
                        self.snake.change_direction(DOWN)
                    elif event.key == pygame.K_a:
                        self.snake.change_direction(LEFT)
                    elif event.key == pygame.K_d:
                        self.snake.change_direction(RIGHT)

            # Update game state
            if not self.snake.update():
                # Snake collided with itself
                print("Game Over! Your score:", self.score)
                time.sleep(2)  # Pause before restarting
                self.reset_game()
                continue

            # Check for apple collision
            if self.snake.get_head_position() == self.apple.position:
                self.snake.grow()
                self.score += 10
                self.apple.randomize_position(self.snake.body)

            # Draw everything
            self.screen.fill(BLACK)  # Clear screen with black background
            self.draw_grid()
            self.snake.draw(self.screen)
            self.apple.draw(self.screen)
            self.draw_score()

            pygame.display.update()  # Update display

            # Control game speed (FPS)
            self.clock.tick(FPS)

    def reset_game(self):
        self.snake.reset()
        self.score = 0
        self.apple.randomize_position(self.snake.body)


if __name__ == "__main__":
    game = Game()
    game.run()

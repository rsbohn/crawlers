"""Main entry point for the Crawlers game."""

import sys
import random
import pygame


class Mushroom:
    """A mushroom obstacle in the game."""

    def __init__(self, x: int, y: int, size: int = 20):
        """Initialize a mushroom at the given position."""
        self.x = x
        self.y = y
        self.size = size
        self.rect = pygame.Rect(x - size // 2, y - size // 2, size, size)
        # Mushrooms can have different health levels
        self.health = random.randint(1, 4)
        self.max_health = self.health

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the mushroom on the screen."""
        # Color based on health (darker = more damaged)
        health_ratio = self.health / self.max_health
        if health_ratio > 0.75:
            color = (139, 69, 19)  # Brown - healthy
        elif health_ratio > 0.5:
            color = (160, 82, 45)  # Saddle brown - slightly damaged
        elif health_ratio > 0.25:
            color = (210, 180, 140)  # Tan - damaged
        else:
            color = (244, 164, 96)  # Sandy brown - heavily damaged

        # Draw mushroom body (rectangle)
        pygame.draw.rect(screen, color, self.rect)

        # Draw mushroom cap (circle on top)
        cap_color = (165, 42, 42) if health_ratio > 0.5 else (205, 92, 92)
        pygame.draw.circle(screen, cap_color, (self.x, self.rect.top), self.size // 3)

        # Draw spots on cap
        spot_color = (255, 255, 255)
        for i in range(2):
            spot_x = self.x + random.randint(-self.size // 4, self.size // 4)
            spot_y = self.rect.top + random.randint(-self.size // 6, self.size // 6)
            pygame.draw.circle(screen, spot_color, (spot_x, spot_y), 2)

    def take_damage(self) -> bool:
        """Mushroom takes damage. Returns True if destroyed."""
        self.health -= 1
        return self.health <= 0


def generate_mushroom_field(
    screen_width: int, screen_height: int, count: int = 25
) -> list[Mushroom]:
    """Generate a field of randomly placed mushrooms."""
    mushrooms = []

    # Create a grid to ensure good distribution
    grid_cols = 10
    grid_rows = 8
    cell_width = screen_width // grid_cols
    cell_height = (screen_height - 100) // grid_rows  # Leave space at top/bottom

    placed_count = 0
    attempts = 0
    max_attempts = count * 3

    while placed_count < count and attempts < max_attempts:
        attempts += 1

        # Pick a random grid cell
        col = random.randint(0, grid_cols - 1)
        row = random.randint(1, grid_rows - 2)  # Avoid top and bottom rows

        # Random position within the cell
        x = col * cell_width + random.randint(20, cell_width - 20)
        y = 80 + row * cell_height + random.randint(20, cell_height - 20)

        # Check if this position is too close to existing mushrooms
        too_close = False
        min_distance = 40

        for existing in mushrooms:
            distance = ((x - existing.x) ** 2 + (y - existing.y) ** 2) ** 0.5
            if distance < min_distance:
                too_close = True
                break

        if not too_close:
            size = random.randint(15, 25)
            mushrooms.append(Mushroom(x, y, size))
            placed_count += 1

    return mushrooms


def main() -> None:
    """Main game function."""
    pygame.init()
    pygame.font.init()

    # Game constants
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    FPS = 60

    # Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (0, 100, 255)

    # Initialize display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Crawlers")
    clock = pygame.time.Clock()

    print("Welcome to Crawlers!")
    print("The crawlers move. You shoot. They turn into mushrooms.")
    print("Press ESC to quit, SPACE to start...")

    running = True
    game_started = False
    mushrooms = []

    # Player properties
    player_radius = 15
    player_x = SCREEN_WIDTH // 2
    player_y = SCREEN_HEIGHT - 50
    player_speed = 5

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    game_started = True
                    # Generate mushrooms when game starts
                    mushrooms = generate_mushroom_field(SCREEN_WIDTH, SCREEN_HEIGHT)
                    print(
                        f"Game started! Generated {len(mushrooms)} mushrooms on the playfield."
                    )
                elif event.key == pygame.K_r and game_started:
                    # R key to regenerate mushrooms
                    mushrooms = generate_mushroom_field(SCREEN_WIDTH, SCREEN_HEIGHT)
                    print(f"Regenerated {len(mushrooms)} mushrooms!")
            elif event.type == pygame.MOUSEBUTTONDOWN and game_started:
                # Click on mushrooms to damage them
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for mushroom in mushrooms[:]:  # Use slice copy to safely modify list
                    # Check if click is near mushroom
                    distance = (
                        (mouse_x - mushroom.x) ** 2 + (mouse_y - mushroom.y) ** 2
                    ) ** 0.5
                    if distance <= mushroom.size:
                        if mushroom.take_damage():
                            mushrooms.remove(mushroom)
                            print(f"Mushroom destroyed! {len(mushrooms)} remaining.")
                        else:
                            print(f"Mushroom damaged! Health: {mushroom.health}")
                        break  # Only damage one mushroom per click

        # Handle continuous key presses for smooth movement
        if game_started:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                player_x -= player_speed
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                player_x += player_speed

            # Keep player within screen bounds (6 pixels from border)
            border_margin = 6
            player_x = max(
                border_margin + player_radius,
                min(SCREEN_WIDTH - border_margin - player_radius, player_x),
            )

        # Clear screen
        screen.fill(BLACK)

        if game_started:
            # Draw border guidelines (subtle lines showing player movement area)
            border_margin = 6
            left_boundary = border_margin + player_radius
            right_boundary = SCREEN_WIDTH - border_margin - player_radius

            # Draw subtle boundary lines
            boundary_color = (50, 50, 50)  # Dark gray
            pygame.draw.line(
                screen,
                boundary_color,
                (left_boundary, 0),
                (left_boundary, SCREEN_HEIGHT),
                1,
            )
            pygame.draw.line(
                screen,
                boundary_color,
                (right_boundary, 0),
                (right_boundary, SCREEN_HEIGHT),
                1,
            )

            # Draw all mushrooms
            for mushroom in mushrooms:
                mushroom.draw(screen)

            # Draw player character (simple circle for now)
            pygame.draw.circle(screen, BLUE, (player_x, player_y), player_radius)

            # Draw game info
            font = pygame.font.Font(None, 24)
            info_text = f"Mushrooms: {len(mushrooms)} | Use ← → or A/D to move"
            text = font.render(info_text, True, WHITE)
            screen.blit(text, (10, 10))

            # Draw instructions
            font_small = pygame.font.Font(None, 18)
            instructions = [
                "• Arrow keys or A/D to move left/right",
                "• Click mushrooms to damage/destroy them",
                "• Press R to regenerate mushroom field",
                "• Player stays 6px from screen borders",
            ]
            for i, instruction in enumerate(instructions):
                text = font_small.render(instruction, True, WHITE)
                screen.blit(text, (10, SCREEN_HEIGHT - 80 + i * 20))
        else:
            # Show start screen
            font = pygame.font.Font(None, 48)
            title = font.render("CRAWLERS", True, WHITE)
            title_rect = title.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
            )
            screen.blit(title, title_rect)

            font_small = pygame.font.Font(None, 24)
            subtitle = font_small.render(
                "Press SPACE to start, ESC to quit", True, WHITE
            )
            subtitle_rect = subtitle.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)
            )
            screen.blit(subtitle, subtitle_rect)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()

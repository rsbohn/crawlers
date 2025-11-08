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


class Crawler:
    """A millipede-style crawler that moves horizontally and drops down when hitting obstacles."""

    def __init__(self, start_x: int, start_y: int, segment_count: int = 8):
        """Initialize a crawler with multiple segments."""
        self.segments = []
        self.segment_size = 12
        self.speed = 2
        self.direction = 1  # 1 for right, -1 for left
        self.drop_distance = 20  # How far down it moves when changing direction

        # Create segments (head to tail)
        for i in range(segment_count):
            segment_x = start_x - (i * self.segment_size)
            self.segments.append(
                {
                    "x": segment_x,
                    "y": start_y,
                    "rect": pygame.Rect(
                        segment_x - self.segment_size // 2,
                        start_y - self.segment_size // 2,
                        self.segment_size,
                        self.segment_size,
                    ),
                }
            )

    def update(self, screen_width: int, mushrooms: list) -> None:
        """Update crawler position and handle collisions."""
        if not self.segments:
            return

        head = self.segments[0]
        new_x = head["x"] + (self.speed * self.direction)

        # Check for screen boundary collision
        hit_boundary = (
            new_x <= self.segment_size // 2
            or new_x >= screen_width - self.segment_size // 2
        )

        # Check for mushroom collision (only check head segment)
        hit_mushroom = False
        head_rect = pygame.Rect(
            new_x - self.segment_size // 2,
            head["y"] - self.segment_size // 2,
            self.segment_size,
            self.segment_size,
        )

        for mushroom in mushrooms:
            if head_rect.colliderect(mushroom.rect):
                hit_mushroom = True
                break

        # If hit something, change direction and drop down
        if hit_boundary or hit_mushroom:
            self.direction *= -1  # Reverse direction
            # Move all segments down
            for segment in self.segments:
                segment["y"] += self.drop_distance
                segment["rect"].y = segment["y"] - self.segment_size // 2
        else:
            # Normal horizontal movement - follow the leader
            # Store previous positions for trailing effect
            prev_positions = [(seg["x"], seg["y"]) for seg in self.segments]

            # Move head
            head["x"] = new_x
            head["rect"].x = new_x - self.segment_size // 2

            # Each segment follows the one in front of it
            for i in range(1, len(self.segments)):
                if i - 1 < len(prev_positions):
                    self.segments[i]["x"] = prev_positions[i - 1][0]
                    self.segments[i]["y"] = prev_positions[i - 1][1]
                    self.segments[i]["rect"].x = (
                        self.segments[i]["x"] - self.segment_size // 2
                    )
                    self.segments[i]["rect"].y = (
                        self.segments[i]["y"] - self.segment_size // 2
                    )

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the crawler segments."""
        for i, segment in enumerate(self.segments):
            # Different colors for head vs body
            if i == 0:  # Head
                color = (255, 100, 100)  # Red head
                # Draw eyes
                pygame.draw.circle(
                    screen, color, (segment["x"], segment["y"]), self.segment_size // 2
                )
                # Add eyes
                eye_color = (255, 255, 255)
                eye_offset = self.segment_size // 4
                pygame.draw.circle(
                    screen,
                    eye_color,
                    (segment["x"] - eye_offset // 2, segment["y"] - eye_offset // 2),
                    2,
                )
                pygame.draw.circle(
                    screen,
                    eye_color,
                    (segment["x"] + eye_offset // 2, segment["y"] - eye_offset // 2),
                    2,
                )
            else:  # Body segments
                # Gradient from red to orange along the body
                intensity = max(100, 255 - (i * 20))
                color = (
                    intensity,
                    max(50, intensity - 50),
                    0,
                )  # Red to orange gradient
                pygame.draw.circle(
                    screen,
                    color,
                    (segment["x"], segment["y"]),
                    self.segment_size // 2 - 1,
                )

    def get_rect(self) -> pygame.Rect:
        """Get bounding rectangle of the entire crawler (for collision detection)."""
        if not self.segments:
            return pygame.Rect(0, 0, 0, 0)

        min_x = min(seg["x"] for seg in self.segments) - self.segment_size // 2
        max_x = max(seg["x"] for seg in self.segments) + self.segment_size // 2
        min_y = min(seg["y"] for seg in self.segments) - self.segment_size // 2
        max_y = max(seg["y"] for seg in self.segments) + self.segment_size // 2

        return pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)

    def is_off_screen(self, screen_height: int) -> bool:
        """Check if crawler has moved off the bottom of the screen."""
        if not self.segments:
            return True
        return min(seg["y"] for seg in self.segments) > screen_height + 50


class Projectile:
    """A projectile shot by the player that travels upward."""

    def __init__(self, x: int, y: int):
        """Initialize a projectile at the given position."""
        self.x = x
        self.y = y
        self.speed = 8  # Pixels per frame
        self.radius = 3
        self.rect = pygame.Rect(
            x - self.radius, y - self.radius, self.radius * 2, self.radius * 2
        )

    def update(self) -> None:
        """Update projectile position."""
        self.y -= self.speed  # Negative speed will make projectile go down
        self.rect.y = self.y - self.radius

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the projectile."""
        # Draw a small yellow/white projectile
        pygame.draw.circle(screen, (255, 255, 100), (self.x, self.y), self.radius)
        # Add a small white center for visibility
        pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), 1)

    def is_off_screen(self, screen_height: int = 600) -> bool:
        """Check if projectile has moved off the screen (top or bottom)."""
        return self.y < -10 or self.y > screen_height + 10

    def is_in_top_half(self, screen_height: int) -> bool:
        """Check if projectile is in the top half of the screen."""
        return self.y <= screen_height // 2


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
    print("Press ESC to quit, S to start...")

    running = True
    game_started = False
    mushrooms = []

    # Player properties
    player_radius = 15
    player_x = SCREEN_WIDTH // 2
    player_y = SCREEN_HEIGHT - 50
    player_speed = 5

    # Crawler properties
    crawlers = []
    crawler_spawn_timer = 0
    crawler_spawn_delay = 180  # Spawn every 3 seconds at 60 FPS

    # Projectile properties
    projectiles = []
    can_shoot = True

    # Score system
    score = 0
    mushroom_points = 10  # Points for destroying a mushroom
    crawler_points = 100  # Points for destroying a crawler
    crawler_segment_points = 10  # Points per crawler segment destroyed

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_s:
                    game_started = True
                    # Reset game state
                    score = 0
                    projectiles = []
                    can_shoot = True
                    # Generate mushrooms when game starts
                    mushrooms = generate_mushroom_field(SCREEN_WIDTH, SCREEN_HEIGHT)
                    # Initialize with one crawler
                    crawlers = [Crawler(SCREEN_WIDTH // 2, 30)]
                    crawler_spawn_timer = 0
                    print(
                        f"Game started! Generated {len(mushrooms)} mushrooms and 1 crawler on the playfield. Score: {score}"
                    )
                elif event.key == pygame.K_r and game_started:
                    # R key to regenerate mushrooms
                    mushrooms = generate_mushroom_field(SCREEN_WIDTH, SCREEN_HEIGHT)
                    print(f"Regenerated {len(mushrooms)} mushrooms!")
                elif (
                    (event.key == pygame.K_UP or event.key == pygame.K_w or event.key == pygame.K_SPACE)
                    and game_started
                    and can_shoot
                    and len(projectiles) < 3  # Maximum 3 projectiles on screen
                ):
                    # Shoot projectile
                    projectiles.append(Projectile(player_x, player_y - player_radius))
                    can_shoot = False
                    print(f"Projectile fired! Total projectiles: {len(projectiles)}")
                elif (
                    (event.key == pygame.K_UP or event.key == pygame.K_w or event.key == pygame.K_SPACE)
                    and game_started
                    and len(projectiles) >= 3
                ):
                    # Can't shoot - too many projectiles on screen
                    print(
                        f"Can't shoot! Maximum 3 projectiles on screen (current: {len(projectiles)})"
                    )
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
                            score += (
                                mushroom_points // 2
                            )  # Half points for manual destruction
                            print(
                                f"Mushroom destroyed! {len(mushrooms)} remaining. +{mushroom_points//2} points! Score: {score}"
                            )
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

            # Update crawlers
            for crawler in crawlers[:]:  # Use slice copy for safe modification
                crawler.update(SCREEN_WIDTH, mushrooms)
                # Remove crawlers that have moved off screen
                if crawler.is_off_screen(SCREEN_HEIGHT):
                    crawlers.remove(crawler)
                    print("Crawler reached the bottom!")

            # Spawn new crawlers periodically
            crawler_spawn_timer += 1
            if crawler_spawn_timer >= crawler_spawn_delay:
                crawler_spawn_timer = 0
                # Spawn from random side (left or right)
                start_x = random.choice([20, SCREEN_WIDTH - 20])
                crawlers.append(Crawler(start_x, 30))
                print(f"New crawler spawned! Total crawlers: {len(crawlers)}")

            # Update projectiles
            for projectile in projectiles[:]:  # Use slice copy for safe modification
                projectile.update()
                projectile_hit_something = False

                # Check if projectile reached top half (allow new shooting)
                if not can_shoot and projectile.is_in_top_half(SCREEN_HEIGHT):
                    can_shoot = True
                    print("Can shoot again!")

                # Check collision with mushrooms
                for mushroom in mushrooms[:]:  # Use slice copy for safe modification
                    if projectile.rect.colliderect(mushroom.rect):
                        # 1/10 chance to ricochet (10% chance)
                        if random.randint(1, 10) == 1:
                            # Ricochet - reverse projectile direction and move it away from mushroom
                            projectile.speed = -projectile.speed  # Reverse direction
                            print(
                                f"Projectile ricocheted off mushroom! New direction: {'up' if projectile.speed < 0 else 'down'}"
                            )
                        else:
                            # Normal hit - damage mushroom and destroy projectile
                            if mushroom.take_damage():
                                mushrooms.remove(mushroom)
                                score += mushroom_points
                                print(
                                    f"Projectile destroyed mushroom! {len(mushrooms)} mushrooms remaining. +{mushroom_points} points! Score: {score}"
                                )
                            else:
                                print(
                                    f"Projectile damaged mushroom! Mushroom health: {mushroom.health}"
                                )
                            projectile_hit_something = True
                        break  # Only hit one mushroom per frame

                # Check collision with crawlers (only if projectile didn't hit mushroom)
                if not projectile_hit_something:
                    for crawler in crawlers[:]:  # Use slice copy for safe modification
                        # Check collision with any crawler segment
                        for segment in crawler.segments:
                            segment_rect = pygame.Rect(
                                segment["x"] - crawler.segment_size // 2,
                                segment["y"] - crawler.segment_size // 2,
                                crawler.segment_size,
                                crawler.segment_size,
                            )
                            if projectile.rect.colliderect(segment_rect):
                                # Projectile hits crawler - both are destroyed
                                crawler_score = crawler_points + (
                                    len(crawler.segments) * crawler_segment_points
                                )
                                score += crawler_score
                                crawlers.remove(crawler)
                                projectile_hit_something = True
                                print(
                                    f"Projectile destroyed crawler! {len(crawlers)} crawlers remaining. +{crawler_score} points! Score: {score}"
                                )
                                break
                        if projectile_hit_something:
                            break

                # Remove projectile if it hit something (except ricochet)
                if projectile_hit_something:
                    projectiles.remove(projectile)
                    continue

                # Remove projectiles that have moved off screen
                if projectile.is_off_screen(SCREEN_HEIGHT):
                    projectiles.remove(projectile)

            # Update shooting availability based on projectile count and reload status
            # Can shoot if: fewer than 3 projectiles AND (can_shoot is True OR no projectiles left)
            if len(projectiles) < 3 and (can_shoot or len(projectiles) == 0):
                if not can_shoot:
                    can_shoot = True

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

            # Draw all crawlers
            for crawler in crawlers:
                crawler.draw(screen)

            # Draw all projectiles
            for projectile in projectiles:
                projectile.draw(screen)

            # Draw player character (simple circle for now)
            pygame.draw.circle(screen, BLUE, (player_x, player_y), player_radius)

            # Draw game info
            font = pygame.font.Font(None, 22)
            if len(projectiles) >= 3:
                shoot_status = "MAX PROJECTILES"
            elif can_shoot:
                shoot_status = "CAN SHOOT"
            else:
                shoot_status = "RELOADING..."
            # Draw score prominently at top
            score_text = f"SCORE: {score:,}"
            score_font = pygame.font.Font(None, 32)
            score_surface = score_font.render(score_text, True, (255, 255, 0))  # Yellow
            screen.blit(score_surface, (10, 10))

            # Draw game status info below score
            info_text = f"Mushrooms: {len(mushrooms)} | Crawlers: {len(crawlers)} | Projectiles: {len(projectiles)}/3 | {shoot_status}"
            text = font.render(info_text, True, WHITE)
            screen.blit(text, (10, 45))

            # Draw instructions
            font_small = pygame.font.Font(None, 18)
            instructions = [
                "• ← → or A/D to move | ↑ or W or SPACE to shoot",
                f"• Scoring: Mushrooms {mushroom_points}pts | Crawlers {crawler_points}pts + {crawler_segment_points}pts per segment",
                "• Max 3 projectiles | Reload when reaching top half",
                "• Click mushrooms to damage/destroy | R to regenerate",
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
                "Press S to start, ESC to quit", True, WHITE
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

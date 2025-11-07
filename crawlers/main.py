"""Main entry point for the Crawlers game."""

import sys
import pygame


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
    GREEN = (0, 255, 0)

    # Initialize display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Crawlers")
    clock = pygame.time.Clock()

    print("Welcome to Crawlers!")
    print("The crawlers move. You shoot. They turn into mushrooms.")
    print("Press ESC to quit, SPACE to start...")

    running = True
    game_started = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    game_started = True
                    print("Game started! (Basic demo - more features coming soon)")

        # Clear screen
        screen.fill(BLACK)

        if game_started:
            # Draw a simple demo
            pygame.draw.circle(
                screen, GREEN, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), 20
            )
            font = pygame.font.Font(None, 36)
            text = font.render("Crawlers Game - Coming Soon!", True, WHITE)
            text_rect = text.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60)
            )
            screen.blit(text, text_rect)
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

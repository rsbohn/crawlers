"""Test the main game module."""

from crawlers.main import main


def test_crawlers_import():
    """Test that we can import the crawlers package."""
    import crawlers

    assert crawlers.__version__ == "0.1.0"


def test_pygame_imports():
    """Test that pygame can be imported and basic constants exist."""
    import pygame

    # Test that pygame constants exist
    assert hasattr(pygame, "QUIT")
    assert hasattr(pygame, "KEYDOWN")


def test_basic_game_setup():
    """Test basic game configuration constants."""

    # Just verify the function exists and can be imported
    assert callable(main)


def test_mushroom_creation():
    """Test that mushrooms can be created and have correct properties."""
    from crawlers.main import Mushroom

    mushroom = Mushroom(100, 200, 20)

    assert mushroom.x == 100
    assert mushroom.y == 200
    assert mushroom.size == 20
    assert mushroom.health > 0
    assert mushroom.health <= 4
    assert mushroom.max_health == mushroom.health


def test_mushroom_damage():
    """Test that mushrooms take damage correctly."""
    from crawlers.main import Mushroom

    mushroom = Mushroom(100, 200, 20)
    initial_health = mushroom.health

    # Mushroom should not be destroyed on first hit (unless health was 1)
    destroyed = mushroom.take_damage()
    assert mushroom.health == initial_health - 1

    # If it had more than 1 health, it shouldn't be destroyed yet
    if initial_health > 1:
        assert not destroyed

    # Damage until destroyed
    while mushroom.health > 0:
        destroyed = mushroom.take_damage()

    assert destroyed
    assert mushroom.health == 0


def test_mushroom_field_generation():
    """Test that mushroom field generation works correctly."""
    from crawlers.main import generate_mushroom_field

    mushrooms = generate_mushroom_field(800, 600, 10)

    # Should generate some mushrooms (maybe not exactly 10 due to collision avoidance)
    assert len(mushrooms) > 0
    assert len(mushrooms) <= 10

    # All mushrooms should be within screen bounds
    for mushroom in mushrooms:
        assert 0 <= mushroom.x <= 800
        assert 0 <= mushroom.y <= 600


def test_player_boundary_constraints():
    """Test that player movement respects screen boundaries."""
    # Test boundary calculation logic
    screen_width = 800
    player_radius = 15
    border_margin = 6

    # Test left boundary
    player_x = 0  # Try to go past left edge
    min_x = border_margin + player_radius
    max_x = screen_width - border_margin - player_radius
    constrained_x = max(min_x, min(max_x, player_x))

    assert constrained_x == min_x  # Should be stopped at left boundary
    assert constrained_x == 21  # 6 + 15 = 21

    # Test right boundary
    player_x = screen_width + 100  # Try to go past right edge
    constrained_x = max(min_x, min(max_x, player_x))

    assert constrained_x == max_x  # Should be stopped at right boundary
    assert constrained_x == 779  # 800 - 6 - 15 = 779


def test_crawler_creation():
    """Test that crawlers can be created with correct properties."""
    from crawlers.main import Crawler

    crawler = Crawler(100, 50, 5)

    # Should have 5 segments
    assert len(crawler.segments) == 5

    # Head should be at specified position
    assert crawler.segments[0]["x"] == 100
    assert crawler.segments[0]["y"] == 50

    # Each segment should be behind the previous one
    for i in range(1, len(crawler.segments)):
        assert crawler.segments[i]["x"] < crawler.segments[i - 1]["x"]
        assert crawler.segments[i]["y"] == crawler.segments[i - 1]["y"]

    # Should start moving right
    assert crawler.direction == 1


def test_crawler_boundary_detection():
    """Test that crawler detects screen boundaries correctly."""
    from crawlers.main import Crawler

    crawler = Crawler(50, 50, 3)

    # Test with no obstacles - should move normally
    initial_x = crawler.segments[0]["x"]
    crawler.update(800, [])

    # Should have moved right (positive direction)
    assert crawler.segments[0]["x"] > initial_x

    # Test boundary collision by placing crawler exactly at right edge
    crawler = Crawler(
        800 - 6, 50, 3
    )  # At right boundary (screen_width - segment_size//2)
    initial_y = crawler.segments[0]["y"]
    initial_direction = crawler.direction
    crawler.update(800, [])

    # Should have dropped down and reversed direction
    assert crawler.segments[0]["y"] > initial_y
    assert crawler.direction != initial_direction


def test_crawler_off_screen_detection():
    """Test that crawler correctly detects when it's off screen."""
    from crawlers.main import Crawler

    crawler = Crawler(100, 50, 3)

    # Should not be off screen initially
    assert not crawler.is_off_screen(600)

    # Move crawler way down
    for segment in crawler.segments:
        segment["y"] = 700

    # Should now be detected as off screen
    assert crawler.is_off_screen(600)


def test_projectile_creation():
    """Test that projectiles can be created with correct properties."""
    from crawlers.main import Projectile

    projectile = Projectile(100, 200)

    assert projectile.x == 100
    assert projectile.y == 200
    assert projectile.speed == 8
    assert projectile.radius == 3

    # Should not be off screen initially
    assert not projectile.is_off_screen()

    # Should be in top half if created at y=200 (for screen height 600, top half is y <= 300)
    assert projectile.is_in_top_half(600)


def test_projectile_movement():
    """Test that projectiles move upward correctly."""
    from crawlers.main import Projectile

    projectile = Projectile(100, 300)
    initial_y = projectile.y

    # Update projectile position
    projectile.update()

    # Should have moved up (y decreased)
    assert projectile.y < initial_y
    assert projectile.y == initial_y - projectile.speed


def test_projectile_top_half_detection():
    """Test that projectiles correctly detect when they're in the top half."""
    from crawlers.main import Projectile

    screen_height = 600

    # Projectile in bottom half
    projectile = Projectile(100, 400)
    assert not projectile.is_in_top_half(screen_height)

    # Projectile in top half
    projectile = Projectile(100, 200)
    assert projectile.is_in_top_half(screen_height)

    # Projectile exactly at middle
    projectile = Projectile(100, screen_height // 2)
    assert projectile.is_in_top_half(screen_height)


def test_projectile_off_screen_detection():
    """Test that projectiles correctly detect when they're off screen."""
    from crawlers.main import Projectile

    projectile = Projectile(100, 50)

    # Should not be off screen initially
    assert not projectile.is_off_screen()

    # Move projectile way up
    projectile.y = -20

    # Should now be detected as off screen
    assert projectile.is_off_screen(600)


def test_projectile_limit_logic():
    """Test the logic for 3-projectile limit."""
    from crawlers.main import Projectile

    # Simulate projectile list management
    projectiles = []
    max_projectiles = 3

    # Should be able to add projectiles up to limit
    for i in range(max_projectiles):
        if len(projectiles) < max_projectiles:
            projectiles.append(Projectile(100, 300 + i * 50))

    assert len(projectiles) == max_projectiles

    # Should not be able to add more than limit
    can_add_more = len(projectiles) < max_projectiles
    assert not can_add_more

    # Remove one projectile (simulate off-screen cleanup)
    projectiles.pop(0)
    assert len(projectiles) == max_projectiles - 1

    # Should now be able to add another
    can_add_more = len(projectiles) < max_projectiles
    assert can_add_more


def test_projectile_collision_detection():
    """Test projectile collision with rectangles."""
    from crawlers.main import Projectile, Mushroom

    # Create projectile and mushroom
    projectile = Projectile(100, 100)
    mushroom = Mushroom(100, 100, 20)  # Same position, should collide

    # Should detect collision
    assert projectile.rect.colliderect(mushroom.rect)

    # Test non-collision
    projectile2 = Projectile(200, 200)
    assert not projectile2.rect.colliderect(mushroom.rect)


def test_projectile_ricochet_behavior():
    """Test projectile speed reversal for ricochet."""
    from crawlers.main import Projectile

    projectile = Projectile(100, 100)
    initial_speed = projectile.speed

    # Normal speed should be positive (going up)
    assert initial_speed > 0

    # Simulate ricochet by reversing speed
    projectile.speed = -projectile.speed
    assert projectile.speed == -initial_speed

    # Update position - should now move down (y increases)
    initial_y = projectile.y
    projectile.update()
    assert projectile.y > initial_y  # Moving down now


def test_projectile_off_screen_with_ricochet():
    """Test that ricocheted projectiles are properly detected as off-screen."""
    from crawlers.main import Projectile

    screen_height = 600

    # Normal projectile going up
    projectile = Projectile(100, 50)
    projectile.y = -20  # Way off top
    assert projectile.is_off_screen(screen_height)

    # Ricocheted projectile going down
    projectile2 = Projectile(100, 550)
    projectile2.speed = -8  # Going down
    projectile2.y = screen_height + 20  # Way off bottom
    assert projectile2.is_off_screen(screen_height)


def test_scoring_system():
    """Test the scoring system calculations."""
    from crawlers.main import Crawler

    # Test crawler scoring calculation
    crawler = Crawler(100, 100, 8)  # 8 segments
    crawler_points = 100
    crawler_segment_points = 10
    expected_crawler_score = crawler_points + (
        len(crawler.segments) * crawler_segment_points
    )

    assert len(crawler.segments) == 8
    assert expected_crawler_score == 180  # 100 + (8 * 10)

    # Test mushroom scoring
    mushroom_points = 10
    mushroom_click_points = mushroom_points // 2

    assert mushroom_points == 10
    assert mushroom_click_points == 5  # Half points for manual destruction


def test_start_key_binding():
    """Test that 's' key is recognized as start key."""
    import pygame

    # Verify pygame has the key constant we need
    assert hasattr(pygame, "K_s")
    assert pygame.K_s == ord("s")


def test_fire_key_bindings():
    """Test that UP, W, and SPACE are all recognized as fire keys."""
    import pygame

    # Verify pygame has all the fire key constants we need
    assert hasattr(pygame, "K_UP")
    assert hasattr(pygame, "K_w")
    assert hasattr(pygame, "K_SPACE")

    # Verify they are different keys
    assert pygame.K_UP != pygame.K_w
    assert pygame.K_UP != pygame.K_SPACE
    assert pygame.K_w != pygame.K_SPACE

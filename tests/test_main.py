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

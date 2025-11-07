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

# Crawlers

The crawlers move. You shoot. They turn into mushrooms.
What other threats will you encounter? Find out here...

## About

Crawlers is a classic-style arcade game built with Python and Pygame. Navigate through waves of crawlers, shoot them down, and watch them transform into mushrooms while avoiding new threats!

## Installation & Setup

This project uses [uv](https://astral.sh/uv/) for fast Python package management.

### Prerequisites

- Python 3.13+
- uv package manager

### Quick Start

1. Clone or download this project
2. Install dependencies:
   ```bash
   uv sync --dev
   ```

3. Run the game:
   ```bash
   uv run python -m crawlers.main
   ```

   Or alternatively:
   ```bash
   uv run python run_game.py
   ```

## Development

### Project Structure

```
crawlers/
├── crawlers/           # Main game package
│   ├── __init__.py
│   └── main.py        # Game entry point
├── main.py            # Legacy entry point
├── run_game.py        # Convenient run script
├── pyproject.toml     # Project configuration
└── README.md
```

### Development Commands

- **Run the game**: `uv run python -m crawlers.main`
- **Run tests**: `uv run pytest`
- **Format code**: `uv run black .`
- **Lint code**: `uv run ruff check .`
- **Type check**: `uv run mypy crawlers/`

### Adding Dependencies

- Runtime dependency: `uv add package_name`
- Development dependency: `uv add --dev package_name`

## Game Controls

- **ESC**: Quit the game
- **SPACE**: Start the game
- More controls coming soon!

## Roadmap

- [ ] Implement crawler movement
- [ ] Add player character and shooting mechanics  
- [ ] Mushroom transformation system
- [ ] Score tracking
- [ ] Sound effects and music
- [ ] Multiple levels/waves
- [ ] Power-ups and special weapons

## License

MIT License - see the project configuration for details.
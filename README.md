# 🐉 Treasure Hunter Quest

A terminal-based Python game where you explore a mysterious island, collect magical crystals, and dodge dangerous volcanoes — all from your command line.

> *An ancient island is filled with hidden gems and dangerous traps. Collect 10 magical crystals before the island's curses catch you!*

```
┌──────┬──────┬──────┬──────┬──────┐
│  🐉  │  ·   │  ·   │  ·   │  ·   │
├──────┼──────┼──────┼──────┼──────┤
│  ·   │  ·   │  ·   │  ·   │  ·   │
├──────┼──────┼──────┼──────┼──────┤
│  ·   │  ·   │  ·   │  📦  │  ·   │
├──────┼──────┼──────┼──────┼──────┤
│  ·   │  ·   │  ·   │  ·   │  ·   │
├──────┼──────┼──────┼──────┼──────┤
│  ·   │  ·   │  🌋  │  ·   │  ·   │
└──────┴──────┴──────┴──────┴──────┘

  Score: 0/10
```

---

## Features

- **WASD Movement** — Navigate a 5x5 grid using `W` (up), `A` (left), `S` (down), `D` (right)
- **Collectible System** — Pick up `📦` items scattered across the grid to increase your score
- **Hazard Tiles** — Avoid `🌋` volcano tiles or face an immediate game over
- **Win Condition** — Collect 10 crystals to escape the island as a legendary Treasure Hunter
- **Lose Condition** — Step on a volcano and the island's guardian catches you
- **Play Again** — After winning or losing, choose to restart or exit cleanly
- **Boundary Protection** — Movement is clamped to the grid; you can't walk off the edge
- **Box-Drawn Grid** — Clean Unicode borders with visible dot markers on empty cells

---

## How to Run

### Launch the Game

```bash
python game.py
```

### Run the Tests

```bash
pytest test_game.py -v
```

All 34 tests cover grid rendering, movement, spawning logic, collection, and boundary checks.

---

## What I Learned

### Iterative Development

This game wasn't built in one shot. It started as a bare 5x5 grid with a blinking cursor, and grew feature by feature — movement, collectibles, hazards, scoring, win/lose conditions, play-again loops, and finally a visual theme. Each step built on a working foundation, which made it easy to spot and fix issues early.

### Engineering Prompts to Prevent Regression

Every time a new feature was added, the existing tests were re-run to make sure nothing broke. When the grid switched from ASCII symbols (`@`, `*`, `X`) to emojis (`🐉`, `📦`, `🌋`), three tests failed immediately because the rendering changed. That's exactly the point — the tests caught the regression before it shipped. Writing clear, specific test cases upfront makes this kind of safety net possible.

### Automated Testing with pytest

Writing 34 automated tests taught me how to isolate logic from presentation. Functions like `process_move()`, `spawn_collectible()`, and `collect_item()` were designed to be testable — they take inputs and return outputs with no side effects. Meanwhile, `draw_grid()` was tested by capturing stdout. This separation made it straightforward to swap the entire visual theme without rewriting a single test for the game logic.

---

## Project Structure

```
ai-terminal-game/
├── game.py          # Main game — grid rendering, movement, spawning, game loop
├── test_game.py     # 34 pytest tests covering all game functions
└── README.md        # This file
```

---

## Built With

- **Python 3.11** — No external dependencies, just the standard library
- **pytest** — For automated testing

---

## License

This project was built as a learning exercise. Use it however you like.

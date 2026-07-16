import os
import random

# ============================================
# Treasure Hunter Quest
# ============================================

# --- Constants ---
GRID_SIZE = 5
WIN_SCORE = 10

# --- Theme ---
GAME_NAME = "Treasure Hunter Quest"
STORY_INTRO = (
    "An ancient island is filled with hidden gems and dangerous traps. "
    "Collect 10 magical crystals before the island's curses catch you!"
)
PLAYER = "\U0001F409"        # 🐉
COLLECTIBLE = "\U0001F4E6"   # 📦
HAZARD = "\U0001F30B"        # 🌋
WIN_MESSAGE = (
    "You collected all 10 magical crystals and escaped the island "
    "as a legendary Treasure Hunter!"
)
LOSE_MESSAGE = (
    "The island's guardian caught you. Your treasure hunt has come to an end!"
)


def draw_grid(
    row: int,
    col: int,
    item_row: int,
    item_col: int,
    hazard_row: int,
    hazard_col: int,
    score: int,
) -> None:
    """Draw the grid with the player, collectible, and hazard on it.

    Uses themed emojis for each entity on the grid.
    """
    for r in range(GRID_SIZE):
        cells = []
        for c in range(GRID_SIZE):
            if r == row and c == col:
                cells.append(PLAYER)
            elif r == item_row and c == item_col:
                cells.append(COLLECTIBLE)
            elif r == hazard_row and c == hazard_col:
                cells.append(HAZARD)
            else:
                cells.append("  ")  # two spaces for empty cell
        print(" ".join(cells))

    # Show the score below the grid
    print(f"\nScore: {score}/{WIN_SCORE}")


def process_move(row: int, col: int, command: str) -> tuple[int, int]:
    """Process a WASD movement command and return the new position.

    Returns the new (row, col) if the move is valid.
    Returns the same (row, col) if the move would go out of bounds.
    """
    if command == "w" and row > 0:
        row -= 1
    elif command == "s" and row < GRID_SIZE - 1:
        row += 1
    elif command == "a" and col > 0:
        col -= 1
    elif command == "d" and col < GRID_SIZE - 1:
        col += 1
    return row, col


def spawn_collectible(player_row: int, player_col: int) -> tuple[int, int]:
    """Pick a random grid position that is not the player's position."""
    while True:
        row = random.randint(0, GRID_SIZE - 1)
        col = random.randint(0, GRID_SIZE - 1)
        if row != player_row or col != player_col:
            return row, col


def spawn_hazard(
    player_row: int, player_col: int, item_row: int, item_col: int
) -> tuple[int, int]:
    """Pick a random grid position that is not the player or the collectible."""
    while True:
        row = random.randint(0, GRID_SIZE - 1)
        col = random.randint(0, GRID_SIZE - 1)
        if (row, col) != (player_row, player_col) and (row, col) != (item_row, item_col):
            return row, col


def collect_item(
    player_row: int,
    player_col: int,
    item_row: int,
    item_col: int,
    score: int,
) -> tuple[int, int, int]:
    """Check if the player is on the collectible.

    If yes, increase the score and return the new score along with a
    flag (1) so the caller knows to respawn the item.
    """
    if player_row == item_row and player_col == item_col:
        return score + 1, 1, 1
    return score, 0, 0


# --- Main Game Loop ---
if __name__ == "__main__":
    print(f"=== {GAME_NAME} ===\n")
    print(f"{STORY_INTRO}\n")
    print(f"You are the {PLAYER} symbol. Collect the {COLLECTIBLE} items!")
    print("WASD to move. Type 'quit' to exit.\n")

    playing = True

    while playing:
        # Reset all game state for a new round
        player_row = 0
        player_col = 0
        score = 0
        item_row, item_col = spawn_collectible(player_row, player_col)
        hazard_row, hazard_col = spawn_hazard(
            player_row, player_col, item_row, item_col
        )

        game_over = False

        while not game_over:
            # 1. Clear the screen so we get a clean redraw each turn
            os.system("clear")

            # 2. Draw the current state of the grid
            draw_grid(
                player_row, player_col,
                item_row, item_col,
                hazard_row, hazard_col,
                score,
            )

            # 3. Wait for the player to type something
            user_input = input("\n> ").strip().lower()

            # 4. Check if the player wants to quit
            if user_input == "quit":
                playing = False
                game_over = True
                break

            # 5. Process WASD movement with boundary checking
            player_row, player_col = process_move(
                player_row, player_col, user_input
            )

            # 6. Check if the player hit the hazard
            if player_row == hazard_row and player_col == hazard_col:
                os.system("clear")
                draw_grid(
                    player_row, player_col,
                    item_row, item_col,
                    hazard_row, hazard_col,
                    score,
                )
                print(f"\n{LOSE_MESSAGE}")
                game_over = True
                break

            # 7. Check if the player collected the item
            score, collected, _ = collect_item(
                player_row, player_col, item_row, item_col, score
            )
            if collected:
                item_row, item_col = spawn_collectible(
                    player_row, player_col
                )

            # 8. Check win condition
            if score >= WIN_SCORE:
                os.system("clear")
                draw_grid(
                    player_row, player_col,
                    item_row, item_col,
                    hazard_row, hazard_col,
                    score,
                )
                print(f"\n{WIN_MESSAGE}")
                game_over = True
                break

        # After win/loss — prompt to play again
        if playing:
            answer = input("\nPlay again? (y/n) ").strip().lower()
            if answer != "y":
                playing = False

    print("Thanks for playing!")

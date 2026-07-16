import os

# ============================================
# Terminal Game - Basic 5x5 Grid
# ============================================

# --- Constants ---
GRID_SIZE = 5

# --- Game State ---
# The player starts at the top-left corner (row 0, column 0)
player_row = 0
player_col = 0


def draw_grid(row: int, col: int) -> None:
    """Draw the grid with the player on it.

    This function loops through every cell in the grid.
    If the current cell matches the player's position, we draw '@'.
    Otherwise, we draw '.' to represent an empty space.
    """
    for r in range(GRID_SIZE):
        # Build one row at a time as a string
        line = ""
        for c in range(GRID_SIZE):
            if r == row and c == col:
                line += " @"
            else:
                line += " ."
        # Print the finished row, then clear the line buffer so
        # the next print starts fresh (no trailing whitespace)
        print(line.rstrip())


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


# --- Main Game Loop ---
if __name__ == "__main__":
    print("Welcome to the Grid Game!")
    print("You are the '@' symbol.")
    print("WASD to move. Type 'quit' to exit.\n")

    while True:
        # 1. Clear the screen so we get a clean redraw each turn
        os.system("clear")

        # 2. Draw the current state of the grid
        draw_grid(player_row, player_col)

        # 3. Wait for the player to type something
        user_input = input("\n> ").strip().lower()

        # 4. Check if the player wants to quit
        if user_input == "quit":
            print("Thanks for playing!")
            break

        # 5. Process WASD movement with boundary checking
        player_row, player_col = process_move(player_row, player_col, user_input)

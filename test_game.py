import io
import sys

from game import draw_grid, process_move, GRID_SIZE


# ============================================
# Tests for draw_grid()
# ============================================

def test_grid_size() -> None:
    """The grid should be GRID_SIZE rows tall."""
    captured = io.StringIO()
    sys.stdout = captured
    draw_grid(0, 0)
    sys.stdout = sys.__stdout__

    lines = captured.getvalue().strip().split("\n")
    assert len(lines) == GRID_SIZE


def test_player_at_origin() -> None:
    """Player at (0,0) should appear in the top-left cell."""
    captured = io.StringIO()
    sys.stdout = captured
    draw_grid(0, 0)
    sys.stdout = sys.__stdout__

    lines = captured.getvalue().splitlines()
    # The first line should contain the player in the first cell
    cells = lines[0].split()
    assert cells[0] == "@"
    # All other lines should NOT contain the player
    for line in lines[1:]:
        assert "@" not in line


def test_player_at_bottom_right() -> None:
    """Player at (4,4) should appear in the bottom-right cell."""
    captured = io.StringIO()
    sys.stdout = captured
    draw_grid(4, 4)
    sys.stdout = sys.__stdout__

    lines = captured.getvalue().strip().split("\n")
    # The last line should end with " @"
    assert lines[-1].rstrip().endswith("@")
    # All other lines should not contain "@"
    for line in lines[:-1]:
        assert "@" not in line


def test_player_in_middle() -> None:
    """Player at (2,2) should appear in the exact centre."""
    captured = io.StringIO()
    sys.stdout = captured
    draw_grid(2, 2)
    sys.stdout = sys.__stdout__

    lines = captured.getvalue().strip().split("\n")
    middle_line = lines[2]
    # The '@' should be in the third position (index 2)
    cells = middle_line.split()
    assert cells[2] == "@"


def test_each_row_has_five_cells() -> None:
    """Every row should have exactly 5 cells separated by spaces."""
    captured = io.StringIO()
    sys.stdout = captured
    draw_grid(1, 3)
    sys.stdout = sys.__stdout__

    lines = captured.getvalue().strip().split("\n")
    for line in lines:
        cells = line.split()
        assert len(cells) == GRID_SIZE


def test_only_one_player_symbol() -> None:
    """There should be exactly one '@' on the entire grid."""
    captured = io.StringIO()
    sys.stdout = captured
    draw_grid(2, 3)
    sys.stdout = sys.__stdout__

    full_output = captured.getvalue()
    assert full_output.count("@") == 1


# ============================================
# Tests for process_move()
# ============================================

def test_move_right() -> None:
    """D should increase the column by 1."""
    row, col = process_move(0, 0, "d")
    assert (row, col) == (0, 1)


def test_move_left() -> None:
    """A should decrease the column by 1."""
    row, col = process_move(0, 2, "a")
    assert (row, col) == (0, 1)


def test_move_down() -> None:
    """S should increase the row by 1."""
    row, col = process_move(0, 0, "s")
    assert (row, col) == (1, 0)


def test_move_up() -> None:
    """W should decrease the row by 1."""
    row, col = process_move(2, 0, "w")
    assert (row, col) == (1, 0)


def test_boundary_top() -> None:
    """Moving W at row 0 should stay at row 0."""
    row, col = process_move(0, 2, "w")
    assert (row, col) == (0, 2)


def test_boundary_bottom() -> None:
    """Moving S at the last row should stay put."""
    last = GRID_SIZE - 1
    row, col = process_move(last, 2, "s")
    assert (row, col) == (last, 2)


def test_boundary_left() -> None:
    """Moving A at column 0 should stay at column 0."""
    row, col = process_move(2, 0, "a")
    assert (row, col) == (2, 0)


def test_boundary_right() -> None:
    """Moving D at the last column should stay put."""
    last = GRID_SIZE - 1
    row, col = process_move(2, last, "d")
    assert (row, col) == (2, last)


def test_invalid_key_does_nothing() -> None:
    """An unknown key should leave the position unchanged."""
    row, col = process_move(2, 2, "x")
    assert (row, col) == (2, 2)


def test_empty_input_does_nothing() -> None:
    """An empty string should leave the position unchanged."""
    row, col = process_move(2, 2, "")
    assert (row, col) == (2, 2)

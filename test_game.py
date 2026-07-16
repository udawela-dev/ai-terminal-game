import io
import sys

from game import (
    draw_grid,
    process_move,
    spawn_collectible,
    spawn_hazard,
    collect_item,
    GRID_SIZE,
    WIN_SCORE,
    PLAYER,
    COLLECTIBLE,
    HAZARD,
)


# ============================================
# Tests for draw_grid()
# ============================================

def test_grid_has_borders() -> None:
    """The grid should have top, middle, and bottom borders."""
    captured = io.StringIO()
    sys.stdout = captured
    draw_grid(0, 0, 3, 3, 4, 4, 0)
    sys.stdout = sys.__stdout__

    full_output = captured.getvalue()
    # Should have top border, separators, and bottom border
    assert "┌" in full_output  # top-left corner
    assert "└" in full_output  # bottom-left corner
    assert "├" in full_output  # row separator
    assert "┼" in full_output  # inner junction


def test_player_at_origin() -> None:
    """Player at (0,0) should appear in the top-left cell."""
    captured = io.StringIO()
    sys.stdout = captured
    draw_grid(0, 0, 3, 3, 4, 4, 0)
    sys.stdout = sys.__stdout__

    lines = captured.getvalue().splitlines()
    # First data row (index 1, after top border) should have player
    assert PLAYER in lines[1]
    # Player should NOT appear in other data rows
    for line in lines[2:GRID_SIZE * 2]:
        if "│" in line:  # only check data rows
            if line != lines[1]:
                assert PLAYER not in line


def test_player_at_bottom_right() -> None:
    """Player at (4,4) should appear in the bottom-right cell."""
    captured = io.StringIO()
    sys.stdout = captured
    draw_grid(4, 4, 0, 0, 2, 2, 0)
    sys.stdout = sys.__stdout__

    lines = captured.getvalue().splitlines()
    # Last data row (index -3, before bottom border and score) should have player
    data_rows = [l for l in lines if "│" in l]
    assert PLAYER in data_rows[-1]
    # All other data rows should not contain player
    for row in data_rows[:-1]:
        assert PLAYER not in row


def test_player_in_middle() -> None:
    """Player at (2,2) should appear in the exact centre."""
    captured = io.StringIO()
    sys.stdout = captured
    draw_grid(2, 2, 0, 0, 4, 4, 0)
    sys.stdout = sys.__stdout__

    lines = captured.getvalue().splitlines()
    data_rows = [l for l in lines if "│" in l]
    # Player should be in the middle data row
    assert PLAYER in data_rows[2]
    # Player should NOT appear in other data rows
    assert PLAYER not in data_rows[0]
    assert PLAYER not in data_rows[1]


def test_empty_cells_have_dots() -> None:
    """Empty cells should display a visible dot marker."""
    captured = io.StringIO()
    sys.stdout = captured
    draw_grid(0, 0, 4, 4, 3, 3, 0)
    sys.stdout = sys.__stdout__

    full_output = captured.getvalue()
    # Empty cells use the dot character
    assert "·" in full_output


def test_only_one_player_symbol() -> None:
    """There should be exactly one player emoji on the entire grid."""
    captured = io.StringIO()
    sys.stdout = captured
    draw_grid(2, 3, 0, 0, 4, 4, 0)
    sys.stdout = sys.__stdout__

    full_output = captured.getvalue()
    assert full_output.count(PLAYER) == 1


def test_collectible_drawn() -> None:
    """The collectible emoji should appear on the grid."""
    captured = io.StringIO()
    sys.stdout = captured
    draw_grid(0, 0, 2, 2, 4, 4, 0)
    sys.stdout = sys.__stdout__

    full_output = captured.getvalue()
    assert full_output.count(COLLECTIBLE) == 1


def test_hazard_drawn() -> None:
    """The hazard emoji should appear on the grid."""
    captured = io.StringIO()
    sys.stdout = captured
    draw_grid(0, 0, 2, 2, 3, 3, 0)
    sys.stdout = sys.__stdout__

    full_output = captured.getvalue()
    assert full_output.count(HAZARD) == 1


def test_score_displayed() -> None:
    """The score should appear in the output."""
    captured = io.StringIO()
    sys.stdout = captured
    draw_grid(0, 0, 3, 3, 4, 4, 5)
    sys.stdout = sys.__stdout__

    full_output = captured.getvalue()
    assert f"Score: 5/{WIN_SCORE}" in full_output


def test_player_overlaps_collectible() -> None:
    """If player and collectible share a cell, player takes priority."""
    captured = io.StringIO()
    sys.stdout = captured
    draw_grid(2, 2, 2, 2, 0, 0, 0)
    sys.stdout = sys.__stdout__

    full_output = captured.getvalue()
    # Player should be visible
    assert PLAYER in full_output
    # Collectible should NOT appear when overlapping with player
    assert COLLECTIBLE not in full_output


def test_theme_constants_used() -> None:
    """The grid should use the themed emojis, not ASCII symbols."""
    captured = io.StringIO()
    sys.stdout = captured
    draw_grid(1, 1, 3, 3, 0, 0, 0)
    sys.stdout = sys.__stdout__

    full_output = captured.getvalue()
    # Should NOT contain old ASCII symbols
    assert "@" not in full_output
    assert "*" not in full_output
    assert "X" not in full_output
    # Should contain themed emojis
    assert PLAYER in full_output
    assert COLLECTIBLE in full_output
    assert HAZARD in full_output


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


# ============================================
# Tests for spawn_collectible()
# ============================================

def test_spawn_not_on_player() -> None:
    """The collectible should never spawn on the player."""
    for _ in range(50):
        row, col = spawn_collectible(2, 2)
        assert (row, col) != (2, 2)


def test_spawn_within_grid() -> None:
    """The collectible should always be within grid bounds."""
    for _ in range(50):
        row, col = spawn_collectible(0, 0)
        assert 0 <= row < GRID_SIZE
        assert 0 <= col < GRID_SIZE


def test_spawn_at_various_positions() -> None:
    """Spawn should be able to reach different positions over many calls."""
    seen = set()
    for _ in range(200):
        row, col = spawn_collectible(4, 4)
        seen.add((row, col))
    assert len(seen) > 1


# ============================================
# Tests for spawn_hazard()
# ============================================

def test_hazard_not_on_player() -> None:
    """The hazard should never spawn on the player."""
    for _ in range(50):
        row, col = spawn_hazard(2, 2, 0, 0)
        assert (row, col) != (2, 2)


def test_hazard_not_on_collectible() -> None:
    """The hazard should never spawn on the collectible."""
    for _ in range(50):
        row, col = spawn_hazard(0, 0, 3, 3)
        assert (row, col) != (3, 3)


def test_hazard_within_grid() -> None:
    """The hazard should always be within grid bounds."""
    for _ in range(50):
        row, col = spawn_hazard(0, 0, 4, 4)
        assert 0 <= row < GRID_SIZE
        assert 0 <= col < GRID_SIZE


def test_hazard_at_various_positions() -> None:
    """Hazard spawn should reach different positions over many calls."""
    seen = set()
    for _ in range(200):
        row, col = spawn_hazard(0, 0, 4, 4)
        seen.add((row, col))
    assert len(seen) > 1


# ============================================
# Tests for collect_item()
# ============================================

def test_collect_increases_score() -> None:
    """Collecting an item should increase the score by 1."""
    score, collected, _ = collect_item(2, 2, 2, 2, 5)
    assert score == 6
    assert collected == 1


def test_collect_returns_flag() -> None:
    """Collecting should return a collected flag of 1."""
    _, collected, flag = collect_item(2, 2, 2, 2, 0)
    assert collected == 1
    assert flag == 1


def test_no_collect() -> None:
    """Not standing on the item should not change the score."""
    score, collected, _ = collect_item(0, 0, 2, 2, 5)
    assert score == 5
    assert collected == 0


def test_no_collect_returns_zero_flag() -> None:
    """Not collecting should return a flag of 0."""
    _, collected, flag = collect_item(0, 0, 2, 2, 0)
    assert collected == 0
    assert flag == 0


def test_collect_at_origin() -> None:
    """Should collect when player and item are both at (0,0)."""
    score, collected, _ = collect_item(0, 0, 0, 0, 0)
    assert score == 1
    assert collected == 1


def test_collect_at_bottom_right() -> None:
    """Should collect when both are at the bottom-right corner."""
    last = GRID_SIZE - 1
    score, collected, _ = collect_item(last, last, last, last, 9)
    assert score == 10
    assert collected == 1

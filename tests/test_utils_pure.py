import pandas as pd
from unittest.mock import patch
from rich.table import Table

from pandasnoir.utils import check_key, draw_mascot, render, get_colors, rich_df, DOT, BRIGHT, MID


# --- check_key ---

def test_check_key_pk():
    assert check_key("id") == "PK"


def test_check_key_fk():
    assert check_key("person_id") == "FK"
    assert check_key("hotel_id") == "FK"


def test_check_key_none_for_regular_column():
    assert check_key("name") is None
    assert check_key("description") is None


def test_check_key_id_substring_not_pk():
    assert check_key("identity") is None


def test_check_key_id_prefix_not_fk():
    assert check_key("id_number") is None


# --- draw_mascot ---

@patch("os.get_terminal_size")
def test_draw_mascot_large_terminal(mock_size):
    mock_size.return_value = (120, 60)
    assert draw_mascot() is True


@patch("os.get_terminal_size")
def test_draw_mascot_small_terminal(mock_size):
    mock_size.return_value = (60, 20)
    assert draw_mascot() is False


@patch("os.get_terminal_size")
def test_draw_mascot_boundary(mock_size):
    mock_size.return_value = (100, 60)  # 6000 == 6000
    assert draw_mascot() is True


@patch("os.get_terminal_size")
def test_draw_mascot_just_below_boundary(mock_size):
    mock_size.return_value = (99, 60)  # 5940 < 6000
    assert draw_mascot() is False


# --- render ---

def test_render_returns_string():
    result = render("pandas.noir")
    assert isinstance(result, str)


def test_render_has_three_lines():
    result = render("pandas.noir")
    assert result.count("\n") == 2


def test_render_contains_block_chars():
    result = render("a")
    assert any(c in result for c in ("\u2588", "\u2580", "\u2584"))


def test_render_single_char():
    result = render("i")
    assert isinstance(result, str) and len(result) > 0


# --- get_colors ---

def test_get_colors_length_matches_input():
    colors = get_colors("pandas.noir")
    assert len(colors) == len("pandas.noir")


def test_get_colors_returns_tuples():
    colors = get_colors("ab")
    for item in colors:
        assert isinstance(item, tuple) and len(item) == 2


def test_get_colors_dot_gets_dot_color():
    colors = get_colors(".")
    assert colors[0] == (DOT, DOT)


def test_get_colors_first_six_nonperiod_are_bright():
    colors = get_colors("pandas.noir")
    for i in range(6):  # 'p','a','n','d','a','s'
        assert colors[i] == (BRIGHT, MID)


# --- rich_df ---

def test_rich_df_returns_table():
    df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    table = rich_df(df)
    assert isinstance(table, Table)


def test_rich_df_column_count():
    df = pd.DataFrame({"x": [1], "y": [2], "z": [3]})
    table = rich_df(df)
    assert len(table.columns) == 3


def test_rich_df_row_count():
    df = pd.DataFrame({"a": [10, 20, 30]})
    table = rich_df(df)
    assert table.row_count == 3


def test_rich_df_empty_dataframe():
    df = pd.DataFrame({"a": []})
    table = rich_df(df)
    assert table.row_count == 0
    assert len(table.columns) == 1

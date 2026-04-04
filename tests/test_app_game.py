from unittest.mock import patch
from textual.widgets import TextArea, RichLog, Input, TabbedContent

from pandasnoir.app import PandasNoirApp, GameScreen, CasesScreen, SuccessModal


async def navigate_to_game(pilot):
    """From app start, navigate to GameScreen for the first focusable case."""
    await pilot.press("enter")   # Menu -> CasesScreen
    await pilot.press("tab")     # focus a Case (grid order may vary)
    await pilot.press("enter")   # CasesScreen -> GameScreen


async def submit_answer(app, pilot, answer):
    """Switch to Submit Answer tab, enter an answer, and press enter."""
    tabbed = app.screen.query_one(TabbedContent)
    tabbed.active = "submission-pane"
    await pilot.pause()
    input_widget = app.screen.query_one("#submit", Input)
    input_widget.focus()
    await pilot.pause()
    input_widget.value = answer
    await pilot.pause()
    await pilot.press("enter")
    await pilot.pause()


@patch("pandasnoir.app.draw_mascot", return_value=False)
async def test_game_screen_has_five_tabs(_):
    app = PandasNoirApp()
    async with app.run_test(size=(120, 40)) as pilot:
        await navigate_to_game(pilot)
        assert isinstance(app.screen, GameScreen)
        tabbed = app.screen.query_one(TabbedContent)
        assert len(tabbed.query("TabPane")) == 5


@patch("pandasnoir.app.draw_mascot", return_value=False)
async def test_game_workspace_has_editor_and_output(_):
    app = PandasNoirApp()
    async with app.run_test(size=(120, 40)) as pilot:
        await navigate_to_game(pilot)
        assert app.screen.query_one(".workspace-editor", TextArea) is not None
        assert app.screen.query_one(RichLog) is not None


@patch("pandasnoir.app.draw_mascot", return_value=False)
async def test_game_workspace_loads_saved_content(_):
    app = PandasNoirApp()
    async with app.run_test(size=(120, 40)) as pilot:
        await navigate_to_game(pilot)
        editor = app.screen.query_one(".workspace-editor", TextArea)
        assert "import pandas as pd" in editor.text


@patch("pandasnoir.app.draw_mascot", return_value=False)
async def test_game_submit_wrong_answer(_):
    app = PandasNoirApp()
    async with app.run_test(size=(120, 40), notifications=True) as pilot:
        await navigate_to_game(pilot)
        await submit_answer(app, pilot, "Wrong Person")
        assert isinstance(app.screen, GameScreen)


@patch("pandasnoir.app.draw_mascot", return_value=False)
async def test_game_submit_correct_answer_shows_success(_):
    app = PandasNoirApp()
    async with app.run_test(size=(120, 40)) as pilot:
        await navigate_to_game(pilot)
        solution = app.screen.case_info.solution
        await submit_answer(app, pilot, solution)
        assert isinstance(app.screen, SuccessModal)


@patch("pandasnoir.app.draw_mascot", return_value=False)
async def test_game_submit_correct_answer_case_insensitive(_):
    app = PandasNoirApp()
    async with app.run_test(size=(120, 40)) as pilot:
        await navigate_to_game(pilot)
        solution = app.screen.case_info.solution.lower()
        await submit_answer(app, pilot, solution)
        assert isinstance(app.screen, SuccessModal)


@patch("pandasnoir.app.draw_mascot", return_value=False)
async def test_success_modal_dismiss_returns_to_cases(_):
    app = PandasNoirApp()
    async with app.run_test(size=(120, 40)) as pilot:
        await navigate_to_game(pilot)
        solution = app.screen.case_info.solution
        await submit_answer(app, pilot, solution)
        assert isinstance(app.screen, SuccessModal)
        await pilot.press("enter")  # dismiss
        await pilot.pause()
        assert isinstance(app.screen, CasesScreen)


@patch("pandasnoir.app.draw_mascot", return_value=False)
async def test_escape_from_game_returns_to_cases(_):
    app = PandasNoirApp()
    async with app.run_test(size=(120, 40)) as pilot:
        await navigate_to_game(pilot)
        assert isinstance(app.screen, GameScreen)
        await pilot.press("escape")
        assert isinstance(app.screen, CasesScreen)


@patch("pandasnoir.app.draw_mascot", return_value=False)
async def test_game_run_code_no_crash(_):
    app = PandasNoirApp()
    async with app.run_test(size=(120, 40)) as pilot:
        await navigate_to_game(pilot)
        tabbed = app.screen.query_one(TabbedContent)
        tabbed.active = "workspace"
        await pilot.pause()
        editor = app.screen.query_one(".workspace-editor", TextArea)
        editor.text = "1 + 1"
        await pilot.press("ctrl+r")
        await pilot.pause()
        assert isinstance(app.screen, GameScreen)


@patch("pandasnoir.app.draw_mascot", return_value=False)
async def test_game_run_code_syntax_error_no_crash(_):
    app = PandasNoirApp()
    async with app.run_test(size=(120, 40)) as pilot:
        await navigate_to_game(pilot)
        tabbed = app.screen.query_one(TabbedContent)
        tabbed.active = "workspace"
        await pilot.pause()
        editor = app.screen.query_one(".workspace-editor", TextArea)
        editor.text = "def foo(:"
        await pilot.press("ctrl+r")
        await pilot.pause()
        assert isinstance(app.screen, GameScreen)

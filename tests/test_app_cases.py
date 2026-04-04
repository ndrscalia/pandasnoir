from unittest.mock import patch
from pandasnoir.app import PandasNoirApp, CasesScreen, Case, GameScreen


@patch("pandasnoir.app.draw_mascot", return_value=False)
async def test_cases_screen_shows_six_cases(_):
    app = PandasNoirApp()
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("enter")  # Menu -> CasesScreen
        cases = app.screen.query(Case)
        assert len(cases) == 6


@patch("pandasnoir.app.draw_mascot", return_value=False)
async def test_cases_screen_tab_focuses_case(_):
    app = PandasNoirApp()
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("enter")
        await pilot.press("tab")
        assert isinstance(app.screen.focused, Case)


@patch("pandasnoir.app.draw_mascot", return_value=False)
async def test_cases_enter_pushes_game_screen(_):
    app = PandasNoirApp()
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("enter")   # -> CasesScreen
        await pilot.press("tab")     # focus first Case
        await pilot.press("enter")   # -> GameScreen
        assert isinstance(app.screen, GameScreen)


@patch("pandasnoir.app.draw_mascot", return_value=False)
async def test_solved_case_shows_checkmark(_):
    from pandasnoir._cases_data import CASES
    CASES[0].solved = True
    app = PandasNoirApp()
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("enter")
        await pilot.press("tab")
        case_widget = app.screen.query(Case).first()
        title_label = case_widget.query_one("#title")
        assert "\u2714" in str(title_label.content)


@patch("pandasnoir.app.draw_mascot", return_value=False)
async def test_escape_from_cases_returns_to_menu(_):
    from pandasnoir.app import MenuScreen
    app = PandasNoirApp()
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("enter")
        assert isinstance(app.screen, CasesScreen)
        await pilot.press("escape")
        assert isinstance(app.screen, MenuScreen)

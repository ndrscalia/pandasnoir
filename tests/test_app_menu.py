from unittest.mock import patch
from textual.widgets import Footer

from pandasnoir.app import PandasNoirApp, MenuScreen, CasesScreen, AboutScreen


@patch("pandasnoir.app.draw_mascot", return_value=False)
async def test_app_starts_on_menu_screen(_):
    app = PandasNoirApp()
    async with app.run_test(size=(120, 40)) as pilot:
        assert isinstance(app.screen, MenuScreen)


@patch("pandasnoir.app.draw_mascot", return_value=False)
async def test_menu_has_three_items(_):
    app = PandasNoirApp()
    async with app.run_test(size=(120, 40)) as pilot:
        items = app.screen.query(".menu-item")
        assert len(items) == 3


@patch("pandasnoir.app.draw_mascot", return_value=False)
async def test_menu_initial_selection_is_zero(_):
    app = PandasNoirApp()
    async with app.run_test(size=(120, 40)) as pilot:
        assert app.screen.selected == 0


@patch("pandasnoir.app.draw_mascot", return_value=False)
async def test_menu_navigation_down(_):
    app = PandasNoirApp()
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("j")
        assert app.screen.selected == 1
        await pilot.press("down")
        assert app.screen.selected == 2


@patch("pandasnoir.app.draw_mascot", return_value=False)
async def test_menu_navigation_wraps(_):
    app = PandasNoirApp()
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("k")  # wrap from 0 to 2
        assert app.screen.selected == 2


@patch("pandasnoir.app.draw_mascot", return_value=False)
async def test_menu_enter_view_cases_pushes_cases_screen(_):
    app = PandasNoirApp()
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("enter")
        assert isinstance(app.screen, CasesScreen)


@patch("pandasnoir.app.draw_mascot", return_value=False)
async def test_menu_enter_about_pushes_about_screen(_):
    app = PandasNoirApp()
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("j")
        await pilot.press("enter")
        assert isinstance(app.screen, AboutScreen)


@patch("pandasnoir.app.draw_mascot", return_value=False)
async def test_escape_from_cases_returns_to_menu(_):
    app = PandasNoirApp()
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("enter")  # -> CasesScreen
        assert isinstance(app.screen, CasesScreen)
        await pilot.press("escape")
        assert isinstance(app.screen, MenuScreen)


@patch("pandasnoir.app.draw_mascot", return_value=False)
async def test_menu_has_footer(_):
    app = PandasNoirApp()
    async with app.run_test(size=(120, 40)) as pilot:
        footer = app.screen.query(Footer)
        assert len(footer) == 1

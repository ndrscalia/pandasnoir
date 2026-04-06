from pathlib import Path

import pandas as pd
import webbrowser

from textual.app import App, ComposeResult
from textual.screen import ModalScreen, Screen
from textual.widgets import RichLog, Static, Footer, Label, Markdown, TabPane, TabbedContent, TextArea, Input
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, ItemGrid, VerticalScroll, Center
from textual.reactive import reactive

from rich.text import Text

from .utils import draw_mascot, render, rich_df, update_progress, check_progress, Schema, populate_saves, SAVES_DIR
from .mascot import Mascot
from ._cases_data import CaseInfo, CASES

banner = Text.from_ansi(render("pandas.noir"))

CASES_MD = """\
# Cases Files
"""

class PandasNoirApp(App):


    BINDINGS = [
            Binding("escape", "go_back", "Back"),
            Binding("q", "quit", "Quit"),
            Binding(
                "ctrl+a",
                "app.maximize",
                "Maximize",
                tooltip="Maximize the focused widget (if possible)",
            ),
        ]

    def action_maximize(self) -> None:
        if getattr(self.screen, "ALLOW_MAXIMIZE", True) is False:
            return
        if self.screen.is_maximized:
            return
        if self.screen.focused is None:
            self.notify(
                "Nothing to be maximized (try pressing [b]tab[/b])",
                title="Maximize",
                severity="warning",
            )
        else:
            if self.screen.maximize(self.screen.focused):
                self.notify(
                    "You are now in the maximized view. Press [b]escape[/b] to return.",
                    title="Maximize",
                )
            else:
                self.notify(
                    "This widget may not be maximized.",
                    title="Maximize",
                    severity="warning",
                )

    def action_go_back(self):
        if len(self.app.screen_stack) > 1:
            if isinstance(self.screen, GameScreen):
                self.screen.save_data()
            self.screen.dismiss()
            
    def on_mount(self):
        populate_saves()
        self.push_screen(MenuScreen())

    async def action_quit(self) -> None:
        if isinstance(self.screen, GameScreen):
            self.screen.save_data()
            await super().action_quit()
        else:
            await super().action_quit()

class MenuScreen(Screen):

    CSS = """
    Screen {
        align: center middle;
    }

    #menu {
        align: center middle;
    }

    #menu .header{
        margin: 0 0 2 0;
    }

    #credits {
        dock: bottom;
        text-align: center;
        width: 100%;
        color: $text-muted;
        margin-bottom: 3;
    }

    #copyright {
        dock: bottom;
        text-align: center;
        width: 100%;
        color: $text-muted;
        margin-bottom: 1;
    }

    Static {
        text-align: center;
        width: 100%;
    }

    Mascot {
    layer: overlay;
    position: absolute;
    offset: -3 -3;
    width: auto;
    height: auto;
    }
    """

    selected = reactive(0)

    BINDINGS = [
            Binding("up,k", "move_up", "Up"),
            Binding("down,j", "move_down", "Down"),
            Binding("enter", "select", "Select"),
            ]

    MENU_ITEMS = [
            "View Cases",
            "About",
            "Leave a star"
            ]

    def compose(self) -> ComposeResult:
        with Vertical(id="menu"):
            yield Static(banner, classes="header")
            for label in self.MENU_ITEMS:
                yield Static(label, classes="menu-item")
            yield Static("Inspired by sqlnoir.com", id="credits")
            yield Static("Copyright (c) 2026 Andrea Scalia", id ="copyright")
        if draw_mascot():
            yield Mascot(Path(__file__).parent/"assets/body.png", sizes=(47,13), title="Body", id="mascot-left")
            yield Mascot(Path(__file__).parent/"assets/detective_2.png", sizes=(20,32), title="Detective", id="mascot-right")
        yield Footer()

    def watch_selected(self, new_value: int):
        items = list(self.query(".menu-item").results(Static))
        for i, item in enumerate(items):
            if i == new_value:
                item.update(f"▸ {self.MENU_ITEMS[i]}")
            else:
                item.update(f"  {self.MENU_ITEMS[i]}")

    def action_move_down(self):
        items = list(self.query(".menu-item").results(Static))
        self.selected = (self.selected +1) % len(items)

    def action_move_up(self):
        items = list(self.query(".menu-item").results(Static))
        self.selected = (self.selected -1) % len(items)

    def action_select(self):
        label = self.MENU_ITEMS[self.selected]
        if label == "View Cases":
            self.app.push_screen(CasesScreen())
        if label == "About":
            self.app.push_screen(AboutScreen())
        if label == "Leave a star":
            webbrowser.open("https://github.com/ndrscalia/pandasnoir", new=1)

    def on_mount(self):
        self.watch_selected(self.selected)
        mascots = self.query(Mascot)
        for mascot in mascots:
            if mascot.id == "mascot-right":
                mascot.styles.offset = (
                        self.size.width - 50,
                        self.size.height - 25,
                        )
            elif mascot.id == "mascot-left":
                mascot.styles.offset = (
                        10,
                        self.size.height - 17,
                        )

class AboutScreen(Screen):

    def compose(self):

        with open(Path(__file__).parent/"ABOUT.md", "r") as f:
            text = f.read()
            yield Markdown(text)
        yield Footer()

class Case(Vertical, can_focus=True, can_focus_children=False):

    ALLOW_MAXIMIZE = True
    DEFAULT_CSS = """
    Case {
        width: auto;
        height: auto;
        padding: 0 1;
        border: tall transparent;
        box-sizing: border-box;
        &:focus {
            border: tall $text-primary;
            background: $primary 20%;
            }
        & #title { text-style: bold; width: 1fr; }
        & .header { height: auto; }
        & .description { color: $text-muted; }
        &.-hover { opacity: 1; }
    }
    """

    def __init__(self, case_info: CaseInfo) -> None:
        self.case_info = case_info
        super().__init__()

    def compose(self):
        info = self.case_info
        with Horizontal(classes="header"):
            if info.solved:
                yield Label(f"{info.title} [green]\u2714[/green]", id="title")
            else:
                yield Label(info.title, id="title")
        yield Label(f"Level: {info.level}", id="level")
        yield Static(info.description, classes="description")


class CasesScreen(Screen):

    AUTO_FOCUS = None
    CSS = """
    Screen {
        width: 100%;
        height: auto;
        overflow-y: auto;
        }

    CasesScreen {
        align-horizontal: center;
        ItemGrid {
            margin: 2 4;
            padding: 1 2;
            background: $boost;
            width: 1fr;
            height: auto;
            grid-gutter: 1 1;
            grid-rows: auto;
            keyline:thin $foreground 30%;
        }
        Markdown {
            margin: 0;
            padding: 0 2;
            max-width: 100;
            background: transparent;
        }
    }
    """

    BINDINGS = [
            Binding("enter", "select", "Select"),
            ]
    
    def compose(self) -> ComposeResult:
        with VerticalScroll() as container:
            container.can_focus = False
            with Center():
                yield Markdown(CASES_MD)
            with ItemGrid(min_column_width=40, stretch_height=True, regular=True):
                for case in CASES:
                    yield Case(case)
        yield Footer()


    def action_select(self):
        if isinstance(self.screen.focused, Case):
            self.app.push_screen(GameScreen(
                                        case_info=self.screen.focused.case_info,
                                        saves_path=Path(f"{SAVES_DIR}/case_{self.screen.focused.case_info.case_id}")
                                 ))

    def on_mount(self):
        check_progress()
        self.notify("Press Tab to cycle through cases.")

    def on_screen_resume(self):
        check_progress()
        for case_widget in self.query(Case):
            title_label = case_widget.query_one("#title", Label)
            if case_widget.case_info.solved:
                title_label.update(f"{case_widget.case_info.title} [green]\u2714[/green]")

class GameScreen(Screen):

    ALLOW_MAXIMIZE = False
    DEFAULT_CSS = """
    TextArea { height: 1fr; border: round $secondary; border-title-align: center; }
    RichLog { height: 1fr; border: round $accent; border-title-align: center; }

    #schema {
        align-horizontal: center;
        ItemGrid {
            margin: 2 4;
            padding: 1 2;
            background: $background;
            width: 1fr;
            height: auto;
            grid-gutter: 1 1;
            grid-rows: auto;
            keyline: none;
        }
    }

    #schema Static {
        content-align: center middle;
        border: tab $primary;
        border-title-align: center;
    }
    
    #submission-pane {
        align: center middle;
        height: 1fr;
    }

    #submission-box {
        width: 50;
        height: auto;
        padding: 1 2;
        background: $panel;
        border: tall $secondary;
    }

    #submission-box Static {
        text-align: center;
        margin: 0 0 1 0;
        color: $text;
            }
    """

    BINDINGS = [
      #Binding("escape", "go_back", "Back", priority=True),
      Binding("ctrl+r", "run_code", "Run", priority=True),
      #Binding("ctrl+o", "show_tab('case')", "Case Overview", priority=True),
      #Binding("ctrl+g", "show_tab('workspace')", "Workspace", priority=True),
      #Binding("ctrl+n", "show_tab('notes')", "Notes", priority=True),
      #Binding("ctrl+s", "show_tab('schema')", "Schema", priority=True),
      ]

    def __init__(self, case_info: CaseInfo, saves_path: Path) -> None:
        self.case_info = case_info
        self.saves_path = saves_path
        super().__init__()

    def save_data(self):
        for save_type in ["workspace", "notes"]:
            with open(f"{self.saves_path}/{save_type}.txt", "w") as save:
                save.write(self.query_one(f".{save_type}-editor", TextArea).text)

    def compose(self) -> ComposeResult:

        with TabbedContent(initial="case"):

            with TabPane("Case Overview", id="case"):
                files_path = Path(__file__).parent/"cases_docs"

                with open(f"{files_path}/case_{self.case_info.case_id}.md") as f:
                    content = f.read()

                    bullet_points = "\n".join(f"- {obj}" for obj in self.case_info.objectives)

                    result = content.format(
                            title=self.case_info.title,
                            instructions=self.case_info.instructions,
                            objectives=bullet_points
                            )
                if result:
                    yield Markdown(result)

            with TabPane("Workspace", id="workspace"):

                source = TextArea(
                        language="python",
                        theme="css",
                        show_line_numbers=True,
                        id="source",
                        tab_behavior="focus",
                        classes="workspace-editor"
                        )
                source.border_title = "Code"
                source.border_subtitle = "ctrl+r to run"
                log = RichLog(id="output")
                log.border_title = "Output"
                yield source
                yield log

            with TabPane("Notes", id="notes"):
                yield TextArea(placeholder="Write your notes here...", classes="notes-editor")

            with TabPane("Schema", id="schema"):
                with VerticalScroll() as container:
                    container.can_focus = False
                    with ItemGrid(min_column_width=40, stretch_height=True, regular=True):
                        text_color = self.app.current_theme.foreground
                        border_color = self.app.current_theme.primary
                        case_schema = Schema(self.case_info.case_id, text_style=str(text_color), border_style=str(border_color))

                        for table in case_schema.draw_tables():
                            static = Static(table)
                            static.border_title = str(table.dataset_name)
                            yield static

            with TabPane("Submit Answer", id="submission-pane"):
                yield Vertical(
                        Static("Who committed the crime?"),
                        Input(placeholder="Type your answer and press enter...", id="submit"),
                        id="submission-box"
                        )
        yield Footer()

    def on_success(self, _):
        self.save_data()
        self.dismiss()

    def on_input_submitted(self, event: Input.Submitted):
        answer = event.value
        if answer.lower() == self.case_info.solution.lower():
            update_progress(self.case_info.case_id)
            self.app.push_screen(SuccessModal(), callback=self.on_success)
        else:
            self.notify("Wrong! Keep investigating", severity="error")

    def action_show_tab(self, tab: str) -> None:
        self.get_child_by_type(TabbedContent).active = tab

    def on_mount(self):
        self.namespace = {}
        self.notify(
                "Use [b]tab[/b] to switch focus, [b]arrow keys[/b] to cycle through tabs while focused on tabs' labels, and [b]enter[/b] to select the highlighted tab.",
                timeout=10.0
                )
        
        for save in self.saves_path.iterdir():
            if save.name.startswith("workspace"):
                workspace_saved_content = save.read_text()
                self.query_one(".workspace-editor", TextArea).text = workspace_saved_content
            if save.name.startswith("notes"):
                notes_saved_content = save.read_text()
                self.query_one(".notes-editor", TextArea).text = notes_saved_content

    def action_run_code(self):
      source = self.query_one(".workspace-editor", TextArea).text
      log = self.query_one(RichLog)
      log.clear()

      import io, sys

      capture = io.StringIO()
      old_stdout, old_stderr = sys.stdout, sys.stderr
      sys.stdout = sys.stderr = capture
      try:
          lines = source.strip().splitlines()
          if len(lines) > 1:
              exec("\n".join(lines[:-1]), self.namespace)
          last = lines[-1] if lines else ""
          try:
              result = eval(last, self.namespace)
              if result is not None:
                  if isinstance(result, pd.DataFrame):
                      log.write(rich_df(result))
                  else:   
                      print(repr(result))
          except SyntaxError:
              exec(last, self.namespace)
      except Exception:
          import traceback
          traceback.print_exc()
      finally:
          sys.stdout, sys.stderr = old_stdout, old_stderr

      output = capture.getvalue()
      if output:
          log.write(output)

class SuccessModal(ModalScreen):

    DEFAULT_CSS = """

    SuccessModal {
        align: center middle;
        height: 1fr;
    }

    #success_popup {
        width: 50;
        height: auto;
        min-height: 9;
        padding: 1 2;
        background: $panel;
        border: tall $secondary;
    }

    #success_popup Static {
        text-align: center;
        margin: 0 0 1 0;
        color: $text;
            }

    """

    BINDINGS = [
            Binding("enter", "back_to_cases")
            ]

    def compose(self) -> ComposeResult:
        yield Vertical(
            Static("[green][bold]Correct![/bold][/green]\nYou solved the case!\nPress [bold]ENTER[/bold] to go back to cases."),
            id="success_popup"
            )

    def action_back_to_cases(self):
        self.dismiss(True)

def main():
    app = PandasNoirApp()
    app.run()

if __name__ == "__main__":
    main()

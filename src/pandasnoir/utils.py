import os
import json
import pandas as pd
from ._cases_data import CASES
from rich.table import Table
from rich import box
from pathlib import Path

USER_DIR = Path.home() / ".pandasnoir"
SAVES_DIR = USER_DIR / "saves"
PROGRESS = USER_DIR / "saves" / "progress.json"


def draw_mascot():

    cols, rows = os.get_terminal_size()

    surface = cols * rows

    if surface < 6000:
        return False
    else:
        return True


def populate_saves():
    SAVES_DIR.mkdir(parents=True, exist_ok=True)

    if not PROGRESS.exists():
        PROGRESS.write_text('{"solved": []}')

    for case in CASES:
        for file_type in ["workspace", "notes"]:
            path = Path(f"{SAVES_DIR}/case_{case.case_id}/{file_type}.txt")

            if path.exists():
                continue
            else:
                path.parent.mkdir(parents=True, exist_ok=True)

                if file_type == "workspace":
                    csv_dir = Path(__file__).parent / "cases" / f"case_{case.case_id}"
                    lines = [
                        f"{name.split('.')[0]} = pd.read_csv(r'{csv_dir / name}')"
                        for name in case.datasets
                    ]
                    content = "import pandas as pd\n\n" + "\n".join(lines) + "\n\n"

                    path.write_text(content)

                if file_type == "notes":
                    path.touch()


class Schema:
    def __init__(self, case_id: int, text_style: str, border_style: str):
        self.case_id = case_id
        self.text_style = text_style
        self.border_style = border_style
        self.datasets = {}

        DATA_PATH = Path(__file__).parent / "cases" / f"case_{self.case_id}"

        for dataset in DATA_PATH.iterdir():
            if dataset.name.endswith(".csv"):
                self.datasets[dataset.name] = pd.read_csv(f"{DATA_PATH}/{dataset.name}")

    def draw_tables(self):

        tables = []

        for k, v in self.datasets.items():
            df_name = k.split(".")[0]
            df_cols = v.columns

            table = Table(
                title_style="bold", box=box.ROUNDED, border_style=self.border_style
            )
            table.dataset_name = df_name
            table.add_column("column", style=self.text_style, justify="left")
            table.add_column("type", style=self.text_style, justify="center")
            table.add_column("key", style=self.text_style, justify="center")

            for col in df_cols:
                table.add_row(col, str(v[col].dtype), check_key(col))

            tables.append(table)

        return tables


def check_key(col_name: str):
    """Check if column is PK, FK or no key when drawing datasets' schemas."""

    if col_name == "id":
        return "PK"
    elif col_name.endswith("_id"):
        return "FK"
    else:
        return None


# check progress to update CasesScreen
def check_progress():
    with open(PROGRESS, "r") as file:
        content = json.load(file)

        for case in CASES:
            if case.case_id in content["solved"]:
                case.solved = True


# update progress if case gets solved
def update_progress(id: int):
    with open(PROGRESS, "r") as file:
        data = json.load(file)

    if id in data["solved"]:
        pass

    else:
        data["solved"].append(id)

        with open(PROGRESS, "w") as file:
            json.dump(data, file)


# Unicode blocks renderer
BRIGHT = "\033[38;5;255m"
MID = "\033[38;5;250m"
GRAY = "\033[38;5;245m"
GRAY2 = "\033[38;5;240m"
DIM = "\033[38;5;236m"
DOT = "\033[38;5;248m"
R = "\033[0m"

glyphs = {
    "p": ["###", "#.#", "###", "#..", "#.."],
    "a": [".##.", "#..#", "####", "#..#", "#..#"],
    "n": ["#..#", "##.#", "#.##", "#..#", "#..#"],
    "d": ["###.", "#..#", "#..#", "#..#", "###."],
    "s": [".###", "#...", ".##.", "...#", "###."],
    ".": [".", ".", ".", ".", "#"],
    "o": [".##.", "#..#", "#..#", "#..#", ".##."],
    "i": ["#", "#", "#", "#", "#"],
    "r": ["###.", "#..#", "###.", "#.#.", "#..#"],
    "(": [".#", "#.", "#.", "#.", ".#"],
    ")": ["#.", ".#", ".#", ".#", "#."],
}


def get_colors(text):
    result = []
    pandas_count = 0
    for ch in text:
        if pandas_count < 6 and ch != ".":
            result.append((BRIGHT, MID))
            pandas_count += 1
        elif ch == ".":
            result.append((DOT, DOT))
        elif ch in "()":
            result.append((GRAY2, DIM))
        else:
            result.append((GRAY, GRAY2))
    return result


def render(text):
    chars = [glyphs[ch] for ch in text]
    colors = get_colors(text)
    lines = []

    for text_row in range(3):
        line = ""
        top_row = text_row * 2
        bot_row = text_row * 2 + 1

        for gi, glyph in enumerate(chars):
            col_top, col_bot = colors[gi]
            for col in range(len(glyph[0])):
                top = top_row < 5 and glyph[top_row][col] == "#"
                bot = bot_row < 5 and glyph[bot_row][col] == "#"
                if top and bot:
                    line += col_top + "█"
                elif top:
                    line += col_top + "▀"
                elif bot:
                    line += col_bot + "▄"
                else:
                    line += " "
            if gi < len(chars) - 1:
                line += " "

        lines.append(line + R)

    return "\n".join(lines)


# rich rendering for dataframe
def rich_df(df):
    table = Table(show_lines=True)
    for col in df.columns:
        table.add_column(str(col), style="cyan")
    for i, row in df.iterrows():
        style = "on grey15" if i % 2 == 0 else ""
        table.add_row(*[str(v) for v in row], style=style)
    return table

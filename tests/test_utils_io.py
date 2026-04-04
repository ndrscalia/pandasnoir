import json
from unittest.mock import patch
from rich.table import Table

from pandasnoir._cases_data import CASES


# --- populate_saves ---

def test_populate_saves_creates_structure(tmp_path):
    saves = tmp_path / "saves"
    progress = saves / "progress.json"

    with patch("pandasnoir.utils.SAVES_DIR", saves), \
         patch("pandasnoir.utils.PROGRESS", progress):
        from pandasnoir.utils import populate_saves
        populate_saves()

    assert saves.exists()
    assert progress.exists()
    data = json.loads(progress.read_text())
    assert data == {"solved": []}

    for case in CASES:
        assert (saves / f"case_{case.case_id}" / "workspace.txt").exists()
        assert (saves / f"case_{case.case_id}" / "notes.txt").exists()


def test_populate_saves_workspace_contains_imports(tmp_path):
    saves = tmp_path / "saves"
    progress = saves / "progress.json"

    with patch("pandasnoir.utils.SAVES_DIR", saves), \
         patch("pandasnoir.utils.PROGRESS", progress):
        from pandasnoir.utils import populate_saves
        populate_saves()

    ws = (saves / "case_1" / "workspace.txt").read_text()
    assert "import pandas as pd" in ws
    assert "pd.read_csv" in ws


def test_populate_saves_idempotent(tmp_path):
    saves = tmp_path / "saves"
    progress = saves / "progress.json"

    with patch("pandasnoir.utils.SAVES_DIR", saves), \
         patch("pandasnoir.utils.PROGRESS", progress):
        from pandasnoir.utils import populate_saves
        populate_saves()

    ws_path = saves / "case_1" / "workspace.txt"
    ws_path.write_text("custom content")

    with patch("pandasnoir.utils.SAVES_DIR", saves), \
         patch("pandasnoir.utils.PROGRESS", progress):
        populate_saves()

    assert ws_path.read_text() == "custom content"


# --- check_progress ---

def test_check_progress_marks_solved(progress_file):
    progress_file.write_text(json.dumps({"solved": [1, 3]}))

    with patch("pandasnoir.utils.PROGRESS", progress_file):
        from pandasnoir.utils import check_progress
        check_progress()

    assert CASES[0].solved is True   # case_id=1
    assert CASES[1].solved is False  # case_id=2
    assert CASES[2].solved is True   # case_id=3


def test_check_progress_empty_solved(progress_file):
    progress_file.write_text(json.dumps({"solved": []}))

    with patch("pandasnoir.utils.PROGRESS", progress_file):
        from pandasnoir.utils import check_progress
        check_progress()

    for case in CASES:
        assert case.solved is False


# --- update_progress ---

def test_update_progress_adds_id(progress_file):
    progress_file.write_text(json.dumps({"solved": []}))

    with patch("pandasnoir.utils.PROGRESS", progress_file):
        from pandasnoir.utils import update_progress
        update_progress(1)

    data = json.loads(progress_file.read_text())
    assert 1 in data["solved"]


def test_update_progress_idempotent(progress_file):
    progress_file.write_text(json.dumps({"solved": [1]}))

    with patch("pandasnoir.utils.PROGRESS", progress_file):
        from pandasnoir.utils import update_progress
        update_progress(1)

    data = json.loads(progress_file.read_text())
    assert data["solved"].count(1) == 1


def test_update_progress_preserves_existing(progress_file):
    progress_file.write_text(json.dumps({"solved": [2]}))

    with patch("pandasnoir.utils.PROGRESS", progress_file):
        from pandasnoir.utils import update_progress
        update_progress(3)

    data = json.loads(progress_file.read_text())
    assert 2 in data["solved"]
    assert 3 in data["solved"]


# --- Schema ---

def test_schema_loads_datasets():
    from pandasnoir.utils import Schema
    schema = Schema(case_id=1, text_style="white", border_style="blue")
    assert len(schema.datasets) == 3


def test_schema_draw_tables_returns_rich_tables():
    from pandasnoir.utils import Schema
    schema = Schema(case_id=1, text_style="white", border_style="blue")
    tables = schema.draw_tables()
    assert len(tables) == 3
    for t in tables:
        assert isinstance(t, Table)


def test_schema_tables_have_three_columns():
    from pandasnoir.utils import Schema
    schema = Schema(case_id=1, text_style="white", border_style="blue")
    for table in schema.draw_tables():
        assert len(table.columns) == 3

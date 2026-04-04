import json
import pytest
from pandasnoir._cases_data import CASES


@pytest.fixture(autouse=True)
def reset_cases_solved():
    """Reset the global mutable CASES[].solved state after every test."""
    original = [c.solved for c in CASES]
    yield
    for case, was_solved in zip(CASES, original):
        case.solved = was_solved


@pytest.fixture
def save_dir(tmp_path):
    """Temporary save directory mirroring ~/.pandasnoir/saves/."""
    saves = tmp_path / "saves"
    saves.mkdir()
    progress = saves / "progress.json"
    progress.write_text(json.dumps({"solved": []}))
    for case_id in range(1, 7):
        case_dir = saves / f"case_{case_id}"
        case_dir.mkdir()
        (case_dir / "workspace.txt").write_text("import pandas as pd\n\n")
        (case_dir / "notes.txt").touch()
    return saves


@pytest.fixture
def progress_file(save_dir):
    """Path to the temporary progress.json."""
    return save_dir / "progress.json"

from pathlib import Path
from pandasnoir._cases_data import CASES, CaseInfo

CASES_DIR = Path(__file__).resolve().parent.parent / "src" / "pandasnoir" / "cases"
DOCS_DIR = Path(__file__).resolve().parent.parent / "src" / "pandasnoir" / "cases_docs"


def test_cases_is_nonempty_list():
    assert len(CASES) >= 1


def test_all_cases_are_caseinfo():
    for case in CASES:
        assert isinstance(case, CaseInfo)


def test_case_ids_unique_and_sequential():
    ids = [c.case_id for c in CASES]
    assert ids == list(range(1, len(CASES) + 1))


def test_all_cases_have_nonempty_solution():
    for case in CASES:
        assert isinstance(case.solution, str) and len(case.solution.strip()) > 0


def test_dataset_csv_files_exist():
    for case in CASES:
        case_dir = CASES_DIR / f"case_{case.case_id}"
        for dataset in case.datasets:
            csv_path = case_dir / dataset
            assert csv_path.exists(), f"Missing CSV: {csv_path}"


def test_case_docs_exist():
    for case in CASES:
        doc = DOCS_DIR / f"case_{case.case_id}.md"
        assert doc.exists(), f"Missing doc: {doc}"


def test_cases_default_unsolved():
    fresh = CaseInfo(
        case_id=99, title="t", description="d",
        instructions="i", objectives=[], datasets=[],
        level="Beginner", solution="s",
    )
    assert fresh.solved is False


def test_valid_levels():
    valid = {"Beginner", "Intermediate", "Advanced"}
    for case in CASES:
        assert case.level in valid, f"Case {case.case_id} has unknown level: {case.level}"

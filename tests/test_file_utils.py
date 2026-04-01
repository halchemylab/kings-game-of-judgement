# tests/test_file_utils.py
import os
import pytest
from file_utils import save_case, list_past_cases, generate_case_id, PAST_CASES_DIR
from models import CaseRecord, InquiryEntry

@pytest.fixture
def temp_case_dir(tmp_path):
    """Fixture to use a temporary directory for past cases during tests."""
    import file_utils
    original_dir = file_utils.PAST_CASES_DIR
    temp_dir = tmp_path / "test_past_cases"
    file_utils.PAST_CASES_DIR = str(temp_dir)
    yield temp_dir
    file_utils.PAST_CASES_DIR = original_dir

def test_save_case(temp_case_dir):
    case_id = "test_case_123"
    player_name = "TestJudge"
    difficulty = "Moderate"
    scenario = "A test scenario."
    judgment = "A test judgment."
    analysis = "A test analysis."
    inquiry_history = [InquiryEntry(character="Farmer", question="Why?", response="Because.")]

    case_record = CaseRecord(
        case_id=case_id,
        player_name=player_name,
        difficulty=difficulty,
        scenario=scenario,
        judgment=judgment,
        analysis=analysis,
        inquiry_history=inquiry_history
    )

    success = save_case(case_record)
    assert success is True
    assert os.path.exists(os.path.join(str(temp_case_dir), f"case_{case_id}.json"))

def test_load_case(temp_case_dir):
    from file_utils import load_case
    case_id = "load_test_456"
    player_name = "LoaderJudge"
    difficulty = "Simple"
    scenario = "The case of the missing cake."
    judgment = "The baker is innocent."
    analysis = "A fair ruling indeed."
    inquiry_history = [InquiryEntry(character="Baker", question="Did you?", response="No.")]

    case_record = CaseRecord(
        case_id=case_id,
        player_name=player_name,
        difficulty=difficulty,
        scenario=scenario,
        judgment=judgment,
        analysis=analysis,
        inquiry_history=inquiry_history
    )

    save_case(case_record)
    
    loaded_case = load_case(f"case_{case_id}.json")
    assert loaded_case is not None
    assert loaded_case.case_id == case_id
    assert loaded_case.player_name == player_name
    assert loaded_case.scenario == scenario
    assert len(loaded_case.inquiry_history) == 1
    assert loaded_case.inquiry_history[0].character == "Baker"

def test_generate_case_id():
    case_id = generate_case_id()
    assert isinstance(case_id, str)
    assert len(case_id) > 0

def test_list_past_cases(temp_case_dir):
    # Ensure directory exists
    os.makedirs(str(temp_case_dir), exist_ok=True)
    
    # Create a dummy case file
    with open(os.path.join(str(temp_case_dir), "case_20240101_120000_000000.json"), "w") as f:
        f.write("{}")
    
    cases = list_past_cases()
    assert len(cases) == 1
    assert "case_20240101_120000_000000.json" in cases

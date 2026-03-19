import os
import pytest
from file_utils import save_case, list_past_cases, generate_case_id, PAST_CASES_DIR

@pytest.fixture
def temp_case_dir(tmp_path, monkeypatch):
    """Fixture to use a temporary directory for past cases during tests."""
    test_dir = tmp_path / "test_past_cases"
    test_dir.mkdir()
    monkeypatch.setattr("file_utils.PAST_CASES_DIR", str(test_dir))
    return test_dir

def test_generate_case_id():
    case_id = generate_case_id()
    assert isinstance(case_id, str)
    assert len(case_id) > 0

def test_save_case(temp_case_dir):
    case_id = "test_case_123"
    player_name = "TestJudge"
    scenario = "A test scenario."
    judgment = "A test judgment."
    analysis = "A test analysis."
    
    success = save_case(case_id, player_name, scenario, judgment, analysis)
    
    assert success is not False # save_case returns None on success currently
    
    case_file = temp_case_dir / f"case_{case_id}.txt"
    assert case_file.exists()
    
    content = case_file.read_text(encoding="utf-8")
    assert f"Case ID: {case_id}" in content
    assert f"--- JUDGMENT BY JUDGE {player_name} ---" in content
    assert scenario in content

def test_list_past_cases(temp_case_dir):
    # Initially empty
    assert list_past_cases() == []
    
    # Add a dummy case file
    case_file = temp_case_dir / "case_20230101_120000_000.txt"
    case_file.write_text("dummy content")
    
    # Add a non-case file
    (temp_case_dir / "other.txt").write_text("ignore me")
    
    cases = list_past_cases()
    assert len(cases) == 1
    assert "case_20230101_120000_000.txt" in cases

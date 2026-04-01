# file_utils.py
import os
import datetime
import re
import json
from models import CaseRecord, InquiryEntry

PAST_CASES_DIR = "past_cases"

def ensure_past_cases_dir_exists():
    """Ensures the directory for past cases exists."""
    if not os.path.exists(PAST_CASES_DIR):
        try:
            os.makedirs(PAST_CASES_DIR)
        except OSError as e:
            print(f"Error creating directory {PAST_CASES_DIR}: {e}")
            return False
    return True

def save_case(case_record: CaseRecord):
    """Saves a completed case to a JSON file."""
    if not ensure_past_cases_dir_exists():
        return False

    filename = os.path.join(PAST_CASES_DIR, f"case_{case_record.case_id}.json")

    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(case_record.model_dump_json(indent=4))
        return True
    except IOError as e:
        print(f"Error saving case {case_record.case_id} to {filename}: {e}")
        return False

def load_case(filename):
    """Loads and parses a case file (JSON or legacy TXT) from the past_cases directory."""
    path = os.path.join(PAST_CASES_DIR, filename)
    if not os.path.exists(path):
        return None

    try:
        if filename.endswith(".json"):
            with open(path, "r", encoding="utf-8") as f:
                return CaseRecord.model_validate_json(f.read())
        else:
            # Legacy TXT parsing
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

            # Extract Case ID and Date
            case_id_match = re.search(r"Case ID: (.*)\n", content)
            date_match = re.search(r"Date: (.*)\n", content)
            
            case_id = case_id_match.group(1).strip() if case_id_match else "Unknown"
            date = date_match.group(1).strip() if date_match else "Unknown"

            scenario_match = re.search(r"--- SCENARIO ---\n(.*?)\n\n--- (?:INQUIRY|JUDGMENT)", content, re.DOTALL)
            inquiry_match = re.search(r"--- INQUIRY TRANSCRIPT ---\n(.*?)\n\n--- JUDGMENT", content, re.DOTALL)
            judgment_match = re.search(r"--- JUDGMENT BY JUDGE (.*?) ---\n(.*?)\n\n--- ADVISOR'S ANALYSIS", content, re.DOTALL)
            analysis_match = re.search(r"--- ADVISOR'S ANALYSIS ---\n(.*?)\n----------------------------------------", content, re.DOTALL)

            scenario = scenario_match.group(1).strip() if scenario_match else ""
            
            inquiry_history = []
            if inquiry_match:
                inquiry_text = inquiry_match.group(1).strip()
                # Simple split for legacy inquiry - might not be perfect but covers basics
                entries = inquiry_text.split("\n\n")
                for entry in entries:
                    lines = entry.split("\n")
                    if len(lines) >= 2:
                        char_q = lines[0].replace("To ", "")
                        if ": " in char_q:
                            char, q = char_q.split(": ", 1)
                            resp = lines[1].replace("Response: ", "")
                            inquiry_history.append(InquiryEntry(character=char, question=q, response=resp))

            player_name = "Unknown"
            judgment = ""
            if judgment_match:
                player_name = judgment_match.group(1).strip()
                judgment = judgment_match.group(2).strip()

            analysis = analysis_match.group(1).strip() if analysis_match else ""

            return CaseRecord(
                case_id=case_id,
                date=date,
                player_name=player_name,
                difficulty="Unknown", # Not stored in legacy TXT
                scenario=scenario,
                inquiry_history=inquiry_history,
                judgment=judgment,
                analysis=analysis
            )
    except Exception as e:
        print(f"Error loading case {filename}: {e}")
        return None

def generate_case_id():
    """Generates a unique case ID based on timestamp."""
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")

def list_past_cases():
    if not os.path.exists(PAST_CASES_DIR):
        return []
    # Sort files by date (newest first) based on their filename timestamp
    files = [f for f in os.listdir(PAST_CASES_DIR) if f.startswith("case_") and (f.endswith(".txt") or f.endswith(".json"))]
    return sorted(files, reverse=True)

# file_utils.py
import os
import datetime
import re
import streamlit as st # Keep st import in case you want to use st.error here later

PAST_CASES_DIR = "past_cases"

def ensure_past_cases_dir_exists():
    """Ensures the directory for past cases exists."""
    if not os.path.exists(PAST_CASES_DIR):
        try:
            os.makedirs(PAST_CASES_DIR)
        except OSError as e:
            # Using print for now, as st.error might not always be appropriate in a utility function
            # if it's called from a non-Streamlit context in the future.
            # However, for this app, st.error would be fine.
            print(f"Error creating directory {PAST_CASES_DIR}: {e}")
            return False
    return True

def save_case(case_id, player_name, scenario, judgment, analysis, case_path=None):
    """Saves a completed case to a text file. Uses a safe path if provided."""
    if not ensure_past_cases_dir_exists():
        return False

    if case_path is not None:
        filename = case_path
    else:
        filename = os.path.join(PAST_CASES_DIR, f"case_{case_id}.txt")

    content = f"Case ID: {case_id}\n"
    content += f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    content += "--- SCENARIO ---\n"
    content += scenario + "\n\n"
    content += f"--- JUDGMENT BY JUDGE {player_name} ---\n"
    content += judgment + "\n\n"
    content += "--- ADVISOR'S ANALYSIS ---\n"
    content += analysis + "\n"
    content += "----------------------------------------\n"

    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    except IOError as e:
        print(f"Error saving case {case_id} to {filename}: {e}")
        return False

def load_case(filename):
    """Loads and parses a case file from the past_cases directory."""
    path = os.path.join(PAST_CASES_DIR, filename)
    if not os.path.exists(path):
        return None

    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        case_data = {}

        # Extract Case ID and Date
        case_id_match = re.search(r"Case ID: (.*)\n", content)
        date_match = re.search(r"Date: (.*)\n", content)

        case_data['case_id'] = case_id_match.group(1).strip() if case_id_match else "Unknown"
        case_data['date'] = date_match.group(1).strip() if date_match else "Unknown"

        # Extract sections using delimiters
        # We look for text between the markers
        scenario_match = re.search(r"--- SCENARIO ---\n(.*?)\n\n--- JUDGMENT", content, re.DOTALL)
        judgment_match = re.search(r"--- JUDGMENT BY JUDGE (.*?) ---\n(.*?)\n\n--- ADVISOR'S ANALYSIS", content, re.DOTALL)
        analysis_match = re.search(r"--- ADVISOR'S ANALYSIS ---\n(.*?)\n----------------------------------------", content, re.DOTALL)

        case_data['scenario'] = scenario_match.group(1).strip() if scenario_match else ""
        if judgment_match:
            case_data['player_name'] = judgment_match.group(1).strip()
            case_data['judgment'] = judgment_match.group(2).strip()
        else:
            case_data['player_name'] = "Unknown"
            case_data['judgment'] = ""

        case_data['analysis'] = analysis_match.group(1).strip() if analysis_match else ""

        return case_data
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
    files = [f for f in os.listdir(PAST_CASES_DIR) if f.startswith("case_") and f.endswith(".txt")]
    return sorted(files, reverse=True)
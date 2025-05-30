# file_utils.py
import os
import datetime
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

def save_case(case_id, player_name, scenario, judgment, analysis):
    """Saves a completed case to a text file."""
    if not ensure_past_cases_dir_exists():
        return False

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

def generate_case_id():
    """Generates a unique case ID based on timestamp."""
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")

def list_past_cases():
    if not os.path.exists(PAST_CASES_DIR):
        return []
    return [f for f in os.listdir(PAST_CASES_DIR) if f.startswith("case_") and f.endswith(".txt")]
# app.py
import streamlit as st
import os
from llm_integration import OPENAI_API_KEY
from file_utils import list_past_cases
from ui.styles import inject_custom_css
from ui.welcome import display_welcome
from ui.scenario import display_scenario_and_task
from ui.analysis import display_ai_analysis
from ui.archives import display_archives

# --- Page Configuration ---
st.set_page_config(
    page_title="The King's Game of Judgement",
    page_icon="👑",
    layout="wide"
)

# --- Inject CSS ---
inject_custom_css()

# --- Session State Initialization ---
def init_session_state():
    if "player_name" not in st.session_state:
        st.session_state.player_name = ""
    if "judge_name" not in st.session_state:
        st.session_state.judge_name = ""
    if "game_stage" not in st.session_state:
        st.session_state.game_stage = "welcome"
    if "current_scenario" not in st.session_state:
        st.session_state.current_scenario = None
    if "characters" not in st.session_state:
        st.session_state.characters = []
    if "inquiry_history" not in st.session_state:
        st.session_state.inquiry_history = []
    if "questions_remaining" not in st.session_state:
        st.session_state.questions_remaining = 3 
    if "selected_witness" not in st.session_state:
        st.session_state.selected_witness = None
    if "player_judgment" not in st.session_state:
        st.session_state.player_judgment = ""
    if "ai_analysis" not in st.session_state:
        st.session_state.ai_analysis = None
    if "current_case_id" not in st.session_state:
        st.session_state.current_case_id = None
    if "api_key_valid" not in st.session_state:
        st.session_state.api_key_valid = bool(OPENAI_API_KEY)
    if "difficulty" not in st.session_state:
        st.session_state.difficulty = "Moderate"
    if "selected_archive_case" not in st.session_state:
        st.session_state.selected_archive_case = None

init_session_state()

# --- Main Application Flow ---
if not st.session_state.api_key_valid and st.session_state.game_stage != "welcome":
    st.session_state.game_stage = "welcome"

if st.session_state.game_stage == "welcome":
    display_welcome()
elif st.session_state.game_stage == "scenario_presented":
    display_scenario_and_task()
elif st.session_state.game_stage == "judgment_submitted":
    display_ai_analysis()
elif st.session_state.game_stage == "archives":
    display_archives()
else:
    st.error("An unexpected error occurred in the game flow. Resetting.")
    st.session_state.game_stage = "welcome"
    st.rerun()

# --- Sidebar ---
st.sidebar.markdown('<div class="sidebar-title" role="heading" aria-level="2">Game Panel</div>', unsafe_allow_html=True)
if st.session_state.player_name:
    st.sidebar.markdown(f'<div class="sidebar-card" role="region" aria-label="Judge Name">Judge: <b>{st.session_state.judge_name}</b></div>', unsafe_allow_html=True)
    st.sidebar.markdown(f'<div class="sidebar-card" role="region" aria-label="Difficulty">Difficulty: <b>{st.session_state.difficulty}</b></div>', unsafe_allow_html=True)
    st.sidebar.markdown(f'<div class="sidebar-card" role="region" aria-label="Current Stage">Current Stage: <b>{st.session_state.game_stage.replace("_", " ").title()}</b></div>', unsafe_allow_html=True)
    
    if st.session_state.game_stage != "archives":
        st.sidebar.markdown('<div class="sidebar-btn">', unsafe_allow_html=True)
        if st.sidebar.button("📜 View Royal Archives", key="view_archives_btn", use_container_width=True):
            st.session_state.game_stage = "archives"
            st.rerun()
        st.sidebar.markdown('</div>', unsafe_allow_html=True)
    
    if st.sidebar.button("🔄 Reset Game", key="reset_game_btn", use_container_width=True):
        st.session_state.game_stage = "welcome"
        st.session_state.player_name = ""
        st.session_state.current_scenario = None
        st.session_state.player_judgment = ""
        st.session_state.ai_analysis = None
        st.session_state.current_case_id = None
        st.rerun()
else:
    st.sidebar.markdown('<div class="sidebar-card" role="region" aria-label="Awaiting Judge">Awaiting Judge\'s arrival.</div>', unsafe_allow_html=True)

resolved_cases_count = len([f for f in os.listdir('past_cases') if f.startswith('case_')]) if os.path.exists('past_cases') else 0
st.sidebar.markdown(f'<div class="sidebar-card" role="region" aria-label="Cases Resolved">Cases Resolved: <b>{resolved_cases_count}</b></div>', unsafe_allow_html=True)
st.sidebar.markdown('<hr class="royal-divider" />', unsafe_allow_html=True)
st.sidebar.markdown('<div class="sidebar-card" role="region" aria-label="How to Play">How to Play:<br><ul><li>Enter your name to begin.</li><li>Read the case and submit your judgment.</li><li>Review the Royal Advisor\'s analysis.</li><li>Try as many cases as you wish!</li></ul></div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="sidebar-card" role="region" aria-label="Powered by OpenAI">Powered by <b>OpenAI</b></div>', unsafe_allow_html=True)
if not st.session_state.api_key_valid:
    st.sidebar.markdown('<div class="sidebar-critical" role="alert" aria-label="API Key Missing">API Key Missing!</div>', unsafe_allow_html=True)

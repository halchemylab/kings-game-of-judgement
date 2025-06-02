# app.py
import streamlit as st
import os # For joining path in save_case success message
import time
from llm_integration import generate_scenario_with_llm, analyze_judgment_with_llm, OPENAI_API_KEY
from file_utils import save_case, generate_case_id

# --- Page Configuration ---
st.set_page_config(
    page_title="The King's Game of Judgement",
    page_icon="👑",
    layout="wide"
)

# --- Custom CSS for Legible, Modern Theme ---
st.markdown(
    """
    <style>
    html, body, [class*='css']  {
        font-family: 'Segoe UI', 'Arial', sans-serif !important;
        background: #f6f8fa !important;
        color: #22272e !important;
    }
    .main {
        background: #fff !important;
        border-radius: 16px;
        box-shadow: 0 4px 24px 0 rgba(60, 60, 60, 0.07);
        padding: 2rem 2.5rem 2rem 2.5rem;
        margin-top: 2rem;
    }
    .stButton>button {
        background: linear-gradient(90deg, #6dd5ed 0%, #2193b0 100%);
        color: #fff;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1.08rem;
        border: none;
        transition: 0.2s;
        box-shadow: 0 2px 8px #6dd5ed33;
    }
    .stButton>button:active {
        background: #2193b0;
    }
    /* Rainbow effect for critical buttons */
    .rainbow-btn {
        background: linear-gradient(90deg, #ff5858, #f09819, #fffa65, #43e97b, #38f9d7, #2193b0, #ee0979, #ff5858);
        background-size: 300% 300%;
        color: #fff !important;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        box-shadow: 0 2px 12px #fffa6533;
        transition: background-position 0.5s, color 0.2s;
    }
    .rainbow-btn:hover {
        background-position: 100% 0;
        color: #22272e !important;
        box-shadow: 0 4px 24px #fffa6533;
    }
    .royal-banner {
        background: #2193b0;
        color: #fff;
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin-bottom: 1.5rem;
        font-size: 2rem;
        font-family: 'Segoe UI', 'Arial', sans-serif;
        text-align: center;
        font-weight: 700;
        letter-spacing: 1px;
        box-shadow: 0 2px 8px #2193b033;
    }
    .royal-card {
        background: #f6f8fa;
        border-radius: 10px;
        padding: 1.2rem 1.2rem 1rem 1.2rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 2px 8px #2193b022;
        border: 1px solid #e3e8ee;
    }
    .royal-divider {
        border: 0;
        height: 2px;
        background: linear-gradient(90deg, #6dd5ed 0%, #2193b0 100%);
        margin: 1.2rem 0 1.2rem 0;
    }
    .royal-label {
        font-family: 'Segoe UI', 'Arial', sans-serif;
        font-size: 1.08rem;
        color: #2193b0;
        font-weight: 600;
    }
    .stTextInput>div>input, .stTextArea>div>textarea {
        background: #f6f8fa;
        border: 1.5px solid #6dd5ed88;
        border-radius: 8px;
        font-size: 1.08rem;
        color: #22272e;
    }
    .stTextInput>div>input:focus, .stTextArea>div>textarea:focus {
        border: 2px solid #2193b0;
        outline: none;
    }
    /* Sidebar redesign */
    section[data-testid="stSidebar"] {
        background: #1a2a36;
        border-right: 2px solid #2193b0;
        box-shadow: 2px 0 12px #2193b022;
        padding-top: 1.5rem;
    }
    .sidebar-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #6dd5ed;
        margin-bottom: 0.7rem;
        text-align: center;
    }
    .sidebar-card {
        background: #223344;
        border-radius: 8px;
        padding: 1rem 1rem 0.7rem 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px #2193b022;
        border: 1px solid #2193b0;
        font-size: 1.05rem;
        color: #fff;
    }
    .sidebar-critical {
        color: #ee0979;
        font-weight: bold;
        margin-top: 1.2rem;
        text-align: center;
    }
    /* Text area background for better contrast */
    .stTextArea>div>textarea {
        background: #223344 !important;
        color: #fff !important;
        border: 1.5px solid #6dd5ed88;
    }
    .stTextArea>div>textarea:focus {
        border: 2px solid #2193b0;
        outline: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

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
    if "player_judgment" not in st.session_state:
        st.session_state.player_judgment = ""
    if "ai_analysis" not in st.session_state:
        st.session_state.ai_analysis = None
    if "current_case_id" not in st.session_state:
        st.session_state.current_case_id = None
    if "api_key_valid" not in st.session_state: # Track API key status
        st.session_state.api_key_valid = bool(OPENAI_API_KEY)


init_session_state()

# --- Helper function to check for errors from LLM calls ---
def handle_llm_response(response_text, success_callback, error_message_prefix=""):
    if response_text and response_text.startswith("Error:"):
        st.error(f"{error_message_prefix}{response_text}")
        return False
    elif not response_text:
        st.error(f"{error_message_prefix}Received an empty response from the AI. Please try again.")
        return False
    else:
        success_callback(response_text)
        return True

# --- Game UI and Logic ---

def display_welcome():
    st.markdown('<div class="royal-banner">👑 Welcome to <b>The King\'s Game of Judgement!</b> 👑</div>', unsafe_allow_html=True)

    if not st.session_state.api_key_valid:
        st.error(
            "OpenAI API Key is missing or not configured correctly. "
            "Please ensure your `OPENAI_API_KEY` is set in a `.env` file "
            "in the root directory of the application and that you have installed the `python-dotenv` package."
        )
        st.markdown("""Your `.env` file should look like this:\n```
OPENAI_API_KEY=\"your_actual_api_key_here\"\n```
""")
        st.stop()

    st.markdown(
        '<div class="royal-card">'
        '<span class="royal-label">Hark, noble one!</span><br>'
        'You are about to embark on a journey of wisdom and discernment.<br>'
        'As a venerable Judge in this kingdom, your keen intellect and balanced perspective '
        'will be called upon to resolve complex disputes.'
        '</div>', unsafe_allow_html=True)

    name_input = st.text_input("Pray, tell us your esteemed name to begin:", key="player_name_input_key")

    st.markdown('<hr class="royal-divider" />', unsafe_allow_html=True)

    if st.button("✨ Begin My Tenure as Judge", key="begin_judge_btn", help="Start the game!"):
        if name_input:
            st.session_state.player_name = name_input.strip()
            st.session_state.judge_name = f"Judge {st.session_state.player_name}"
            st.session_state.game_stage = "scenario_presented"
            st.session_state.current_case_id = generate_case_id()
            with st.spinner(f"Summoning a new case for {st.session_state.judge_name}... This may take a moment."):
                scenario_text = generate_scenario_with_llm(st.session_state.player_name)
            def set_scenario(text):
                st.session_state.current_scenario = text
            if handle_llm_response(scenario_text, set_scenario, "Failed to generate scenario: "):
                st.rerun()
            else:
                st.session_state.game_stage = "welcome"
        else:
            st.warning("A Judge must have a name! Please enter yours.")


def display_scenario_and_task():
    # Animated transition: Balloons when a new case is presented
    if st.session_state.get('show_balloons', False):
        st.balloons()
        time.sleep(1.2)
        st.session_state.show_balloons = False
    st.markdown('<div class="royal-banner">A New Case Awaits, {}</div>'.format(st.session_state.judge_name), unsafe_allow_html=True)
    if st.session_state.current_scenario:
        st.markdown('<div class="royal-card"><span class="royal-label">📜 The Case Before You:</span><br>{}</div>'.format(st.session_state.current_scenario), unsafe_allow_html=True)
        st.markdown('<hr class="royal-divider" />', unsafe_allow_html=True)
        st.markdown('<div class="royal-card"><span class="royal-label">Your Task, {}</span><br>'.format(st.session_state.judge_name) +
            "Considering the facts, the written rules (if any were implied or provided in the scenario), "
            "and the 'human values' and 'normative choices' at play:<br><ul>"
            "<li>Who should [the disputed object/resolution] go to / What should be the outcome?</li>"
            "<li>What is your reasoning?</li>"
            "<li>What values are you prioritizing in your decision?</li>"
            "</ul>Take your time, my king! I await your wise judgment. 👑📝</div>", unsafe_allow_html=True)
        judgment_text = st.text_area("Enter your judgment here:", height=200, key="judgment_input_key")
        st.markdown('<hr class="royal-divider" />', unsafe_allow_html=True)
        if st.button("⚖️ Submit Your Judgment", key="submit_judgment_btn", help="Submit your decision!", use_container_width=True):
            if judgment_text.strip():
                st.session_state.player_judgment = judgment_text.strip()
                st.session_state.game_stage = "judgment_submitted"
                st.rerun()
            else:
                st.warning("An empty scroll offers no wisdom. Please pen your judgment.")
    else:
        st.error("Apologies, the scenario is missing. Let's try to fetch a new one.")
        if st.button("Fetch New Case", key="fetch_new_case_btn"):
            st.session_state.game_stage = "welcome"
            st.session_state.player_name = ""
            st.rerun()


def display_ai_analysis():
    # Animated transition: Snow/confetti when analysis is shown
    if st.session_state.get('show_snow', False):
        st.snow()
        time.sleep(1.2)
        st.session_state.show_snow = False
    st.markdown('<div class="royal-banner">The Royal Advisor\'s Counsel for {}</div>'.format(st.session_state.judge_name), unsafe_allow_html=True)
    if st.session_state.ai_analysis is None:
        with st.spinner(f"The Royal Advisor is diligently reviewing your judgment, {st.session_state.judge_name}... This may take a moment."):
            analysis_result = analyze_judgment_with_llm(
                st.session_state.player_judgment,
                st.session_state.current_scenario,
                st.session_state.player_name
            )
        def set_analysis(text):
            st.session_state.ai_analysis = text
        if not handle_llm_response(analysis_result, set_analysis, "Failed to get Advisor's analysis: "):
            if st.button("Try Analysis Again", key="try_analysis_btn"):
                st.session_state.ai_analysis = None
                st.rerun()
            return
    if st.session_state.ai_analysis:
        st.markdown('<div class="royal-card"><span class="royal-label">🧐 Advisor\'s Analysis:</span><br>{}</div>'.format(st.session_state.ai_analysis), unsafe_allow_html=True)
        st.markdown('<hr class="royal-divider" />', unsafe_allow_html=True)
        if st.session_state.current_case_id and st.session_state.current_scenario and st.session_state.player_judgment and st.session_state.ai_analysis:
            if not st.session_state.ai_analysis.startswith("Error:"):
                if save_case(
                    st.session_state.current_case_id,
                    st.session_state.player_name,
                    st.session_state.current_scenario,
                    st.session_state.player_judgment,
                    st.session_state.ai_analysis
                ):
                    st.success(f"This case (ID: {st.session_state.current_case_id}) has been chronicled in the royal archives ({os.path.join('past_cases', f'case_{st.session_state.current_case_id}.txt')}).")
                else:
                    st.error("There was an issue archiving this case.")
            else:
                st.info("Case not saved as the AI analysis encountered an error.")
        # Rainbow button for critical action
        rainbow_btn_html = '''<button class="rainbow-btn" onclick="window.location.reload()" style="width:100%;margin-top:1.2rem;padding:0.7rem 0;font-size:1.1rem;">📜 Hear Another Case</button>'''
        st.markdown(rainbow_btn_html, unsafe_allow_html=True)
    else:
        st.error("The Advisor seems to be indisposed. Unable to retrieve analysis at this time.")
        if st.button("Try Analysis Again", key="try_analysis_btn2"):
            st.session_state.ai_analysis = None
            st.rerun()


# --- Main Application Flow ---
if not st.session_state.api_key_valid and st.session_state.game_stage != "welcome":
    st.session_state.game_stage = "welcome"

if st.session_state.game_stage == "welcome":
    display_welcome()
elif st.session_state.game_stage == "scenario_presented":
    # Animated transition trigger for scenario
    if not st.session_state.get('show_balloons', False):
        st.session_state.show_balloons = True
    display_scenario_and_task()
elif st.session_state.game_stage == "judgment_submitted":
    # Animated transition trigger for analysis
    if not st.session_state.get('show_snow', False):
        st.session_state.show_snow = True
    display_ai_analysis()
else:
    st.error("An unexpected error occurred in the game flow. Resetting.")
    st.session_state.game_stage = "welcome"
    st.rerun()

# --- Sidebar ---
st.sidebar.markdown('<div class="sidebar-title">Game Panel</div>', unsafe_allow_html=True)
if st.session_state.player_name:
    st.sidebar.markdown(f'<div class="sidebar-card">Judge: <b>{st.session_state.judge_name}</b></div>', unsafe_allow_html=True)
    st.sidebar.markdown(f'<div class="sidebar-card">Current Stage: <b>{st.session_state.game_stage.replace("_", " ").title()}</b></div>', unsafe_allow_html=True)
else:
    st.sidebar.markdown('<div class="sidebar-card">Awaiting Judge\'s arrival.</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="sidebar-card">Cases Resolved: <b>{}</b></div>'.format(len([f for f in os.listdir('past_cases') if f.startswith('case_')]) if os.path.exists('past_cases') else 0), unsafe_allow_html=True)
st.sidebar.markdown('<hr class="royal-divider" />', unsafe_allow_html=True)
st.sidebar.markdown('<div class="sidebar-card">How to Play:<br><ul><li>Enter your name to begin.</li><li>Read the case and submit your judgment.</li><li>Review the Royal Advisor\'s analysis.</li><li>Try as many cases as you wish!</li></ul></div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="sidebar-card">Powered by <b>OpenAI</b></div>', unsafe_allow_html=True)
if not st.session_state.api_key_valid:
    st.sidebar.markdown('<div class="sidebar-critical">API Key Missing!</div>', unsafe_allow_html=True)
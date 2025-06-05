# app.py
import streamlit as st
import os # For joining path in save_case success message
import time
from llm_integration import generate_scenario_with_llm, analyze_judgment_with_llm, OPENAI_API_KEY, highlight_important_parts_with_llm, highlight_important_parts_in_analysis_with_llm
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
    html, body {
        font-size: 16px;
        background: #f8fafc;
        color: #1a1a1a;
    }
    .main {
        padding: 2rem 2.5rem;
        margin-top: 2rem;
        max-width: 900px;
        margin-left: auto;
        margin-right: auto;
    }
    .stButton>button {
        font-weight: 600;
        font-size: 1.1rem;
        width: 100%;
        min-height: 48px;
        border-radius: 6px;
        outline: 2px solid transparent;
        outline-offset: 2px;
        transition: outline 0.2s, box-shadow 0.2s, transform 0.1s, background 0.2s;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        background: #f3f4f6;
    }
    .stButton>button:hover {
        box-shadow: 0 4px 16px rgba(55, 65, 81, 0.12);
        background: #fbbf24;
        color: #7c4700;
        transform: scale(1.03);
        transition: box-shadow 0.2s, background 0.2s, color 0.2s, transform 0.1s;
    }
    .stButton>button:active {
        background: #fde68a;
        color: #a16207;
        transform: scale(0.98);
        box-shadow: 0 2px 8px rgba(55, 65, 81, 0.10);
    }
    .rainbow-btn {
        width: 100%;
        margin-top: 1.2rem;
        padding: 0.7rem 0;
        font-size: 1.1rem;
        border-radius: 6px;
        background: linear-gradient(90deg, #fbbf24, #a78bfa, #34d399, #f472b6);
        color: #1a1a1a;
        font-weight: 700;
        border: none;
        cursor: pointer;
        outline: 2px solid transparent;
        outline-offset: 2px;
        transition: outline 0.2s;
    }
    .rainbow-btn:focus {
        outline: 2px solid #3b82f6;
        outline-offset: 2px;
    }
    .rainbow-btn:active {
        filter: brightness(0.95);
    }
    .rainbow-btn[aria-disabled="true"] {
        opacity: 0.6;
        cursor: not-allowed;
    }
    .royal-banner {
        padding: 1rem 1.5rem;
        margin-bottom: 1.5rem;
        font-size: 2rem;
        text-align: center;
        font-weight: 700;
        letter-spacing: 1px;
        background: #fffbe6;
        color: #7c4700;
        border-radius: 0.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    .royal-card {
        padding: 1.2rem;
        margin-bottom: 1.2rem;
        border-radius: 0.5rem;
        background: #ffffff;
        color: #1a1a1a;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04);
        transition: box-shadow 0.2s, transform 0.1s;
    }
    .royal-card:hover {
        box-shadow: 0 6px 24px rgba(55, 65, 81, 0.13);
        transform: scale(1.01);
        background: #f3f4f6;
    }
    .royal-card:active {
        box-shadow: 0 2px 8px rgba(55, 65, 81, 0.10);
        transform: scale(0.98);
        background: #fbbf24;
    }
    .royal-divider {
        margin: 1.2rem 0;
        border: none;
        border-top: 2px solid #e5e7eb;
    }
    .royal-label {
        font-size: 1.15rem;
        font-weight: 700;
        color: #3b3b3b;
    }
    .stTextInput>div>input, .stTextArea>div>textarea {
        font-size: 1.08rem;
        min-height: 44px;
        border-radius: 6px;
    }
    .stTextInput>div>input:focus, .stTextArea>div>textarea:focus {
        outline: 2px solid #3b82f6 !important;
        outline-offset: 2px;
    }
    /* Sidebar layout */
    section[data-testid="stSidebar"] {
        padding-top: 1.5rem;
        background: #f3f4f6;
    }
    .sidebar-title {
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 0.7rem;
        text-align: center;
        color: #3b3b3b;
    }
    .sidebar-card {
        padding: 1rem 1rem 0.7rem 1rem;
        margin-bottom: 1rem;
        border-radius: 0.5rem;
        font-size: 1.08rem;
        background: #fff;
        color: #1a1a1a;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    }
    .sidebar-critical {
        color: #fff;
        background: #dc2626;
        padding: 0.7rem 1rem;
        border-radius: 0.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    /* Focus outline for all interactive elements */
    button:focus, input:focus, textarea:focus {
        outline: 2px solid #3b82f6 !important;
        outline-offset: 2px;
    }
    /* Responsive adjustments */
    @media (max-width: 700px) {
        .main {
            padding: 1rem 0.5rem;
            margin-top: 1rem;
        }
        .royal-banner {
            font-size: 1.3rem;
            padding: 0.7rem 0.5rem;
        }
        .royal-card {
            padding: 0.7rem;
            font-size: 1rem;
        }
        .sidebar-title, .sidebar-card {
            font-size: 1rem;
            padding: 0.7rem 0.5rem;
        }
        .stButton>button, .rainbow-btn {
            font-size: 1rem;
            min-height: 40px;
        }
        .stTextInput>div>input, .stTextArea>div>textarea {
            font-size: 1rem;
            min-height: 36px;
        }
    }
    /* High contrast for accessibility */
    @media (prefers-contrast: more) {
        .royal-banner, .royal-card, .sidebar-card {
            background: #fff !important;
            color: #000 !important;
            border: 2px solid #000 !important;
        }
        .rainbow-btn {
            color: #000 !important;
        }
    }
    /* Accessibility: visually hidden utility class for screen readers */
    .sr-only {
        position: absolute;
        width: 1px;
        height: 1px;
        padding: 0;
        margin: -1px;
        overflow: hidden;
        clip: rect(0,0,0,0);
        border: 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Input Sanitization Utilities ---
def sanitize_input(user_input, max_length=100, allow_chars=None):
    """Sanitize user input to prevent code/HTML/script injection and limit length."""
    import html
    if not isinstance(user_input, str):
        return ""
    sanitized = user_input.strip()[:max_length]
    sanitized = html.escape(sanitized)
    if allow_chars:
        sanitized = ''.join(c for c in sanitized if c in allow_chars)
    return sanitized

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
    if "difficulty" not in st.session_state:
        st.session_state.difficulty = "Moderate"  # Default difficulty


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
    placeholder = st.empty()
    with placeholder.container():
        st.markdown('<div class="royal-banner" role="banner" aria-label="Welcome Banner">👑 Welcome to <b>The King\'s Game of Judgement!</b> 👑</div>', unsafe_allow_html=True)

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
            '<section class="royal-card" role="region" aria-label="Game Introduction">'
            '<span class="royal-label">Hark, noble one!</span><br>'
            'You are about to embark on a journey of wisdom and discernment.<br>'
            'As a venerable Judge in this kingdom, your keen intellect and balanced perspective '
            'will be called upon to resolve complex disputes.'
            '</section>', unsafe_allow_html=True)

        # Difficulty selection (only at start)
        difficulty = st.radio(
            "Select Case Difficulty:",
            ["Simple", "Moderate", "Complex"],
            index=["Simple", "Moderate", "Complex"].index(st.session_state.get("difficulty", "Moderate")),
            key="difficulty_radio_key",
            help="Choose how challenging the cases will be.",
            # ARIA label for accessibility
            label_visibility="visible"
        )
        st.session_state.difficulty = difficulty

        name_input = st.text_input("Pray, tell us your esteemed name to begin:", key="player_name_input_key", help="Enter your name to start the game.")

        st.markdown('<hr class="royal-divider" />', unsafe_allow_html=True)

        if st.button("✨ Begin My Tenure as Judge", key="begin_judge_btn", help="Start the game!", type="primary"):
            sanitized_name = sanitize_input(name_input, max_length=32, allow_chars=None)
            if sanitized_name:
                st.session_state.player_name = sanitized_name
                st.session_state.judge_name = f"Judge {sanitized_name}"
                st.session_state.game_stage = "scenario_presented"
                st.session_state.current_case_id = generate_case_id()
                with st.spinner(f"Summoning a new case for {st.session_state.judge_name}... This may take a moment."):
                    scenario_text = generate_scenario_with_llm(st.session_state.player_name, st.session_state.difficulty)
                    if not scenario_text.startswith("Error:"):
                        highlighted = highlight_important_parts_with_llm(scenario_text)
                        if not highlighted.startswith("Error:"):
                            scenario_text = highlighted
                def set_scenario(text):
                    st.session_state.current_scenario = text
                if handle_llm_response(scenario_text, set_scenario, "Failed to generate scenario: "):
                    placeholder.empty()
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.session_state.game_stage = "welcome"
            else:
                st.warning("A Judge must have a valid name! Please enter yours.")


def display_scenario_and_task():
    placeholder = st.empty()
    with placeholder.container():
        st.markdown('<div class="royal-banner" role="heading" aria-level="1">A New Case Awaits, {} <span style="font-size:1.1rem;font-weight:400;">({} Difficulty)</span></div>'.format(st.session_state.judge_name, st.session_state.difficulty), unsafe_allow_html=True)
        if st.session_state.current_scenario:
            st.markdown('<section class="royal-card" role="region" aria-label="Case Scenario"><span class="royal-label">📜 The Case Before You:</span><br>', unsafe_allow_html=True)
            st.markdown(st.session_state.current_scenario)
            st.markdown('</section>', unsafe_allow_html=True)
            st.markdown('<hr class="royal-divider" />', unsafe_allow_html=True)
            st.markdown('<section class="royal-card" role="region" aria-label="Your Task"><span class="royal-label">Your Task, {}</span><br>'.format(st.session_state.judge_name) +
                "Considering the facts, the written rules (if any were implied or provided in the scenario), "
                "and the 'human values' and 'normative choices' at play:<br><ul>"
                "<li>Who should [the disputed object/resolution] go to / What should be the outcome?</li>"
                "<li>What is your reasoning?</li>"
                "<li>What values are you prioritizing in your decision?</li>"
                "</ul>Take your time, my king! I await your wise judgment. 👑📝</section>", unsafe_allow_html=True)
            judgment_text = st.text_area("Enter your judgment here:", height=200, key="judgment_input_key", help="Describe your judgment and reasoning.")
            st.markdown('<hr class="royal-divider" />', unsafe_allow_html=True)
            if st.button("⚖️ Submit Your Judgment", key="submit_judgment_btn", help="Submit your decision!", use_container_width=True, type="primary"):
                sanitized_judgment = sanitize_input(judgment_text, max_length=1000, allow_chars=None)
                if sanitized_judgment:
                    st.session_state.player_judgment = sanitized_judgment
                    st.session_state.game_stage = "judgment_submitted"
                    placeholder.empty()
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.warning("An empty or invalid scroll offers no wisdom. Please pen your judgment.")
        else:
            st.error("Apologies, the scenario is missing. Let's try to fetch a new one.")
            if st.button("Fetch New Case", key="fetch_new_case_btn"):
                st.session_state.game_stage = "welcome"
                st.session_state.player_name = ""
                st.session_state.current_scenario = None
                st.session_state.player_judgment = ""
                st.session_state.ai_analysis = None
                st.session_state.current_case_id = None
                placeholder.empty()
                time.sleep(0.5)
                st.rerun()


def display_ai_analysis():
    placeholder = st.empty()
    with placeholder.container():
        st.balloons()
        st.markdown('<div class="royal-banner" role="heading" aria-level="1">The Royal Advisor\'s Counsel for {}</div>'.format(st.session_state.judge_name), unsafe_allow_html=True)
        if st.session_state.ai_analysis is None:
            with st.spinner(f"The Royal Advisor is diligently reviewing your judgment, {st.session_state.judge_name}... This may take a moment."):
                analysis_result = analyze_judgment_with_llm(
                    st.session_state.player_judgment,
                    st.session_state.current_scenario,
                    st.session_state.player_name
                )
                if not analysis_result.startswith("Error:"):
                    highlighted = highlight_important_parts_in_analysis_with_llm(analysis_result)
                    if not highlighted.startswith("Error:"):
                        analysis_result = highlighted
            def set_analysis(text):
                st.session_state.ai_analysis = text
            if not handle_llm_response(analysis_result, set_analysis, "Failed to get Advisor's analysis: "):
                if st.button("Try Analysis Again", key="try_analysis_btn"):
                    st.session_state.ai_analysis = None
                    st.rerun()
                return
        if st.session_state.ai_analysis:
            st.markdown('<section class="royal-card" role="region" aria-label="Advisor Analysis"><span class="royal-label">🧐 Advisor\'s Analysis:</span><br>', unsafe_allow_html=True)
            st.markdown(st.session_state.ai_analysis)
            st.markdown('</section>', unsafe_allow_html=True)
            st.markdown('<hr class="royal-divider" />', unsafe_allow_html=True)
            if st.session_state.current_case_id and st.session_state.current_scenario and st.session_state.player_judgment and st.session_state.ai_analysis:
                if not st.session_state.ai_analysis.startswith("Error:"):
                    case_path = safe_case_filename(st.session_state.current_case_id)
                    try:
                        if save_case(
                            st.session_state.current_case_id,
                            st.session_state.player_name,
                            st.session_state.current_scenario,
                            st.session_state.player_judgment,
                            st.session_state.ai_analysis,
                            case_path=case_path
                        ):
                            st.success(f"This case (ID: {st.session_state.current_case_id}) has been chronicled in the royal archives ({case_path}).")
                        else:
                            st.error("There was an issue archiving this case.")
                    except Exception as e:
                        st.error("There was a secure file handling error while archiving this case.")
                else:
                    st.info("Case not saved as the AI analysis encountered an error.")
            if st.button("📜 Hear Another Case", key="hear_another_case_btn", help="Start a new case", use_container_width=True, type="primary"):
                st.session_state.game_stage = "welcome"
                st.session_state.player_name = ""
                st.session_state.current_scenario = None
                st.session_state.player_judgment = ""
                st.session_state.ai_analysis = None
                st.session_state.current_case_id = None
                placeholder.empty()
                time.sleep(0.5)
                st.rerun()
        else:
            st.error("The Advisor seems to be indisposed. Unable to retrieve analysis at this time.")
            if st.button("Try Analysis Again", key="try_analysis_btn2"):
                st.session_state.ai_analysis = None
                st.rerun()


# --- Secure File Handling for Case Saving/Loading ---
def safe_case_filename(case_id):
    """Generate a safe filename for a case, preventing path traversal."""
    import re
    safe_id = re.sub(r'[^\w\-]', '', str(case_id))
    return os.path.join('past_cases', f'case_{safe_id}.txt')


# --- Main Application Flow ---
if not st.session_state.api_key_valid and st.session_state.game_stage != "welcome":
    st.session_state.game_stage = "welcome"

if st.session_state.game_stage == "welcome":
    display_welcome()
elif st.session_state.game_stage == "scenario_presented":
    display_scenario_and_task()
elif st.session_state.game_stage == "judgment_submitted":
    display_ai_analysis()
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
else:
    st.sidebar.markdown('<div class="sidebar-card" role="region" aria-label="Awaiting Judge">Awaiting Judge\'s arrival.</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="sidebar-card" role="region" aria-label="Cases Resolved">Cases Resolved: <b>{}</b></div>'.format(len([f for f in os.listdir('past_cases') if f.startswith('case_')]) if os.path.exists('past_cases') else 0), unsafe_allow_html=True)
st.sidebar.markdown('<hr class="royal-divider" />', unsafe_allow_html=True)
st.sidebar.markdown('<div class="sidebar-card" role="region" aria-label="How to Play">How to Play:<br><ul><li>Enter your name to begin.</li><li>Read the case and submit your judgment.</li><li>Review the Royal Advisor\'s analysis.</li><li>Try as many cases as you wish!</li></ul></div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="sidebar-card" role="region" aria-label="Powered by OpenAI">Powered by <b>OpenAI</b></div>', unsafe_allow_html=True)
if not st.session_state.api_key_valid:
    st.sidebar.markdown('<div class="sidebar-critical" role="alert" aria-label="API Key Missing">API Key Missing!</div>', unsafe_allow_html=True)
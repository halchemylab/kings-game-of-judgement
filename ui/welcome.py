# ui/welcome.py
import streamlit as st
import time
from ui.styles import sanitize_input
from llm_integration import generate_scenario_with_llm, OPENAI_API_KEY
from file_utils import generate_case_id

def handle_llm_response(response, success_callback, error_message_prefix=""):
    if isinstance(response, dict):
        if "error" in response:
            st.error(f"{error_message_prefix}{response['error']}")
            return False
        success_callback(response)
        return True
    
    if response and isinstance(response, str) and response.startswith("Error:"):
        st.error(f"{error_message_prefix}{response}")
        return False
    elif not response:
        st.error(f"{error_message_prefix}Received an empty response from the AI. Please try again.")
        return False
    else:
        success_callback(response)
        return True

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
                    scenario_data = generate_scenario_with_llm(st.session_state.player_name, st.session_state.difficulty)
                
                def set_scenario(data):
                    st.session_state.current_scenario = data.get("highlighted_scenario", data.get("scenario", ""))
                    st.session_state.characters = data.get("characters", [])
                    st.session_state.inquiry_history = []
                    st.session_state.questions_remaining = 3
                    st.session_state.selected_witness = None
                
                if handle_llm_response(scenario_data, set_scenario, "Failed to generate scenario: "):
                    placeholder.empty()
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.session_state.game_stage = "welcome"
            else:
                st.warning("A Judge must have a valid name! Please enter yours.")

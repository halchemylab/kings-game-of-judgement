# app.py
import streamlit as st
import os # For joining path in save_case success message
from llm_integration import generate_scenario_with_llm, analyze_judgment_with_llm, OPENAI_API_KEY
from file_utils import save_case, generate_case_id

# --- Page Configuration ---
st.set_page_config(
    page_title="The King's Game of Judgement",
    page_icon="👑",
    layout="wide"
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
    st.title("👑 Welcome to The King's Game of Judgement! 👑")

    if not st.session_state.api_key_valid:
        st.error(
            "OpenAI API Key is missing or not configured correctly. "
            "Please ensure your `OPENAI_API_KEY` is set in a `.env` file "
            "in the root directory of the application and that you have installed the `python-dotenv` package."
        )
        st.markdown("Your `.env` file should look like this:\n```\nOPENAI_API_KEY=\"your_actual_api_key_here\"\n```")
        st.stop() # Halt execution if API key is not set up

    st.markdown("""
    Hark, noble one! You are about to embark on a journey of wisdom and discernment.
    As a venerable Judge in this kingdom, your keen intellect and balanced perspective
    will be called upon to resolve complex disputes.
    """)
    
    name_input = st.text_input("Pray, tell us your esteemed name to begin:", key="player_name_input_key") # Changed key to avoid conflict
    
    if st.button("Begin My Tenure as Judge"):
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
                # Error handled by handle_llm_response, user can try again or fix API key
                st.session_state.game_stage = "welcome" # Stay on welcome page if error
        else:
            st.warning("A Judge must have a name! Please enter yours.")

def display_scenario_and_task():
    st.header(f"A New Case Awaits, {st.session_state.judge_name}")
    
    if st.session_state.current_scenario:
        st.markdown("---")
        st.subheader("📜 The Case Before You:")
        st.markdown(st.session_state.current_scenario)
        st.markdown("---")

        st.subheader(f"Your Task, {st.session_state.judge_name}:")
        st.markdown(f"""
        Considering the facts, the written rules (if any were implied or provided in the scenario), 
        and the 'human values' and 'normative choices' at play:

        *   Who should [the disputed object/resolution] go to / What should be the outcome?
        *   What is your reasoning?
        *   What values are you prioritizing in your decision?

        Take your time, my king! I await your wise judgment. 👑📝
        """)

        judgment_text = st.text_area("Enter your judgment here:", height=300, key="judgment_input_key") # Changed key

        if st.button("⚖️ Submit Your Judgment"):
            if judgment_text.strip():
                st.session_state.player_judgment = judgment_text.strip()
                st.session_state.game_stage = "judgment_submitted"
                st.rerun()
            else:
                st.warning("An empty scroll offers no wisdom. Please pen your judgment.")
    else:
        # This case should ideally be caught earlier during scenario generation
        st.error("Apologies, the scenario is missing. Let's try to fetch a new one.")
        if st.button("Fetch New Case"):
            st.session_state.game_stage = "welcome" # Reset to re-trigger name and scenario gen
            st.session_state.player_name = "" # Force re-entry or re-confirmation
            st.rerun()


def display_ai_analysis():
    st.header(f"The Royal Advisor's Counsel for {st.session_state.judge_name}")
    
    if st.session_state.ai_analysis is None: # Analysis not yet generated
        with st.spinner(f"The Royal Advisor is diligently reviewing your judgment, {st.session_state.judge_name}... This may take a moment."):
            analysis_result = analyze_judgment_with_llm(
                st.session_state.player_judgment,
                st.session_state.current_scenario,
                st.session_state.player_name
            )
        
        def set_analysis(text):
            st.session_state.ai_analysis = text

        if not handle_llm_response(analysis_result, set_analysis, "Failed to get Advisor's analysis: "):
            # Error displayed by handle_llm_response. Allow user to try again or proceed.
            # Optionally, could add a button here to "Try generating analysis again"
            if st.button("Try Analysis Again"):
                 st.session_state.ai_analysis = None # Reset to trigger re-analysis
                 st.rerun()
            return # Stop further processing if analysis failed

    if st.session_state.ai_analysis:
        st.markdown("---")
        st.subheader("🧐 Advisor's Analysis:")
        st.markdown(st.session_state.ai_analysis)
        st.markdown("---")

        # Save the case
        if st.session_state.current_case_id and st.session_state.current_scenario and st.session_state.player_judgment and st.session_state.ai_analysis:
            # Ensure analysis is not an error message before saving
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
        
        if st.button("Hear Another Case 📜"):
            # Reset for a new case
            st.session_state.game_stage = "scenario_presented"
            st.session_state.current_scenario = None # Will be fetched
            st.session_state.player_judgment = ""
            st.session_state.ai_analysis = None
            st.session_state.current_case_id = generate_case_id()
            
            with st.spinner(f"Summoning a new challenge for {st.session_state.judge_name}... This may take a moment."):
                scenario_text = generate_scenario_with_llm(st.session_state.player_name)
            
            def set_scenario(text):
                st.session_state.current_scenario = text

            if handle_llm_response(scenario_text, set_scenario, "Failed to generate new scenario: "):
                 st.rerun()
            else:
                # Error handled, stay on current page or revert to welcome
                st.session_state.game_stage = "welcome" # Revert to welcome if new scenario fails critically
                st.rerun()

    else:
        # This state should be covered by the loading spinner and handle_llm_response logic
        st.error("The Advisor seems to be indisposed. Unable to retrieve analysis at this time.")
        if st.button("Try Analysis Again"):
            st.session_state.ai_analysis = None # Reset to trigger re-analysis
            st.rerun()


# --- Main Application Flow ---
if not st.session_state.api_key_valid and st.session_state.game_stage != "welcome":
    # If API key becomes invalid mid-game (e.g., after app restart without .env)
    st.session_state.game_stage = "welcome" # Force back to welcome to show API key error

if st.session_state.game_stage == "welcome":
    display_welcome()
elif st.session_state.game_stage == "scenario_presented":
    if not st.session_state.player_name or not st.session_state.api_key_valid:
        st.session_state.game_stage = "welcome"
        st.rerun()
    else:
        display_scenario_and_task()
elif st.session_state.game_stage == "judgment_submitted":
    if not st.session_state.api_key_valid:
        st.session_state.game_stage = "welcome"
        st.rerun()
    else:
        display_ai_analysis()
else:
    st.error("An unexpected error occurred in the game flow. Resetting.")
    st.session_state.game_stage = "welcome"
    st.rerun()

# --- Sidebar ---
st.sidebar.header("Game Information")
if st.session_state.player_name:
    st.sidebar.write(f"Current Judge: {st.session_state.judge_name}")
else:
    st.sidebar.write("Awaiting Judge's arrival.")

st.sidebar.markdown("---")
st.sidebar.caption("The King's Game of Judgement v0.2 (OpenAI Powered)")
if not st.session_state.api_key_valid:
    st.sidebar.error("API Key Missing!")
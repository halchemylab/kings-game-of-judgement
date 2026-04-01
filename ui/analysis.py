# ui/analysis.py
import streamlit as st
import time
import os
from llm_integration import analyze_judgment_with_llm
from file_utils import save_case
from ui.welcome import handle_llm_response
from models import Analysis, CaseRecord

def display_ai_analysis():
    placeholder = st.empty()
    with placeholder.container():
        st.balloons()
        st.markdown('<div class="royal-banner" role="heading" aria-level="1">The Royal Advisor\'s Counsel for {}</div>'.format(st.session_state.judge_name), unsafe_allow_html=True)
        if st.session_state.ai_analysis is None:
            with st.spinner(f"The Royal Advisor is diligently reviewing your judgment, {st.session_state.judge_name}... This may take a moment."):
                analysis_data = analyze_judgment_with_llm(
                    st.session_state.player_judgment,
                    st.session_state.current_scenario,
                    st.session_state.player_name
                )
            
            def set_analysis(data):
                if isinstance(data, Analysis):
                    st.session_state.ai_analysis = data.highlighted_analysis
                else:
                    st.session_state.ai_analysis = data.get("highlighted_analysis", data.get("analysis", ""))
            
            if not handle_llm_response(analysis_data, set_analysis, "Failed to get Advisor's analysis: "):
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
                    try:
                        case_record = CaseRecord(
                            case_id=st.session_state.current_case_id,
                            player_name=st.session_state.player_name,
                            difficulty=st.session_state.difficulty,
                            scenario=st.session_state.current_scenario,
                            inquiry_history=st.session_state.inquiry_history,
                            judgment=st.session_state.player_judgment,
                            analysis=st.session_state.ai_analysis
                        )
                        if save_case(case_record):
                            st.success(f"This case (ID: {st.session_state.current_case_id}) has been chronicled in the royal archives.")
                        else:
                            st.error("There was an issue archiving this case.")
                    except Exception as e:
                        print(f"Error creating CaseRecord or saving: {e}")
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

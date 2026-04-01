# ui/analysis.py
import streamlit as st
import time
import os
from llm_integration import analyze_judgment_with_llm
from file_utils import save_case
from ui.welcome import handle_llm_response

def safe_case_filename(case_id):
    """Generate a safe filename for a case, preventing path traversal."""
    import re
    safe_id = re.sub(r'[^\w\-]', '', str(case_id))
    return os.path.join('past_cases', f'case_{safe_id}.txt')

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
                    case_path = safe_case_filename(st.session_state.current_case_id)
                    try:
                        if save_case(
                            st.session_state.current_case_id,
                            st.session_state.player_name,
                            st.session_state.current_scenario,
                            st.session_state.player_judgment,
                            st.session_state.ai_analysis,
                            inquiry_history=st.session_state.inquiry_history,
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

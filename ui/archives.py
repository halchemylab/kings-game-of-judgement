# ui/archives.py
import streamlit as st
from file_utils import list_past_cases, load_case
from models import CaseRecord

def display_archives():
    placeholder = st.empty()
    with placeholder.container():
        st.markdown('<div class="royal-banner" role="heading" aria-level="1">The Royal Archives</div>', unsafe_allow_html=True)
        
        past_cases = list_past_cases()
        if not past_cases:
            st.info("The royal archives are currently empty. Resolve some cases to see them here!")
            if st.button("Back to Kingdom", key="back_to_kingdom_empty_btn"):
                st.session_state.game_stage = "welcome"
                st.rerun()
            return

        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown('<span class="royal-label">Select a Case:</span>', unsafe_allow_html=True)
            for case_file in past_cases:
                # Format label for better readability (e.g., from case_20240325_... to 2024-03-25 ...)
                label = case_file.replace("case_", "").replace(".json", "").replace(".txt", "").replace("_", " ")
                if st.button(f"📜 {label}", key=f"select_{case_file}"):
                    st.session_state.selected_archive_case = case_file
            
            st.markdown('<hr class="royal-divider" />', unsafe_allow_html=True)
            if st.button("🔙 Back to Kingdom", key="back_to_kingdom_btn", use_container_width=True):
                st.session_state.game_stage = "welcome"
                st.session_state.selected_archive_case = None
                st.rerun()

        with col2:
            if st.session_state.selected_archive_case:
                case_data = load_case(st.session_state.selected_archive_case)
                if case_data:
                    # case_data is now a CaseRecord object or a dict (if legacy TXT fallback worked)
                    if isinstance(case_data, CaseRecord):
                        st.markdown(f'<section class="royal-card"><b>Case ID:</b> {case_data.case_id}<br><b>Date:</b> {case_data.date}<br><b>Judge:</b> {case_data.player_name}<br><b>Difficulty:</b> {case_data.difficulty}</section>', unsafe_allow_html=True)
                        
                        st.markdown('<section class="royal-card"><span class="royal-label">📜 The Case:</span><br>', unsafe_allow_html=True)
                        st.markdown(case_data.scenario)
                        st.markdown('</section>', unsafe_allow_html=True)
                        
                        if case_data.inquiry_history:
                            st.markdown('<section class="royal-card"><span class="royal-label">🕵️ Investigation:</span><br>', unsafe_allow_html=True)
                            for entry in case_data.inquiry_history:
                                st.markdown(f"**To {entry.character}:** {entry.question}")
                                st.markdown(f"**Response:** {entry.response}")
                                st.markdown("---")
                            st.markdown('</section>', unsafe_allow_html=True)
                        
                        st.markdown('<section class="royal-card"><span class="royal-label">⚖️ Judgment:</span><br>', unsafe_allow_html=True)
                        st.markdown(case_data.judgment)
                        st.markdown('</section>', unsafe_allow_html=True)
                        
                        st.markdown('<section class="royal-card" style="background:#fefce8;"><span class="royal-label">🧐 Advisor\'s Analysis:</span><br>', unsafe_allow_html=True)
                        st.markdown(case_data.analysis)
                        st.markdown('</section>', unsafe_allow_html=True)
                    else:
                        # Legacy dict fallback
                        st.markdown(f'<section class="royal-card"><b>Case ID:</b> {case_data.get("case_id")}<br><b>Date:</b> {case_data.get("date")}<br><b>Judge:</b> {case_data.get("player_name")}</section>', unsafe_allow_html=True)
                        
                        st.markdown('<section class="royal-card"><span class="royal-label">📜 The Case:</span><br>', unsafe_allow_html=True)
                        st.markdown(case_data.get("scenario"))
                        st.markdown('</section>', unsafe_allow_html=True)
                        
                        if case_data.get("inquiry"):
                            st.markdown('<section class="royal-card"><span class="royal-label">🕵️ Investigation:</span><br>', unsafe_allow_html=True)
                            st.markdown(case_data.get("inquiry"))
                            st.markdown('</section>', unsafe_allow_html=True)
                        
                        st.markdown('<section class="royal-card"><span class="royal-label">⚖️ Judgment:</span><br>', unsafe_allow_html=True)
                        st.markdown(case_data.get("judgment"))
                        st.markdown('</section>', unsafe_allow_html=True)
                        
                        st.markdown('<section class="royal-card" style="background:#fefce8;"><span class="royal-label">🧐 Advisor\'s Analysis:</span><br>', unsafe_allow_html=True)
                        st.markdown(case_data.get("analysis"))
                        st.markdown('</section>', unsafe_allow_html=True)
                else:
                    st.error("Failed to load case data.")
            else:
                st.info("Select a scroll from the left to read its chronicles.")

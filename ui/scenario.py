# ui/scenario.py
import streamlit as st
import time
from ui.styles import sanitize_input
from llm_integration import get_witness_response_with_llm
from models import WitnessResponse, InquiryEntry

def display_scenario_and_task():
    placeholder = st.empty()
    with placeholder.container():
        st.markdown('<div class="royal-banner" role="heading" aria-level="1">A New Case Awaits, {} <span style="font-size:1.1rem;font-weight:400;">({} Difficulty)</span></div>'.format(st.session_state.judge_name, st.session_state.difficulty), unsafe_allow_html=True)
        if st.session_state.current_scenario:
            st.markdown('<section class="royal-card" role="region" aria-label="Case Scenario"><span class="royal-label">📜 The Case Before You:</span><br>', unsafe_allow_html=True)
            st.markdown(st.session_state.current_scenario)
            st.markdown('</section>', unsafe_allow_html=True)
            st.markdown('<hr class="royal-divider" />', unsafe_allow_html=True)

            # --- Witness Inquiry Section ---
            if st.session_state.characters:
                st.markdown('<section class="royal-card" role="region" aria-label="Summon Witnesses"><span class="royal-label">📜 Summon the Witnesses:</span><br>'
                            f'You may summon up to {st.session_state.questions_remaining} more witnesses or ask further questions.', unsafe_allow_html=True)
                
                cols = st.columns(len(st.session_state.characters))
                for i, char in enumerate(st.session_state.characters):
                    if cols[i].button(f"👤 {char}", key=f"char_{i}"):
                        st.session_state.selected_witness = char
                
                if st.session_state.selected_witness:
                    st.markdown(f"**Questioning: {st.session_state.selected_witness}**")
                    if st.session_state.questions_remaining > 0:
                        q_input = st.text_input("What is your question, Sire?", key="witness_q_input")
                        if st.button("Ask Question", key="ask_q_btn"):
                            if q_input:
                                with st.spinner(f"{st.session_state.selected_witness} is preparing a response..."):
                                    resp_data = get_witness_response_with_llm(
                                        st.session_state.current_scenario,
                                        st.session_state.selected_witness,
                                        q_input
                                    )
                                
                                response_text = ""
                                if isinstance(resp_data, WitnessResponse):
                                    response_text = resp_data.response
                                elif isinstance(resp_data, dict) and "response" in resp_data:
                                    response_text = resp_data["response"]
                                
                                if response_text:
                                    st.session_state.inquiry_history.append(InquiryEntry(
                                        character=st.session_state.selected_witness,
                                        question=q_input,
                                        response=response_text
                                    ))
                                    st.session_state.questions_remaining -= 1
                                    st.rerun()
                            else:
                                st.warning("The King must speak his mind. Please enter a question.")
                    else:
                        st.info("You have exhausted your inquiries for this case.")

                if st.session_state.inquiry_history:
                    st.markdown("---")
                    for entry in st.session_state.inquiry_history:
                        # Handle both models and legacy dicts (though new should be models)
                        if isinstance(entry, InquiryEntry):
                            st.markdown(f"**You asked {entry.character}:** *{entry.question}*")
                            st.markdown(f"**{entry.character} says:** {entry.response}")
                        else:
                            st.markdown(f"**You asked {entry['character']}:** *{entry['question']}*")
                            st.markdown(f"**{entry['character']} says:** {entry['response']}")
                
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

# llm_integration.py
import os
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_TO_USE = "gpt-4o" # Specify the model here

# Initialize OpenAI client globally if API key is available
if OPENAI_API_KEY:
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
else:
    client = None # Will be checked in functions

# --- LLM PROMPT DESIGNS (Remain the same as before) ---

# Prompt for Scenario Generation
SCENARIO_GENERATION_PROMPT_TEMPLATE = """
You are a master storyteller and game designer. Your task is to create a concise and compelling legal or ethical dilemma scenario for "The King's Game of Judgement," where the player acts as a wise king or judge.

The scenario should be suitable for a text-based adventure game and must include:
1.  **Clearly defined parties:** For example, "Villager Alaric (the plaintiff)" and "Guildmaster Borin (the defendant)." You can invent thematic names.
2.  **A specific object or issue of dispute:** For example, "a contested plot of fertile land," "an inheritance of a renowned smithy," "a broken contract for a rare artifact," or "the rightful ownership of a unique draft animal."
3.  **A compelling set of background facts:** Briefly explain how the dispute arose, providing context and motivations for each party. Make it feel like a real, perhaps medieval or fantastical, situation.
4.  **The core dispute or question that needs resolving:** Clearly state what the judge needs to decide. For instance, "Who is the rightful owner of the land?" or "Should Guildmaster Borin compensate Villager Alaric, and if so, how?"
5.  **A neutral tone:** Present the facts objectively, allowing the player (the Judge) to form their own conclusions. Do not imply a "correct" answer.
6.  **Brevity:** The entire scenario should be no more than 3-4 short paragraphs.

The scenario should begin by addressing the judge directly, using second person ("Before you stand two individuals..." or similar). Do NOT mention the judge's name or title; simply refer to them as "you" throughout.

DIFFICULTY: The scenario should be written at a "{difficulty}" level. For "Simple," keep the facts and dispute straightforward, with minimal ambiguity. For "Moderate," introduce some complexity, competing interests, or subtle ambiguities. For "Complex," make the scenario multi-layered, with conflicting values, unclear facts, and significant moral or legal dilemmas.

Do not include any preamble like "Okay, here's a scenario:". Just provide the scenario text directly.
Ensure the scenario is engaging and presents a genuine dilemma.
"""

# Prompt for Judgment Analysis
JUDGMENT_ANALYSIS_PROMPT_TEMPLATE = """
You are an insightful and highly supportive Royal Advisor to Judge {player_name} in "The King's Game of Judgement."
The Judge has just reviewed a complex scenario and rendered their judgment. Your role is to provide thoughtful, constructive, and encouraging feedback on their decision-making process.

The scenario presented was:
--- SCENARIO START ---
{scenario_details}
--- SCENARIO END ---

Judge {player_name}'s judgment was:
--- JUDGMENT START ---
{player_judgment}
--- JUDGMENT END ---

Your analysis should adhere to the following guidelines:

1.  **Acknowledge and Praise:** Begin by acknowledging the Judge's effort and the thoughtfulness of their judgment. Use respectful and encouraging language, like "Wow, Judge {player_name}, that's a truly insightful/well-reasoned/thoughtful judgment!" or "A most wise decision, Judge {player_name}!"
2.  **Identify Key Aspects of the Judgment:** Briefly summarize or highlight the core components of the Judge's decision: who they sided with (if applicable), their proposed resolution, and their primary reasoning.
3.  **Analyze Prioritized Values:** Discuss the values the Judge appeared to prioritize (e.g., fairness, compassion, adherence to rules, community harmony, individual rights, economic stability, precedent). If they explicitly stated their prioritized values, comment on that.
4.  **Connect to "Human Values" and "Normative Choices":** Evaluate how the judgment considered the human elements, ethical considerations, and societal norms relevant to the scenario. Did they balance competing interests effectively? How did they navigate any ambiguities or moral gray areas?
5.  **Interpretation of Facts:** Comment on how the Judge interpreted the facts of the scenario. Were there any assumptions made? Were there alternative interpretations of the facts that could lead to different conclusions?
6.  **Constructive Feedback (if applicable):** If there are alternative perspectives, potential unintended consequences of the judgment, or aspects that could have been explored further, present these gently and constructively. Frame these as "additional considerations" or "alternative viewpoints to ponder for future deliberations" rather than criticisms. For example: "One might also consider..." or "Another perspective, for future reflection, could be that..."
7.  **Reinforce Strengths:** Highlight what the Judge did particularly well (e.g., clear articulation of reasoning, empathy shown, astute understanding of the core issue, balanced approach).
8.  **Supportive and Encouraging Tone:** Maintain a consistently positive, supportive, and respectful tone throughout. The goal is to make the Judge feel empowered, validated, and keen to continue learning and judging, even when offering suggestions.
9.  **Kingly Theme & Conclusion:** Conclude with a strong, positive affirmation fitting the "kingly" theme, such as "Excellent work, Judge {player_name}! Your wisdom shines brightly in this realm and guides us towards justice." or "The kingdom is fortunate to have your judicious mind, Judge {player_name}! Well done."

Do not include any preamble like "Okay, here's my analysis:". Just provide the analysis text directly.
Be specific in your feedback, referring to parts of the scenario and the judgment.
"""

# --- Highlight Important Parts Prompt ---
HIGHLIGHT_IMPORTANT_PARTS_PROMPT_TEMPLATE = """
Given the following scenario from a legal/ethical game, identify and highlight the most important names, objects, and facts by wrapping them in double asterisks for bold (Markdown: **like this**). Do not use any colors or HTML, only Markdown bold. Return the scenario with the important parts bolded, preserving the original structure and wording as much as possible.

Scenario:
{scenario}
"""

# --- Highlight Important Parts in Analysis Prompt ---
HIGHLIGHT_ANALYSIS_IMPORTANT_PARTS_PROMPT_TEMPLATE = """
Given the following analysis from a legal/ethical game, identify and highlight the most important names, values, and conclusions by wrapping them in double asterisks for bold (Markdown: **like this**). Do not use any colors or HTML, only Markdown bold. Return the analysis with the important parts bolded, preserving the original structure and wording as much as possible.

Analysis:
{analysis}
"""

# --- LLM API FUNCTIONS ---

def generate_scenario_with_llm(player_name, difficulty="Moderate"):
    """
    Generates a scenario by calling the OpenAI API, with difficulty support.
    Ensures the judge's name is passed correctly and consistently.
    """
    if not client:
        return "Error: OpenAI API key not configured. Please set OPENAI_API_KEY in your .env file."

    # Always pass the raw player_name (not prefixed with 'Judge')
    prompt = SCENARIO_GENERATION_PROMPT_TEMPLATE.format(player_name=player_name, difficulty=difficulty)
    try:
        response = client.chat.completions.create(
            model=MODEL_TO_USE,
            messages=[
                {"role": "system", "content": "You are a master storyteller creating scenarios for a game."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8, # Add some creativity
            max_tokens=500   # Ensure scenario is not excessively long
        )
        scenario_text = response.choices[0].message.content.strip()
        # Replace any incorrect judge name with the correct one (force consistency)
        scenario_text = scenario_text.replace(f"Judge {player_name}", f"Judge {player_name}")
        return scenario_text
    except openai.APIConnectionError as e:
        print(f"OpenAI API Connection Error: {e}")
        return f"Error: Failed to connect to the Royal Scribes (OpenAI API: {e}). Please check your connection and API key."
    except openai.RateLimitError as e:
        print(f"OpenAI API Rate Limit Error: {e}")
        return f"Error: The Royal Scribes are overwhelmed at the moment (Rate limit exceeded: {e}). Please try again later."
    except openai.APIStatusError as e:
        print(f"OpenAI API Status Error: {e}")
        return f"Error: The Royal Scribes report an issue (API Status {e.status_code}: {e.response}). Please try again later."
    except Exception as e:
        print(f"An unexpected error occurred during scenario generation: {e}")
        return f"Error: An unexpected disturbance in the æther (Error: {e}). The scribes are confused."


def analyze_judgment_with_llm(player_judgment, scenario_details, player_name):
    """
    Analyzes the player's judgment by calling the OpenAI API.
    """
    if not client:
        return "Error: OpenAI API key not configured. Please set OPENAI_API_KEY in your .env file."

    prompt = JUDGMENT_ANALYSIS_PROMPT_TEMPLATE.format(
        player_name=player_name,
        scenario_details=scenario_details,
        player_judgment=player_judgment
    )

    try:
        response = client.chat.completions.create(
            model=MODEL_TO_USE,
            messages=[
                {"role": "system", "content": "You are an insightful and supportive Royal Advisor."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=700 # Allow for detailed analysis
        )
        analysis_text = response.choices[0].message.content.strip()
        return analysis_text
    except openai.APIConnectionError as e:
        print(f"OpenAI API Connection Error: {e}")
        return f"Error: Failed to connect to the Royal Advisor (OpenAI API: {e}). Please check your connection and API key."
    except openai.RateLimitError as e:
        print(f"OpenAI API Rate Limit Error: {e}")
        return f"Error: The Royal Advisor is very busy (Rate limit exceeded: {e}). Please try again later."
    except openai.APIStatusError as e:
        print(f"OpenAI API Status Error: {e}")
        return f"Error: The Royal Advisor reports an issue (API Status {e.status_code}: {e.response}). Please try again later."
    except Exception as e:
        print(f"An unexpected error occurred during judgment analysis: {e}")
        return f"Error: An unexpected disturbance in the æther (Error: {e}). The advisor is momentarily perplexed."


def highlight_important_parts_with_llm(scenario_text):
    """
    Calls the LLM to bold important parts of the scenario using Markdown.
    """
    if not client:
        return "Error: OpenAI API key not configured. Please set OPENAI_API_KEY in your .env file."
    prompt = HIGHLIGHT_IMPORTANT_PARTS_PROMPT_TEMPLATE.format(scenario=scenario_text)
    try:
        response = client.chat.completions.create(
            model=MODEL_TO_USE,
            messages=[
                {"role": "system", "content": "You are an assistant that highlights important parts of a scenario for a game using Markdown bold only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=600
        )
        highlighted_text = response.choices[0].message.content.strip()
        return highlighted_text
    except Exception as e:
        print(f"Error during highlighting: {e}")
        return f"Error: Could not highlight important parts ({e})"

def highlight_important_parts_in_analysis_with_llm(analysis_text):
    """
    Calls the LLM to bold important parts of the analysis using Markdown.
    """
    if not client:
        return "Error: OpenAI API key not configured. Please set OPENAI_API_KEY in your .env file."
    prompt = HIGHLIGHT_ANALYSIS_IMPORTANT_PARTS_PROMPT_TEMPLATE.format(analysis=analysis_text)
    try:
        response = client.chat.completions.create(
            model=MODEL_TO_USE,
            messages=[
                {"role": "system", "content": "You are an assistant that highlights important parts of an analysis for a game using Markdown bold only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=700
        )
        highlighted_text = response.choices[0].message.content.strip()
        return highlighted_text
    except Exception as e:
        print(f"Error during analysis highlighting: {e}")
        return f"Error: Could not highlight important parts in analysis ({e})"
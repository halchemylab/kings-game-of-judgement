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

# --- LLM PROMPT DESIGNS ---

# Prompt for Scenario Generation (JSON)
SCENARIO_GENERATION_JSON_PROMPT_TEMPLATE = """
You are a master storyteller and game designer. Your task is to create a concise and compelling legal or ethical dilemma scenario for "The King's Game of Judgement," where the player acts as a wise king or judge.

The scenario must include:
1. Clearly defined parties with thematic names.
2. A specific object or issue of dispute.
3. Compelling background facts.
4. The core dispute that needs resolving.
5. A neutral, objective tone.
6. Brevity (3-4 short paragraphs).

DIFFICULTY: {difficulty}. Adjust complexity based on this level.

In addition to the raw scenario, provide a version where important names, objects, and facts are wrapped in double asterisks for bold (Markdown: **like this**).

Return your response as a JSON object with the following keys:
- "scenario": The raw text of the scenario.
- "highlighted_scenario": The scenario text with key parts bolded using Markdown.
"""

# Prompt for Judgment Analysis (JSON)
JUDGMENT_ANALYSIS_JSON_PROMPT_TEMPLATE = """
You are an insightful and highly supportive Royal Advisor to Judge {player_name} in "The King's Game of Judgement."
Provide thoughtful, constructive feedback on the Judge's decision.

Scenario: {scenario_details}
Judge {player_name}'s judgment: {player_judgment}

Analysis Guidelines:
1. Acknowledge and praise the effort.
2. Summarize the core components of the decision.
3. Analyze prioritized values (fairness, compassion, etc.).
4. Evaluate consideration of human elements and norms.
5. Comment on interpretation of facts and assumptions.
6. Provide gentle alternative perspectives if applicable.
7. Reinforce strengths and maintain a kingly, supportive tone.

In addition to the raw analysis, provide a version where important names, values, and conclusions are wrapped in double asterisks for bold (Markdown: **like this**).

Return your response as a JSON object with the following keys:
- "analysis": The raw text of the advisor's analysis.
- "highlighted_analysis": The analysis text with key parts bolded using Markdown.
"""

# --- LLM API FUNCTIONS ---

import json

def generate_scenario_with_llm(player_name, difficulty="Moderate"):
    """
    Generates a structured scenario (raw and highlighted) in a single LLM call.
    """
    if not client:
        return {"error": "OpenAI API key not configured."}

    prompt = SCENARIO_GENERATION_JSON_PROMPT_TEMPLATE.format(difficulty=difficulty)
    try:
        response = client.chat.completions.create(
            model=MODEL_TO_USE,
            messages=[
                {"role": "system", "content": "You are a master storyteller. Respond ONLY with a JSON object containing 'scenario' and 'highlighted_scenario'."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.8,
            max_tokens=1000
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"Error during scenario generation: {e}")
        return {"error": str(e)}


def analyze_judgment_with_llm(player_judgment, scenario_details, player_name):
    """
    Analyzes the player's judgment (raw and highlighted) in a single LLM call.
    """
    if not client:
        return {"error": "OpenAI API key not configured."}

    prompt = JUDGMENT_ANALYSIS_JSON_PROMPT_TEMPLATE.format(
        player_name=player_name,
        scenario_details=scenario_details,
        player_judgment=player_judgment
    )

    try:
        response = client.chat.completions.create(
            model=MODEL_TO_USE,
            messages=[
                {"role": "system", "content": "You are a supportive Royal Advisor. Respond ONLY with a JSON object containing 'analysis' and 'highlighted_analysis'."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.7,
            max_tokens=1200
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"Error during judgment analysis: {e}")
        return {"error": str(e)}

# Deprecated functions kept for compatibility if needed, but updated to use new logic internally or return errors.
def highlight_important_parts_with_llm(scenario_text):
    return "Error: Use generate_scenario_with_llm for consolidated results."

def highlight_important_parts_in_analysis_with_llm(analysis_text):
    return "Error: Use analyze_judgment_with_llm for consolidated results."
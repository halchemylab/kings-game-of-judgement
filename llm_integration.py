# llm_integration.py
import os
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_TO_USE = os.getenv("OPENAI_MODEL", "gpt-4o")
CHEAP_MODEL_TO_USE = os.getenv("OPENAI_CHEAP_MODEL", "gpt-4o-mini")

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

DIFFICULTY LEVEL: {difficulty}
Strictly follow these structural constraints based on the difficulty:
- **Simple**: Focus on exactly two parties and one clear physical object of dispute. The moral choice should be straightforward, testing basic fairness.
- **Moderate**: Introduce a third party or a conflicting cultural norm/local law. The dispute should involve secondary consequences or multiple valid points of view.
- **Complex**: Involve systemic societal issues, multiple conflicting values (e.g., mercy vs. strict justice), and ambiguous facts where no single "perfect" answer exists. The decision should have long-term implications for the kingdom.

In addition to the raw scenario, provide a version where important names, objects, and facts are wrapped in double asterisks for bold (Markdown: **like this**).

Return your response as a JSON object with the following keys:
- "scenario": The raw text of the scenario.
- "highlighted_scenario": The scenario text with key parts bolded using Markdown.
- "characters": A list of 2-3 key characters involved in the dispute (e.g., ["The Accused Merchant", "The Royal Guard"]).
"""

# Prompt for Witness Roleplay (JSON)
WITNESS_ROLEPLAY_PROMPT_TEMPLATE = """
You are performing as a character in "The King's Game of Judgement."
The player (The King/Judge) is asking you a question to help them reach a decision.

Scenario: {scenario_details}
Your Character: {character_name}
The King's Question: {question}

Guidelines:
1. Stay strictly in character. Use a thematic tone (e.g., humble, defensive, or wise).
2. Do not reveal facts outside of what is mentioned or strongly implied in the scenario.
3. If the question asks for something you wouldn't know, respond naturally as the character (e.g., "I saw nothing of the sort, Sire!").
4. Keep the response concise (2-3 sentences).
5. Do not give the "correct" answer to the case; only provide your perspective or "testimony."

Return your response as a JSON object with the following key:
- "response": The character's spoken response to the King.
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
- "thought_process": Your internal, step-by-step reasoning about the case and the judgment. Use this to ensure your final analysis is logical and consistent. This part will be hidden from the player.
- "analysis": The raw text of the advisor's analysis.
- "highlighted_analysis": The analysis text with key parts bolded using Markdown.
"""

# --- LLM API FUNCTIONS ---

import json

def generate_scenario_with_llm(player_name, difficulty="Moderate", model=CHEAP_MODEL_TO_USE):
    """
    Generates a structured scenario (raw and highlighted) in a single LLM call.
    Uses a cheaper model by default to save costs.
    """
    if not client:
        return {"error": "OpenAI API key not configured."}

    prompt = SCENARIO_GENERATION_JSON_PROMPT_TEMPLATE.format(difficulty=difficulty)
    try:
        response = client.chat.completions.create(
            model=model,
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
                {"role": "system", "content": "You are a supportive Royal Advisor. Respond ONLY with a JSON object containing 'thought_process', 'analysis', and 'highlighted_analysis'."},
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


def get_witness_response_with_llm(scenario, character, question, model=CHEAP_MODEL_TO_USE):
    """
    Simulates a witness or character response based on the scenario and a player's question.
    """
    if not client:
        return {"error": "OpenAI API key not configured."}

    prompt = WITNESS_ROLEPLAY_PROMPT_TEMPLATE.format(
        scenario_details=scenario,
        character_name=character,
        question=question
    )

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a character in a medieval kingdom. Respond ONLY with a JSON object containing 'response'."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.7,
            max_tokens=500
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"Error during witness response: {e}")
        return {"error": str(e)}


# Deprecated functions kept for compatibility if needed, but updated to use new logic internally or return errors.
def highlight_important_parts_with_llm(scenario_text):
    return "Error: Use generate_scenario_with_llm for consolidated results."

def highlight_important_parts_in_analysis_with_llm(analysis_text):
    return "Error: Use analyze_judgment_with_llm for consolidated results."
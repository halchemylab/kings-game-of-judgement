# The King's Game of Judgement

A text-based, interactive ethical and legal dilemma game powered by OpenAI's GPT-4o and Streamlit.

## Overview

**The King's Game of Judgement** places you in the role of a wise judge in a fantastical kingdom. You will be presented with unique, AI-generated cases involving disputes, moral quandaries, and legal dilemmas. After rendering your judgment, a Royal Advisor (powered by GPT-4o) provides thoughtful, supportive analysis of your decision.

## Features
- **AI-Generated Scenarios:** Each case is crafted by GPT-4o, with adjustable difficulty (Simple, Moderate, Complex).
- **Interactive Judging:** Enter your judgment and reasoning for each scenario.
- **Royal Advisor Feedback:** Receive detailed, encouraging analysis of your decisions from the AI.
- **Case Archiving:** All resolved cases are saved locally for review.
- **Modern, Accessible UI:** Built with Streamlit, featuring custom styling and accessibility enhancements.

## Demo
![Screenshot of The King's Game of Judgement](screenshot.png) <!-- Add a screenshot if available -->

## Getting Started

### Prerequisites
- Python 3.8+
- An OpenAI API key ([get one here](https://platform.openai.com/account/api-keys))

### Installation
1. **Clone the repository:**
   ```sh
   git clone <repo-url>
   cd kings-game-of-judgement
   ```
2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
3. **Set up your environment variables:**
   - Create a `.env` file in the project root:
     ```env
     OPENAI_API_KEY=your_openai_api_key_here
     ```
   - Do **not** use quotes around the API key.

### Running the App
```sh
streamlit run app.py
```

The app will open in your browser. Enter your name, select a difficulty, and begin judging cases!

## File Structure
- `app.py` — Main Streamlit app and UI logic
- `llm_integration.py` — Handles all OpenAI API interactions and prompt templates
- `file_utils.py` — Utilities for saving and listing past cases
- `requirements.txt` — Python dependencies
- `.env` — Your OpenAI API key (not committed to git)
- `past_cases/` — Saved case files (auto-created)

## Environment Variables
- `OPENAI_API_KEY` — Your OpenAI API key (required)

## Troubleshooting
- **API Key Errors:**
  - Ensure `.env` is in the project root and contains `OPENAI_API_KEY=...` (no quotes).
  - Restart the app after editing `.env`.
  - Your key must be active and have GPT-4o access.
- **No Scenarios/Analysis:**
  - Check your internet connection.
  - Review the Streamlit logs for error messages.

## Security & Privacy
- Your API key is never shared or logged.
- All case data is stored locally in `past_cases/`.

## License
MIT License. See [LICENSE](LICENSE) for details.

## Credits
- Powered by [OpenAI](https://openai.com/) and [Streamlit](https://streamlit.io/).
- Game and prompt design by the project author.
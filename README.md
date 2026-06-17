# TrainWise AI

**AI Fitness and Athletic Performance Coach**

TrainWise AI is a Streamlit-based application designed to help users with fitness planning, athletic development, sport-specific training, and injury-aware programming.

---

## MVP Version Details

- **Current Version:** Local Rule-Based MVP. The planning engine operates entirely locally using deterministic, rule-based screening and logic rather than third-party AI models.
- **OpenAI Integration:** Fully integrated agentic capabilities using OpenAI and image models are slated for a future release stage.
- **Medical Warning:** This app is not a medical diagnosis tool. Users experiencing severe, sharp, or persistent pain must stop training immediately and consult a qualified medical professional or physiotherapist.

---

## Setup Guide

### 1. Create and Activate a Virtual Environment

```bash
# Create the virtual environment
python -m venv venv

# Activate on macOS / Linux
source venv/bin/activate

# Activate on Windows
venv\Scripts\activate
```

---

### 2. Install Requirements

With your virtual environment active, install all dependencies:

```bash
pip install -r requirements.txt
```

---

### 3. Fill in the `.env` File

Open the `.env` file in the project root and add your API keys:

```
OPENAI_API_KEY=your_openai_api_key_here
IMAGE_MODEL_API_KEY=your_image_model_key_here
APP_ENV=development
```

> **Note:** The app will raise an error on startup if `OPENAI_API_KEY` is missing or empty.

---

### 4. Run the App with Streamlit

From the `trainwise_ai/` directory, run:

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

---

## ⚠️ Medical Disclaimer

**TrainWise AI is not a medical diagnosis tool.**

This application provides general fitness and training guidance only. It is not intended to replace professional medical advice, diagnosis, or treatment.

If you experience serious or worsening symptoms — such as chest pain, severe pain, numbness, dizziness, or any sudden injury — **stop exercising immediately and consult a qualified doctor, physiotherapist, or healthcare professional** before continuing any training program.

Always seek the advice of a qualified health provider with any questions you may have regarding a medical condition or injury.

---

## Project Structure

```
trainwise_ai/
├── app.py                   # Main Streamlit entry point
├── requirements.txt         # Python dependencies
├── .env                     # API keys (not committed to git)
├── .gitignore
├── README.md
└── src/
    ├── config/
    │   └── settings.py      # Environment variable loading
    ├── memory/
    │   └── user_profile_store.py  # In-memory profile storage
    ├── safety/
    │   ├── injury_rules.py  # Pain area constants
    │   └── medical_flags.py # Red flag symptom constants
    ├── planning/
    │   ├── goal_engine.py
    │   ├── sport_engine.py
    │   └── workout_builder.py
    ├── exercises/
    │   ├── exercise_library.py
    │   └── image_prompts.py
    ├── agents/
    │   └── fitness_agent.py
    └── ui/
        ├── components.py
        ├── onboarding_page.py
        ├── plan_page.py
        └── results_page.py
```

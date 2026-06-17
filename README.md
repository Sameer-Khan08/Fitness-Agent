# TrainWise AI

TrainWise AI is a premium, personal athletic coaching dashboard designed to deliver structured, goal-driven, and injury-aware fitness programming.

---

## What the App Does
TrainWise AI dynamically builds custom weekly fitness schedules tailored to your primary training goals, sport demands, current fitness level, and joint pain or injuries. It screens for physiological warning signs and constructs safe, tailored exercise routines, daily recovery readiness checks, and baseline nutritional guidance.

---

## Features
- **Deterministic Screening & Safety Classification**: Processes pain rating and injuries to classify readiness as green, yellow, or red status.
- **Sport-Specific Conditioning & Prehab**: Customizes training schedules to integrate relevant drills and movement requirements for sports like football, cricket, running, etc.
- **Personalized Exercise Cards**: Displays comprehensive instructions, target sets/reps, coach guidelines, customized reasons ("why this for you"), and common mistakes for 18 built-in movements.
- **Daily Check-ins**: Adapts the day's exercise selection, load, and intensity based on sleeping quality, energy, stress, and muscle soreness.
- **Nutrition Guidance**: Estimates caloric targets, baseline proteins, and hydration schedules derived from physical parameters and fitness goals.
- **Saved Plans**: Local session-state persistence allows viewing past plans in a consolidated athlete dashboard.

---

## Safety Disclaimer

> [!CAUTION]
> **Important Safety & Medical Information**
> 
> - **Not Medical Diagnosis**: TrainWise AI is a fitness education tool. It does not provide medical diagnosis, clinical evaluations, or treatment plans.
> - **Guidance Can Be Wrong**: AI and rule-based systems are deterministic helpers. Their recommendations can be incorrect, inappropriate, or inaccurate for your specific physiology.
> - **Professional Help Required**: Severe pain (pain rating $\ge 8$) or medical red flags (e.g. chest pain, dizziness, fainting) require immediate attention from a qualified medical doctor, physiotherapist, or clinical specialist. **Do not attempt intense training if pain is severe.**
> - **Inaccurate Images**: Any generated exercise demonstration images or previews are illustrative and may be anatomically or mechanically inaccurate. Always prioritize the written safety cues and instructions over visual illustrations.

---

## Setup

### 1. Create and Activate a Virtual Environment
```bash
# Create the virtual environment
python -m venv venv

# Activate on macOS / Linux
source venv/bin/activate

# Activate on Windows
venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## Environment Variables
Create a `.env` file in the project root matching the template below:
```env
OPENAI_API_KEY=your_openai_api_key
IMAGE_MODEL_API_KEY=your_image_model_key
TOGETHER_API_KEY=your_together_ai_api_key
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
APP_ENV=development
```
*Note: All Supabase keys and database connection parameters are fully optional. If they are missing, TrainWise AI runs completely locally using session state.*

---

## How to Run
Run the Streamlit application from the root directory:
```bash
streamlit run app.py
```
Open `http://localhost:8501` in your browser.

To run the automated test suite:
```bash
python scripts/smoke_test.py
```

---

## Current Limitations
- **Session-bound Storage**: Saved plans and daily check-in histories persist only in memory for the duration of the Streamlit session unless Supabase PostgreSQL is connected.
- **Static Catalog**: The initial catalog comprises 18 starter exercises.
- **Local Fallback**: Calorie targets use standard Mifflin-St Jeor defaults rather than real-time biometric metabolic trackers.

---

## Future Roadmap
- **Supabase Cloud Syncing**: Enable persistent cross-session athletic accounts.
- **Full AI-Agent Integration**: Empower the Coach Agent with direct OpenAI API tools to refine training volume and regress/progress exercises dynamically.
- **Demo Image Rendering**: Integrate serverless FLUX/Together AI APIs to render step-by-step 2x2 movement demonstration cards.

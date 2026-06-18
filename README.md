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

## Deployment
To deploy this application to Streamlit Community Cloud:

1. **Push Code to GitHub**: Ensure the repository contains the entire codebase. Do **NOT** commit or push the local `.env` file (which is ignored by `.gitignore`).
2. **Setup secrets on Streamlit Cloud**: In your Streamlit Community Cloud app dashboard, navigate to settings, open the **Secrets manager**, and enter your keys in the following format:
   ```toml
   OPENAI_API_KEY = "your_key_here"
   TOGETHER_API_KEY = "your_key_here"
   SUPABASE_URL = "your_supabase_url"
   SUPABASE_KEY = "your_supabase_key"
   APP_ENV = "production"
   ```
3. **Verify Dependencies**: Make sure [requirements.txt](file:///Users/themacstore/Desktop/Fitness%20Agent/requirements.txt) includes all needed external packages.
4. **App Entry Point**: Choose `app.py` as the main application entry point when configuring the Streamlit deploy setup.

---

## Current Limitations
- **Session-bound Storage**: Saved plans and daily check-in histories persist only in memory for the duration of the Streamlit session unless Supabase PostgreSQL is connected.
- **Static Catalog**: The initial catalog comprises 18 starter exercises.
- **Local Fallback**: Calorie targets use standard Mifflin-St Jeor defaults rather than real-time biometric metabolic trackers.

---

## Demo Profiles
TrainWise AI includes pre-configured demo athlete profiles to make verification and testing straightforward:
- **Load Demo Athlete Profile / Football Groin Pain**: Loads an intermediate athlete playing football with a moderate pain rating (5/10) in the groin during sprinting. This generates a modified yellow-status plan that restricts sprinting/high-impact drills while including prehab.
- **Beginner Weight Loss**: Loads a beginner weight loss profile with no pain rating. Generates a safe green-status starter routine.
- **Red Flag Lower Back Pain**: Loads an advanced athlete reporting severe lower back pain (8/10) radiating down the leg. Generates a red-status plan warning to seek immediate professional clinical help and capping training to low-intensity active recovery.

---

## MVP Limitations
- **Rule-based Planner**: The core planner uses a basic rule-based engine to customize training.
- **Optional AI Coach**: AI explanations require an active OpenAI key. If missing, this feature is disabled.
- **Optional Demo Images**: Image generation requires Together AI configured and may be anatomically inaccurate.
- **No Medical Diagnosis**: This application is not a medical device and does not provide clinical assessments or physical therapy diagnosis.
- **No Wearable Integration**: Biometric inputs (steps, sleep, active energy) are self-reported and do not sync with external smartwatches/fitness trackers.
- **No Camera Form Checking**: Movement assessment is currently questionnaire-based; camera computer vision form check is not active.

---

## Roadmap
- **Better Sport-Specific Periodization**: Support multi-week training blocks with progressive overload planning.
- **Larger Exercise Library**: Extend the database beyond the core 18 movements to include more advanced athletic exercises.
- **Verified Exercise Media**: Replace AI-generated prompts with verified, professional movement demonstration videos or photos.
- **Camera Form Checking**: Integrate real-time computer vision computer-assisted form feedback via webcams.
- **Coach Dashboard**: Build a trainer dashboard allowing human fitness coaches to review and manually override plans.
- **Mobile Application**: Port the React/Vite/Streamlit interface into a native iOS and Android app.

---

## Screenshots
*Coming soon.*

---

## Demo Flow
Follow this 7-step sequence to demo the core capabilities of TrainWise AI:

1. **Athlete Onboarding**: Click on **Profile Setup** in the sidebar. Fill out the onboarding form with your biometrics, target goal (e.g. Strength), sport focus (e.g. Football), training availability, and any active pain or injury history.
2. **Plan Dashboard**: After submitting the onboarding form, review the Plan Builder Dashboard which outlines what parameters the coaching engine will evaluate.
3. **Plan Generation**: Click "Generate My Training Plan" to run the rule-based coaching planner.
4. **Safety & Screening (Reality Check)**: On the results page, inspect your **Safety Status** (Green, Yellow, or Red) and the **Reality Check** expander detailing movement patterns to avoid.
5. **Weekly Schedule & Exercise Details**: Scroll to **Weekly Plan** and expand a training day. Expand individual exercise cards to inspect written form instructions, common mistakes, "Avoid If" conditions, and the underlying AI image generation prompt.
6. **Daily Check-in Adjustment**: Click **Daily Check-in** in the sidebar. Input today's sleep quality, soreness, and pain. Submit the form to view your updated readiness score, action plan, and the day's adjusted workout.
7. **Nutrition & Saved Plans**: Navigate to **Nutrition** in the sidebar to review custom metabolic calorie/macronutrient baseline estimates. Navigate to **Saved Plans / Dashboard** to save your active program and view plan histories.

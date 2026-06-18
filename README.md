# TrainWise AI

AI-powered fitness and athletic performance coaching platform. Generates personalised, injury-aware training plans using rule-based engines with optional AI enhancements.

## Features

- **Profile Setup** — Age, gender, biometrics, goal, sport, fitness level, injury/pain screening
- **Rule-Based Plan Generation** — Weekly training plans built from safety rules, goal priorities, sport demands, and an exercise library
- **Safety Screening** — Green/Yellow/Red traffic-light system based on pain rating and injury keywords
- **Medical Red Flag Detection** — Automatically warns about symptoms requiring professional attention
- **Exercise Cards** — Detailed exercise info with instructions, common mistakes, avoid-if notes, and coaching cues
- **AI Coach Explanation** — Optional Together AI-powered plan explanation (requires API key)
- **Exercise Demo Images** — Optional AI-generated exercise demonstration images via Together AI (requires API key)
- **Image Caching & Session Limit** — Generated images are cached; max 5 images per session
- **Daily Check-in** — Track sleep, energy, soreness, stress, and pain to calculate readiness
- **Readiness-Based Workout Adjustment** — Automatically modifies today's workout based on check-in results
- **Nutrition Guidance** — Calorie targets (Mifflin-St Jeor), protein ranges, hydration, meal structure
- **Saved Plans & Dashboard** — Archive generated plans for reference; view API/deployment status

## Safety Disclaimer

> **This tool provides general fitness guidance only. It is not a medical diagnosis or treatment plan.**
> For severe, worsening, sharp, or unusual symptoms, consult a qualified doctor or physiotherapist.

## Setup

### 1. Clone the repository

```bash
git clone <repo-url>
cd trainwise_ai
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate    # Linux/Mac
venv\Scripts\activate       # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example file and fill in your keys:

```bash
cp .env.example .env
```

The app can run with only `TOGETHER_API_KEY`.

Minimum local `.env`:
```
TOGETHER_API_KEY=your_together_key_here
APP_ENV=development
FLASK_SECRET_KEY=dev-secret-key
```

Optional keys:
| Variable | Required | Description |
|---|---|---|
| `IMAGE_MODEL_API_KEY` | No | Fallback for TOGETHER_API_KEY |
| `SUPABASE_URL` | No | Cloud database URL |
| `SUPABASE_KEY` | No | Cloud database key |

> **Note:** The app works fully without any API keys. The core rule-based planner runs locally.
> Together AI powers AI Coach explanations, nutrition explanations, and exercise demo images. Supabase is completely optional, the app will run in local mode without it.

## How to Run

### Development

```bash
python app.py
```

or:

```bash
flask --app app run --debug
```

Then open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

### Production

```bash
gunicorn app:app
```

## Project Structure

```
trainwise_ai/
├── app.py                          # Flask entry point (minimal setup)
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── templates/                      # Root Jinja2 HTML templates
├── static/                         # Root CSS, JS, images
├── src/
│   ├── config/
│   │   └── settings.py             # Environment variable loader
│   ├── safety/
│   │   ├── injury_rules.py         # Green/Yellow/Red classification
│   │   └── medical_flags.py        # Red flag symptom detection
│   ├── planning/
│   │   ├── goal_engine.py          # Goal-to-priority mapping
│   │   ├── sport_engine.py         # Sport demand mapping
│   │   ├── workout_builder.py      # Weekly plan generator
│   │   ├── readiness_engine.py     # Daily readiness scoring
│   │   └── workout_adjuster.py     # Readiness-based plan adjustment
│   ├── nutrition/
│   │   └── nutrition_engine.py     # Calorie/macro estimation
│   ├── exercises/
│   │   ├── exercise_library.py     # Curated exercise catalog
│   │   └── image_prompts.py        # Image generation prompts + Together AI
│   ├── agents/
│   │   ├── fitness_agent.py        # Plan generation + AI explanation (injury aware)
│   │   └── nutrition_agent.py      # Nutrition AI explanation
│   ├── memory/
│   │   ├── user_profile_store.py   # In-memory profile storage
│   │   ├── plan_store.py           # Session-based plan storage
│   │   ├── checkin_store.py        # Session-based check-in storage
│   │   └── image_cache.py          # Session-based image cache
│   ├── core/                       # Core Package (shared helpers)
│   │   ├── __init__.py
│   │   ├── constants.py            # General constants
│   │   └── utils.py                # Utility functions
│   └── web/
│       ├── __init__.py
│       ├── helpers.py              # Basic session & deployment helpers
│       ├── forms/                  # Forms Package (separated parsing logic)
│       │   ├── __init__.py
│       │   ├── profile_forms.py    # Profile setup parsing
│       │   └── checkin_forms.py    # Daily check-in parsing
│       ├── services/               # Services Package (business state wrappers)
│       │   ├── __init__.py
│       │   ├── session_interface.py# Custom MemorySessionInterface
│       │   ├── session_service.py  # Typed session state getters/setters
│       │   ├── flash_service.py    # Categorized user flash messaging
│       │   └── api_status_service.py# Third-party integrations state checkers
│       └── routes/                 # Routes Package (decoupled controllers)
│           ├── __init__.py         # Web blueprint definition & context processor
│           ├── main_routes.py      # Root indices and starting over
│           ├── profile_routes.py   # Profile creation and questionnaires
│           ├── plan_routes.py      # Workout plan generation & presentation
│           ├── checkin_routes.py   # Daily physical readiness tracking
│           ├── nutrition_routes.py # Macro estimation guides
│           ├── image_routes.py     # Session-bound exercise image generation
│           └── saved_plan_routes.py# Local workout archives & dashboards
```

## Design Mode

To focus on UI/UX layout and styling without relying on external API connections, TrainWise AI includes an offline **Design Mode**.

When `DESIGN_MODE=true` is set in your `.env` file:
- All external Together AI text and image generation API calls are completely disabled.
- The sidebar displays neutral, non-scary **Design Mode** statuses for the AI Coach and Exercise Images, and **Local Mode** for the Database.
- The **AI Coach Explanation** card is pre-populated with a polished preview placeholder.
- **Exercise Visuals** show a clean placeholder indicating they are disabled in design mode, with the action buttons disabled.
- Core rule-based planning, safety checks, nutrition targets, and daily readiness check-ins remain fully operational.

To re-enable online AI features:
1. Set `DESIGN_MODE=false` (or remove the flag).
2. Set `AI_COACH_ENABLED=true` and `EXERCISE_IMAGES_ENABLED=true`.
3. Provide a valid `TOGETHER_API_KEY` in your `.env` file.

## Exercise Images

* **Technology**: Powered by Together AI (using the primary or fallback image models).
* **Manual Trigger**: Images are never generated automatically; they are created only when you click the "Generate Exercise Visual" or "Regenerate Visual" buttons.
* **Caching**: Generated images and their prompt metadata are cached in the Flask session so they do not incur multiple API costs when you reload the page.
* **Session Limit**: To keep costs predictable, there is a hard limit of 5 image generation API calls per session.
* **Regeneration**: If you are not satisfied with a generated image, you can click "Regenerate Visual". This will make a new API call, replace the cached visual, and count towards your session limit.
* **Safety & Accuracy**: AI-generated visuals may contain anatomical inaccuracies, form anomalies, or minor errors. Written instructions and warning notes remain the primary guide for safe exercise execution.

## Current Limitations

- Plans are session-based (in-memory); they reset when the server restarts
- No persistent user accounts without Supabase configuration
- AI features require external API keys
- Exercise library contains 18 starter exercises
- Image generation uses Together AI models; quality varies
- No payment or subscription system
- No camera-based form checking

## Roadmap

- Expand exercise library
- Add plan history export (PDF/CSV)
- Progressive overload tracking
- Integration with wearable devices
- Enhanced periodisation models

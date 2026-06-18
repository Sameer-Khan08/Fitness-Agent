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
- **Demo Profiles** — Pre-built test profiles (athlete, weight loss, groin pain, red flag back pain)

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
├── app.py                          # Flask entry point
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
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
│   │   ├── fitness_agent.py        # Plan generation + AI explanation
│   │   └── nutrition_agent.py      # Nutrition AI explanation
│   ├── memory/
│   │   ├── user_profile_store.py   # In-memory profile storage
│   │   ├── plan_store.py           # Session-based plan storage
│   │   ├── checkin_store.py        # Session-based check-in storage
│   │   └── image_cache.py          # Session-based image cache
│   └── web/
│       ├── routes.py               # Flask Blueprint routes
│       ├── forms.py                # Form parsing helpers
│       ├── helpers.py              # Session management helpers
│       ├── templates/              # Jinja2 HTML templates
│       └── static/                 # CSS, JS, images
└── scripts/
    └── smoke_test.py               # Automated smoke tests
```

## Smoke Tests

```bash
python scripts/smoke_test.py
```

Tests cover: green/yellow/red plan generation, nutrition estimation, readiness scoring, and image prompt generation.

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

# Prompt 1 — Project hygiene + requirements + optional auth

Use this first.

We are continuing the existing Streamlit Python project `trainwise_ai`.

Task:
Clean the project setup and make the app easier to test locally.

Important:

* Do not add new features.
* Do not add OpenAI logic.
* Do not add image generation logic.
* Do not change the core planner yet.
* Only fix project hygiene, requirements, and startup/auth behavior.

Fix these issues:

1. Update `.gitignore`

Make sure it excludes:

.env
.env.local
venv/
**pycache**/
*.pyc
.DS_Store
tmp/
.streamlit/
trainwise.db
__MACOSX/
.git/

2. Update `requirements.txt`

Add missing package:

pandas

Keep all existing packages.

3. Add a safety note in `README.md`

Add a short section explaining:

* `.env` should never be committed or shared.
* API keys should be kept private.
* If API keys were uploaded or exposed, they should be rotated/regenerated.
* The app is not a medical diagnosis tool.

4. Make Supabase/auth optional for development

Current problem:
The app starts at auth, which makes testing harder if Supabase keys are missing.

Update `app.py` so:

* If `SUPABASE_URL` and `SUPABASE_KEY` exist, keep the existing auth/dashboard flow.
* If Supabase keys are missing, skip auth and start directly at onboarding.
* Do not break the existing auth flow.
* Do not remove auth files.
* Do not require Supabase for testing the core fitness planner.

Expected behavior:

* With Supabase keys: auth works as before.
* Without Supabase keys: app opens directly to onboarding and the planner can be tested.

Testing:
Run:

python -m compileall .

Then run:

streamlit run app.py

Confirm:

* no import errors
* app loads even if Supabase keys are missing
* onboarding can be reached without auth in development mode
* existing auth is not deleted

---

# Prompt 2 — Fix exercise library + image prompt preview only

Use this after Prompt 1 passes.

We are continuing the existing Streamlit Python project `trainwise_ai`.

Task:
Improve the exercise library and image prompt system, but do not generate real images yet.

Important:

* Do not call Together AI.
* Do not call OpenAI.
* Do not generate real images.
* Do not add database features.
* Keep image generation as a later feature.
* For now, only prepare clean image prompts and placeholders.

Fix these files:

1. `src/exercises/image_prompts.py`

Fix the bug where the prompt literally contains `{exercise_name}` instead of the real exercise name.

Make sure `build_exercise_image_prompt(exercise_name: str) -> str` uses an f-string.

Add or update this function:

`build_exercise_demo_prompt(exercise: dict) -> str`

It should create a realistic exercise demo prompt using:

* exercise name
* category
* level
* demo_focus

The prompt should ask for:

* realistic human fitness demonstration
* clean gym or neutral background
* correct posture
* full body visible where needed
* no text in the image
* no distorted anatomy
* no unsafe form

Example style:

"Realistic full-body fitness demonstration photo of a person performing a bodyweight squat in a clean gym setting. Show correct posture, neutral spine, knees tracking over toes, and controlled depth. No text, no labels, no distorted anatomy, no unsafe form."

2. `src/exercises/exercise_library.py`

Update every exercise in `EXERCISES` so each exercise has this structure:

{
"name": str,
"category": str,
"level": "beginner" | "intermediate" | "advanced",
"goal_tags": list[str],
"sport_tags": list[str],
"sets": str,
"reps": str,
"instructions": list[str],
"common_mistakes": list[str],
"avoid_if": list[str],
"risk_tags": list[str],
"demo_focus": str
}

Keep these exercises:

* bodyweight squat
* incline push-up
* glute bridge
* dead bug
* plank
* side plank
* calf raise
* split squat
* Romanian deadlift
* row
* pull-up
* walking
* low-impact bike
* jump rope
* Copenhagen plank
* adductor squeeze
* hamstring bridge
* ankle balance drill

For every exercise:

* Add 3-5 simple instruction steps.
* Add 2-4 common mistakes.
* Add clear avoid-if notes.
* Add useful risk tags.

Use risk tags such as:

* jumping
* sprinting
* heavy hinge
* deep knee bend
* overhead pressing
* grip intensive
* plyometric
* loaded spinal flexion
* hard change of direction
* intense core
* low risk

3. Disable real image generation from UI

If any UI component currently calls the image API from exercise cards, remove that call.

Instead, exercise cards should only show:

* placeholder box: “Exercise demo image will appear here in a later version.”
* expander: “Image Prompt Preview”
* inside the expander, show the generated prompt text

Do not delete the existing image generation function if it exists. Just do not call it from the UI.

Testing:
Run:

python -m compileall .

Then run:

streamlit run app.py

Confirm:

* no import errors
* exercise library loads
* no image API call happens
* image prompt preview shows the actual exercise name, not `{exercise_name}`

---

# Prompt 3 — Fix planner output + exercise cards + safety filtering

This is the most important one.

We are continuing the existing Streamlit Python project `trainwise_ai`.

Task:
Stabilize the core rule-based fitness planner and results UI.

Important:

* Do not use OpenAI yet.
* Do not generate real images yet.
* Do not add new database features.
* Do not add payments.
* Keep the logic rule-based.
* Keep the app stable and beginner-friendly.

Fix these issues:

1. Keep full exercise dictionaries in `workout_builder.py`

Current problem:
The planner strips exercise details and only keeps name, sets, reps, and notes.

Change it so every exercise inside `weekly_plan[i]["exercises"]` keeps the full exercise dictionary.

Add extra fields without deleting original fields:

{
...full exercise dict,
"why_you": str,
"coach_note": str
}

This is required so the UI can display:

* instructions
* common mistakes
* avoid-if notes
* risk tags
* image prompt preview

2. Standardize weekly plan day format

Every day inside `weekly_plan` should use this structure:

{
"day": "Day 1",
"session_type": str,
"session_goal": str,
"focus": str,
"intensity": "low" | "moderate" | "high",
"duration_minutes": int,
"warm_up": str,
"exercises": list[dict],
"cool_down": str,
"coaching_note": str
}

Make sure the UI and planner use the same keys.

3. Improve safety filtering

Use:

* safety avoid list
* exercise `avoid_if`
* exercise `risk_tags`
* pain rating
* injury text

Rules:

For red status:

* all sessions must be low intensity
* only low-risk exercises
* no jumping
* no sprinting
* no plyometrics
* no heavy hinge
* no loaded spinal flexion
* no hard change of direction
* no advanced exercises
* no intense core exercises
* if unsure, choose walking, low-impact bike, dead bug, glute bridge, gentle mobility, adductor squeeze only if pain-free

For yellow status:

* avoid exercises that match the user's injury area or avoid list
* avoid high-risk drills
* avoid sprinting/jumping/plyometric-heavy exercises if the injury is lower-body related
* use low/moderate intensity
* include controlled strength, mobility, and prehab

For green status:

* allow normal training based on user fitness level
* beginners should still avoid advanced exercises
* advanced users can receive harder exercises if they have no red/yellow warnings

4. Fix lower-back red case

For a user with:

* goal: strength
* sport: gym only
* fitness level: advanced
* lower back pain
* pain rating: 8

The plan must NOT include:

* jump rope
* Copenhagen plank
* Romanian deadlift
* heavy hinge
* loaded spinal flexion
* high intensity drills

It should give:

* low-intensity sessions
* simple safe options
* clear recommendation to consult a qualified professional

5. Fix medical dictionary mismatch

`medical_flags.py` returns:

{
"has_red_flags": bool,
"flags": list[str],
"message": str
}

Make sure all UI files use `flags`, not `warnings`.

6. Update `src/ui/components.py`

Add or improve this function:

`render_exercise_card(exercise: dict, day_idx: int = 0, ex_idx: int = 0) -> None`

It should display:

* exercise name
* category
* level
* sets and reps
* instructions
* common mistakes
* avoid-if notes
* why this exercise was selected
* coach note
* image prompt preview
* placeholder image box

Use safe `.get()` access everywhere so the app does not crash if a field is missing.

7. Update workout day UI

Update `workout_day_card()` or the equivalent results UI function so each day displays:

* day
* session_type
* session_goal
* focus
* intensity
* duration
* warm-up
* exercise cards
* cool-down
* coaching note

Use Streamlit expanders to avoid clutter.

8. Testing

Run:

python -m compileall .

Then test these profiles:

Test 1:
Goal: Weight Loss
Sport: None
Fitness level: Beginner
Pain rating: 1

Expected:

* green status
* beginner-friendly plan
* low/moderate intensity
* no advanced exercises

Test 2:
Goal: Athletic Performance
Sport: Football
Fitness level: Intermediate
Injuries: groin pain during sprinting
Pain rating: 5

Expected:

* yellow status
* avoid sprinting, hard cutting, aggressive adductor stretching
* no sprinting/jumping/plyometric-heavy exercises
* include safe prehab and controlled strength

Test 3:
Goal: Strength
Sport: Gym Only
Fitness level: Advanced
Injuries: lower back pain
Pain rating: 8

Expected:

* red status
* low-intensity only
* no jump rope
* no Copenhagen plank
* no Romanian deadlift
* no heavy hinge
* no loaded spinal flexion
* clear message to consult a qualified doctor or physiotherapist

After this, run:

streamlit run app.py

Confirm:

* no import errors
* onboarding works
* plan generation works
* results page works
* exercise cards display full details
* no image API call happens from the UI
* app does not crash if fields are missing

---

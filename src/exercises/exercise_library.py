"""
exercise_library.py
-------------------
Curated library of 18 starter exercises with difficulty, categories, goal/sport tags,
injury avoidance tags, risk tags, common mistakes, and demo focus.
Used by the rule-based planner.
"""

EXERCISES: list[dict] = [
    {
        "name": "bodyweight squat",
        "category": "lower body",
        "level": "beginner",
        "goal_tags": ["general fitness", "weight loss", "mobility", "endurance"],
        "sport_tags": ["soccer", "football", "basketball", "running"],
        "sets": "3",
        "reps": "10-15",
        "instructions": [
            "Stand with feet shoulder-width apart.",
            "Lower your hips down and back keeping chest tall.",
            "Push through feet to return to start."
        ],
        "common_mistakes": [
            "Knees collapsing inward (valgus collapse)",
            "Heels lifting off the ground, shifting weight to toes",
            "Rounding the lower back at the bottom of the squat"
        ],
        "avoid_if": ["knee"],
        "risk_tags": ["deep knee bend"],
        "demo_focus": "Proper squat depth and knee alignment tracking over toes"
    },
    {
        "name": "incline push-up",
        "category": "upper body push",
        "level": "beginner",
        "goal_tags": ["general fitness", "muscle gain", "strength", "endurance"],
        "sport_tags": ["cricket", "tennis", "basketball", "badminton"],
        "sets": "3",
        "reps": "8-12",
        "instructions": [
            "Place hands shoulder-width apart on an elevated surface.",
            "Lower chest to the surface keeping body straight.",
            "Push back to starting position."
        ],
        "common_mistakes": [
            "Flaring elbows out too wide (90 degrees)",
            "Sagging hips or hyperextending core",
            "Not touching chest to the elevated surface"
        ],
        "avoid_if": ["shoulder", "wrist"],
        "risk_tags": [],
        "demo_focus": "Neutral spine alignment and controlled elbow angle"
    },
    {
        "name": "glute bridge",
        "category": "lower body",
        "level": "beginner",
        "goal_tags": ["mobility", "rehab", "general fitness", "weight loss"],
        "sport_tags": ["running", "soccer", "football"],
        "sets": "3",
        "reps": "12-15",
        "instructions": [
            "Lie on your back with knees bent and feet flat.",
            "Squeeze your glutes and lift hips toward the ceiling.",
            "Lower slowly back to the ground."
        ],
        "common_mistakes": [
            "Hyperextending the lower back at the top",
            "Not engaging the glutes, overloading hamstrings",
            "Pushing through toes instead of heels"
        ],
        "avoid_if": ["lower back"],
        "risk_tags": [],
        "demo_focus": "Hip extension and glute contraction at peak"
    },
    {
        "name": "dead bug",
        "category": "core",
        "level": "beginner",
        "goal_tags": ["general fitness", "mobility", "strength", "rehab"],
        "sport_tags": ["cricket", "soccer", "tennis", "badminton", "running"],
        "sets": "3",
        "reps": "10 per side",
        "instructions": [
            "Lie on back with arms extended up and knees at 90 degrees.",
            "Slowly lower opposite arm and leg toward floor.",
            "Return to start and repeat on opposite side."
        ],
        "common_mistakes": [
            "Lower back arching off the floor",
            "Moving legs and arms too quickly",
            "Losing coordination of opposite limbs"
        ],
        "avoid_if": ["lower back"],
        "risk_tags": [],
        "demo_focus": "Lower back flat against the floor and braced core"
    },
    {
        "name": "plank",
        "category": "core",
        "level": "beginner",
        "goal_tags": ["general fitness", "strength", "endurance", "weight loss"],
        "sport_tags": ["running", "cricket", "basketball"],
        "sets": "3",
        "reps": "30-60s",
        "instructions": [
            "Hold a push-up position on forearms.",
            "Keep body in straight line from head to heels.",
            "Squeeze core and glutes."
        ],
        "common_mistakes": [
            "Sagging hips towards the floor",
            "Poking butt high in the air",
            "Shrugging shoulders or dropping the neck"
        ],
        "avoid_if": ["lower back", "shoulder"],
        "risk_tags": [],
        "demo_focus": "Straight line from head to heels and active shoulder push"
    },
    {
        "name": "side plank",
        "category": "core",
        "level": "intermediate",
        "goal_tags": ["general fitness", "strength", "athletic performance", "muscle gain"],
        "sport_tags": ["tennis", "badminton", "soccer", "basketball"],
        "sets": "3",
        "reps": "20-45s per side",
        "instructions": [
            "Lie on side, elbow under shoulder, lift hips.",
            "Keep body in straight line.",
            "Hold position."
        ],
        "common_mistakes": [
            "Hips sagging toward the floor",
            "Rotating hips forward or backward off alignment",
            "Straining the neck by looking down"
        ],
        "avoid_if": ["shoulder", "elbow"],
        "risk_tags": [],
        "demo_focus": "Hips raised and aligned vertically with shoulders and ankles"
    },
    {
        "name": "calf raise",
        "category": "lower body",
        "level": "beginner",
        "goal_tags": ["general fitness", "endurance", "rehab", "mobility"],
        "sport_tags": ["running", "soccer", "football", "basketball", "tennis"],
        "sets": "3",
        "reps": "15-20",
        "instructions": [
            "Stand on flat floor or step edge.",
            "Raise up onto balls of your feet.",
            "Lower slowly back down."
        ],
        "common_mistakes": [
            "Bouncing at the bottom to use momentum",
            "Not reaching full height at the top",
            "Ankles rolling outward (supination) at the top"
        ],
        "avoid_if": ["ankle", "achilles"],
        "risk_tags": [],
        "demo_focus": "Controlled rise and lower with ankles stable"
    },
    {
        "name": "split squat",
        "category": "lower body",
        "level": "intermediate",
        "goal_tags": ["strength", "muscle gain", "athletic performance", "weight loss"],
        "sport_tags": ["soccer", "football", "basketball", "tennis"],
        "sets": "3",
        "reps": "8-12 per side",
        "instructions": [
            "Step one foot forward and one foot backward.",
            "Lower hips straight down until back knee is near floor.",
            "Drive back up to starting position."
        ],
        "common_mistakes": [
            "Front knee sliding too far forward of the toes",
            "Back knee collapsing inward",
            "Losing balance or leaning torso too far forward"
        ],
        "avoid_if": ["knee", "ankle"],
        "risk_tags": ["deep knee bend"],
        "demo_focus": "Vertical torso and front knee tracking with toes"
    },
    {
        "name": "Romanian deadlift",
        "category": "lower body",
        "level": "intermediate",
        "goal_tags": ["strength", "muscle gain", "athletic performance"],
        "sport_tags": ["football", "soccer", "cricket", "running"],
        "sets": "3",
        "reps": "8-12",
        "instructions": [
            "Hold weight in front of hips, soft knee bend.",
            "Hinge forward from hips, pushing butt back.",
            "Keep back flat, lower weight to mid-shin, drive up using glutes."
        ],
        "common_mistakes": [
            "Rounding the back (flexing the spine) under load",
            "Bending knees too much (turning it into a squat)",
            "Keeping the weight too far away from the shins"
        ],
        "avoid_if": ["lower back"],
        "risk_tags": ["heavy hinge", "loaded spinal flexion"],
        "demo_focus": "Hips moving backwards with a flat back and vertical shins"
    },
    {
        "name": "row",
        "category": "upper body pull",
        "level": "beginner",
        "goal_tags": ["general fitness", "strength", "muscle gain", "endurance"],
        "sport_tags": ["cricket", "tennis", "badminton"],
        "sets": "3",
        "reps": "10-12",
        "instructions": [
            "Hold weight or handle, pull elbow back toward hip.",
            "Squeeze shoulder blades together.",
            "Return slowly to start position."
        ],
        "common_mistakes": [
            "Using torso momentum or shrugging shoulders to pull",
            "Rounding the lower back during bent-over variations",
            "Not squeezing shoulder blades at peak contraction"
        ],
        "avoid_if": ["shoulder", "lower back"],
        "risk_tags": ["grip intensive"],
        "demo_focus": "Elbow drive and shoulder blade retraction"
    },
    {
        "name": "pull-up",
        "category": "upper body pull",
        "level": "advanced",
        "goal_tags": ["strength", "muscle gain", "athletic performance"],
        "sport_tags": ["basketball", "gym only"],
        "sets": "3",
        "reps": "5-8",
        "instructions": [
            "Hang from pull-up bar with overhand grip.",
            "Pull chest up to the bar leading with elbows.",
            "Lower body back down under control."
        ],
        "common_mistakes": [
            "Kicking or swinging legs (kipping) to get over the bar",
            "Not reaching full extension at the bottom or chin over bar at top",
            "Shrugging shoulders at the top, putting stress on neck"
        ],
        "avoid_if": ["shoulder", "elbow"],
        "risk_tags": ["grip intensive"],
        "demo_focus": "Full range of motion and active shoulders"
    },
    {
        "name": "walking",
        "category": "cardio",
        "level": "beginner",
        "goal_tags": ["weight loss", "mobility", "rehab", "endurance", "general fitness"],
        "sport_tags": ["running", "soccer", "none", "gym only"],
        "sets": "1",
        "reps": "15-30 mins",
        "instructions": [
            "Walk at a comfortable or brisk pace.",
            "Keep head up and shoulders relaxed.",
            "Swing arms naturally."
        ],
        "common_mistakes": [
            "Slouching or poor posture",
            "Taking overly large strides which stresses heels",
            "Looking down at feet instead of ahead"
        ],
        "avoid_if": [],
        "risk_tags": [],
        "demo_focus": "Upright posture and natural arm swing"
    },
    {
        "name": "low-impact bike",
        "category": "cardio",
        "level": "beginner",
        "goal_tags": ["weight loss", "rehab", "endurance", "general fitness"],
        "sport_tags": ["none", "running", "gym only"],
        "sets": "1",
        "reps": "10-20 mins",
        "instructions": [
            "Pedal at a moderate resistance level.",
            "Keep upright posture.",
            "Ensure knee is slightly bent at bottom of pedal."
        ],
        "common_mistakes": [
            "Seat height set too low or too high",
            "Rounding the upper back over the handlebars",
            "Pedaling with toes only instead of midfoot"
        ],
        "avoid_if": [],
        "risk_tags": [],
        "demo_focus": "Slight bend in knee at pedal bottom and upright posture"
    },
    {
        "name": "jump rope",
        "category": "cardio",
        "level": "intermediate",
        "goal_tags": ["athletic performance", "endurance", "weight loss", "general fitness"],
        "sport_tags": ["soccer", "football", "basketball", "badminton", "tennis"],
        "sets": "3",
        "reps": "1 min",
        "instructions": [
            "Hold jump rope handles, rotate rope over head.",
            "Jump slightly off ground as rope passes under feet.",
            "Land softly on balls of feet."
        ],
        "common_mistakes": [
            "Jumping too high off the floor",
            "Using entire arms instead of wrists to turn the rope",
            "Landing flat-footed or on heels"
        ],
        "avoid_if": ["ankle", "achilles", "knee"],
        "risk_tags": ["jumping", "plyometric"],
        "demo_focus": "Soft landing on balls of feet and minimal jump height"
    },
    {
        "name": "Copenhagen plank",
        "category": "core",
        "level": "advanced",
        "goal_tags": ["athletic performance", "strength", "rehab", "muscle gain"],
        "sport_tags": ["soccer", "football", "tennis", "basketball", "badminton"],
        "sets": "3",
        "reps": "15-30s per side",
        "instructions": [
            "Place top leg on a bench, support forearm on floor.",
            "Raise hips so body is straight and bottom leg is hovered.",
            "Hold this adductor isolation."
        ],
        "common_mistakes": [
            "Hips sagging down or twisting forward",
            "Top knee bending or slipping off the support bench",
            "Holding breath during the isometric hold"
        ],
        "avoid_if": ["groin", "knee", "shoulder"],
        "risk_tags": ["intense core"],
        "demo_focus": "Straight line from shoulder to ankle with top leg supported"
    },
    {
        "name": "adductor squeeze",
        "category": "lower body",
        "level": "beginner",
        "goal_tags": ["rehab", "mobility", "general fitness", "endurance"],
        "sport_tags": ["soccer", "football", "running"],
        "sets": "3",
        "reps": "10-15",
        "instructions": [
            "Sit or lie down, place a ball or foam block between knees.",
            "Squeeze inner thighs together firmly.",
            "Hold squeeze for 3 seconds, then release."
        ],
        "common_mistakes": [
            "Squeezing too aggressively too fast",
            "Hyperextending the neck or arching the back",
            "Holding breath during contraction"
        ],
        "avoid_if": ["groin"],
        "risk_tags": [],
        "demo_focus": "Controlled squeeze and release of the foam block"
    },
    {
        "name": "hamstring bridge",
        "category": "lower body",
        "level": "intermediate",
        "goal_tags": ["strength", "athletic performance", "rehab", "muscle gain"],
        "sport_tags": ["soccer", "football", "running", "basketball"],
        "sets": "3",
        "reps": "8-12",
        "instructions": [
            "Lie on back, bend knees slightly (longer angle than glute bridge).",
            "Drive heels into floor and lift hips off the ground.",
            "Feel engagement primarily in hamstrings, lower slowly."
        ],
        "common_mistakes": [
            "Hyperextending the lower back at the top",
            "Placing feet too close to butt (makes it a glute bridge)",
            "Not engaging hamstrings, shifting focus to lower back"
        ],
        "avoid_if": ["lower back"],
        "risk_tags": [],
        "demo_focus": "Longer knee angle and driving heels down to engage hamstrings"
    },
    {
        "name": "ankle balance drill",
        "category": "mobility",
        "level": "beginner",
        "goal_tags": ["rehab", "mobility", "general fitness", "athletic performance"],
        "sport_tags": ["running", "soccer", "football", "basketball", "tennis", "badminton"],
        "sets": "3",
        "reps": "30s per side",
        "instructions": [
            "Stand tall on one foot.",
            "Focus eyes on a single point on wall.",
            "Hold balance, micro-adjusting through foot and ankle."
        ],
        "common_mistakes": [
            "Letting the ankle collapse inward (pronation)",
            "Holding breath or clenching jaw",
            "Stiffening up completely without micro-adjustments"
        ],
        "avoid_if": [],
        "risk_tags": [],
        "demo_focus": "Micro-adjustments in the foot to maintain vertical balance"
    }
]

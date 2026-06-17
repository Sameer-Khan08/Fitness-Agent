"""
exercise_library.py
-------------------
Curated library of 18 starter exercises with difficulty, categories, goal/sport tags,
and injury avoidance tags. Used by the rule-based planner.
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
        "avoid_if": ["knee"]
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
        "avoid_if": ["shoulder", "wrist"]
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
        "avoid_if": ["lower back"]
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
        "avoid_if": ["lower back"]
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
        "avoid_if": ["lower back", "shoulder"]
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
        "avoid_if": ["shoulder", "elbow"]
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
        "avoid_if": ["ankle", "achilles"]
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
        "avoid_if": ["knee", "ankle"]
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
        "avoid_if": ["lower back"]
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
        "avoid_if": ["shoulder", "lower back"]
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
        "avoid_if": ["shoulder", "elbow"]
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
        "avoid_if": []
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
        "avoid_if": []
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
        "avoid_if": ["ankle", "achilles", "knee"]
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
        "avoid_if": ["groin", "knee", "shoulder"]
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
        "avoid_if": ["groin"]
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
        "avoid_if": ["lower back"]
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
        "avoid_if": []
    }
]

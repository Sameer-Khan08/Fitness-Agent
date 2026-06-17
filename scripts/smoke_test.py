import sys
import os
# Ensure root directory is in the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.planning.workout_builder import build_weekly_plan
from src.planning.readiness_engine import calculate_readiness
from src.nutrition.nutrition_engine import estimate_nutrition_targets

def run_tests():
    passed = True

    # 1. Green Plan
    try:
        print("Testing Green Plan...")
        profile_green = {
            "main_goal": "Weight Loss",
            "sport": "None",
            "fitness_level": "Beginner",
            "pain_rating": 1,
            "injuries": ""
        }
        res_green = build_weekly_plan(profile_green)
        assert res_green["safety"]["status"] == "green", "Green plan failed status check"
        print("🟢 Green Plan: PASS")
    except Exception as e:
        print(f"🔴 Green Plan: FAIL ({e})")
        passed = False

    # 2. Yellow Groin Football Plan
    try:
        print("Testing Yellow Plan...")
        profile_yellow = {
            "main_goal": "Athletic Performance",
            "sport": "Football",
            "fitness_level": "Intermediate",
            "pain_rating": 5,
            "injuries": "groin pain during sprinting"
        }
        res_yellow = build_weekly_plan(profile_yellow)
        assert res_yellow["safety"]["status"] == "yellow", "Yellow plan failed status check"
        
        # Verify avoids groin exercises like Copenhagen plank and adductor squeeze
        for day in res_yellow["weekly_plan"]:
            for ex in day["exercises"]:
                name = ex["name"].lower()
                assert "copenhagen" not in name, f"Included Copenhagen plank in yellow groin plan: {name}"
                assert "adductor" not in name, f"Included adductor squeeze in yellow groin plan: {name}"
        print("🟢 Yellow Plan: PASS")
    except Exception as e:
        print(f"🔴 Yellow Plan: FAIL ({e})")
        passed = False

    # 3. Red Lower Back Plan
    try:
        print("Testing Red Plan...")
        profile_red = {
            "main_goal": "Strength",
            "sport": "Gym Only",
            "fitness_level": "Advanced",
            "pain_rating": 8,
            "injuries": "lower back pain"
        }
        res_red = build_weekly_plan(profile_red)
        assert res_red["safety"]["status"] == "red", "Red plan failed status check"
        
        # Verify no advanced exercises or heavy hinge
        for day in res_red["weekly_plan"]:
            for ex in day["exercises"]:
                assert ex["level"] != "advanced", f"Included advanced exercise in red plan: {ex['name']}"
                risk_tags = [r.lower() for r in ex.get("risk_tags", [])]
                assert "heavy hinge" not in risk_tags, f"Included heavy hinge in red plan: {ex['name']}"
                assert "loaded spinal flexion" not in risk_tags, f"Included loaded flexion in red plan: {ex['name']}"
        print("🟢 Red Plan: PASS")
    except Exception as e:
        print(f"🔴 Red Plan: FAIL ({e})")
        passed = False

    # 4. Nutrition Estimate
    try:
        print("Testing Nutrition Estimate...")
        profile_nut = {
            "main_goal": "Weight Loss",
            "training_days_per_week": 3,
            "gender": "male",
            "age": "25",
            "weight_kg": "80",
            "height_cm": "180"
        }
        nut = estimate_nutrition_targets(profile_nut)
        assert nut["target_calories"] is not None, "Failed to calculate nutrition target"
        print(f"Calorie Target: {nut['target_calories']}, Protein Target: {nut['protein_range_g']}")
        print("🟢 Nutrition: PASS")
    except Exception as e:
        print(f"🔴 Nutrition: FAIL ({e})")
        passed = False

    # 5. Readiness Check
    try:
        print("Testing Readiness Check...")
        checkin_good = {
            "sleep_quality": "good",
            "energy_level": "high",
            "soreness": 1,
            "stress": 2,
            "pain_rating": 0,
            "pain_trend": "better"
        }
        readiness_good = calculate_readiness(checkin_good)
        assert readiness_good["readiness"] == "green", "Expected green readiness"
        
        checkin_bad = {
            "sleep_quality": "poor",
            "energy_level": "low",
            "soreness": 8,
            "stress": 8,
            "pain_rating": 8,
            "pain_trend": "worse"
        }
        readiness_bad = calculate_readiness(checkin_bad)
        assert readiness_bad["readiness"] == "red", "Expected red readiness for high pain/poor recovery"
        print("🟢 Readiness: PASS")
    except Exception as e:
        print(f"🔴 Readiness: FAIL ({e})")
        passed = False

    if passed:
        print("\n🎉 ALL MVP SMOKE TESTS PASSED 🎉")
        sys.exit(0)
    else:
        print("\n❌ SOME MVP SMOKE TESTS FAILED ❌")
        sys.exit(1)

if __name__ == "__main__":
    run_tests()

import pytest
from datetime import date
from marshmallow import ValidationError

from schemas import ExerciseSchema, WorkoutSchema, WorkoutExerciseSchema


def test_exercise_schema_loads_valid_data():
    schema = ExerciseSchema()

    data = {
        "name": "Push-up",
        "category": "Strength",
        "equipment_needed": False
    }

    result = schema.load(data)

    assert result["name"] == "Push-up"
    assert result["category"] == "Strength"
    assert result["equipment_needed"] is False


def test_exercise_schema_rejects_blank_name():
    schema = ExerciseSchema()

    with pytest.raises(ValidationError):
        schema.load({
            "name": "",
            "category": "Strength",
            "equipment_needed": False
        })

    with pytest.raises(ValidationError):
        schema.load({
            "name": "   ",
            "category": "Strength",
            "equipment_needed": False
        })


def test_workout_schema_loads_valid_data():
    schema = WorkoutSchema()

    data = {
        "date": "2026-05-22",
        "duration_minutes": 45,
        "notes": "Upper body workout"
    }

    result = schema.load(data)

    assert result["date"] == date(2026, 5, 22)
    assert result["duration_minutes"] == 45
    assert result["notes"] == "Upper body workout"


def test_workout_schema_rejects_non_positive_duration():
    schema = WorkoutSchema()

    with pytest.raises(ValidationError):
        schema.load({
            "date": "2026-05-22",
            "duration_minutes": 0,
            "notes": "Invalid workout"
        })

    with pytest.raises(ValidationError):
        schema.load({
            "date": "2026-05-22",
            "duration_minutes": -20,
            "notes": "Invalid workout"
        })


def test_workout_exercise_schema_loads_valid_data():
    schema = WorkoutExerciseSchema()

    data = {
        "workout_id": 1,
        "exercise_id": 1,
        "reps": 15,
        "sets": 3,
        "duration_seconds": 0
    }

    result = schema.load(data)

    assert result["workout_id"] == 1
    assert result["exercise_id"] == 1
    assert result["reps"] == 15
    assert result["sets"] == 3
    assert result["duration_seconds"] == 0


def test_workout_exercise_schema_allows_timed_exercises():
    schema = WorkoutExerciseSchema()

    data = {
        "workout_id": 1,
        "exercise_id": 3,
        "reps": 0,
        "sets": 3,
        "duration_seconds": 60
    }

    result = schema.load(data)

    assert result["reps"] == 0
    assert result["sets"] == 3
    assert result["duration_seconds"] == 60


def test_workout_exercise_schema_rejects_invalid_numbers():
    schema = WorkoutExerciseSchema()

    with pytest.raises(ValidationError):
        schema.load({
            "workout_id": 1,
            "exercise_id": 1,
            "reps": -1,
            "sets": 3,
            "duration_seconds": 0
        })

    with pytest.raises(ValidationError):
        schema.load({
            "workout_id": 1,
            "exercise_id": 1,
            "reps": 10,
            "sets": 0,
            "duration_seconds": 0
        })

    with pytest.raises(ValidationError):
        schema.load({
            "workout_id": 1,
            "exercise_id": 1,
            "reps": 10,
            "sets": 3,
            "duration_seconds": -30
        })
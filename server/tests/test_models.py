import pytest
from datetime import date
from flask import Flask

from models import db, Exercise, Workout, WorkoutExercise


@pytest.fixture
def test_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["TESTING"] = True

    db.init_app(app)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


def test_exercise_has_expected_fields(test_app):
    exercise = Exercise(
        name="Push-up",
        category="Strength",
        equipment_needed=False
    )

    db.session.add(exercise)
    db.session.commit()

    saved_exercise = Exercise.query.first()

    assert saved_exercise.id is not None
    assert saved_exercise.name == "Push-up"
    assert saved_exercise.category == "Strength"
    assert saved_exercise.equipment_needed is False


def test_workout_has_expected_fields(test_app):
    workout = Workout(
        date=date(2026, 5, 22),
        duration_minutes=45,
        notes="Upper body workout"
    )

    db.session.add(workout)
    db.session.commit()

    saved_workout = Workout.query.first()

    assert saved_workout.id is not None
    assert saved_workout.date == date(2026, 5, 22)
    assert saved_workout.duration_minutes == 45
    assert saved_workout.notes == "Upper body workout"


def test_workout_exercise_has_expected_fields(test_app):
    exercise = Exercise(
        name="Squat",
        category="Strength",
        equipment_needed=False
    )

    workout = Workout(
        date=date(2026, 5, 22),
        duration_minutes=60,
        notes="Leg day"
    )

    db.session.add_all([exercise, workout])
    db.session.commit()

    workout_exercise = WorkoutExercise(
        workout_id=workout.id,
        exercise_id=exercise.id,
        reps=10,
        sets=3,
        duration_seconds=0
    )

    db.session.add(workout_exercise)
    db.session.commit()

    saved_workout_exercise = WorkoutExercise.query.first()

    assert saved_workout_exercise.id is not None
    assert saved_workout_exercise.workout_id == workout.id
    assert saved_workout_exercise.exercise_id == exercise.id
    assert saved_workout_exercise.reps == 10
    assert saved_workout_exercise.sets == 3
    assert saved_workout_exercise.duration_seconds == 0
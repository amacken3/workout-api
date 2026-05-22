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

def test_workout_exercise_belongs_to_workout_and_exercise(test_app):
    exercise = Exercise(
        name="Bench Press",
        category="Strength",
        equipment_needed=True
    )

    workout = Workout(
        date=date(2026, 5, 22),
        duration_minutes=50,
        notes="Chest day"
    )

    db.session.add_all([exercise, workout])
    db.session.commit()

    workout_exercise = WorkoutExercise(
        workout_id=workout.id,
        exercise_id=exercise.id,
        reps=8,
        sets=4,
        duration_seconds=0
    )

    db.session.add(workout_exercise)
    db.session.commit()

    assert workout_exercise.workout == workout
    assert workout_exercise.exercise == exercise


def test_workout_has_many_workout_exercises(test_app):
    workout = Workout(
        date=date(2026, 5, 22),
        duration_minutes=45,
        notes="Full body workout"
    )

    exercise_one = Exercise(
        name="Push-up",
        category="Strength",
        equipment_needed=False
    )

    exercise_two = Exercise(
        name="Jump Rope",
        category="Cardio",
        equipment_needed=True
    )

    db.session.add_all([workout, exercise_one, exercise_two])
    db.session.commit()

    workout_exercise_one = WorkoutExercise(
        workout_id=workout.id,
        exercise_id=exercise_one.id,
        reps=15,
        sets=3,
        duration_seconds=0
    )

    workout_exercise_two = WorkoutExercise(
        workout_id=workout.id,
        exercise_id=exercise_two.id,
        reps=0,
        sets=3,
        duration_seconds=60
    )

    db.session.add_all([workout_exercise_one, workout_exercise_two])
    db.session.commit()

    assert len(workout.workout_exercises) == 2
    assert workout_exercise_one in workout.workout_exercises
    assert workout_exercise_two in workout.workout_exercises


def test_exercise_has_many_workout_exercises(test_app):
    exercise = Exercise(
        name="Plank",
        category="Core",
        equipment_needed=False
    )

    workout_one = Workout(
        date=date(2026, 5, 22),
        duration_minutes=30,
        notes="Core day"
    )

    workout_two = Workout(
        date=date(2026, 5, 23),
        duration_minutes=40,
        notes="Conditioning day"
    )

    db.session.add_all([exercise, workout_one, workout_two])
    db.session.commit()

    workout_exercise_one = WorkoutExercise(
        workout_id=workout_one.id,
        exercise_id=exercise.id,
        reps=0,
        sets=3,
        duration_seconds=45
    )

    workout_exercise_two = WorkoutExercise(
        workout_id=workout_two.id,
        exercise_id=exercise.id,
        reps=0,
        sets=4,
        duration_seconds=60
    )

    db.session.add_all([workout_exercise_one, workout_exercise_two])
    db.session.commit()

    assert len(exercise.workout_exercises) == 2
    assert workout_exercise_one in exercise.workout_exercises
    assert workout_exercise_two in exercise.workout_exercises


def test_workout_has_many_exercises_through_workout_exercises(test_app):
    workout = Workout(
        date=date(2026, 5, 22),
        duration_minutes=60,
        notes="Mixed workout"
    )

    exercise_one = Exercise(
        name="Squat",
        category="Strength",
        equipment_needed=False
    )

    exercise_two = Exercise(
        name="Burpee",
        category="Conditioning",
        equipment_needed=False
    )

    db.session.add_all([workout, exercise_one, exercise_two])
    db.session.commit()

    workout_exercise_one = WorkoutExercise(
        workout_id=workout.id,
        exercise_id=exercise_one.id,
        reps=10,
        sets=3,
        duration_seconds=0
    )

    workout_exercise_two = WorkoutExercise(
        workout_id=workout.id,
        exercise_id=exercise_two.id,
        reps=12,
        sets=3,
        duration_seconds=0
    )

    db.session.add_all([workout_exercise_one, workout_exercise_two])
    db.session.commit()

    assert exercise_one in workout.exercises
    assert exercise_two in workout.exercises


def test_exercise_has_many_workouts_through_workout_exercises(test_app):
    exercise = Exercise(
        name="Push-up",
        category="Strength",
        equipment_needed=False
    )

    workout_one = Workout(
        date=date(2026, 5, 22),
        duration_minutes=30,
        notes="Upper body"
    )

    workout_two = Workout(
        date=date(2026, 5, 23),
        duration_minutes=45,
        notes="Circuit training"
    )

    db.session.add_all([exercise, workout_one, workout_two])
    db.session.commit()

    workout_exercise_one = WorkoutExercise(
        workout_id=workout_one.id,
        exercise_id=exercise.id,
        reps=15,
        sets=3,
        duration_seconds=0
    )

    workout_exercise_two = WorkoutExercise(
        workout_id=workout_two.id,
        exercise_id=exercise.id,
        reps=20,
        sets=4,
        duration_seconds=0
    )

    db.session.add_all([workout_exercise_one, workout_exercise_two])
    db.session.commit()

    assert workout_one in exercise.workouts
    assert workout_two in exercise.workouts
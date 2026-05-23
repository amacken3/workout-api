import pytest
from datetime import date

from app import app
from models import db, Exercise, Workout, WorkoutExercise


@pytest.fixture
def client():
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["TESTING"] = True

    with app.app_context():
        db.create_all()

        WorkoutExercise.query.delete()
        Workout.query.delete()
        Exercise.query.delete()
        db.session.commit()

        push_up = Exercise(
            name="Push-up",
            category="Strength",
            equipment_needed=False
        )

        plank = Exercise(
            name="Plank",
            category="Core",
            equipment_needed=False
        )

        workout = Workout(
            date=date(2026, 5, 22),
            duration_minutes=45,
            notes="Upper body workout"
        )

        db.session.add_all([push_up, plank, workout])
        db.session.commit()

        workout_exercise = WorkoutExercise(
            workout_id=workout.id,
            exercise_id=push_up.id,
            reps=15,
            sets=3,
            duration_seconds=0
        )

        db.session.add(workout_exercise)
        db.session.commit()

        yield app.test_client()

        db.session.remove()
        db.drop_all()


def test_index_route_returns_success(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"Workout API" in response.data


def test_get_exercises_returns_exercise_list(client):
    response = client.get("/exercises")
    data = response.get_json()

    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["name"] == "Push-up"


def test_get_single_exercise_returns_exercise(client):
    response = client.get("/exercises/1")
    data = response.get_json()

    assert response.status_code == 200
    assert data["id"] == 1
    assert data["name"] == "Push-up"
    assert "workouts" in data


def test_get_single_exercise_returns_404_for_missing_exercise(client):
    response = client.get("/exercises/999")
    data = response.get_json()

    assert response.status_code == 404
    assert data["error"] == "Exercise not found"


def test_create_exercise_creates_record(client):
    response = client.post("/exercises", json={
        "name": "Jump Rope",
        "category": "Cardio",
        "equipment_needed": True
    })

    data = response.get_json()

    assert response.status_code == 201
    assert data["name"] == "Jump Rope"
    assert data["category"] == "Cardio"
    assert data["equipment_needed"] is True

    assert Exercise.query.filter_by(name="Jump Rope").first() is not None


def test_get_workouts_returns_workout_list(client):
    response = client.get("/workouts")
    data = response.get_json()

    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["duration_minutes"] == 45


def test_get_single_workout_returns_workout(client):
    response = client.get("/workouts/1")
    data = response.get_json()

    assert response.status_code == 200
    assert data["id"] == 1
    assert data["duration_minutes"] == 45
    assert "exercises" in data


def test_create_workout_creates_record(client):
    response = client.post("/workouts", json={
        "date": "2026-05-23",
        "duration_minutes": 30,
        "notes": "Core conditioning workout"
    })

    data = response.get_json()

    assert response.status_code == 201
    assert data["duration_minutes"] == 30
    assert data["notes"] == "Core conditioning workout"

    assert Workout.query.filter_by(notes="Core conditioning workout").first() is not None


def test_add_exercise_to_workout_creates_join_record(client):
    response = client.post("/workouts/1/exercises/2/workout_exercises", json={
        "reps": 0,
        "sets": 3,
        "duration_seconds": 60
    })

    data = response.get_json()

    assert response.status_code == 201
    assert data["workout_id"] == 1
    assert data["exercise_id"] == 2
    assert data["sets"] == 3
    assert data["duration_seconds"] == 60

    join_record = WorkoutExercise.query.filter_by(
        workout_id=1,
        exercise_id=2
    ).first()

    assert join_record is not None


def test_delete_exercise_removes_record(client):
    response = client.delete("/exercises/2")

    assert response.status_code == 204
    assert Exercise.query.get(2) is None
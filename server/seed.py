#!/usr/bin/env python3

from datetime import date

from app import app
from models import db, Exercise, Workout, WorkoutExercise


with app.app_context():
    print("Clearing old data...")

    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    print("Creating exercises...")

    push_up = Exercise(
        name="Push-up",
        category="Strength",
        equipment_needed=False
    )

    bench_press = Exercise(
        name="Bench Press",
        category="Strength",
        equipment_needed=True
    )

    plank = Exercise(
        name="Plank",
        category="Core",
        equipment_needed=False
    )

    jump_rope = Exercise(
        name="Jump Rope",
        category="Cardio",
        equipment_needed=True
    )

    squat = Exercise(
        name="Bodyweight Squat",
        category="Strength",
        equipment_needed=False
    )

    exercises = [push_up, bench_press, plank, jump_rope, squat]

    print("Creating workouts...")

    upper_body = Workout(
        date=date(2026, 5, 22),
        duration_minutes=45,
        notes="Upper body strength workout focused on chest, shoulders, and arms."
    )

    core_conditioning = Workout(
        date=date(2026, 5, 23),
        duration_minutes=30,
        notes="Core and conditioning workout with timed movements."
    )

    full_body = Workout(
        date=date(2026, 5, 24),
        duration_minutes=60,
        notes="Full body circuit combining strength and cardio."
    )

    workouts = [upper_body, core_conditioning, full_body]

    db.session.add_all(exercises + workouts)
    db.session.commit()

    print("Creating workout exercises...")

    workout_exercises = [
        WorkoutExercise(
            workout_id=upper_body.id,
            exercise_id=push_up.id,
            reps=15,
            sets=3,
            duration_seconds=0
        ),
        WorkoutExercise(
            workout_id=upper_body.id,
            exercise_id=bench_press.id,
            reps=8,
            sets=4,
            duration_seconds=0
        ),
        WorkoutExercise(
            workout_id=core_conditioning.id,
            exercise_id=plank.id,
            reps=0,
            sets=3,
            duration_seconds=60
        ),
        WorkoutExercise(
            workout_id=core_conditioning.id,
            exercise_id=jump_rope.id,
            reps=0,
            sets=5,
            duration_seconds=120
        ),
        WorkoutExercise(
            workout_id=full_body.id,
            exercise_id=squat.id,
            reps=20,
            sets=4,
            duration_seconds=0
        ),
        WorkoutExercise(
            workout_id=full_body.id,
            exercise_id=jump_rope.id,
            reps=0,
            sets=3,
            duration_seconds=90
        ),
    ]

    db.session.add_all(workout_exercises)
    db.session.commit()

    print("Seed data created successfully.")
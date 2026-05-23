# Workout API

A Flask backend API for a workout tracking application used by personal trainers. This API allows trainers to create workouts, manage reusable exercises, and attach exercises to workouts with sets, reps, and duration data.

## Project Description

This project is a backend API built with Flask, SQLAlchemy, Flask-Migrate, and Marshmallow. It models a workout tracking system where workouts can contain multiple reusable exercises. The join model, `WorkoutExercise`, stores the workout-specific details for each exercise, such as sets, reps, and duration.

The API includes:

- Workout creation, viewing, and deletion
- Exercise creation, viewing, and deletion
- Adding exercises to workouts
- SQLAlchemy model relationships
- Database constraints
- Model-level validations
- Marshmallow schemas and schema validations
- Seed data for local development
- Pytest test coverage for models, schemas, and routes

## Tech Stack

- Python 3.10.11
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Marshmallow
- SQLite
- Pipenv
- Pytest

## Project Structure

```bash
workout-api/
├── Pipfile
├── Pipfile.lock
├── README.md
├── .gitignore
└── server/
    ├── app.py
    ├── models.py
    ├── schemas.py
    ├── seed.py
    ├── migrations/
    └── tests/
        ├── conftest.py
        ├── test_models.py
        ├── test_routes.py
        └── test_schemas.py
```

## Models

### Exercise

Represents a reusable exercise that can be added to many workouts.

Fields:

- `id`
- `name`
- `category`
- `equipment_needed`

### Workout

Represents a workout session or plan.

Fields:

- `id`
- `date`
- `duration_minutes`
- `notes`

### WorkoutExercise

Join model that connects workouts and exercises while storing workout-specific exercise details.

Fields:

- `id`
- `workout_id`
- `exercise_id`
- `reps`
- `sets`
- `duration_seconds`

## Relationships

- A `WorkoutExercise` belongs to a `Workout`
- A `WorkoutExercise` belongs to an `Exercise`
- A `Workout` has many `WorkoutExercises`
- An `Exercise` has many `WorkoutExercises`
- A `Workout` has many `Exercises` through `WorkoutExercises`
- An `Exercise` has many `Workouts` through `WorkoutExercises`

## Validations and Constraints

This project includes table constraints, model validations, and schema validations.

Examples include:

- Exercise names must be unique
- Exercise names cannot be blank
- Required fields cannot be null
- Workout duration must be positive
- Sets must be positive
- Reps and duration seconds cannot be negative

## Installation

```bash
git clone https://github.com/amacken3/workout-api.git

cd workout-api

pipenv install

cd server
```


## Database Setup

Run the database migrations:

```bash
pipenv run flask db upgrade head
```

Seed the database with example data:

```bash
pipenv run python seed.py
```

The seed file clears existing records and recreates sample data, so it can be rerun at any time to reset the database.

## Running the Server

From the `server/` directory, run:

```bash
pipenv run python app.py
```

```bash
http://127.0.0.1:5555
```


## Running Tests

From the `server/` directory, run:

```bash
pipenv run pytest -x
```

The test suite covers:

- Model fields
- Model relationships
- Table constraints
- Model validations
- Schema validations
- API route behavior


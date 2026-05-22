from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False)
    workout_exercises = db.relationship('WorkoutExercise', back_populates='exercise')
    workouts = db.relationship(
        'Workout',
        secondary='workout_exercises',
        viewonly=True
    )

    @validates('name')
    def validate_name(self, key, name):
        if not name or not name.strip():
            raise ValueError('Exercise must have a name.')
        
        return name.strip()

class Workout(db.Model):
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text, nullable=False)
    workout_exercises = db.relationship('WorkoutExercise', back_populates='workout')
    exercises = db.relationship(
        'Exercise',
        secondary='workout_exercises',
        viewonly=True
    )

    @validates('duration_minutes')
    def validate_duration_minutes(self, key, duration_minutes):
        if duration_minutes is None or duration_minutes <= 0:
            raise ValueError('Workout duration must be positive')
        
        return duration_minutes

class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(
        db.Integer, 
        db.ForeignKey('workouts.id'), 
        nullable=False
        )
    workout = db.relationship('Workout', back_populates='workout_exercises')
    exercise_id = db.Column(
        db.Integer,
        db.ForeignKey('exercises.id'), 
        nullable=False
        )
    exercise = db.relationship('Exercise', back_populates='workout_exercises')
    reps = db.Column(db.Integer, nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    duration_seconds = db.Column(db.Integer, nullable=False)

    @validates('reps', 'sets', 'duration_seconds')
    def validate_workout_numbers(self, key, value):
        if value is None:
            raise ValueError(f'{key} is required.')

        if key == 'sets' and value <= 0:
            raise ValueError('Amount of sets must be positive.')

        if key in ['reps', 'duration_seconds'] and value < 0:
            raise ValueError(f'{key} cannot be negative.')

        return value    
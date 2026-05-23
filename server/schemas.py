from marshmallow import Schema, fields, validates, ValidationError

class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    category = fields.Str(required=True)
    equipment_needed = fields.Bool(required=True)
    workouts = fields.Nested(
        "WorkoutSchema",
        many=True,
        exclude=("exercises",)
    )

    @validates('name')
    def validate_name(self, name):
        if not name or not name.strip():
            raise ValidationError('Exercise name cannot be blank.')


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True)
    notes = fields.Str(required=True)
    exercises = fields.Nested(
        "ExerciseSchema",
        many=True,
        exclude=("workouts",)
    )

    @validates('duration_minutes')
    def validate_duration_minutes(self, duration_minutes):
        if duration_minutes is None or duration_minutes <= 0:
            raise ValidationError('Duration must be positive.')


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(required=True)
    exercise_id = fields.Int(required=True)
    reps = fields.Int(required=True)
    sets = fields.Int(required=True)
    duration_seconds = fields.Int(required=True)

    @validates('reps')
    def validate_reps(self, reps):
        if reps is None or reps < 0:
            raise ValidationError('Reps cannot be negative.')


    @validates('sets')
    def validate_sets(self, sets):
        if sets is None or sets <= 0:
            raise ValidationError('Sets must be positive.')


    @validates('duration_seconds')
    def validate_duration_seconds(self, duration_seconds):
        if duration_seconds is None or duration_seconds < 0:
            raise ValidationError('Duration seconds cannot be negative.')
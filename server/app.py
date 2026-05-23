from flask import Flask, make_response, request
from flask_migrate import Migrate
from models import db, Exercise, Workout, WorkoutExercise
from schemas import ExerciseSchema, WorkoutSchema, WorkoutExerciseSchema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Workout API</h1>'


@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()

    workout_schema = WorkoutSchema(many=True)
    workouts_data = workout_schema.dump(workouts)
    
    return workouts_data, 200


@app.route('/workouts/<int:workout_id>', methods=['GET'])
def get_workout_by_id(workout_id):
    workout = Workout.query.get(workout_id)

    if not workout:
        response = make_response({'error': 'Workout not found'}, 404)
        return response
    
    workout_schema = WorkoutSchema()
    workout_data = workout_schema.dump(workout)

    return workout_data, 200


@app.route('/workouts', methods=['POST'])
def create_workout():
    data = request.get_json()

    workout_schema = WorkoutSchema()
    valid_data = workout_schema.load(data)

    workout = Workout(**valid_data)

    db.session.add(workout)
    db.session.commit()

    return workout_schema.dump(workout), 201


@app.route('/workouts/<int:workout_id>', methods=['DELETE'])
def delete_workout(workout_id):
    workout = Workout.query.get(workout_id)

    if not workout:
        response = make_response({'error': 'Workout not found'}, 404)
        return response
    
    db.session.delete(workout)
    db.session.commit()

    response = make_response('', 204)
    return response


@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()

    exercise_schema = ExerciseSchema(many=True)
    exercises_data = exercise_schema.dump(exercises)

    return exercises_data, 200


@app.route('/exercises/<int:exercise_id>', methods=['GET'])
def get_exercise_by_id(exercise_id):
    exercise = Exercise.query.get(exercise_id)

    if not exercise:
        response = make_response({'error': 'Exercise not found'}, 404)
        return response
    
    exercise_schema = ExerciseSchema()
    exercise_data = exercise_schema.dump(exercise)

    return exercise_data, 200


@app.route('/exercises', methods=['POST'])
def create_exercise():
    data = request.get_json()

    exercise_schema = ExerciseSchema()
    valid_data = exercise_schema.load(data)

    exercise = Exercise(**valid_data)

    db.session.add(exercise)
    db.session.commit()

    return exercise_schema.dump(exercise), 201


@app.route('/exercises/<int:exercise_id>', methods=['DELETE'])
def delete_exercise(exercise_id):
    exercise = Exercise.query.get(exercise_id)

    if not exercise:
        response = make_response({'error': 'Exercise not found'}, 404)
        return response
    
    db.session.delete(exercise)
    db.session.commit()

    response = make_response('', 204)
    return response


@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    workout = Workout.query.get(workout_id)
    exercise = Exercise.query.get(exercise_id)

    if not workout:
        response = make_response({'error': 'Workout not found'}, 404)
        return response

    if not exercise:
        response = make_response({'error': 'Exercise not found'}, 404)
        return response
    
    data = request.get_json()
    data["workout_id"] = workout_id
    data["exercise_id"] = exercise_id

    workout_exercise_schema = WorkoutExerciseSchema()
    valid_data = workout_exercise_schema.load(data)

    workout_exercise = WorkoutExercise(**valid_data)

    db.session.add(workout_exercise)
    db.session.commit()

    return workout_exercise_schema.dump(workout_exercise), 201

if __name__ == '__main__':
    app.run(port=5555, debug=True)
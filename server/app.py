from flask import Flask, make_response, request
from flask_migrate import Migrate
from models import db, Exercise, Workout, WorkoutExercise

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
    return {'message': 'List all workouts'}


@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout_by_id(id):
    return {'message': f'Show workout {id}'}


@app.route('/workouts', methods=['POST'])
def create_workout():
    return {'message': 'Create a workout'}, 201


@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    return '', 204


@app.route('/exercises', methods=['GET'])
def get_exercises():
    return {'message': 'List all exercises'}


@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise_by_id(id):
    return {'message': f'Show exercise {id}'}


@app.route('/exercises', methods=['POST'])
def create_exercise():
    return {'message': 'Create an exercise'}, 201


@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    return '', 204


@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    return {
        'message': f'Add exercise {exercise_id} to workout {workout_id}'
    }, 201

if __name__ == '__main__':
    app.run(port=5555, debug=True)
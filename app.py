import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import hashlib
import os
from datetime import datetime, timedelta
import json

app = Flask(__name__)
app.secret_key = 'fitness_tracker_secret_key_2025'

DATABASE = 'fitness_tracker.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with schema"""
    conn = get_db_connection()
    with open('schema.sql', 'r') as f:
        conn.executescript(f.read())
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

if not os.path.exists(DATABASE):
    init_db()


@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('register.html')

        conn = get_db_connection()

        # Check if username already exists
        existing_user = conn.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone()
        if existing_user:
            flash('Username already exists', 'error')
            conn.close()
            return render_template('register.html')

        # Create new user
        hashed_password = hash_password(password)
        conn.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)',
                    (username, hashed_password))
        conn.commit()
        conn.close()

        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT id, password_hash FROM users WHERE username = ?', 
                           (username,)).fetchone()
        conn.close()

        if user and user['password_hash'] == hash_password(password):
            session['user_id'] = user['id']
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()

    # Get user's routines
    routines = conn.execute(
        'SELECT * FROM routines WHERE user_id = ? ORDER BY created_at DESC',
        (session['user_id'],)
    ).fetchall()

    # Get recent workouts
    recent_workouts = conn.execute("""
        SELECT w.id, w.date, r.name as routine_name, 
               COUNT(we.id) as exercise_count
        FROM workouts w
        LEFT JOIN routines r ON w.routine_id = r.id
        LEFT JOIN workout_exercises we ON w.id = we.workout_id
        WHERE w.user_id = ?
        GROUP BY w.id
        ORDER BY w.date DESC
        LIMIT 5
    """, (session['user_id'],)).fetchall()

    # Get workout stats
    total_workouts = conn.execute(
        'SELECT COUNT(*) as count FROM workouts WHERE user_id = ?',
        (session['user_id'],)
    ).fetchone()['count']

    conn.close()

    return render_template('dashboard.html', 
                         routines=routines, 
                         recent_workouts=recent_workouts,
                         total_workouts=total_workouts)

@app.route('/routines')
def routines():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    user_routines = conn.execute(
        'SELECT * FROM routines WHERE user_id = ? ORDER BY created_at DESC',
        (session['user_id'],)
    ).fetchall()
    conn.close()

    return render_template('routines.html', routines=user_routines)

@app.route('/add_routine', methods=['GET', 'POST'])
def add_routine():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        description = request.form.get('description', '')

        conn = get_db_connection()
        conn.execute(
            'INSERT INTO routines (user_id, name, description) VALUES (?, ?, ?)',
            (session['user_id'], name, description)
        )
        conn.commit()
        conn.close()

        flash('Routine created successfully!', 'success')
        return redirect(url_for('routines'))

    return render_template('add_routine.html')

@app.route('/log_workout', methods=['GET', 'POST'])
def log_workout():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()

    if request.method == 'POST':
        routine_id = request.form['routine_id']
        date = request.form['date']

        # Create workout entry
        cursor = conn.execute(
            'INSERT INTO workouts (user_id, routine_id, date) VALUES (?, ?, ?)',
            (session['user_id'], routine_id, date)
        )
        workout_id = cursor.lastrowid

        # Process exercises
        exercises = request.form.getlist('exercise_name[]')
        sets_list = request.form.getlist('sets[]')
        reps_list = request.form.getlist('reps[]')
        weights_list = request.form.getlist('weight[]')

        for i in range(len(exercises)):
            if exercises[i]:  # Only add if exercise name is provided
                conn.execute("""
                    INSERT INTO workout_exercises 
                    (workout_id, exercise_name, sets, reps, weight) 
                    VALUES (?, ?, ?, ?, ?)
                """, (workout_id, exercises[i], sets_list[i], reps_list[i], weights_list[i]))

        conn.commit()
        conn.close()

        flash('Workout logged successfully!', 'success')
        return redirect(url_for('history'))

    # GET request - show form
    routines = conn.execute(
        'SELECT * FROM routines WHERE user_id = ?',
        (session['user_id'],)
    ).fetchall()
    conn.close()

    return render_template('log_workout.html', routines=routines)

@app.route('/history')
def history():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()

    workouts = conn.execute("""
        SELECT w.id, w.date, r.name as routine_name,
               COUNT(we.id) as exercise_count
        FROM workouts w
        LEFT JOIN routines r ON w.routine_id = r.id
        LEFT JOIN workout_exercises we ON w.id = we.workout_id
        WHERE w.user_id = ?
        GROUP BY w.id
        ORDER BY w.date DESC
    """, (session['user_id'],)).fetchall()

    conn.close()

    return render_template('history.html', workouts=workouts)

@app.route('/workout/<int:workout_id>')
def workout_detail(workout_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()

    # Get workout info
    workout = conn.execute("""
        SELECT w.*, r.name as routine_name
        FROM workouts w
        LEFT JOIN routines r ON w.routine_id = r.id
        WHERE w.id = ? AND w.user_id = ?
    """, (workout_id, session['user_id'])).fetchone()

    if not workout:
        flash('Workout not found', 'error')
        return redirect(url_for('history'))

    # Get exercises for this workout
    exercises = conn.execute(
        'SELECT * FROM workout_exercises WHERE workout_id = ?',
        (workout_id,)
    ).fetchall()

    conn.close()

    return render_template('workout_detail.html', workout=workout, exercises=exercises)

@app.route('/progress/<exercise_name>')
def exercise_progress(exercise_name):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()

    progress_data = conn.execute("""
        SELECT w.date, we.weight, we.sets, we.reps
        FROM workout_exercises we
        JOIN workouts w ON we.workout_id = w.id
        WHERE w.user_id = ? AND we.exercise_name = ?
        ORDER BY w.date
    """, (session['user_id'], exercise_name)).fetchall()

    conn.close()

    return render_template('exercise_progress.html', 
                         exercise_name=exercise_name, 
                         progress_data=progress_data)

@app.route('/api/progress/<exercise_name>')
def api_exercise_progress(exercise_name):
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    conn = get_db_connection()

    progress_data = conn.execute("""
        SELECT w.date, we.weight, we.sets, we.reps
        FROM workout_exercises we
        JOIN workouts w ON we.workout_id = w.id
        WHERE w.user_id = ? AND we.exercise_name = ?
        ORDER BY w.date
    """, (session['user_id'], exercise_name)).fetchall()

    conn.close()

    # Format data for Chart.js
    labels = [row['date'] for row in progress_data]
    weights = [float(row['weight']) for row in progress_data]

    return jsonify({
        'labels': labels,
        'weights': weights
    })

@app.route('/api/exercises')
def api_exercises():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    conn = get_db_connection()

    exercises = conn.execute("""
        SELECT DISTINCT exercise_name
        FROM workout_exercises we
        JOIN workouts w ON we.workout_id = w.id
        WHERE w.user_id = ?
        ORDER BY exercise_name
    """, (session['user_id'],)).fetchall()

    conn.close()

    exercise_names = [row['exercise_name'] for row in exercises]
    return jsonify({'exercises': exercise_names})

if __name__ == '__main__':
    app.run(debug=True)

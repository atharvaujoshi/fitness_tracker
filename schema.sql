-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(80) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Routines table
CREATE TABLE IF NOT EXISTS routines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Workouts table
CREATE TABLE IF NOT EXISTS workouts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    routine_id INTEGER,
    date DATE NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (routine_id) REFERENCES routines (id)
);

-- Workout exercises table
CREATE TABLE IF NOT EXISTS workout_exercises (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    workout_id INTEGER NOT NULL,
    exercise_name VARCHAR(100) NOT NULL,
    sets INTEGER NOT NULL,
    reps INTEGER NOT NULL,
    weight DECIMAL(5,2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (workout_id) REFERENCES workouts (id)
);

-- Insert sample users (for testing - passwords are 'password123')
INSERT OR IGNORE INTO users (username, password_hash) VALUES 
('user1', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f'),
('user2', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f');

-- Insert sample routines
INSERT OR IGNORE INTO routines (user_id, name, description) VALUES 
(1, 'Push Day', 'Chest, Shoulders, Triceps workout'),
(1, 'Pull Day', 'Back and Biceps workout'),
(1, 'Leg Day', 'Lower body workout'),
(2, 'Full Body', 'Complete body workout routine');
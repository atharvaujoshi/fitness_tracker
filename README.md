# Fitness Tracker Web App

A comprehensive workout tracking application built with Flask, featuring a dark theme and mobile-first design.

## Features

- **User Authentication**: Secure registration and login system
- **Workout Routines**: Create and manage custom workout routines
- **Exercise Logging**: Log exercises with sets, reps, and weights
- **Progress Tracking**: Visual charts showing weight progress over time
- **Workout History**: Complete history of all logged workouts
- **Mobile-First Design**: Responsive design optimized for mobile devices
- **Dark Theme**: Modern dark UI with red accent colors

## Tech Stack

- **Backend**: Python Flask
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Charts**: Chart.js
- **Icons**: Font Awesome
- **Deployment**: Render-ready with Gunicorn

## Local Development

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Clone or download this repository
2. Navigate to the project directory:
   ```bash
   cd fitness_tracker
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

6. Run the application:
   ```bash
   python app.py
   ```

7. Open your browser and visit `http://localhost:5000`

### Demo Users

The application comes with two pre-configured demo users:
- **Username**: user1, **Password**: password123
- **Username**: user2, **Password**: password123

## Deployment on Render

This application is ready for deployment on Render.com:

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Use the following settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Environment**: Python 3

The app will automatically create the database and sample data on first run.

## File Structure

```
fitness_tracker/
├── app.py                  # Main Flask application
├── schema.sql             # Database schema
├── requirements.txt       # Python dependencies
├── Procfile              # Render deployment config
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── login.html        # Login page
│   ├── register.html     # Registration page
│   ├── dashboard.html    # Main dashboard
│   ├── routines.html     # Routines management
│   ├── add_routine.html  # Add new routine
│   ├── log_workout.html  # Log workout form
│   ├── history.html      # Workout history
│   ├── workout_detail.html # Individual workout details
│   └── exercise_progress.html # Exercise progress charts
└── static/
    └── css/
        └── dark.css      # Custom dark theme styles
```

## Usage

1. **Registration**: Create a new account or use demo credentials
2. **Create Routines**: Set up workout routines (Push/Pull/Legs, etc.)
3. **Log Workouts**: Record exercises with sets, reps, and weights
4. **Track Progress**: View charts showing improvement over time
5. **Review History**: Browse past workouts and analyze performance

## Features in Detail

### Dark Theme
- Background: #0D1117 (GitHub dark)
- Primary Accent: #E74C3C (Red)
- Text: #FFFFFF (White)
- Mobile-optimized with responsive design

### Progress Charts
- Line charts showing weight progression
- Interactive Chart.js visualizations
- Exercise-specific progress tracking

### Mobile-First Design
- Bootstrap 5 responsive grid
- Touch-friendly interface
- Optimized for smartphones and tablets

## License

This project is open source and available under the MIT License.

## Support

For issues or questions, please check the code comments or create an issue in the repository.

# ---------------------
# BACKEND TESTING
# ---------------------

# tests/test_routes.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from main import app, db
from model import UserAccounts  # Ensure model.py is in the project root
from model import Exercise
from model import Logs  

# ---------------------------
# Test Setup
# ---------------------------
@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for test simplicity
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory DB
    with app.app_context():
        db.create_all()
    with app.test_client() as client:
        yield client


# ---------------------------
# Testing Homepage & Other Pages
# ---------------------------
def test_base_route(client):
    """Test index route (/)"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'html' in response.data.lower()

def test_homepage_route(client):
    """Test homepage route (/home)"""
    response = client.get('/home')
    assert response.status_code == 200
    assert b'html' in response.data.lower()

def test_about_route(client):
    """Test about app route (/about)"""
    response = client.get('/about')
    assert response.status_code == 200
    assert b'html' in response.data.lower()


# ---------------------------
# Testing Login Page (GET and POST)
# ---------------------------
def test_login_get(client):
    """Test login page loads successfully"""
    response = client.get('/login')
    assert response.status_code == 200
    assert b'login' in response.data.lower() or b'email' in response.data.lower()

def test_login_post_invalid(client):
    """Test login with invalid credentials"""
    response = client.post('/login', data={
        'email': 'fake@example.com',
        'password': 'wrongpassword'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'invalid credentials' in response.data.lower()


# ------------------------------------
# Testing Register Page (GET and POST)
# ------------------------------------
def test_register_get(client):
    """Test register page loads successfully"""
    response = client.get('/register')
    assert response.status_code == 200
    assert b'register' in response.data.lower() or b'email' in response.data.lower()

def test_register_post_mismatched_passwords(client):
    """Test register with mismatched passwords"""
    response = client.post('/register', data={
        'username': 'mismatchuser',
        'email': 'mismatch@example.com', 
        'password': 'Password123!',
        'confirm_password': 'DifferentPass!'
    }, follow_redirects=True)
    print(response.data.decode()) 
    assert response.status_code == 200
    assert b'passwords do not match' in response.data.lower()

def test_register_post_weak_password(client):
    """Test register with weak password"""
    response = client.post('/register', data={
        'username': 'weakuser',
        'email': 'weak@example.com',
        'password': 'weak',
        'confirm_password': 'weak'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'passwords must be at least' in response.data.lower()


# ---------------------------
# Testing Register Success
# ---------------------------
def test_register_post_success(client):
    """Test register with valid credentials"""
    response = client.post('/register', data={
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'StrongPass@12',
        'confirm_password': 'StrongPass@12'
    }, follow_redirects=True)
    # Check we are redirected to the homepage after registration
    assert response.status_code == 200
    assert b'html' in response.data.lower()


# ---------------------------
# Testing Login with Valid Credentials
# ---------------------------
def test_login_post_valid(client):
    """Test login with valid credentials"""
    # Register a new user
    client.post('/register', data={
        'username': 'validuser',
        'email': 'valid@example.com',
        'password': 'ValidPass123@',
        'confirm_password': 'ValidPass123@'
    }, follow_redirects=True)

    # Log out (if auto-logged in after registration)
    client.get('/logout', follow_redirects=True)

    # Try to log in with the same credentials
    response = client.post('/login', data={
        'email': 'valid@example.com',
        'password': 'ValidPass123@'
    }, follow_redirects=True)

    # Confirm successful login (redirect to homepage)
    assert response.status_code == 200
    assert b'html' in response.data.lower()


# ---------------------------
# Register & Login Helper
# ---------------------------
def register_and_login(client):
    """Helper to register and log in a test user"""
    # Register the user
    client.post('/register', data={
        'username': 'routeuser',
        'email': 'routeuser@example.com',
        'password': 'RoutePass@123',
        'confirm_password': 'RoutePass@123'
    }, follow_redirects=True)

    # Explicit login to set session
    client.post('/login', data={
        'email': 'routeuser@example.com',
        'password': 'RoutePass@123'
    }, follow_redirects=True)


# ---------------------------
# Testing Routes (Protected)
# ---------------------------
def test_stress_route(client):
    """Test access to /stress page"""
    register_and_login(client)
    response = client.get('/stress')
    assert response.status_code == 200
    assert b'stress' in response.data.lower()

def test_exercise_route(client):
    """Test access to /exercise page"""
    register_and_login(client)
    response = client.get('/exercise')
    assert response.status_code == 200
    assert b'exercise' in response.data.lower()

def test_notes_route(client):
    """Test access to /notes page"""
    register_and_login(client)
    response = client.get('/notes')
    assert response.status_code == 200
    assert b'note' in response.data.lower()

def test_notification_route(client):
    """Test access to /notification page"""
    response = client.get('/notification')
    assert response.status_code == 200
    assert b'notification' in response.data.lower() or b'reminder' in response.data.lower()

def test_breathe_route(client):
    """Test access to /breathe page"""
    response = client.get('/breathe')
    assert response.status_code == 200
    assert b'breathe' in response.data.lower()

def test_logout_route(client):
    """Test /logout route functionality"""
    register_and_login(client)
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'logged out' in response.data.lower() or b'home' in response.data.lower()


# ---------------------------
# Testing POST: /stress (Log Stress Entry)
# ---------------------------
def test_post_stress_log(client):
    """Test logging a new stress entry"""
    register_and_login(client)

    response = client.post('/stress', data={
        'stress-level': '3',
        'stress-cause': 'Exam pressure',
        'additional-notes': 'Upcoming deadline'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'exam pressure' in response.data.lower()
    assert b'upcoming deadline' in response.data.lower()
    assert b'3' in response.data  


# ---------------------------
# Testing POST: /exercise (Log Exercise Entry)
# ---------------------------
def test_post_exercise_log(client):
    """Test logging a new exercise entry via JSON"""
    register_and_login(client)

    response = client.post('/exercise', json={
        'Exercise': 'Cardio',
        'duration': '45 mins'
    })

    assert response.status_code == 200
    json_data = response.get_json()

    assert isinstance(json_data, list)
    assert json_data[0]['type'] == 'Cardio'
    assert json_data[0]['duration'] == '45 mins'


# ---------------------------
# Testing POST: /notes (Log Reflection Note)
# ---------------------------
def test_post_note(client):
    """Test logging a new reflection note"""
    register_and_login(client)

    response = client.post('/notes', data={
        'title': '1234',  
        'description': 'Reflected on my productivity today.'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'notes' in response.data.lower() or b'textarea' in response.data.lower()


# ---------------------------
# Testing DELETE: /stress/delete/<id>
# ---------------------------
def test_delete_stress_log(client):
    """Test deleting a stress log"""
    register_and_login(client)

    # Create a stress log
    client.post('/stress', data={
        'stress-level': '4',
        'stress-cause': 'Deadline',
        'additional-notes': 'Group project pressure'
    }, follow_redirects=True)

    # Fetch logs via /get-latest-logs to get ID
    response = client.get('/get-latest-logs')
    logs = response.get_json()
    assert logs, "No logs found"
    log_id = logs[0]['id']

    # DELETE the log
    delete_response = client.delete(f'/stress/delete/{log_id}')
    assert delete_response.status_code == 200
    assert delete_response.get_json()['success'] is True

    # Verify it was deleted
    confirm_response = client.get('/get-latest-logs')
    updated_logs = confirm_response.get_json()
    assert all(log['id'] != log_id for log in updated_logs)


# ---------------------------
# Testing DELETE: /exercise/delete/<id>
# ---------------------------
def test_delete_exercise_log(client):
    """Test deleting an exercise log (manual insert)"""
    register_and_login(client)

    # Fetch the user manually
    with app.app_context():
        user = UserAccounts.query.filter_by(email='routeuser@example.com').first()

        new_exercise = Exercise(
            made_by=user.id,
            type=1,  # assuming 1 is valid if type is int; otherwise use a valid string or enum if adjusted
            duration="30 mins"
        )
        db.session.add(new_exercise)
        db.session.commit()
        log_id = new_exercise.log_id

    # DELETE the exercise
    delete_response = client.delete(f'/exercise/delete/{log_id}')
    assert delete_response.status_code == 200
    assert delete_response.get_json()['success'] is True

    # Confirm deletion
    confirm_response = client.get('/get-latest-exercises')
    updated_logs = confirm_response.get_json()
    assert all(log['id'] != log_id for log in updated_logs)


# ---------------------------
# Testing GET: /stress/<id> (Legacy Delete)
# ---------------------------
def test_legacy_stress_delete(client):
    register_and_login(client)

    # Create a stress log
    client.post('/stress', data={
        'stress-level': '5',
        'stress-cause': 'Testing legacy delete',
        'additional-notes': 'This should be deleted'
    }, follow_redirects=True)

    # Get the log ID
    logs = client.get('/get-latest-logs').get_json()
    assert logs, "No stress logs found"
    log_id = logs[0]['id']

    # Delete using legacy GET route
    response = client.get(f'/stress/{log_id}', follow_redirects=True)
    assert response.status_code == 200

    # Confirm it's gone
    updated_logs = client.get('/get-latest-logs').get_json()
    assert all(log['id'] != log_id for log in updated_logs)


# ---------------------------
# Testing GET: /exercise/<id> (Legacy Delete)
# ---------------------------
def test_legacy_exercise_delete(client):
    register_and_login(client)

    # Insert exercise manually
    with app.app_context():
        user = UserAccounts.query.filter_by(email='routeuser@example.com').first()
        new_exercise = Exercise(made_by=user.id, type=1, duration="20 mins")
        db.session.add(new_exercise)
        db.session.commit()
        log_id = new_exercise.log_id

    # Call GET-based delete
    response = client.get(f'/exercise/{log_id}', follow_redirects=True)
    assert response.status_code == 200

    # Confirm deletion
    updated_logs = client.get('/get-latest-exercises').get_json()
    assert all(log['id'] != log_id for log in updated_logs)


# ---------------------------
# Testing GET: /clear-exercises
# ---------------------------
def test_clear_exercises(client):
    register_and_login(client)

    # Insert two exercises
    with app.app_context():
        user = UserAccounts.query.filter_by(email='routeuser@example.com').first()
        for _ in range(2):
            db.session.add(Exercise(made_by=user.id, type=1, duration="10 mins"))
        db.session.commit()

    # Confirm they exist
    logs = client.get('/get-latest-exercises').get_json()
    assert len(logs) >= 2

    # Clear them
    response = client.get('/clear-exercises')
    assert response.status_code == 200
    assert b'cleared' in response.data.lower()

    # Confirm they're gone
    updated_logs = client.get('/get-latest-exercises').get_json()
    assert updated_logs == []


# ---------------------------
# Testing POST: /stress (Edge Case - Invalid Data)
# ---------------------------
def test_post_stress_invalid_data(client):
    """Test logging a stress entry with invalid data"""
    register_and_login(client)

    # Test missing stress-level
    response = client.post('/stress', data={
        'stress-cause': 'Exam pressure',
        'additional-notes': 'Upcoming deadline'
    }, follow_redirects=True)
    
    # Expecting a 400 Bad Request error
    assert response.status_code == 400
    assert b'bad request' in response.data.lower()

    # Test non-integer stress-level
    response = client.post('/stress', data={
        'stress-level': 'invalid',  # Invalid stress level
        'stress-cause': 'Exam pressure',
        'additional-notes': 'Upcoming deadline'
    }, follow_redirects=True)

    # Check that the stress-level gets stored, even though it's invalid
    assert response.status_code == 200  
    assert b'exam pressure' in response.data.lower()  
    assert b'upcoming deadline' in response.data.lower()  
    assert b'invalid' in response.data.lower()  


# ---------------------------
# Testing GET: /get-latest-logs
# ---------------------------
def test_get_latest_logs(client):
    """Test fetching the latest stress logs"""
    register_and_login(client)

    # Add some logs first
    client.post('/stress', data={
        'stress-level': '3',
        'stress-cause': 'Exam pressure',
        'additional-notes': 'Upcoming deadline'
    }, follow_redirects=True)

    # Get the latest logs
    response = client.get('/get-latest-logs')
    logs = response.get_json()
    assert len(logs) > 0 
    assert 'Exam pressure' in [log['cause'] for log in logs]
    assert 'Upcoming deadline' in [log['description'] for log in logs]


# ---------------------------
# Testing GET: /get-latest-exercises
# ---------------------------
def test_get_latest_exercises(client):
    """Test fetching the latest exercise logs"""
    register_and_login(client)

    # Insert exercise manually
    with app.app_context():
        user = UserAccounts.query.filter_by(email='routeuser@example.com').first()
        new_exercise = Exercise(made_by=user.id, type=1, duration="45 mins")
        db.session.add(new_exercise)
        db.session.commit()

    # Get the latest exercises
    response = client.get('/get-latest-exercises')
    exercises = response.get_json()
    assert len(exercises) > 0  
    assert '45 mins' in [exercise['duration'] for exercise in exercises]


# ---------------------------
# Testing GET: /clear-exercises
# ---------------------------
def test_clear_exercises(client):
    """Test clearing all exercise logs"""
    register_and_login(client)

    # Insert two exercises manually
    with app.app_context():
        user = UserAccounts.query.filter_by(email='routeuser@example.com').first()
        for _ in range(2):
            db.session.add(Exercise(made_by=user.id, type=1, duration="10 mins"))
        db.session.commit()

    # Confirm they exist
    response = client.get('/get-latest-exercises')
    exercises = response.get_json()
    assert len(exercises) == 2  # Ensure two exercises were added

    # Clear them
    response = client.get('/clear-exercises')
    assert response.status_code == 200
    assert b'cleared' in response.data.lower()

    # Confirm they're gone
    response = client.get('/get-latest-exercises')
    exercises = response.get_json()
    assert len(exercises) == 0  # Ensure exercises were cleared


# ---------------------------
# Testing GET: /get-latest-exercises
# ---------------------------
def test_get_latest_exercises(client):
    """Test fetching the latest exercise logs"""
    register_and_login(client)

    # Clear existing exercises
    with app.app_context():
        db.session.query(Exercise).delete()
        db.session.commit()

    # Insert exercise manually
    with app.app_context():
        user = UserAccounts.query.filter_by(email='routeuser@example.com').first()
        new_exercise = Exercise(made_by=user.id, type=1, duration="45 mins")
        db.session.add(new_exercise)
        db.session.commit()

    # Get the latest exercises
    response = client.get('/get-latest-exercises')
    exercises = response.get_json()
    assert len(exercises) > 0  
    assert '45 mins' in [exercise['duration'] for exercise in exercises]


# ---------------------------
# Testing GET: /clear-exercises
# ---------------------------
def test_clear_exercises(client):
    """Test clearing all exercise logs"""
    register_and_login(client)

    # Clear existing exercises
    with app.app_context():
        db.session.query(Exercise).delete()
        db.session.commit()

    # Insert two exercises manually
    with app.app_context():
        user = UserAccounts.query.filter_by(email='routeuser@example.com').first()
        for _ in range(2):
            db.session.add(Exercise(made_by=user.id, type=1, duration="10 mins"))
        db.session.commit()

    # Confirm they exist
    response = client.get('/get-latest-exercises')
    exercises = response.get_json()
    assert len(exercises) == 2  

    # Clear them
    response = client.get('/clear-exercises')
    assert response.status_code == 200
    assert b'cleared' in response.data.lower()

    # Step 5: Confirm they're gone
    response = client.get('/get-latest-exercises')
    exercises = response.get_json()
    assert len(exercises) == 0  

# ---------------------------
# Testing Large Number of Stress Logs
# ---------------------------
def test_large_number_of_stress_logs(client):
    """Test handling a large number of stress logs"""
    register_and_login(client)

    # Clear existing logs in the database
    with app.app_context():
        db.session.query(Logs).delete()  
        db.session.commit()

    # Insert a large number of stress logs
    for i in range(1000): 
        client.post('/stress', data={
            'stress-level': '3',
            'stress-cause': f'Cause {i}',
            'additional-notes': f'Notes for log {i}'
        }, follow_redirects=True)

    # Confirm the logs were added
    response = client.get('/get-latest-logs')
    logs = response.get_json()
    assert len(logs) == 1000  

    # Check for the cause text, case-insensitive
    assert b'cause' in response.data.lower() 


# ---------------------------
# Testing Large Number of Exercise Logs
# ---------------------------
def test_large_number_of_exercise_logs(client):
    """Test handling a large number of exercise logs"""
    register_and_login(client)

    # Clear existing exercises in the database
    with app.app_context():
        db.session.query(Exercise).delete()  
        db.session.commit()

    # Manually insert a large number of exercise logs
    with app.app_context():
        user = UserAccounts.query.filter_by(email='routeuser@example.com').first()
        for i in range(1000):  
            new_exercise = Exercise(made_by=user.id, type=1, duration=f"30 mins {i}")
            db.session.add(new_exercise)
        db.session.commit()

    # Confirm the exercises were added
    response = client.get('/get-latest-exercises')
    exercises = response.get_json()
    assert len(exercises) == 1000  # Ensure only 1000 exercises were added

    # Check for the exercise type, using the integer value (1) instead of 'Cardio'
    assert b'1' in response.data.lower()  
    assert b'30 mins' in response.data.lower()  


from flask import Flask, render_template, redirect, flash, get_flashed_messages, url_for, request
from model import *
from flask_migrate import Migrate
from flask_wtf import *
from flask_mail import *
from itsdangerous import URLSafeTimedSerializer
import base64
import secrets
from functools import wraps
from sqlalchemy import update
from datetime import datetime, timedelta, timezone
# from password_strength import PasswordPolicy
from flask import jsonify


app = Flask(__name__)

app.secret_key = secrets.token_hex(16)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///HealthAdviceGroupDatabase.db"
app.config["SECURITY_PASSWORD_SALT"] = secrets.token_hex(16)


mail = Mail(app)
mail.init_app(app)
db.init_app(app)
migrate = Migrate(app, db)
login.login_view = "login"
login.init_app(app)

with app.app_context():
    db.create_all()

# initialises all configured settings #

tokenprotection = CSRFProtect(app)

# ---- simple password checker to replace password_strength ----
def check_password_rules(pwd: str) -> str | None:
    """Return an error message if password is weak, otherwise None."""
    if len(pwd) < 8:
        return "Password must be at least 8 characters."
    if not any(c.isupper() for c in pwd):
        return "Password must contain at least 1 uppercase letter."
    # count non-letters (digits and symbols)
    non_letters = sum(1 for c in pwd if not c.isalpha())
    if non_letters < 2:
        return "Password must contain at least 2 non-letter characters (numbers or symbols)."
    return None

class SignupForm(FlaskForm):
    recaptcha = RecaptchaField()


def database_reset():
    with app.app_context():
        db.drop_all()
        db.create_all()
        data = UserAccounts.query.all()
        for i in data:
            print(i.username)
            print(i.password_hash)


#database_reset()


@app.route("/")
def base():
    return render_template("index.html")

@app.route("/home")
def homepage():
    return render_template("homepage.html")

@app.route("/about")
def about_app():
    return render_template("about_app.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You’ve been logged out.")
    return redirect(url_for("homepage"))

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        if current_user.is_authenticated:
            # redirects if user logged in #
            return redirect(url_for('homepage'))
        return render_template("login.html")
    if request.method == "POST":
        with app.app_context():
            try:
                email = request.form["email"]
                user_data = UserAccounts.query.filter_by(email=email).first()
                # checks database if username exists or not,
                # then checks password against stored hash and logs the user in if both checks are passed #
                if user_data is None or not user_data.check_password(user_password=request.form["password"]):
                    flash("Invalid credentials!")
                    return render_template('login.html')
                login_user(user_data)
                return redirect(url_for('homepage'))
            except Exception as e:
                flash("An unexpected error occurred when adding your account to our system")
                flash(f'{e}')
                return render_template('login.html')


# policy = PasswordPolicy.from_names(
#     length=8,  # min length: 8
#     uppercase=1,  # need min. 1 uppercase letters
#     nonletters=2,  # need min. 2 non-letter characters (digits, specials, anything)
# )

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        form = SignupForm()
        if current_user.is_authenticated:
            return redirect(url_for("homepage"))
        return render_template("register.html", form=form)

    if request.method == "POST":
        if current_user.is_authenticated:
            return redirect(url_for("homepage"))

        try:
            username = request.form["username"]
            email = request.form["email"]
            user_password = request.form["password"]
            confirm_password = request.form["confirm_password"]

            # ✅ correct checks
            username_exists = UserAccounts.query.filter_by(username=username).first()
            email_exists = UserAccounts.query.filter_by(email=email).first()

            if username_exists or email_exists:
                flash("Email or username is already in use.")
                return render_template("register.html")

            # ✅ password rules (replacement for password_strength)
            pwd_error = check_password_rules(user_password)
            if pwd_error:
                flash(pwd_error)
                return render_template("register.html")

            if user_password != confirm_password:
                flash("Both passwords do not match.")
                return render_template("register.html")

            # ✅ create user
            user = UserAccounts(username=username, email=email)
            user.set_password(user_password)

            db.session.add(user)
            db.session.commit()

            login_user(user)
            return redirect(url_for("homepage"))

        except Exception as e:
            db.session.rollback()
            flash("An unexpected error occurred when adding your account to our system")
            flash(str(e))
            return render_template("register.html")



@app.route("/stress", methods=['GET', 'POST'])
@login_required
def stress():
    if request.method == "GET":
        with app.app_context():
            user_logs = Logs.query.filter_by(made_by=current_user.id)
            stress_logs = [log.to_dict() for log in user_logs]
            return render_template('stress.html', logs=stress_logs)
    if request.method == "POST":
        if request.is_json:
            data = request.get_json()
            stress_level = data.get("stress-level")
            cause = data.get("stress-cause")
            notes = data.get("additional-notes")
        else:
            stress_level = request.form["stress-level"]
            cause = request.form["stress-cause"]
            notes = request.form["additional-notes"]
    
        now = datetime.now()
        log = Logs(made_by=current_user.id, rating=stress_level, cause=cause, user_description=notes, time_recorded=now)

        db.session.add(log)
        db.session.commit()

        user_logs = Logs.query.filter_by(made_by=current_user.id)
        stress_logs = [log.to_dict() for log in user_logs]
        return render_template("stress.html", logs=stress_logs)


@app.route('/stress/<id>', methods=['GET'])
@login_required
def delete_note(id):
    if request.method == "GET":
        with app.app_context():
            stress_log = Logs.query.filter_by(log_id=id, made_by=current_user.id).first()
            if stress_log:
                db.session.delete(stress_log)
                db.session.commit()
                user_logs = Logs.query.filter_by(made_by=current_user.id)
                stress_logs = [log.to_dict() for log in user_logs]
                return render_template('stress.html', logs=stress_logs)
            else:
                flash("There was an error removing your log")

@app.route('/stress/delete/<int:id>', methods=['DELETE'])
@login_required
def delete_stress(id):
    with app.app_context():
        stress_log = Logs.query.filter_by(log_id=id, made_by=current_user.id).first()
        if stress_log:
            db.session.delete(stress_log)
            db.session.commit()
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Entry not found'}), 404



@app.route("/exercise", methods=['GET', 'POST'])
@login_required
def exercise():
    if request.method == "GET":
        return render_template('exercise.html', exercise=[])  # Show nothing on refresh

    if request.method == "POST":
        if request.is_json:
            data = request.get_json()
            exercise = data.get("Exercise")
            duration = data.get("duration")

            if exercise == "Custom":
                exercise = data.get("custom-exercise")

            now = datetime.now().strftime("%Y-%m-%d — %H:%M")

            return jsonify([{
                "type": exercise,
                "duration": duration,
                "time": now
            }]), 200

        return jsonify({"error": "Invalid data format"}), 400

@app.route('/exercise/<id>', methods=['GET'])
@login_required
def delete_exercise(id):
    if request.method == "GET":
        with app.app_context():
            exercise = Exercise.query.filter_by(log_id=id, made_by=current_user.id).first()
            if exercise:
                db.session.delete(exercise)
                db.session.commit()
                user_exercise = Exercise.query.filter_by(made_by=current_user.id)
                exercises_data = [exercise.to_dict() for exercise in user_exercise]
                return render_template('exercise.html', exercise=exercises_data)
            else:
                flash("There was an error removing your exercise")


@app.route('/exercise/delete/<int:id>', methods=['DELETE'])
@login_required
def delete_exercise_ajax(id):
    with app.app_context():
        exercise = Exercise.query.filter_by(log_id=id, made_by=current_user.id).first()
        if exercise:
            db.session.delete(exercise)
            db.session.commit()
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Exercise not found'}), 404


@app.route("/notes", methods=['GET', 'POST'])
@login_required
def notes():
    if request.method == "GET":
        with app.app_context():
            user_notes = Exercise.query.filter_by(made_by=current_user.id)
            return render_template('notes.html', exercise=user_notes)
    if request.method == "POST":
        with app.app_context():
            try:
                note_title = request.form["title"]
                note_description = request.form["description"]
                note = Notes(made_by=current_user.id, title=note_title, user_description=note_description)
                db.session.add(note)
                db.session.commit()
                user_notes = Notes.query.filter_by(made_by=current_user.id)
                db.session.commit()
                return redirect(url_for('notes'))
            except Exception as e:
                print(e)
                return render_template('notes.html')


@app.route("/breathe")
def breathe_flow():
    return render_template("breathe_flow.html")


@app.route("/notification", methods=['GET', 'POST'])
def notification():
    if request.method == "GET":
        return render_template("notification.html")


@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == "GET":
      return render_template("profile.html")
    if request.method == "POST":
       with app.app_context():
         try:
           uploaded_picture = request.files["uploaded_image"]
           encoded_image = base64.b64encode(uploaded_picture.read())
           string_for_database = encoded_image.decode('utf-8')
           update_query = (update(UserAccounts).where(UserAccounts.id == current_user.id).values(profile_image=string_for_database))
           db.session.execute(update_query)
           db.session.commit()
           return 'uploaded'
         except:
             flash("there was an error when attempting to upload your picture")
             return redirect(url_for('homepage'))

# Route to get the latest stress logs
@app.route("/get-latest-logs")
@login_required
def get_latest_logs():
    user_logs = Logs.query.filter_by(made_by=current_user.id).all()
    logs_dict = [log.to_dict() for log in user_logs]
    return jsonify(logs_dict)

# Route to get the latest exercises
@app.route("/get-latest-exercises")
@login_required
def get_latest_exercises():
    exercises = Exercise.query.filter_by(made_by=current_user.id).all()
    exercises_data = [e.to_dict() for e in exercises]
    return jsonify(exercises_data)

# Route to clear all exercises
@app.route("/clear-exercises")
@login_required
def clear_exercises():
    Exercise.query.filter_by(made_by=current_user.id).delete()
    db.session.commit()
    return "All your exercises have been cleared."

if __name__ == '__main__':
    app.run(debug=True)


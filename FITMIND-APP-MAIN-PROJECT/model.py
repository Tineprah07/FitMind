from flask_sqlalchemy import SQLAlchemy, query
import flask_login
from flask_login import UserMixin, login_user, logout_user, LoginManager, login_required, user_logged_in, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy import func, update

db = SQLAlchemy()
login = flask_login.LoginManager()


class UserAccounts(UserMixin, db.Model):
    __tablename__ = "User Accounts"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String())
    profile_image = db.Column(db.String())
    registered_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    verified = db.Column(db.Boolean(), default=False)

    def set_password(self, user_password):
        self.password_hash = generate_password_hash(user_password)

    def check_password(self, user_password):
        return check_password_hash(self.password_hash, user_password)

# functions for login system, such as loading users and setting/checking passwords #
@login.user_loader
def load_user(id):
    return db.session.get(UserAccounts, int(id))

class Posts(db.Model):
    __tablename__ = "Website Posts"
    post_id = db.Column(db.Integer, primary_key=True)
    made_by = db.Column(db.Integer, db.ForeignKey(UserAccounts.id))
    post_title = db.Column(db.String(100))
    post_content = db.Column(db.String(300))
    on_page = db.Column(db.String(100))


class Logs(db.Model):
    log_id = db.Column(db.Integer, primary_key=True)
    made_by = db.Column(db.Integer, db.ForeignKey(UserAccounts.id))
    time_recorded = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    rating = db.Column(db.Integer(), nullable=False)
    cause = db.Column(db.String(50))
    user_description = db.Column(db.String(300))

    def to_dict(self):
        return {
            "id": self.log_id,
            "made_by":  self.made_by,
            "time": self.time_recorded,
            "rating": self.rating,
            "cause": self.cause,
            "description": self.user_description
            # convert other fields as needed
        }

class Exercise(db.Model):
    log_id = db.Column(db.Integer, primary_key=True)
    made_by = db.Column(db.Integer, db.ForeignKey(UserAccounts.id))
    time_recorded = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    type = db.Column(db.Integer(), nullable=False)
    duration = db.Column(db.String(50))

    def to_dict(self):
        return {
            "id": self.log_id,
            "made_by":  self.made_by,
            "time": self.time_recorded,
            "type": self.type,
            "duration": self.duration,
            # convert other fields as needed
        }

class Notes(db.Model):
    note_id = db.Column(db.Integer, primary_key=True)
    made_by = db.Column(db.Integer, db.ForeignKey(UserAccounts.id))
    time_recorded = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    title = db.Column(db.Integer(), nullable=False)
    user_description = db.Column(db.String(300))




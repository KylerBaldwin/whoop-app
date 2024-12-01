from datetime import datetime

from flask_login import UserMixin
from sqlalchemy.sql import func

from . import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(250))
    username = db.Column(db.String(150))
    WhoopAuth = db.relationship('WhoopAuth')

class WhoopAuth(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    refresh_token = db.Column(db.String(250), nullable=True)
    api_key = db.Column(db.String(250), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # Relationship to Whoop Tables (One-to-many)
    recoveries = db.relationship('Recovery', backref='whoopauth', lazy=True)
    sleeps = db.relationship('Sleep', backref='whoopauth', lazy=True)
    workouts = db.relationship('Workout', backref='whoopauth', lazy=True)
    cycles = db.relationship('Cycle', backref='whoopauth', lazy=True)

class Recovery(db.Model):
    # Primary key for the table (auto-generated)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Other columns
    cycle_id = db.Column(db.Integer, nullable=False)
    sleep_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    score_state = db.Column(db.String, nullable=False)
    
    # Flattened fields from the 'score' sub-object
    user_calibrating = db.Column(db.Boolean, nullable=False)
    recovery_score = db.Column(db.Integer, nullable=False)
    resting_heart_rate = db.Column(db.Integer, nullable=False)
    hrv_rmssd_milli = db.Column(db.Float, nullable=False)
    spo2_percentage = db.Column(db.Float, nullable=False)
    skin_temp_celsius = db.Column(db.Float, nullable=False)

    # Relationship to WhoopAuth
    whoopauth_id = db.Column(db.Integer, db.ForeignKey('whoop_auth.id'))

class Sleep(db.Model):
    # Primary key for the table (auto-generated)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Other columns
    cycle_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=False)
    timezone_offset = db.Column(db.String, nullable=False)
    nap = db.Column(db.Boolean, nullable=False)
    score_state = db.Column(db.String, nullable=False)
    
    # Flattened fields from the 'score' sub-object
    stage_summary = db.Column(db.JSON, nullable=True)  # You can store JSON objects or text
    sleep_needed = db.Column(db.JSON, nullable=True)    # Same as above
    respiratory_rate = db.Column(db.Float, nullable=False)
    sleep_performance_percentage = db.Column(db.Float, nullable=False)
    sleep_consistency_percentage = db.Column(db.Float, nullable=False)
    sleep_efficiency_percentage = db.Column(db.Float, nullable=False)

    # Relationship to WhoopAuth
    whoopauth_id = db.Column(db.Integer, db.ForeignKey('whoop_auth.id'))

class Workout(db.Model):
        # Primary key for the table (auto-generated)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Other columns
    sport_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=False)
    timezone_offset = db.Column(db.String, nullable=False)
    score_state = db.Column(db.String, nullable=False)

    # Flattened fields from the 'score' sub-object
    strain = db.Column(db.Float, nullable=False)
    average_heart_rate = db.Column(db.Integer, nullable=False)
    max_heart_rate = db.Column(db.Integer, nullable=False)
    kilojoule = db.Column(db.Float, nullable=False)
    percent_recorded = db.Column(db.Float, nullable=False)
    distance_meter = db.Column(db.Float, nullable=False)
    altitude_gain_meter = db.Column(db.Float, nullable=False)
    altitude_change_meter = db.Column(db.Float, nullable=False)
    zone_duration = db.Column(db.JSON, nullable=True)  # Can store as a JSON object

    # Relationship to WhoopAuth
    whoopauth_id = db.Column(db.Integer, db.ForeignKey('whoop_auth.id'))

class Cycle(db.Model):
    # Primary key for the table (auto-generated)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Other columns
    user_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=False)
    timezone_offset = db.Column(db.String, nullable=False)
    score_state = db.Column(db.String, nullable=False)

    # Flattened fields from the 'score' sub-object
    strain = db.Column(db.Float, nullable=False)
    kilojoule = db.Column(db.Float, nullable=False)
    average_heart_rate = db.Column(db.Integer, nullable=False)
    max_heart_rate = db.Column(db.Integer, nullable=False)

    # Relationship to WhoopAuth
    whoopauth_id = db.Column(db.Integer, db.ForeignKey('whoop_auth.id'))
from __future__ import annotations

import os
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from . import db

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, default="Usuário")
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, pwd: str):
        self.password_hash = generate_password_hash(pwd)

    def check_password(self, pwd: str) -> bool:
        return check_password_hash(self.password_hash, pwd)

class Season(db.Model):
    __tablename__ = "seasons"
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False, default=1)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    thumbnail_url = db.Column(db.Text, nullable=True)
    is_published = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    episodes = db.relationship("Episode", backref="season", cascade="all,delete", lazy=True, order_by="Episode.episode_number.asc()")

class Episode(db.Model):
    __tablename__ = "episodes"
    id = db.Column(db.Integer, primary_key=True)
    season_id = db.Column(db.Integer, db.ForeignKey("seasons.id"), nullable=False)
    episode_number = db.Column(db.Integer, nullable=False, default=1)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    duration_minutes = db.Column(db.Integer, nullable=True)

    youtube_url = db.Column(db.Text, nullable=False)
    thumbnail_url = db.Column(db.Text, nullable=True)

    # 'vertical' (stories/reels) or 'horizontal'
    aspect = db.Column(db.String(16), nullable=False, default="vertical")

    is_published = db.Column(db.Boolean, default=True, nullable=False)
    release_at = db.Column(db.DateTime, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

def seed_admin_if_needed():
    admin_email = os.getenv("ADMIN_EMAIL")
    admin_password = os.getenv("ADMIN_PASSWORD")
    admin_name = os.getenv("ADMIN_NAME", "Admin")

    if not admin_email or not admin_password:
        return

    existing = User.query.filter_by(email=admin_email.lower().strip()).first()
    if existing:
        # ensure admin
        if not existing.is_admin:
            existing.is_admin = True
            db.session.commit()
        return

    u = User(
        name=admin_name,
        email=admin_email.lower().strip(),
        is_admin=True,
    )
    u.set_password(admin_password)
    db.session.add(u)
    db.session.commit()

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from ..forms import LoginForm
from ..models import User
from .. import db

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.get("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm()
    return render_template("auth/login.html", form=form)

@auth_bp.post("/login")
def login_post():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    form = LoginForm()
    if not form.validate_on_submit():
        flash("Verifique seus dados e tente novamente.", "error")
        return render_template("auth/login.html", form=form), 400

    email = form.email.data.lower().strip()
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(form.password.data):
        flash("Email ou senha inválidos.", "error")
        return render_template("auth/login.html", form=form), 401

    login_user(user, remember=bool(form.remember.data))
    nxt = request.args.get("next")
    return redirect(nxt or url_for("main.home"))

@auth_bp.get("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

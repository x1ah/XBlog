#!/usr/bin/env python
# coding:utf-8

from flask import render_template, redirect, request, url_for, flash, current_app
from flask_login import login_user, login_required, logout_user, current_user
from . import auth
from .forms import LoginForm
from ..models import User


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.email == current_app.config.get("ADMIN") and \
            form.password.data == current_app.config.get("ADMIN_PASSWORD") and \
                user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash("Login succeed.")
            return redirect(request.args.get("next") or url_for("main.index"))
        flash("Invalid Username or password.")
    return render_template("auth/login.html", form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Log out succeed.")
    return redirect(request.args.get("next") or url_for("main.index"))

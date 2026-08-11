from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from app.services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated: return redirect(url_for("members.index"))
    if request.method == "POST":
        user = AuthService().authenticate(request.form.get("username", ""), request.form.get("password", ""))
        if user:
            login_user(user)
            return redirect(url_for("members.index"))
        flash("Λανθασμένο όνομα χρήστη ή κωδικός.", "error")
    return render_template("login.html")

@auth_bp.post("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

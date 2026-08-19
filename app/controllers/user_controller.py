from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from app.controllers.security import roles_required
from app.services.auth_service import AuthService

users_bp = Blueprint("users", __name__, url_prefix="/users")

@users_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        password = request.form.get("password", "")
        if password != request.form.get("password_confirmation", ""): flash("Η επιβεβαίωση κωδικού δεν ταιριάζει.", "error")
        else:
            try:
                AuthService().update_own_credentials(current_user.id, request.form.get("username"), password or None)
                flash("Τα στοιχεία σύνδεσής σας ενημερώθηκαν.", "success")
                return redirect(url_for("users.profile"))
            except (ValueError, LookupError) as error: flash(str(error), "error")
    return render_template("profile.html")

@users_bp.get("/")
@roles_required("admin")
def index(): return render_template("users.html", users=AuthService().list_users())

@users_bp.route("/new", methods=["GET", "POST"])
@roles_required("admin")
def create():
    if request.method == "POST":
        password = request.form.get("password", "")
        if password != request.form.get("password_confirmation", ""):
            flash("Η επιβεβαίωση κωδικού δεν ταιριάζει.", "error")
        else:
            try:
                AuthService().create_user(request.form.get("username"), password, request.form.get("role"))
                flash("Ο χρήστης δημιουργήθηκε.", "success")
                return redirect(url_for("users.index"))
            except ValueError as error: flash(str(error), "error")
    return render_template("user_form.html")

@users_bp.route("/<int:user_id>/role", methods=["GET", "POST"])
@roles_required("admin")
def edit_role(user_id):
    service = AuthService(); user = service.get_user(user_id)
    if not user: abort(404)
    if request.method == "POST":
        try:
            service.update_user_role(user_id, request.form.get("role")); flash("Ο ρόλος χρήστη ενημερώθηκε.", "success")
            return redirect(url_for("users.index"))
        except ValueError as error: flash(str(error), "error")
    return render_template("role_form.html", user=user)

@users_bp.post("/<int:user_id>/delete")
@roles_required("admin")
def delete(user_id):
    try: AuthService().delete_user(user_id, current_user.id); flash("Ο χρήστης διαγράφηκε.", "success")
    except LookupError: abort(404)
    except ValueError as error: flash(str(error), "error")
    return redirect(url_for("users.index"))

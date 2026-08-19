from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import login_required
from app.controllers.security import roles_required
from app.services.organization_service import OrganizationService

members_bp = Blueprint("members", __name__)

def data_from_form():
    return {"first_name": request.form.get("first_name", ""), "last_name": request.form.get("last_name", ""), "address": request.form.get("address", ""), "organization_duty": request.form.get("organization_duty", ""), "rank": request.form.get("rank", ""), "phone_number": request.form.get("phone_number", ""), "group_id": int(request.form.get("group_id", 0))}

@members_bp.get("/")
@login_required
def index():
    service = OrganizationService()
    group_id = request.args.get("group", type=int)
    return render_template("members.html", members=service.list_members(group_id), groups=service.list_groups(), selected_group=group_id)

@members_bp.route("/members/new", methods=["GET", "POST"])
@roles_required("admin")
def create():
    service = OrganizationService()
    if request.method == "POST":
        try:
            service.create_member(data_from_form());
            flash("Το μέλος προστέθηκε.", "success")
            return redirect(url_for("members.index"))
        except (ValueError, TypeError) as error: flash(str(error), "error")
    return render_template("member_form.html", groups=service.list_groups(), member=None)

@members_bp.route("/members/<int:member_id>/edit", methods=["GET", "POST"])
@roles_required("admin")
def edit(member_id):
    service = OrganizationService(); member = service.get_member(member_id)
    if not member: abort(404)
    if request.method == "POST":
        try:
            service.update_member(member_id, data_from_form());
            flash("Τα στοιχεία ενημερώθηκαν.", "success")
            return redirect(url_for("members.index"))
        except (ValueError, TypeError) as error:
            flash(str(error), "error")
    return render_template("member_form.html", groups=service.list_groups(), member=member)

@members_bp.post("/members/<int:member_id>/delete")
@roles_required("admin")
def delete(member_id):
    try: OrganizationService().delete_member(member_id); flash("Το μέλος διαγράφηκε.", "success")
    except LookupError: abort(404)
    return redirect(url_for("members.index"))

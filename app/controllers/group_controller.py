from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from app.controllers.security import roles_required
from app.services.organization_service import OrganizationService

groups_bp = Blueprint("groups", __name__, url_prefix="/groups")

@groups_bp.route("/", methods=["GET", "POST"])
@roles_required("admin")
def index():
    service = OrganizationService()
    if request.method == "POST":
        try: service.create_group(request.form.get("name", ""), request.form.get("description", "")); flash("Η ομάδα προστέθηκε.", "success")
        except ValueError as error: flash(str(error), "error")
        return redirect(url_for("groups.index"))
    return render_template("groups.html", groups=service.list_groups())


@groups_bp.post("/<int:group_id>/delete")
@roles_required("admin")
def delete(group_id):
    try: OrganizationService().delete_group(group_id); flash("Η ομάδα διαγράφηκε.", "success")
    except LookupError: abort(404)
    except ValueError as error: flash(str(error), "error")
    return redirect(url_for("groups.index"))

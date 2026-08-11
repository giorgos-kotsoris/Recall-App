from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app.infrastructure.database import db


class UserModel(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="viewer")

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class GroupModel(db.Model):
    __tablename__ = "groups"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(250), nullable=True)
    members = db.relationship("MemberModel", back_populates="group", lazy="select")


class MemberModel(db.Model):
    __tablename__ = "members"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(250), nullable=False)
    organization_duty = db.Column(db.String(120), nullable=False)
    rank = db.Column(db.String(80), nullable=False, default="")
    phone_number = db.Column(db.String(30), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    group = db.relationship("GroupModel", back_populates="members")


def migrate_schema() -> None:
    """Ενημερώνει με ασφάλεια υπάρχουσες SQLite βάσεις."""
    columns = {column[1] for column in db.session.execute(db.text("PRAGMA table_info(members)"))}
    if "rank" not in columns:
        db.session.execute(db.text("ALTER TABLE members ADD COLUMN rank VARCHAR(80) NOT NULL DEFAULT ''"))
        db.session.commit()

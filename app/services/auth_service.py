from app.infrastructure.database import db
from app.infrastructure.models import UserModel
from app.repositories.repositories import UserRepository


class AuthService:
    def __init__(self): self.users = UserRepository()

    def authenticate(self, username, password):
        user = self.users.by_username(username)
        return user if user and user.check_password(password) else None

    def list_users(self): return self.users.all()
    def get_user(self, user_id): return self.users.get(user_id)

    def create_user(self, username, password, role):
        username = (username or "").strip()
        self._validate_username(username); self._validate_password(password, required=True); self._validate_role(role)
        if self.users.by_username(username): raise ValueError("Υπάρχει ήδη χρήστης με αυτό το username.")
        user = UserModel(username=username, role=role); user.set_password(password)
        return self.users.add(user)

    def update_own_credentials(self, user_id, username, password=None):
        user = self.users.get(user_id)
        if not user: raise LookupError("Ο χρήστης δεν βρέθηκε.")
        username = (username or "").strip()
        self._validate_username(username); self._validate_password(password, required=False)
        existing = self.users.by_username(username)
        if existing and existing.id != user.id: raise ValueError("Υπάρχει ήδη χρήστης με αυτό το username.")
        user.username = username
        if password: user.set_password(password)
        db.session.commit()
        return user

    def update_user_role(self, user_id, role):
        user = self.users.get(user_id)
        if not user: raise LookupError("Ο χρήστης δεν βρέθηκε.")
        self._validate_role(role); user.role = role; db.session.commit()
        return user

    def delete_user(self, user_id, current_user_id):
        if user_id == current_user_id: raise ValueError("Δεν μπορείτε να διαγράψετε τον λογαριασμό με τον οποίο είστε συνδεδεμένοι.")
        user = self.users.get(user_id)
        if not user: raise LookupError("Ο χρήστης δεν βρέθηκε.")
        self.users.delete(user)

    @staticmethod
    def _validate_username(username):
        if len(username) < 3: raise ValueError("Το username πρέπει να έχει τουλάχιστον 3 χαρακτήρες.")

    @staticmethod
    def _validate_password(password, required):
        if required and not password: raise ValueError("Ο κωδικός είναι υποχρεωτικός.")
        if password and len(password) < 8: raise ValueError("Ο κωδικός πρέπει να έχει τουλάχιστον 8 χαρακτήρες.")

    @staticmethod
    def _validate_role(role):
        if role not in {"admin", "viewer"}: raise ValueError("Μη έγκυρος ρόλος χρήστη.")

    def ensure_default_admin(self):
        default_username = "Ύπαρχος"
        if self.users.by_username(default_username): return
        legacy = self.users.by_username("admin")
        if legacy and legacy.role == "admin": legacy.username = default_username; db.session.commit(); return
        if not legacy:
            user = UserModel(username=default_username, role="admin"); user.set_password("Admin123!"); self.users.add(user)

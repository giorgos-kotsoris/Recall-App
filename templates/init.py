import os
from flask import Flask
from flask_login import LoginManager
from app.infrastructure.database import db
from app.infrastructure.models import UserModel, migrate_schema

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Παρακαλώ συνδεθείτε για να συνεχίσετε.'
login_manager.login_message_category = 'warning'

@login_manager.user_loader
def load_user(user_id : str) :
    return db.session.get(UserModel, int(user_id))

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', "change this in production"),
        SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL", "sqlite:///organisation.db"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config :
        app.config.update(test_config)

    db.init_app(app)
    login_manager.init_app(app)

    from app.controllers.auth_controller import auth_bp
    from app.controllers.auth_controller import groups_bp
    from app.controllers.auth_controller import members_bp
    from app.controllers.auth_controller import users_bp


    app.register_blueprint(auth_bp)
    app.register_blueprint(groups_bp)
    app.register_blueprint(members_bp)
    app.register_blueprint(users_bp)

    os.makedirs(app.instance_path, exist_ok=True)
    with app.app_context():
        db.create_all()
        migrate_schema()
        from app.services.auth_service import AuthService
        AuthService().ensure_default_admin()

    return app
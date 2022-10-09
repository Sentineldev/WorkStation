from flask_login import LoginManager

from models.models import User


login_manager : LoginManager = LoginManager()
login_manager.login_view = 'auth.login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(user_id=user_id).first()


def init_app(app):
    login_manager.init_app(app)



from flask_login import LoginManager
from . import app
from app import db, models

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'login'
# login_manager.login_message_catagory = 'danger'

@login_manager.user_loader
def load_user(id):
    return db.session.query(models.User).get(int(id))

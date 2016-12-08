from flask_login import LoginManager

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'login_get'
login_manager.login_message_catagory = 'danger'

@login_manager.USE_RELOADER
def load_user(id):
    return session.query(User).get(int(id))

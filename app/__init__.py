from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from raven.contrib.flask import Sentry

app = Flask(__name__)
app.config.from_object('config')
# sentry = Sentry(app, dsn='https://3a56234693434a388ae78c5a1b7fd1b0:51dc66e4314148869728f59e08070a67@sentry.io/134096')


db = SQLAlchemy(app)
from app import views, models, login

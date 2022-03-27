from flask import Flask
from config import Configuration
from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from dashapp.seo_dashboard_app import create_dashboard

PROJECTS = [
    'megaposm',
    'frutoss',
    'mentalshop',
    'da-vita',
    'guinot',
    'big-bears',
    'flexfit',
    'certex',
    'inauto',
    'skurala',
    'elitewheels',
    'elitewheels-msk',
    'kolesa-v-pitere',
    'the-koleso',
    'kypishiny',
]
    
app = Flask(__name__, static_folder='assets')
app.config.from_object(Configuration)

db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

### ADMIN ###
from models import *

admin = Admin(app)
admin.add_view(ModelView(Project, db.session))
admin.add_view(ModelView(Service, db.session))
admin.add_view(ModelView(Note, db.session))

dashboards = {}


with app.app_context():
    for project in PROJECTS:
        dashboard = create_dashboard(app, project)
        dashboards[project] = dashboard





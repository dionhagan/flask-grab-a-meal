import os
from app import create_app, db
from app.models import User, Meal
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

app = create_app('default')
manager = Manager(app)
# migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, User=User, Meal=Meal)
    
manager.add_command('shell', Shell(make_context=make_shell_context))
# manager.add_command('db', MigrateCommand)

from database import db_manager
manager.add_command('db', db_manager)

if __name__ == "__main__":
    manager.run()

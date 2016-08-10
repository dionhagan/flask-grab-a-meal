import os
from app import create_app, db
from app.models import User, Meal
from flask.ext.script import Manager, Shell

app = create_app('default')
manager = Manager(app)

def make_shell_context():
    return dict(app=app, db=db, User=User, Meal=Meal)

@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('test', test())

from database import db_manager
manager.add_command('db', db_manager)

if __name__ == "__main__":
    manager.run()

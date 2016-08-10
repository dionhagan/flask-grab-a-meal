#!flask/bin/python
from flask.ext.script import Command, Manager
from migrate.versioning import api
from config import config
from app import db
import os.path
import imp

db_manager = Manager(usage="Perform database operations")
from manage import app

# get config values
database_uri = app.config['SQLALCHEMY_DATABASE_URI']
migrate_repo = app.config['SQLALCHEMY_MIGRATE_REPO']

@db_manager.command
def create():
    db.create_all()
    if not os.path.exists(migrate_repo):
        api.create(migrate_repo, 'db repository')
        api.version_control(database_uri, migrate_repo)
    else:
        api.version_control(database_uri, migrate_repo, api.version(migrate_repo))

@db_manager.command    
def downgrade():
    v = api.db_version(database_uri, migrate_repo)
    api.downgrade(database_uri, migrate_repo, v - 1)
    v = api.db_version(database_uri, migrate_repo)
    print('Current database version: ' + str(v))

@db_manager.command
def migrate():
    v = api.db_version(database_uri, migrate_repo)
    migration = migrate_repo + ('/versions/%03d_migration.py' % (v+1))
    tmp_module = imp.new_module('old_model')
    old_model = api.create_model(database_uri, migrate_repo)
    exec(old_model, tmp_module.__dict__)
    script = api.make_update_script_for_model(database_uri, migrate_repo, tmp_module.meta, db.metadata)
    open(migration, "wt").write(script)
    api.upgrade(database_uri, migrate_repo)
    v = api.db_version(database_uri, migrate_repo)
    print('New migration saved as ' + migration)
    print('Current database version: ' + str(v))

@db_manager.command
def upgrade():
    api.upgrade(database_uri, migrate_repo)
    v = api.db_version(database_uri, migrate_repo)
    print('Current database version: ' + str(v))

from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
meal = Table('meal', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('house', String(length=64)),
    Column('timestamp', DateTime),
    Column('meal_time', DateTime),
    Column('time', String(length=12)),
    Column('date', String(length=16)),
    Column('user_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['meal'].columns['date'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['meal'].columns['date'].drop()

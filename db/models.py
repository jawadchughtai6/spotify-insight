import datetime
from peewee import *

db = PostgresqlDatabase('computeinsight',
                        user='postgres',
                        password='postgres',
                        host='localhost',
                        port=5432)


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    username = CharField(unique=True)
    client_id = CharField()
    client_secret = CharField()

    class Meta:
        database = db


class Recommendation(BaseModel):
    user = ForeignKeyField(User, backref='recommendations')
    track_id = CharField()
    track_title = CharField()
    track_link = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)
    is_published = BooleanField(default=True)

    class Meta:
        database = db



__author__ = 'ikurakin'

from peewee import *

db = SqliteDatabase('pop3.sqlite', threadlocals=True)

class BaseModel(Model):
    class Meta:
        database = db

class Users(BaseModel):

    name = CharField(unique=True, index=True, max_length=100)
    passw = CharField()

class Emails(BaseModel):

    subject = CharField()
    body = TextField()
    user = ForeignKeyField(Users, related_name='emails')
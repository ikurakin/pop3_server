__author__ = 'ikurakin'

from peewee import *

db = SqliteDatabase('pop3.db')

class BaseModel(Model):
    class Meta:
        database = db

class Users(BaseModel):
    # id =  PrimaryKeyField()
    name = CharField(max_length=100, index=True, unique=True)
    passw = CharField()

class Emails(BaseModel):
    # id = PrimaryKeyField()
    subject = CharField()
    body = TextField()
    user = ForeignKeyField(Users, related_name='emails')
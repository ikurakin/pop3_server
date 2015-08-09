__author__ = 'ikurakin'

import hashlib

import model


class DBQueries():

    def __init__(self):
        self.db = model.db
        self.db.connect()
        self.init_table_data()

    # init_table_data creates tables, if they do not exist and fills them with test data
    def init_table_data(self):
        if not model.Users.table_exists():
            self.create_user_table()
            self.fill_users()
        if not model.Emails.table_exists():
            self.create_emails_table()
            self.fill_emails()

    def create_user_table(self):
        self.db.create_table(model.Users)

    def create_emails_table(self):
        self.db.create_table(model.Emails)

    # fill_users fills user table with test data
    def fill_users(self):
        with self.db.transaction():
            usr_pssw = [
                {"name": "Khil", "passw": self.passw_hash("Trololo")},
                {"name": "Pablo", "passw": self.passw_hash("Pikasso")}
            ]
            for u in usr_pssw:
                model.Users.create(**u)

    # fill_emails fills emails table with test data
    def fill_emails(self):
        with self.db.transaction():
            emails = [
                {"subject": "Khil's email", "user": 1,
                 "body": "I'm riding the prairie on my stallion, so-and-so mustang, and my beloved Mary is thousand miles away knitting a stocking for me"},
                {"subject": "Pablo's email", "body": ";ksjhdflvkahbdcjsdhbfcsjkdavkjsdhvcakjs", "user": 2}
            ]
            for e in emails:
                model.Emails.create(**e)

    # user_exists checks if 
    def user_exists(self, user_name):
        try:
            user = model.Users.get(model.Users.name == user_name)
            if user.name:
                return True
        except:
            return False

    def authenticate_user(self, user_name, passw):
        try:
            user = model.Users.get(model.Users.name == user_name, model.Users.passw == self.passw_hash(passw))
            if user.name:
                return True
        except:
            return False

    def passw_hash(self, passw):
        return hashlib.sha224(passw).hexdigest()

    def get_user_emails(self, user):
        emails = model.Emails.select().join(model.Users).where(model.Users.name == user)
        return ["{id} {subject}".format(id=e.id, subject=e.subject) for e in emails]

    def get_email(self, id):
        try:
            email = model.Emails.get(model.Emails.id == id)
            return email.subject, email.body
        except:
            return None, None
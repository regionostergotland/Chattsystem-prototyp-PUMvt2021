"""
This file is the creation of a database for group 2 in the course TDDD96.
The database is used to save information needed
when healthcare workers communicate with patients through at chatt.
"""
from server import app
import os
from flask_sqlalchemy import SQLAlchemy

# Defalt removed warnings
if 'NAMESPACE' in os.environ and os.environ['NAMESPACE'] == 'heroku':
    db_uri = os.environ['DATABASE_URL']
else: # when running locally with sqlite
    db_path = os.path.join(os.path.dirname(__file__), 'app.db')
    db_uri = 'sqlite:///{}'.format(db_path)

app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db is the database where all information is stored.
db = SQLAlchemy(app)


class Keyword(db.Model):
    """
    The database class that saves keywords.
    It contains object keyword of type String.
    It contains a getter that returns String objects.
    """

    __tablename__ = 'Keyword'
    keyword = db.Column(db.String(), primary_key=True)

    def __init__(self, keyword_in):
        self.keyword = keyword_in

    def get_Keyword(self):
        return self.keyword


class Questions(db.Model):
    """
    The database class that saves user questions and bot answers.
    The class contains getters and setters.
    """

    __tablename__ = 'Questions'
    question = db.Column(db.String(), primary_key=True)
    answer = db.Column(db.String(), nullable=False, unique=False)

    def __init__(self, question_in, answer_in):
        self.question = question_in
        self.answer = answer_in

    def get_queston(self):
        return self.question

    def get_answer(self):
        return self.answer

    def set_answer(self, new_answer):
        self.answer = new_answer


class Bot_Phrases(db.Model):
    """
    The database class that saves bot phrases.
    Contains string objects "situation" and "answer".
    Contains getters and setters for both objects.
    """

    __tablename__ = 'Bot Phrases'
    situation = db.Column(db.String(), primary_key=True)
    answer = db.Column(db.String(), nullable=False, unique=False)

    def __init__(self, situation_in, answer_in):
        self.situation = situation_in
        self.answer = answer_in

    def get_situation(self):
        return self.situation

    def get_answer(self):
        return self.answer

    def set_answer(self, new_answer):
        self.answer = new_answer


class User(db.Model):
    """
    The database class that saves Users.
    Contains string objects "name" and intger "role".
    Contains getters and setters for both objects.
    """

    __tablename__ = 'User'
    name = db.Column(db.String(), primary_key=True)
    role = db.Column(db.Integer, nullable=True, unique=False)

    def __init__(self, name_in, role_in):
        self.name = name_in
        self.role = role_in

    def get_role(self):
        return self.role

    def get_name(self):
        return self.name

    def set_role(self, new_role):
        self.role = new_role


class Message(db.Model):
    """
    A database class that contains the messages of a chatt.
    The class contains the message string, a position index and the user.
    The aspect branch_id is a ForeignKey of it's branch.
    Contains getters for the aspects.
    """

    __tablename__ = 'Message'
    # primary_keys skapar sig själva
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(), nullable=False, unique=False)
    index = db.Column(db.Integer, nullable=False, unique=False)
    user = db.Column(db.String(), db.ForeignKey('User.name'), nullable=False)
    branch_id = db.Column(db.Integer,
                          db.ForeignKey('Branch.id'), nullable=False)

    def __init__(self, index, message, user, branch):
        self.index = index
        self.message = message
        self.user = user
        self.branch_id = branch

    def get_message(self):
        return self.message

    def get_index(self):
        return self.index

    def get_user(self):
        return self.user


branch_user = db.Table('branch_user',
    db.Column('id', db.Integer, db.ForeignKey('Branch.id'), primary_key=True),
    db.Column('name', db.String(), db.ForeignKey('User.name'), primary_key=True)
)


class Branch(db.Model):
    """
    The database class that saves branches in conversations.
    The class contains Integer object "id",
    which is an unique key for the branch.
    It contains the object "user",
    this is a relationship between branch and user.
    It conatins the String object "summary"
    which is a summary of the conversation that occured in the branch.
    It contains the String object "writer"
    which is the name of the auther that wrote the summary.
    The class contains getters and setters for its objects.
    """

    __tablename__ = 'Branch'
    # primary_keys skapar sig själva
    id = db.Column(db.Integer, primary_key=True)
    chatt = db.Column(db.Integer, db.ForeignKey('Chatt.id'), nullable=False)
    summary = db.Column(db.String(), nullable=True, unique=False)
    writer = db.Column(db.String(), nullable=True, unique=False)
    active = db.Column(db.Boolean, nullable=False, default=True, unique=False)

    users = db.relationship('User', secondary=branch_user, lazy='subquery',
        backref=db.backref('Branch', lazy=True))
    message = db.relationship('Message', backref='Branch', lazy=True)

    def __init__(self, chatt):
        self.chatt = chatt

    def get_summary(self):
        return self.summary

    def get_writer(self):
        return self.writer

    def set_summary(self, new_summary, user_in):
        self.summary = new_summary
        self.writer = user_in

    def set_writer(self, new_writer):
        self.writer = new_writer

    def set_active(self, active_status):
        self.active = active_status

    def get_active(self):
        return self.active


class Chatt(db.Model):
    """
    The database class User is the user chatt session.
    The session contains an user and one or more branches.
    Contains getter for the user id.
    """

    __tablename__ = 'Chatt'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(), db.ForeignKey('User.name'),
                        nullable=False, unique=True)
    # lazy är hur databasen hämtar data
    branch = db.relationship('Branch', backref='Chatt', lazy=True)

    def __init__(self, user_in):
        self.user_id = user_in

    def get_patient_id(self):
        return self.user_id

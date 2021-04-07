"""
This file is the creation of a database for group 2 in the course TDDD96.
The database is used to save information needed when healthcare workers communicate
with patients through at chatt.
"""
from flask import json
from server import app
from flask_sqlalchemy import SQLAlchemy

# Defalt removed warnings
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#db is the database where all information is stored.
db = SQLAlchemy(app)

"""
The database class that saves keywords.
It contains object keyword of type String.
It contains a getter that returns String objects.
"""
class Keyword(db.Model):
    __tablename__ = 'Keyword'
    keyword = db.Column(db.String(), primary_key=True)

    def __init__(self, keyword_in):
        self.keyword = keyword_in

    def get_Keyword(self):
        return self.keyword

"""
The database class that saves user questions and bot answers.
The class contains getters and setters.
"""
class Questions(db.Model):
    __tablename__ = 'Questions'
    question = db.Column(db.String(), primary_key=True)
    answer = db.Column(db.String(), nullable=False, unique=False)

    def get_queston(self):
        return self.question

    def get_answer(self):
        return self.answer

    def set_answer(self, new_answer):
        self.answer = new_answer

"""
The database class that saves bot phrases.
Contains string objects "situation" and "answer".
Contains getters and setters for both objects.
"""
class Bot_Phrases(db.Model):
    __tablename__ = 'Bot Phrases'
    situation = db.Column(db.String(), primary_key=True)
    answer = db.Column(db.String(), nullable=False, unique=False)

    def get_situation(self):
        return self.situation

    def get_answer(self):
        return self.answer

    def set_answer(self, new_answer):
        self.answer = new_answer

"""
A database class that contains the messages of a chatt.
The class contains the message string, a position index and the user.
The aspect branch_id is a ForeignKey of it's branch.
Contains getters for the aspects.
"""
class Message(db.Model):
    __tablename__ = 'Message'
    id = db.Column(db.Integer, primary_key = True) #primary_keys skapar sig själva
    message = db.Column(db.String(), nullable = False, unique=False)
    index =  db.Column(db.Integer, nullable = False, unique=False)
    user = db.Column(db.String(), nullable = False, unique=False)
    branch_id = db.Column(db.Integer, db.ForeignKey('Branch.id'), nullable = False)

    def __init__(self,index, message, user):
        self.index = index
        self.message = message
        self.user = user

    def get_message(self):
        return self.message

    def get_index(self):
        return self.index

    def get_user(self):
        return self.user
"""
The database class that saves branches in conversations.
The class contains Integer object "id", which is an unique key for the branch.
It contains the object "user", this is a relationship between branch and user.
It conatins the String object "summary" which is a summary of the conversation
that occured in the branch.
It contains the String object "writer" which is the name of the auther that wrote
the summary.
The class contains getters and setters for its objects.
"""
class Branch(db.Model):
    __tablename__ = 'Branch'
    id = db.Column(db.Integer, primary_key = True) #primary_keys skapar sig själva
    user = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable = False)
    summary =  db.Column(db.String(), nullable = True, unique=False)
    writer = db.Column(db.String(), nullable = True, unique=False)

    Message = db.relationship('Message', backref = 'Branch', lazy = True)

    def __init__(self, user):
        self.user = user

    def get_summary(self):
        return self.summary

    def get_writer(self):
        return self.writer

    def set_summary(self, new_summary):
        self.summary = new_summary

    def set_writer(self, new_writer):
        self.writer = new_writer

"""
The database class User is the user chatt session.
The session contains an user and one or more branches.
Contains getter for the user id.
"""
class User(db.Model):
    __tablename__ = 'User'
    user_id = db.Column(db.Integer, primary_key = True)
    branch = db.relationship('Branch', backref = 'User', lazy = True) #lazy är hur databasen hämtar data

    def get_id(self):
        return self.user_id


#--------------------------Sepret Functions-----------------------------------

"""
The init function for the database.
The function deconstructs and then constructs the database.
"""
def init():
    db.drop_all()
    db.create_all()

"""
This function adds a new keyword to the database.
"""
def add_keyword(keyword_in):
    new_keyword = Keyword(keyword_in)
    db.session.add(new_keyword)
    db.session.commit()

"""
This function return true if the keyword is in the database, False if not.
"""
# TODO: Add the posibility to look at a list of words
def is_keyword(keyword_in):
    return Keyword.query.filter_by(keyword=keyword_in).first() is not None
    # db.session.query(User.id).filter_by(name='davidism').first() is not None

"""
This function deletes the keyword form the database.
"""
def delete_keyword(keyword_in):
    keyword_objekt = Keyword.query.filter_by(keyword=keyword_in).first()
    db.session.delete(keyword_objekt)
    db.session.commit()

"""
This function adds a user question and the bot answer to the database.
"""
def add_question(question, answer):
    new_question = Questions(question, answer)
    db.session.add(new_question)
    db.session.commit()

"""
This function gets the bot answer to a user question from the database.
Returns the answer if it exist, False if not.
"""
def get_question_answer(question_in):
    question_objekt = Questions.query.filter_by(question=question_in).first()
    if question_objekt is not None:
        return question_objekt.get_answer()
    else:
        return False

"""
This function changes the bot answer to a user question in the database.
Returns True if the change was sucsesfull, False if not.
"""
def set_question_answer(question_in, answer_in):
    question_objekt = Questions.query.filter_by(question=question_in).first()
    if question_objekt is None:
        return False
    else:
        question_objekt.set_answer(answer_in)
        return True

"""
This function removes a user question and the bot answer from the database.
"""
def delete_question(question_in):
    question_objekt = Questions.query.filter_by(question=question_in).first()
    db.session.delete(question_objekt)
    db.session.commit()

"""
This function adds a bot phrase for a situation to the database.
"""
def add_phrase(situation, answer):
    new_phrase = Bot_Phrases(situation, answer)
    db.session.add(new_phrase)
    db.session.commit()

"""
This function gets the answer for a phrase from the database.
Returns the phrase if it exits, False if not.
"""
def get_phrase_answer(situation_in):
    phrase_objekt = Bot_Phrases.query.filter_by(situation=situation_in).first()
    if phrase_objekt is not None:
        return phrase_objekt.get_answer()
    else:
        return False

"""
This function changes a current answer to a bot phrase.
The input should be a situation and an answer to the situation.
The function returns true or false depending on if the situation exists in the database.
"""
def set_phrase_answer(situation_in, answer_in):
    phrase_objekt = Bot_Phrases.query.filter_by(situation=situation_in).first()
    if phrase_objekt is None:
        return False
    else:
        phrase_objekt.set_answer(answer_in)
        return True

"""
This function deletes phrases that are saved to the database.
The phrases belong to class Bot_phrases.
"""
def delete_phrase(situation_in):
    phrase_objekt = Bot_Phrases.query.filter_by(situation=situation_in).first()
    db.session.delete(phrase_objekt)
    db.session.commit()


"""
This function creates a new chatt and adds the chatt to the database,
The chatt will belong to class User.
"""
def init_chatt(user):
    new_chatt = User(user)
    db.session.add(new_chatt)
    db.session.commit()

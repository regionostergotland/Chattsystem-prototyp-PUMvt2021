"""
This file is the creation of a database for group 2 in the course TDDD96.
The database is used to save information needed
when healthcare workers communicate with patients through at chatt.
"""
from flask import json
from server import app
from flask_sqlalchemy import SQLAlchemy

# Defalt removed warnings
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"
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
    role = db.Column(db.Integer, nullable=False, unique=False)

    def __init__(self, name_in, role_in):
        self.name = name_in
        self.role = role_in

    def get_role(self):
        return self.role

    def get_role(self):
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

    def __init__(self, index, message, user):
        self.index = index
        self.message = message
        self.user = user

    def get_message(self):
        return self.message

    def get_index(self):
        return self.index

    def get_user(self):
        return self.user


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

    Message = db.relationship('Message', backref='Branch', lazy=True)

    def __init__(self, chatt):
        self.chatt = chatt

    def get_summary(self):
        return self.summary

    def get_writer(self):
        return self.writer

    def set_summary(self, new_summary):
        self.summary = new_summary

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


# --------------------------Sepret Functions-----------------------------------


def init():
    """
    The init function for the database.
    The function deconstructs and then constructs the database.
    """

    db.drop_all()
    db.create_all()


def add_keyword(keyword_in):
    """
    This function adds a new keyword to the database.
    """

    if not is_keyword(keyword_in):
        new_keyword = Keyword(keyword_in)
        db.session.add(new_keyword)
        db.session.commit()
        return True
    else:
        return False


# TODO: Add the posibility to look at a list of words
def is_keyword(keyword_in):
    """
    This function return true if the keyword is in the database, False if not.
    """

    return Keyword.query.filter_by(keyword=keyword_in).first() is not None
    # db.session.query(User.id).filter_by(name='davidism').first() is not None


def delete_keyword(keyword_in):
    """
    This function deletes the keyword form the database.
    """

    keyword_objekt = Keyword.query.filter_by(keyword=keyword_in).first()
    if keyword_objekt is not None:
        db.session.delete(keyword_objekt)
        db.session.commit()
        return True
    else:
        return False


def add_question(question_in, answer):
    """
    This function adds a user question and the bot answer to the database.
    """

    question_exists = Questions.query.filter_by(question=question_in).first()
    if question_exists is None:
        new_question = Questions(question_in, answer)
        db.session.add(new_question)
        db.session.commit()
        return True
    else:
        return False


def get_question_answer(question_in):
    """
    This function gets the bot answer to a user question from the database.
    Returns the answer if it exist, False if not.
    """

    question_objekt = Questions.query.filter_by(question=question_in).first()
    if question_objekt is not None:
        return question_objekt.get_answer()
    else:
        return False


def set_question_answer(question_in, answer_in):
    """
    This function changes the bot answer to a user question in the database.
    Returns True if the change was sucsesfull, False if not.
    """

    question_objekt = Questions.query.filter_by(question=question_in).first()
    if question_objekt is None:
        return False
    else:
        question_objekt.set_answer(answer_in)
        return True


def delete_question(question_in):
    """
    This function removes a user question and the bot answer from the database.
    """

    question_objekt = Questions.query.filter_by(question=question_in).first()
    if question_objekt is not None:
        db.session.delete(question_objekt)
        db.session.commit()
        return True
    else:
        return False


def add_phrase(situation_in, answer):
    """
    This function adds a bot phrase for a situation to the database.
    """

    phrase_exists = Bot_Phrases.query.filter_by(situation=situation_in).first()
    if phrase_exists is None:
        new_phrase = Bot_Phrases(situation_in, answer)
        db.session.add(new_phrase)
        db.session.commit()
        return True
    else:
        return False


def get_phrase_answer(situation_in):
    """
    This function gets the answer for a phrase from the database.
    Returns the phrase if it exits, False if not.
    """

    phrase_objekt = Bot_Phrases.query.filter_by(situation=situation_in).first()
    if phrase_objekt is not None:
        return phrase_objekt.get_answer()
    else:
        return False


def set_phrase_answer(situation_in, answer_in):
    """
    This function changes a current answer to a bot phrase.
    The input should be a situation and an answer to the situation.
    The function returns true or false
    depending on if the situation exists in the database.
    """

    phrase_objekt = Bot_Phrases.query.filter_by(situation=situation_in).first()
    if phrase_objekt is None:
        return False
    else:
        phrase_objekt.set_answer(answer_in)
        return True


def delete_phrase(situation_in):
    """
    This function deletes phrases that are saved to the database.
    The phrases belong to class Bot_phrases.
    """

    phrase_objekt = Bot_Phrases.query.filter_by(situation=situation_in).first()
    if phrase_objekt is not None:
        db.session.delete(phrase_objekt)
        db.session.commit()
        return True
    else:
        return False


def init_chatt(user):
    """
    This function creates a new chatt and adds the chatt to the database,
    The chatt will belong to class User.
    """

    if Chatt.query.filter_by(user_id=user).first() is None:
        new_chatt = Chatt(user)
        new_branch = Branch(user)  # Create a new branch when creating new user
        db.session.add(new_chatt)
        db.session.add(new_branch)
        new_chatt.branch.append(new_branch)
        db.session.commit()
        return True
    else:
        return False


def add_brach(user):
    user_object = Chatt.query.filter_by(user_id=user).first()
    if user_object is not None:
        new_branch = Branch(user)
        db.session.add(new_branch)
        user_object.branch.append(new_branch)
        db.session.commit()
        return True
    else:
        return False


def add_brach_summary(branch_id, summary_in, user_in):
    branch_object = Branch.query.filter_by(id=branch_id).first()
    if branch_object is not None:
        branch_object.set_summary(summary_in, user_in)
        return True
    else:
        return False


def add_user(name_in, role_in=None):
    user_object = User.query.filter_by(name=name_in).first()
    if user_object is None:
        new_user = User(name_in, role_in)
        db.session.add(new_user)
        db.session.commit()
        return True
    else:
        return False


def set_user_role(name_in, role_in):
    user_object = User.query.filter_by(name=name_in).first()
    if user_object is not None:
        user_object.set_role(role_in)
        return True
    else:
        return False


def delete_user(user_id):
    user_object = User.query.filter_by(name=user_id).first()
    if user_object is not None:
        db.session.delete(user_object)
        db.session.commit()
        return True
    else:
        return False

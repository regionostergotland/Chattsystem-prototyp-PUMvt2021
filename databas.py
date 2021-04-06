from flask import json
from server import app
from flask_sqlalcemy import SQLAlcemy

db = SQLAlcemy(app)

class Keyword(db.Model):
    __tablename__ = 'Keyword'
    keyword = db.Column(db.String(), primary_key=True)

    def get_Keyword(self):
        return self.keyword

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


class Message(db.Model):
    __tablename__ = 'Message'
    id = db.Column(db.Integer, primary_key = True) #primary_keys skapar sig själva
    message = db.Column(db.String(), nullable = False, unique=False)
    index =  db.Column(db.Integer, nullable = False, unique=False)
    user = db.Column(db.String(), nullable = False, unique=False)
    branchID = db.Column(db.Integer, db.ForeignKey('Branch.id'), nullable = False)

    def get_message(self):
        return self.message
    def get_index(self):
        return self.index
    def get_user(self):
        return self.user

class Branch(db.Model):
    __tablename__ = 'Branch'
    id = db.Column(db.Integer, primary_key = True) #primary_keys skapar sig själva
    user = db.Column(db.Integer, db.ForeignKey('User.id'), nullable = False)
    summary =  db.Column(db.String(), nullable = False, unique=False)
    writer = db.Column(db.String(), nullable = False, unique=False)

    Message = db.relationship('Message', backref = 'Branch', lazy = True)

    def get_summary(self):
        return self.summary
    def get_writer(self):
        return self.writer

    def set_summary(self, new_summary):
        self.summary = new_summary
    def set_writer(self, new_writer):
        self.writer = new_writer


class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key = True)
    branch = db.relationship('Branch', backref = 'User', lazy = True) #lazy är hur databasen hämtar data

    def get_id(self):
        return self.id

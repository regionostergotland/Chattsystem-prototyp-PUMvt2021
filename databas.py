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

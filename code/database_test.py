import pytest
import database as DB

# Create database
DB.init()


"""
Test adding and deleting keywords
"""
def test_keyword():
    DB.add_keyword("HEJ")
    assert DB.is_keyword("HEJ")

    DB.delete_keyword("HEJ")
    assert not DB.is_keyword("HEJ")


"""
Test adding and deleting the same keyword twice.
"""
def test_double_keyword():
    assert DB.add_keyword("HEJ")
    assert not DB.add_keyword("HEJ")
    assert DB.delete_keyword("HEJ")
    assert not DB.delete_keyword("HEJ")


"""
Test adding and deleting the same questions twice.
"""
def test_double_question():
    assert DB.add_question('question', 'answer')
    assert not DB.add_question('question', 'answer')
    assert DB.delete_question('question')
    assert not DB.delete_question('question')


"""
Test changing the answer to a non-existant question.
"""
def test_change_noquestion():
    assert not DB.set_question_answer('question', 'answer2')


"""
Test changing the answer to a non-existant phrase.
"""
def test_change_nophrase():
    assert not DB.set_phrase_answer('question', 'answer2')


"""
Test adding, changing and deleting the same question.
"""
def test_question():
    question = "Hej?"
    answer1 = "DÅ!"
    answer2 = "Hej!"
    assert DB.add_question(question, answer1)
    assert DB.get_question_answer(question) == answer1

    assert DB.set_question_answer(question, answer2)
    assert DB.get_question_answer(question) == answer2

    assert DB.delete_question(question)
    assert not DB.get_question_answer(question)


"""
Test adding, changing and deleting the same phrase.
"""
def test_phrases():
    situation = "Intro"
    answer1 = "Gå iväg"
    answer2 = "Hej! DU!"
    assert DB.add_phrase(situation, answer1)
    assert DB.get_phrase_answer(situation) == answer1

    assert DB.set_phrase_answer(situation, answer2)
    assert DB.get_phrase_answer(situation) == answer2

    assert DB.delete_phrase(situation)
    assert not DB.get_phrase_answer(situation)


"""
Test adding and deleting the same phrase twice.
"""
def test_double_phrases():
    assert DB.add_phrase('question', 'answer')
    assert not DB.add_phrase('question', 'answer')
    assert DB.delete_phrase('question')
    assert not DB.delete_phrase('question')


"""
Test for creating a new chatt, new branch and adding a
 new branch for a non existing person.
"""
def test_new_chatt():
    assert DB.init_chatt(5)
    assert DB.add_brach(5)
    assert not DB.add_brach(34)

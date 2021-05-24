"""
This is the connector between the modules
that direct messages to and from modules.
Name switchboard seems fitting for this task.
"""

import chatbot.bot as bott
import database_functions as DB


########################################################################
"""
Botfunctions, these functions sends information to and from the bot.
"""


def get_bot_message(message):
    """
    Function for sending a message from a patient to the bot that returns
    the response.
    """
    return bott.bot_main(message)


########################################################################
"""
Database functions, these functions sends information to and from the database
"""


def DB_init():
    """
    Calls the function in the database that initialize the database.
    """
    DB.init()


def DB_getQanswer(question):
    """
    Calls the function in the database that gets the question answer to the
    input question.
    """
    return DB.get_question_answer(question)


def DB_word_match(word):
    """
    Calls the function that get the matching questions from a word in the
    database.
    """
    return DB.get_matching_questions(word)


def DB_addQ(question, answer):
    """
    Calls the function that adds questions to the database in the database.
    """
    return DB.add_question(question, answer)

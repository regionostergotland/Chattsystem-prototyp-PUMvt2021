"""
This is the connector between the modules that direct messages to and from modules. 
Name switchboard seems fitting for this task. 
"""

import chatbot.bot as bott
import chatbot.database_lucy as DB


########################################################################
"""
Botfunctions, these functions sends information to and from the bot. 
"""
########################################################################

"""
Function for sending a message from a patient to the bot that returns the response. 
"""
def botcom(message):
    #something
    print(bott.main_ish(message))



########################################################################
"""
Database functions, these functions sends information to and from the database
"""
########################################################################

"""
something...
idea: take in two arguments: tag, data. tag is what function in the DB that is gonna be called, data is what 
should be put into the function. Data is a list since there could be 0, 1 or 2 arguments to the functions
in the DB.

maybe do a try and catch, so if the db is not initialized then catch that and init before continuing. 
"""
def DBsearch(tag, data):
    #something
    return

def DB_getQanswer(question):
    return DB.get_question_answer(question)

def DB_word_match(word):
    return DB.word_match_db(word)

def DB_addQ(question, answer):
    return DB.add_question(question, answer)




#print("Skriv något: ")
#botcom(input())
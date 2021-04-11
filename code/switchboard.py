"""
This is the connector between the modules that direct messages to and from modules. 
Name switchboard seems fitting for this task. 
"""

import chatbot.bot as bott
import chatbot.database_lucy as DB


########################################################################
"""
Botfunctions, these functions sends information to the bot. 
"""
def botcom(message):
    #something
    print(bott.main_ish(message))



########################################################################
"""
Database functions, these functions sends information to the database
"""
def searchBase(searchWord):
    #something
    return

print("Skriv något: ")
botcom(input())
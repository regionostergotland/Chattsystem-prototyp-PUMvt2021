#https://www.youtube.com/watch?v=9KZwRBg4-P0
"""
This file is the chatbot that can send simple responses to user input. 
The chatbot uses a database which contains a number of responses to different user inputs, this
includes questions, phrases and informative answers. 

The bot uses an algorithm that matches the user input against the database and tries to get the
most similar response possible from the given inputs in the database. 
"""
import random
import string
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy
import time
import warnings
warnings.filterwarnings('ignore')
#Download the punkt package
nltk.download('punkt', quiet =True)

import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
import switchboard as switchboard




def greeting_response(text):

    """
    This function returns a random greeting response to a users greeting.
    """
    #text = text.lower()

    #bots greeting response
    bot_greetings = ['hallå', 'hej', 'Hej där']
    #user greetings

    user_greetings = ['hej', 'hejsan', 'hallå']

    for word in text.split():
        if word in user_greetings:
            return random.choice(bot_greetings)




def index_sort(list_var):

    """
    This function sorts index based on a given lists element value.
    """
    length = len(list_var)
    list_index = list(range(0, length))
    
    x = list_var
    for i in range(length):
        for j in range(length):
            if x[list_index[i]] > x[list_index[j]]:
                #swap
                temp = list_index[i]
                list_index[i]= list_index[j]
                list_index[j]= temp

    return list_index




def bot_response(user_input, list_of_matches):
    """
    This function uses a cosine similarity algorithm to find the best
    matching answer to the users input then returns it. If no answer
    is found the bots excuses itself for not understanding.
    """
    
    #user_input = user_input.lower()
    list_of_matches.append(user_input)

    bot_response = ''
    cm = CountVectorizer().fit_transform(list_of_matches)

    similarity_scores = cosine_similarity(cm[-1], cm)

    similarity_scores_list = similarity_scores.flatten()
    index = index_sort(similarity_scores_list)
    index = index_sort(similarity_scores_list)


    index = index[1:]
    response_flag = 0
    j = 0

    for i in range(len(index)):
        if similarity_scores_list[index[i]] > 0.3:
            bot_response = bot_response +list_of_matches[index[i]]+','
        
           
            response_flag = 1
            j = j + 1
        if j > 2:
            break
    

    if not bot_response == "":
        bot_response = switchboard.DB_getQanswer(bot_response.split(',')[0])
    elif response_flag == 0 or bot_response == False:
        bot_response = "Ursäkta, jag förstår inte."

    return bot_response


def bot_answer(user_input):
    """
    This function checks if the user input exists
    in the database and returns an answer. If the
    user input does not exists, it searches for
    for something similar to the user input and returns an answer.
    """
    if switchboard.DB_getQanswer(user_input):
        return switchboard.DB_getQanswer(user_input)

    else:
        return search(user_input)

    
def search(input):
    """
    This function searched in the database for user inputs that match the current
    user input. It sends a list of matching responses from the database to the
    bot_response -function and returns the answer from that function. 
    """

    all_matches = []   
    for word in input.split():  
        
        #Checks if this word have a match in the database
        match = switchboard.DB_word_match(word) 
        if match != []:     
            for question in match:
                if not question in all_matches: 
                    #Only the questions are relevant and they are put in the list
                    all_matches = all_matches + [question] 
               
    #If there are matches then they are sent to the bot_response function. 
    if all_matches != []:   
        return bot_response(input, all_matches)

    else:
        return "sad"

#A list of exit phrases.        
exit_list = ['hej då', 'hejdå','farväl','adjö','exit','bye']

def bot_main(input):
    """
    This is the function that is used by switchboard.py to contact the bot. If there is an 
    exit message in the input, then the bot sends a exit message back. If there is a greeting 
    (for example 'hej') or another kind of message then it sends back a response from the 
    database. 
    """
    sign_list = ['?', ',', '.', '!', '(', ')', '"','-','_','*','+']
    input = input.lower()
    for char in input:
        if char in sign_list:
            input = input.replace(char, '')

    if input in exit_list:
        return (random.choice(exit_list))
    else:
        time.sleep(2)
        if greeting_response(input) != None:
            return(greeting_response(input))
        else:
            return(bot_answer(input))

if __name__ == '__main__':
    print('Bot: Mitt namn är botten Anna. Jag kommer att besvara dina frågor')
    while True:
        print(bot_main(input()))


"""
#start the chat
print('Bot: Mitt namn är botten Anna. Jag kommer att besvara dina frågor')
exit_list = ['hej då']

while(True):
    user_input = input()
    if user_input.lower() in exit_list:
        print('Bot: chat later bitch')
        break

    
    else:
        time.sleep(2)
        if greeting_response(user_input) != None:
            print('Bot: '+greeting_response(user_input))
        else:
            print("Bot: "+ bot_answer(user_input))
"""

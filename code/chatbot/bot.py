#https://www.youtube.com/watch?v=9KZwRBg4-P0

#description: This is a a smart chat bot program
#installera nltk (pip)
# installera newspaper3k (pip)
#installera sklearn


#import librariers
from newspaper import Article
import random
import string
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
#import warings
#warnings.filterwarnings('ignore')

#download the punkt package
#nltk.download('punkt',quiet=True)

#get the article
article = Article('https://www.1177.se/Ostergotland/sjukdomar--besvar/diabetes/diabetes-typ-1/')
article.download()
article.parse()
article.nlp()
corpus = article.text

#print the article text
#print(corpus)

#tokenization
text = corpus
sentence_list = nltk.sent_tokenize(text) # a list of sentences

#print list of sentences
#print(sentence_list)

#index sort
def index_sort(list_var):
    length = len(list_var)
    list_index = list(range(0, length))

    x = list_var
    for i in range(length):
        for j in range(length):
            if x[list_index[i]] > x[list_index[j]]:
                #swap
                temp = list_index[i]
                list_index[i] = list_index[j]
                list_index[j] = temp
    return list_index

# Function to return random greeting response to user greeting
def greeting_response(text):
    text = text.lower()

    #bot greeting response
    bot_greetings = ['Hej', 'Hejsan', 'Goddag', 'Hallå där!']

    #user greeting
    user_greeting = ['hej', 'goddag', 'hejsan']

    for word in text.split():
        if word in user_greeting:
            return random.choice(bot_greetings)

#create bot response
def bot_response(user_input):
    user_input = user_input.lower()
    sentence_list.append(user_input)
    bot_answer = ''
    cm = CountVectorizer().fit_transform(sentence_list) #count matrix
    similarity_scores = cosine_similarity(cm[-1], cm) #last sentence of user input
    similarity_scores_list = similarity_scores.flatten() 
    index = index_sort(similarity_scores_list) #highest to lowest value in similarity score
    index = index[1:]
    response_flag = 0

    j = 0
    #skulle kunna göra en ändring här att den måste få ett antal träffar
    #och att man då skickar tillbaka svaren med höst similarity score typ

    for i in range(len(index)):
        if similarity_scores_list[index[i]] > 0.0:
            bot_answer = bot_answer + ' ' + sentence_list[index[i]]
            response_flag = 1
            j = j + 1
        if j > 2:
            break;
    
    if response_flag == 0:
        bot_answer = bot_answer + ' ' + "Jag ursäktar men jag försår inte."
    
    sentence_list.remove(user_input)

    return bot_answer
"""
user_input = " hello world "
sentence_list.append(user_input)
bot_answer = ''
cm = CountVectorizer().fit_transform(sentence_list) #count matrix
similarity_scores = cosine_similarity(cm[-1], cm) #last sentence of user input
similarity_scores_list = similarity_scores.flatten() 
index = index_sort(similarity_scores_list) #highest to lowest value in similarity score
"""


#start the chat

print("Botten Anna: Jag är Anna och kan svara på frågor om Diabetes, om du vill gå ur så skriv 'Hejdå' ")

exit_list = ['exit', 'hejdå', 'adjö', 'farväl', 'dra åt helvete']

while True:
    user_input = input()
    if user_input.lower() in exit_list:
        print("Botten Anna: Vi hörs!")
        break
    else:
        if greeting_response(user_input) != None:
            print("Botten Anna: " + greeting_response(user_input))
        else:
            print("Botten Anna: "+bot_response(user_input))


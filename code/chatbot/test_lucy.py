#description: this is a smart chat bot program
import database_lucy as dbl
from newspaper import Article
import random
import string
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy
import warnings
warnings.filterwarnings('ignore')
#Download the punkt package
nltk.download('punkt', quiet =True)


#Get the article
article = Article('https://sv.wikipedia.org/wiki/Diabetes')
article.download()
article.parse()
article.nlp()
corpus = article.text

#print articles text
#print(corpus)

#Tokenization
text = corpus
sentence_list = nltk.sent_tokenize(text) #A list of sentences

#print the list of sentences
#print(sentence_list)


#A function to return a random greeting response to a usrs greeting
def greeting_response(text):
    text = text.lower()

    #bots greeting response
    bot_greetings = ['hallå', 'hej', 'Hej där']
    #user greetings
    user_greetings = ['hej', 'hejsan', 'hallå']

    for word in text.split():
        if word in user_greetings:
            return random.choice(bot_greetings)

def index_sort(list_var):
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




#Create the bots response
def bot_response(user_input, list_of_matches):
    user_input = user_input.lower()
    bot_response = ''
    cm = CountVectorizer().fit_transform(list_of_matches)
    similarity_scores = cosine_similarity(cm[-1], cm)
    similarity_scores_list = similarity_scores.flatten()
    index = index_sort(similarity_scores_list)
    index = index[1:]
    response_flag = 0
    j = 0
    similarity_scores_list.sort()
    for i in range(len(index)):
        if similarity_scores_list[index[i]] > 0.0:
            bot_response = bot_response+',' +list_of_matches[index[i]]
           
            response_flag = 1
            j = j + 1
        if j > 2:
            break

    
    bot_response = dbl.get_question_answer(bot_response.split(',')[-1])
    if response_flag == 0 or bot_response == False:
        bot_response = "Ursäkta, jag förstår inte."

    return bot_response


def bot_answer(user_input):
    prepare_db()
    if dbl.get_question_answer(user_input):
        return dbl.get_question_answer(user_input)

    else:
        return search(user_input)
        
 #Förbereder databasen för användning      
def prepare_db():
    dbl.add_question('vad är diabetes', 'dålig')
    dbl.add_question('hur är diabetes', 'inte bra')
    dbl.add_question('varför är diabetes farligt', 'kan dö')
    dbl.add_question('kan diabetes vara farligt', 'ja')
    dbl.add_question('vad betyder hola', 'det betyder hej')
    dbl.add_question('hus', 'kåk')


    
def search(input):
    all_matches = []    #Lista där alla matchningar läggs till
    for word in input.split():  #för varje ord i användarens fråga
        #print(word)
        match = dbl.word_match_db(word) #Tittar om ordet matchar frågor i databasen
        if match != []:     #om listan inte är tom har vi hittat minst en matchning
           
            for question in match:
                #print(word1.question)
                all_matches = all_matches + [question.question] #Vi tar ut enbart frågorna och inget annat skräp och lägger in i en lista
               
    
    if all_matches != []:   #Om listan inte är tom kan vi titta på vilken fråga i databasen som matchar användarens fråga
        return bot_response(input, all_matches)

    else:
        return "sad"
        #print(result)
        #return result[0].get_answer()





    #start the chat

print('Bot: Mitt namn är botten Anna. Jag kommer att besvara dina frågor')
exit_list = ['hej då']
dbl.add_question('vad är diabetes', 'dåligt')
dbl.add_question('vad betyder hola', 'det betyder hej')
while(True):
    user_input = input()
    if user_input.lower() in exit_list:
        print('Bot: chat later bitch')
        break
    else:
        if greeting_response(user_input) != None:
            print('Bot: '+greeting_response(user_input))
        else:
            print("Bot: "+ bot_answer(user_input))

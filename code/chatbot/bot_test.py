import bot as bot
import prepDB as prep

import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
import switchboard as switchboard

def test_greetings():
    prep
    bot_greetings = ['hallå', 'hej', 'Hej där']

    assert bot.bot_main('hej') in bot_greetings

def test_departure():
    prep 
    exit_list = ['hej då', 'hejdå','farväl','adjö','exit','bye']

    assert bot.bot_main('hej då') in exit_list
    assert bot.bot_main('adjö') in exit_list
    assert bot.bot_main('bye') in exit_list

def test_bot_answer():
    prep
    assert not bot.bot_main('vad är apk') == "Ursäkta, jag förstår inte."
    switchboard.DB_addQ('vad är apk', 'det är alkohol per krona')
    assert bot.bot_main('vad är apk') == 'det är alkohol per krona'
    assert bot.bot_main('vilken är apk') == 'det är alkohol per krona'
    
def test_bot_question():    
    prep
    assert bot.bot_main('jag har haft huvudvärk') == 'har det varat i två veckor?'
    assert bot.bot_main('jag har huvudvärk') == 'har det varat i två veckor?'



"""
if __name__ == '__main__':
    test_greetings()
    test_departure()
    test_bot_answer()
    print('Passed tests')
"""
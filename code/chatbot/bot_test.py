import switchboard as switchboard
import bot as bot
import prepDB as prep

import os
import sys
import inspect
current_dir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)


def test_greetings():
    """
    This function tests the bots respons to greetings.
    """
    prep.prepare_db()
    bot_greetings = ['hallå', 'hej', 'Hej där']

    assert bot.bot_main('hej') in bot_greetings
    assert bot.bot_main('hallå') in bot_greetings


def test_departure():
    """
    This function tests the bots respons to departures.
    """
    prep.prepare_db()
    exit_list = ['hej då', 'hejdå', 'farväl', 'adjö', 'exit', 'bye']

    assert bot.bot_main('hej då') in exit_list
    assert bot.bot_main('adjö') in exit_list
    assert bot.bot_main('bye') in exit_list


def test_bot_answer():
    """
    This function tests the bots respons to questions asked by the user.
    """
    prep.prepare_db()
    assert not bot.bot_main('vad är apk') == "Ursäkta, jag förstår inte."
    switchboard.DB_addQ('vad är apk', 'det är alkohol per krona')
    assert bot.bot_main('vad är apk') == 'det är alkohol per krona'
    assert bot.bot_main('vilken är apk') == 'det är alkohol per krona'


def test_bot_question():
    """
    This function tests the bots question to the user.
    """
    prep.prepare_db()
    assert bot.bot_main(
        'jag har haft huvudvärk') == 'Har det varat i två veckor?'
    assert bot.bot_main('jag har huvudvärk') == 'Har det varat i två veckor?'

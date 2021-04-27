import switchboard as sb
import chatbot.prepDB as DB

def test_switchboard_bot_greetings():
    """
    This function tests the bots respons to greetings.
    """
    DB.prepare_db()
    bot_greetings = ['hallå', 'hej', 'Hej där']

    assert sb.get_bot_message('hej') in bot_greetings
    assert sb.get_bot_message('hallå') in bot_greetings

"""
if __name__ == '__main__':
    test_switchboard_bot_greetings()
    print("ok!") 
"""

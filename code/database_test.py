import database as DB

# Create database
DB.init()


def test_keyword():
    """
    Test adding and deleting keywords
    """

    DB.add_keyword("HEJ")
    assert DB.is_keyword("HEJ")

    DB.delete_keyword("HEJ")
    assert not DB.is_keyword("HEJ")


def test_double_keyword():
    """
    Test adding and deleting the same keyword twice.
    """

    assert DB.add_keyword("HEJ")
    assert not DB.add_keyword("HEJ")
    assert DB.delete_keyword("HEJ")
    assert not DB.delete_keyword("HEJ")


def test_double_question():
    """
    Test adding and deleting the same questions twice.
    """

    assert DB.add_question('question', 'answer')
    assert not DB.add_question('question', 'answer')
    assert DB.delete_question('question')
    assert not DB.delete_question('question')


def test_change_noquestion():
    """
    Test changing the answer to a non-existant question.
    """

    assert not DB.set_question_answer('question', 'answer2')


def test_change_nophrase():
    """
    Test changing the answer to a non-existant phrase.
    """

    assert not DB.set_phrase_answer('question', 'answer2')


def test_question():
    """
    Test adding, changing and deleting the same question.
    """

    question = "Hej?"
    answer1 = "DÅ!"
    answer2 = "Hej!"
    assert DB.add_question(question, answer1)
    assert DB.get_question_answer(question) == answer1

    assert DB.set_question_answer(question, answer2)
    assert DB.get_question_answer(question) == answer2

    assert DB.delete_question(question)
    assert not DB.get_question_answer(question)


def test_phrases():
    """
    Test adding, changing and deleting the same phrase.
    """

    situation = "Intro"
    answer1 = "Gå iväg"
    answer2 = "Hej! DU!"
    assert DB.add_phrase(situation, answer1)
    assert DB.get_phrase_answer(situation) == answer1

    assert DB.set_phrase_answer(situation, answer2)
    assert DB.get_phrase_answer(situation) == answer2

    assert DB.delete_phrase(situation)
    assert not DB.get_phrase_answer(situation)


def test_double_phrases():
    """
    Test adding and deleting the same phrase twice.
    """

    assert DB.add_phrase('question', 'answer')
    assert not DB.add_phrase('question', 'answer')
    assert DB.delete_phrase('question')
    assert not DB.delete_phrase('question')


def test_new_chatt():
    """
    Test for creating a new chatt, new branch and adding a
    new branch for a non existing person.
    """

    assert DB.add_user("Ludwig")
    assert DB.init_chatt("Ludwig")
    assert DB.add_brach("Ludwig")
    #assert DB.

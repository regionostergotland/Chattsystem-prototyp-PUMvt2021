import database as DB


def test_keyword():
    """
    Test adding and deleting keywords
    """

    DB.init()
    DB.add_keyword("HEJ")
    assert DB.is_keyword("HEJ")

    DB.delete_keyword("HEJ")
    assert not DB.is_keyword("HEJ")


def test_double_keyword():
    """
    Test adding and deleting the same keyword twice.
    """

    DB.init()
    assert DB.add_keyword("HEJ")
    assert not DB.add_keyword("HEJ")
    assert DB.delete_keyword("HEJ")
    assert not DB.delete_keyword("HEJ")


def test_double_question():
    """
    Test adding and deleting the same questions twice.
    """

    DB.init()
    assert DB.add_question('question', 'answer')
    assert not DB.add_question('question', 'answer')
    assert DB.delete_question('question')
    assert not DB.delete_question('question')


def test_change_noquestion():
    """
    Test changing the answer to a non-existant question.
    """

    DB.init()
    assert not DB.set_question_answer('question', 'answer2')


def test_change_nophrase():
    """
    Test changing the answer to a non-existant phrase.
    """

    DB.init()
    assert not DB.set_phrase_answer('question', 'answer2')


def test_question():
    """
    Test adding, changing and deleting the same question.
    """

    DB.init()
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
    DB.init()

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
    DB.init()

    assert DB.add_phrase('question', 'answer')
    assert not DB.add_phrase('question', 'answer')
    assert DB.delete_phrase('question')
    assert not DB.delete_phrase('question')


def test_new_chatt():
    """
    """
    DB.init()
    assert DB.add_user("Ludwig")
    assert not DB.add_user("Ludwig")
    assert DB.add_user("Kevin", 2)
    Branch_id = DB.init_chatt("Ludwig")
    assert Branch_id is not None
    assert DB.set_user_role("Ludwig", 1)
    assert DB.delete_user("Ludwig")


def test_new_branch():

    DB.init()
    assert DB.add_user("Ludwig")
    assert DB.add_user("Kevin")
    DB.init_chatt("Ludwig")
    Branch_id = DB.add_brach("Ludwig")
    assert Branch_id is not None
    assert DB.new_message("HEJ", "Ludwig", Branch_id, 0)
    assert DB.add_user_to_brach("Kevin",Branch_id)
    assert DB.new_message("Nej!", "Kevin", Branch_id, 1)
    assert DB.add_brach_summary(Branch_id, "Noob", "Kevin")


def test_user():

    DB.init()
    assert DB.add_user("Kevin")
    assert not DB.add_user("Kevin")
    assert DB.delete_user("Kevin")
    assert not DB.delete_user("Kevin")

    assert DB.add_user("Felicia",2)
    assert DB.set_user_role("Felicia", 0)
    assert not DB.set_user_role("Kevin",7)


def test_brach_errors():

    DB.init()
    assert DB.add_user("Ludwig")
    branch_id = DB.init_chatt("Ludwig")
    assert not DB.init_chatt("Ludwig")
    assert not DB.init_chatt("Kevin")
    assert not DB.add_brach_summary(branch_id+1,"text","Ludwig")
    assert not DB.add_user_to_brach("Kevin", branch_id)
    assert not DB.add_brach("Kevin")

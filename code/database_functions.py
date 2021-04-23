from database import db, Keyword, Questions, Bot_Phrases, User, Message, \
                     Branch, Chatt


def init():
    """
    The init function for the database.
    The function deconstructs and then constructs the database.
    """

    db.drop_all()
    db.create_all()


def add_keyword(keyword_in):
    """
    This function adds a new marked keyword to the database.
    """

    keyword_objekt = Keyword.query.filter_by(keyword=keyword_in).first()
    if keyword_objekt is None:
        new_keyword = Keyword(keyword_in)
        db.session.add(new_keyword)
        db.session.commit()
        return True
    else:
        return False


def get_keywords():
    """
    This function return true if the keyword is in the database, False if not.
    """

    keywords = Keyword.query.all()
    if keywords is not None:
        return [x.get_Keyword() for x in keywords]
    else:
        return []


def delete_keyword(keyword_in):
    """
    This function deletes the keyword form the database.
    """

    keyword_objekt = Keyword.query.filter_by(keyword=keyword_in).first()
    if keyword_objekt is not None:
        db.session.delete(keyword_objekt)
        db.session.commit()
        return True
    else:
        return False


def add_question(question_in, answer):
    """
    This function adds a user question and the bot answer to the database.
    """

    question_exists = Questions.query.filter_by(question=question_in).first()
    if question_exists is None:
        new_question = Questions(question_in, answer)
        db.session.add(new_question)
        db.session.commit()
        return True
    else:
        return False


def get_question_answer(question_in):
    """
    This function gets the bot answer to a user question from the database.
    Returns the answer if it exist, False if not.
    """

    question_objekt = Questions.query.filter_by(question=question_in).first()
    if question_objekt is not None:
        return question_objekt.get_answer()
    else:
        return False


def get_matching_questions(word):
    """
    This function finds questions that contain the input word.
    Returns the answer if it exist, False if not.
    """
    question_objets = Questions.query.\
        filter(Questions.question.like('%'+word+'%')).all()

    if question_objets is not None:
        return [x.get_queston() for x in question_objets]
    else:
        return False


def set_question_answer(question_in, answer_in):
    """
    This function changes the bot answer to a user question in the database.
    Returns True if the change was sucsesfull, False if not.
    """

    question_objekt = Questions.query.filter_by(question=question_in).first()
    if question_objekt is None:
        return False
    else:
        question_objekt.set_answer(answer_in)
        db.session.commit()
        return True


def delete_question(question_in):
    """
    This function removes a user question and the bot answer from the database.
    """

    question_objekt = Questions.query.filter_by(question=question_in).first()
    if question_objekt is not None:
        db.session.delete(question_objekt)
        db.session.commit()
        return True
    else:
        return False


def add_phrase(situation_in, answer):
    """
    This function adds a bot phrase for a situation to the database.
    """

    phrase_exists = Bot_Phrases.query.filter_by(situation=situation_in).first()
    if phrase_exists is None:
        new_phrase = Bot_Phrases(situation_in, answer)
        db.session.add(new_phrase)
        db.session.commit()
        return True
    else:
        return False


def get_phrase_answer(situation_in):
    """
    This function gets the answer for a phrase from the database.
    Returns the phrase if it exits, False if not.
    """

    phrase_objekt = Bot_Phrases.query.filter_by(situation=situation_in).first()
    if phrase_objekt is not None:
        return phrase_objekt.get_answer()
    else:
        return False


def set_phrase_answer(situation_in, answer_in):
    """
    This function changes a current answer to a bot phrase.
    The input should be a situation and an answer to the situation.
    The function returns true or false
    depending on if the situation exists in the database.
    """

    phrase_objekt = Bot_Phrases.query.filter_by(situation=situation_in).first()
    if phrase_objekt is None:
        return False
    else:
        phrase_objekt.set_answer(answer_in)
        db.session.commit()
        return True


def delete_phrase(situation_in):
    """
    This function deletes phrases that are saved to the database.
    The phrases belong to class Bot_phrases.
    """

    phrase_objekt = Bot_Phrases.query.filter_by(situation=situation_in).first()
    if phrase_objekt is not None:
        db.session.delete(phrase_objekt)
        db.session.commit()
        return True
    else:
        return False


def init_chatt(user):
    """
    This function creates a new chatt and adds the chatt to the database,
    The chatt will belong to class User.
    """

    user_object = User.query.filter_by(name=user).first()
    chatt_obejt = Chatt.query.filter_by(user_id=user).first()
    if chatt_obejt is None and user_object is not None:
        new_chatt = Chatt(user)
        new_branch = Branch(user)  # Create a new branch when creating new user
        db.session.add(new_chatt)
        db.session.add(new_branch)
        new_chatt.branch.append(new_branch)
        new_branch.users.append(user_object)
        db.session.commit()
        return new_branch.id
    else:
        return False


def get_chatt(user):
    """
    This function returns all the branches ID's for a user,
    If the user does not exist then False is returned.
    """

    chatt_object = Chatt.query.filter_by(user_id=user).first()
    if chatt_object is not None:
        return [x.id for x in chatt_object.branch]
    else:
        return False


def add_brach(user):
    """
    This function creates a new branch and adds the branch to the database,
    The branch will belong to class Branch.
    """

    chatt_object = Chatt.query.filter_by(user_id=user).first()
    if chatt_object is not None:
        new_branch = Branch(user)
        db.session.add(new_branch)
        chatt_object.branch.append(new_branch)
        user_object = User.query.filter_by(name=user).first()
        new_branch.users.append(user_object)
        db.session.commit()
        return new_branch.id
    else:
        return False


def add_brach_summary(branch_id, summary_in, user_in):
    """
    This function creates a branch summary,
    if there is an existning summary it will be overwritten.
    """

    branch_object = Branch.query.filter_by(id=branch_id).first()
    if branch_object is not None:
        branch_object.set_summary(summary_in, user_in)
        db.session.commit()
        return True
    else:
        return False


def add_user_to_brach(user, branch_id):
    """
    This function adds a user to an existing branch.
    If user has been sucssesfully added then True is returned, otherwise False.
    """
    branch_object = Branch.query.filter_by(id=branch_id).first()
    user_object = User.query.filter_by(name=user).first()
    if branch_object is not None and user_object is not None:
        branch_object.users.append(user_object)
        db.session.commit()
        return True
    else:
        return False


def add_user(name_in, role_in=None):
    """
    This function creates a new user and adds the user to the database,
    If user has been sucssesfully added then True is returned, otherwise False.
    """
    user_object = User.query.filter_by(name=name_in).first()
    if user_object is None:
        new_user = User(name_in, role_in)
        db.session.add(new_user)
        db.session.commit()
        return True
    else:
        return False


def get_user(name_in):
    """
    This function gets the requested user and the respective role
    if user exists, otherwise False.
    """
    user_object = User.query.filter_by(name=name_in).first()
    if user_object is not None:
        return (user_object.get_name(), user_object.get_role())
    else:
        return False


def set_user_role(name_in, role_in):
    """
    This function creates a new user role and adds
    the new role to the database.
    """
    user_object = User.query.filter_by(name=name_in).first()
    if user_object is not None:
        user_object.set_role(role_in)
        db.session.commit()
        return True
    else:
        return False


def delete_user(user_id):
    """
    Delete a user form the database
    Returns true if sucsesfull false if not
    """

    user_object = User.query.filter_by(name=user_id).first()
    if user_object is not None:
        db.session.delete(user_object)
        db.session.commit()
        return True
    else:
        return False


def new_message(message, user, branch_id, index):
    """
    Creates a new message in a branch.
    The index is its posistion in the chat window.
    The user is the owner of this message
    Returns True if the message was created sucsesfully fals if not.
    """

    branch_object = Branch.query.filter_by(id=branch_id).first()
    if branch_object is not None:
        message_object = Message(index, message, user, branch_id)
        db.session.add(message_object)
        branch_object.message.append(message_object)
        db.session.commit()
        return True
    else:
        return False


def get_messages(branch_id):
    """
    Returns the messages in a branch, if the branch does not exist then
    false is returned.
    """
    branch_object = Branch.query.filter_by(id=branch_id).first()
    if branch_object is not None:
        return [[x.get_user(), x.get_message(), x.get_index()]
                for x in branch_object.message]
    else:
        return False

from server import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from flask import json
from datetime import datetime
from sqlalchemy.orm.exc import NoResultFound
from flask_jwt_extended import decode_token


db = SQLAlchemy(app)


#----------------------------DATA---------------------------------------------
readBy = db.Table('readBy',
    db.Column('message_id', db.Integer, db.ForeignKey('Message.id'),primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('User.id'), primary_key=True)
    )


class Message(db.Model):
    __tablename__ = 'Message'
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(70), nullable=False, unique=False)
    readBy = db.relationship('User', secondary=readBy, lazy='subquery',
        backref=db.backref('messages', lazy=True))

    def __init__(self, msg):
        self.message = msg


    def get_message(self):
        return self.message


    def get_msgID(self):
        return self.id

    def get_readBy(self):
        return [x.get_username() for x in self.readBy]


    def get_all(self):
        return {'id':self.id,
                'message':self.message,
                'readBy':self.get_readBy()}

    def __repr__(self):
        return json.dumps({'id':self.id,
                'message':self.message,
                'readBy':self.get_readBy()})

class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False, unique=False)

    def __init__(self,username,password):
        self.username = username
        self.password = password

    def get_id(self):
        return self.id

    def get_username(self):
        return self.username

    def __repr__(self):
        return json.dumps({'username':self.username})


class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    iat = db.Column(db.String(10),nullable=False)
    jti = db.Column(db.String(36), nullable=False)
    expires = db.Column(db.DateTime, nullable=False)
    user_identity = db.Column(db.String(50), nullable=False)
    token_type = db.Column(db.String(10), nullable=False)


    def to_dict(self):
        return {
            'id': self.id,
            'iat' : self.iat,
            'jti': self.jti,
            'expires': self.expires,
            'user_identity': self.user_identity,
            'token_type': self.token_type
            }

#----------------------------DATA---------------------------------------------

#--------------------------Sepret Functions-----------------------------------
def store_message(msg):
    new_message = Message(msg)
    db.session.add(new_message)
    db.session.commit()

    return new_message.id


def delete_message(msg):
    db.session.delete(msg)
    db.session.commit()


def create_user(username,password):
    new_user = User(username,password)
    db.session.add(new_user)
    db.session.commit()

def add_read(user,msg):
    msg.readBy.append(user)
    db.session.commit()

def init():
    db.drop_all()
    db.create_all()


def add_token(token):
    new_token = Token(token)
    db.session.add(new_token)
    db.session.commit()

def get_all_messages():
    return [x.get_all() for x in Message.query.all()]

def get_all_messagesID():
    return [x.get_msgID() for x in Message.query.all()]

def get_messageID(messageID):
    return Message.query.filter_by(id=messageID).first()


def get_user(username):
    return User.query.filter_by(username=username).first()


        #msg = data_handler.get_all_messages()
        #temp_list = []

        #for el in msg:

        #    if not userID in el['readBy']:
        #        temp_list += [el]

        #return temp_list, 200
def get_unread(username):
    message = db.session.query(Message).\
        outerjoin(Message.readBy).filter(or_(User.username.is_(None), User.username != username)).distinct(User.username).all()
    return message

def get_blacklist_jtis():
    return [token.jti for token in Token.query.all()]


def _epoch_utc_to_datetime(epoch_utc):
    return datetime.fromtimestamp(epoch_utc)


def add_token_to_database(token, identity_claim):

    iat = token['iat']
    jti = token['jti']
    token_type = token['type']
    expires = _epoch_utc_to_datetime(token['exp'])

    db_token = Token(
        iat=iat,
        jti=jti,
        token_type=token_type,
        user_identity=identity_claim,
        expires=expires,
    )
    db.session.add(db_token)
    db.session.commit()


def prune_database():
    """
    Delete tokens that have expired from the database.
    How (and if) you call this is entirely up you. You could expose it to an
    endpoint that only administrators could call, you could run it as a cron,
    set it up with flask cli, etc.
    """
    now = datetime.now()
    expired = Token.query.filter(Token.expires < now).all()
    for token in expired:
        db.session.delete(token)
    db.session.commit()

#--------------------------Sepret Functions-----------------------------------

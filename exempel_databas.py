from flask_restful import Resource, Api, reqparse
import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
        JWTManager, jwt_required, get_jwt_identity,
        create_access_token, get_raw_jwt)
from datetime import timedelta


#FLASK_APP=server.py flask run

app = Flask(__name__)
app.debug = True


if 'NAMESPACE' in os.environ and os.environ['NAMESPACE'] == 'heroku':
    db_uri = os.environ['DATABASE_URL']
    debug_flag = False
else: # when running locally with sqlite
    db_path = os.path.join(os.path.dirname(__file__), 'app.db')
    db_uri = 'sqlite:///{}'.format(db_path)
    debug_flag = True

app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']
app.config['JWT_SECRET_KEY'] = os.urandom(20).hex()
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=7)


bcrypt = Bcrypt(app)
import data_handler
jwt = JWTManager(app)
api = Api(app)


# Parser.
parser = reqparse.RequestParser()
parser.add_argument('message')
parser.add_argument('username')
parser.add_argument('password')


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in data_handler.get_blacklist_jtis()


#----------------------------SERVER-------------------------------------------
class Messages(Resource): #/messages


    def get(self):
        """GET-call for /messages, returns message and HTTP 200."""
        all_msg = data_handler.get_all_messages()
        return all_msg , 200

    @jwt_required
    def post(self):
        """POST-call for ../messages, adds message to our message list
        and gives it a unique ID if valid data given. Returns message-ID and
        HTTP 200.
        """
        message = parser.parse_args()['message']

        print(message)

        if not isinstance(message,str) or len(message) > 140:
            return 'No valid data given' , 400

        id = data_handler.store_message(message)
        return {'id': id}, 200


class MessageID(Resource): #/messages/<messageID>

    def get(self,messageID):
        """GET-call for /messages/<messageID>, returns the messages with
        desired message-ID to the user."""

        message = data_handler.get_messageID(messageID)
        if message is None:
            return "Invalid message id.", 404
        else:
            return message.get_all(), 200

    @jwt_required
    def delete(self,messageID):
        """ Deletes all message of given message-ID,
        returns HTTP 200 if successful, otherwise returns HTTP 404 """

        msg = data_handler.get_messageID(messageID)
        if msg is None:
            return "Invalid message ID.", 404
        else:
            data_handler.delete_message(msg)
            return 'Message removed.',200


class Unread(Resource): #/messages/unread/<username>


    @jwt_required
    def get(self,username):
        """ GET-call for messages/unread/<username>, returns list with desired
        user-ID. """
        result = []
        messages = data_handler.get_unread(username)
        for message in messages:
            result.append({'id':message.message_id,
                        'message':message.message,
                        'readBy':message.get_readBy()})

        return result


class Flag(Resource): # /messages/<messageID>/flag/<username>


    @jwt_required
    def post(self, messageID, username):
        """ Flags a given message as read by given user."""

        msg = data_handler.get_messageID(messageID)
        user = data_handler.get_user(username)

        if msg is None:
            return 'Invalid message ID.', 404
        if user is None:
            return 'Invaild username', 404

        data_handler.add_read(user,msg)

        return 'Message read' , 200


class Create(Resource): # /user


    def post(self):
        args = parser.parse_args()
        username = args['username']


        if data_handler.get_user(username) != None:
            return 'username in use',401
        if username == None:
            return 'no username given', 405
        if args['password'] == None:
            return 'no password given' , 405

        password = bcrypt.generate_password_hash(args['password']).decode('utf-8')

        data_handler.create_user(username,password)
        return 'user created', 200


class Login(Resource): # /user/login
    def post(self):
        data_handler.prune_database()

        args = parser.parse_args()
        user = data_handler.get_user(args['username'])

        if user == None:
            return "{'Error':'No such user'}",401
        if args['password'] == None:
            return 'no password given' , 405

        if bcrypt.check_password_hash(user.password,args['password']):
            access_token = create_access_token(identity=user.username)

            return {'token':access_token},200
        return "{'Error':'Wrong password'}", 400


class Logout(Resource): # /user/logout
#,RevokedTokenError

    @jwt_required
    def post(self):
        data_handler.add_token_to_database(get_raw_jwt(),get_jwt_identity())
        return 'Logout successful',200


class init_db(Resource): # /init_dbinit

    def get(self):
        data_handler.init()
        return '',200


class welcome(Resource):

    def get(self):
        return "Welcome"



api.add_resource(welcome, '/')

api.add_resource(Create, '/user')

api.add_resource(Login, '/user/login')

api.add_resource(Logout, '/user/logout')

api.add_resource(Unread, '/messages/unread/<username>')

api.add_resource(Flag, '/messages/<messageID>/flag/<username>')

api.add_resource(MessageID, '/messages/<messageID>')

api.add_resource(Messages, '/messages')

api.add_resource(init_db, '/init_db')


#----------------------------SERVER-------------------------------------------

if __name__ == "__main__":
    data_handler.init()

from enum import Enum
from flask import Flask, render_template, send_from_directory, request
from werkzeug.wrappers import CommonResponseDescriptorsMixin
from flask_socketio import SocketIO
import authentication


clientIdCounter = 0

class Client:
    """
    The Client class
    """

    def __init__(self, sid, name, backgroundColor, userIconSource, role):
        global clientIdCounter
        self.sid = sid
        self.name = name
        self.backgroundColor = backgroundColor
        self.userIconSource = userIconSource
        self.authenticated = False
        self.role = role
        clientIdCounter += 1
        self.id = clientIdCounter


class Chat:
    """
    The Chat class
    """

    def __init__(self, clients, color = "white", imageSource ="/images/user.png", parent= None ):
        self.history = []
        self.clients = clients
        self.active = True
        self.color = color
        self.imageSource = imageSource
        self.parent = parent
 

class Message:
    """
    The Message class
    """

    def __init__(self, sender, text):
        self.sender = sender
        self.text = text


class Roles (Enum):
    """
    Enum for roles
    """
    odefinierad = 0
    patient = 1
    personal = 2


# Initializes the server
app = Flask(__name__)

# Adds socket support for the server
socketio = SocketIO(app)


@app.route('/')
def index():
    """
    Returns the html start page to the client
    """
    return render_template('index.html')


@app.route('/<path:path>')
def open_template(path):
    """
    Returns the html page from a path to the client
    """
    return render_template(path + ".html")


@app.route('/scripts/<path:path>')
def send_js(path):
    """
    Returns the script from a path to the client
    """
    return send_from_directory('scripts/compiled-javascript', path)


@app.route('/images/<path:path>')
def send_images(path):
    """
    Returns the image from a path to the client
    """
    return send_from_directory('images', path)


# All the connected clients
clients = []

# All the chats
chats = {"huvudchatt": Chat([]), "chatt2": Chat([],"blue", "/images/bot.png", "huvudchatt")}


@socketio.on('authenticate')
def authenticate_event(methods=['GET', 'POST']):
    """
    The event for authenticating clients
    """
    client = get_client(request.sid)
    if(not client.authenticated):
        client.authenticated = authentication.authenticate(client)
    if client.authenticated:
        send_info_message(200, "Du är nu autentiserad", request.sid)
    else:
        send_info_message(
            400, "Det uppstod ett fel vid autentisering", request.sid)


# Temporary data
names = ["Ludwig", "Sven", "Anna", "Emma", "Peter", "Kalle"]
backgroundColors = ["Green", "Blue", "Red", "#123", "#FFF", "Cyan"]
userIconSources = ["/images/user.png", "/images/bot.png"]




@socketio.on('get_users')
def get_users_event(methods=['GET', 'POST']):
    """
    The event for when clients connect
    """
    currentSocketId = request.sid
    json = {"users": []}
    for client in clients:

        json["users"].append(
            {"name": client.name, "role": str(client.role.name) }
        )

    socketio.emit('return_users', json, room=currentSocketId)


@socketio.on('get_chats')
def get_chats_event(methods=['GET', 'POST']):
    """
    The event for when clients connect
    """
    currentSocketId = request.sid
    json = {"chats": []}
    for chat in chats:

        json["chats"].append(
            chat
        )

    socketio.emit('return_chats', json, room=currentSocketId)
    



@socketio.on('connect')
def connect_event(methods=['GET', 'POST']):
    """
    The event for when clients connect
    """
    print("\nUser connected: " + request.sid)
    currentSocketId = request.sid
    backgroundColor = "white"
    userIconSource = userIconSources[0]
    name = "anonym"
    role = Roles["odefinierad"]
    add_client(currentSocketId, name, backgroundColor, userIconSource, role)

@socketio.on('disconnect')
def disconnect_event(methods=['GET', 'POST']):
    """
    Removes client from the clients list when disconected.
    """
    client1 = get_client(request.sid)
    clients.remove(client1)
    for chatname in chats:
        chat = chats[chatname]
        for client2 in chat.clients:
            if client1 == client2:
                chat.clients.remove(client1)
    socketio.emit("client_disconnect", {"id": client1.id})
    print("\n"+ client1.name + "(" + str(client1.id) + ") has disconnected")

@socketio.on('details_assignment')
def details_assignment_event(json, methods=['GET', 'POST']):
    """
    The event for asigning credentials
    """
    client = get_client(request.sid)
    client.name = json["name"]
    client.backgroundColor = json["backgroundColor"]
    client.userIconSource = json["userIconSource"]
    client.role = Roles[json["role"]]
    json = {"id": client.id, "name": client.name, "backgroundColor": client.backgroundColor, "userIconSource": client.userIconSource}
    for client2 in clients:
        if client.id != client2.id:
            socketio.emit("client_details_changed", json, room=client2.sid)
    send_info_message(200, "Användarinformation satt", request.sid)


@socketio.on('message')
def message_event(json, methods=['GET', 'POST']):
    """
    The event for when a message is recieved from a client
    """
    print("\nMessage: " + json['message'] + "(" + json['chatName'] + ")")
    sender = get_client(request.sid)
    chatName = json["chatName"]
    if chatName in chats:
        chat = chats[chatName]
        if chat.active:
            message = Message(sender, json['message'])
            chat.history.append(message)
            broadcast_message(message, chatName)
        else:
            send_info_message(200, "Chatten är avslutad", request.sid)
    else:
        send_info_message(404, "Chatten finns inte", request.sid)


@socketio.on('chat_create')
def chat_create_event(json, methods=['GET', 'POST']):
    """
    The event for creating a new chat
    """
    client = get_client(request.sid)
    if not client.role == Roles["personal"]:
        send_info_message(401, "Du har inte rätt roll för att skapa en chatt")
    elif not client.authenticated:
        send_info_message(
            401, "Du är inte autentiserad och kan därför inte skapa chattar")
    else:
        chatName = json["chatName"]
        if chatName in chats:
            send_info_message(400, "Chattnamnet är redan taget", request.sid)
        else:
            chats[chatName] = Chat([client])
            send_info_message(200, "Chatten är skapad", request.sid)


@socketio.on('chat_delete')
def chat_delete_event(json, methods=['GET', 'POST']):
    """
    The event for removing a chat
    """
    client = get_client(request.sid)
    if not client.role == Roles["personal"]:
        send_info_message(
            401, "Du har inte rätt roll för att ta bort en chatt")
    elif not client.authenticated:
        send_info_message(
            401, "Du är inte autentiserad och kan därför inte ta bort chattar")
    else:
        chatName = json["chatName"]
        if chatName in chats:
            del chats[chatName]
            send_info_message(200, "Chatten är borttagen", request.sid)
        else:
            send_info_message(404, "Chatten finns inte", request.sid)


@socketio.on('chat_end')
def chat_end_event(json, methods=['GET', 'POST']):
    """
    The event for ending a chat
    """
    client = get_client(request.sid)
    if not client.role == Roles["personal"]:
        send_info_message(
            401, "Du har inte rätt roll för att avsluta en chatt")
    elif not client.authenticated:
        send_info_message(
            401, "Du är inte autentiserad och kan därför inte avsluta chattar")
    else:
        chatName = json["chatName"]
        if chatName in chats:
            chats[chatName].active = False
            send_info_message(200, "Chatten är avslutad", request.sid)
        else:
            send_info_message(404, "Chatten finns inte", request.sid)


@socketio.on('chat_join')
def chat_join_event(json, methods=['GET', 'POST']):
    """
    The event for creating a new chat
    """
    client = get_client(request.sid)
    chatName = json["chatName"]
    print(request.sid + " has joined " + chatName)
    print(chats["huvudchatt"].clients)
    print(chats["chatt2"].clients)
    print(len(chats[chatName].clients))

    if chatName in chats:
        for otherClient in chats[chatName].clients :
            socketio.emit("client_connect", {
                "chatName": chatName,
                "client": client.name,
                "color": client.backgroundColor,
                "iconSource": client.userIconSource,
                "id": client.id
                }, room=otherClient.sid)
        chats[chatName].clients.append(client)
        send_info_message(
            200, "Klienten har anslutit till chatten", request.sid)
        send_chat_info(client, chatName)
    else:
        send_info_message(404, "Chatten finns inte", request.sid)

@socketio.on('get_chat_history')
def get_chat_history_event(json, methods=['GET', 'POST']):
    """
    Sends the whole chat history of the given chat to a client
    """
    chatName = json["chatName"]
    chat = chats[chatName]
    client = get_client(request.sid)
    for message in chat.history:
        send_message(message, client, chatName)


def send_info_message(statusCode, message, sid):
    """
    Sends the given info message
    """
    json = {'status': statusCode, 'message': message}
    socketio.emit('info', json, room=sid)


def send_chat_info(reciever, chatName):
    """
    Sends the whole chat history of the given chat to a client
    """
    chat = chats[chatName]
    clients = []
    for client in chat.clients:
        clients.append({'name': client.name, 'background': client.backgroundColor, 'userIconSource': client.userIconSource, 'id': client.id})
    json = {'chatName': chatName, 'color': chat.color, 'imageSource': chat.imageSource, 'clients': clients}
    if not chat.parent == None:
        json["parent"] = chat.parent
    socketio.emit('chat_info', json, room=reciever.sid)


    


def broadcast_message(message, chatName, ignoreSender=True):
    """
    Broadcasts the message to all clients
    """
    sender = message.sender
    json = {
            'sender': sender.name,
            'icon-source': sender.userIconSource,
            'background': sender.backgroundColor,
            'message': message.text,
            'chatName': chatName
        }
    
    for client in chats[chatName].clients:
        if(not ignoreSender or not client.sid == sender.sid):
            socketio.emit('message', json, room=client.sid)


def send_message(message, reciever, chatName):
    """
    Sends the message to a client
    """
    sender = message.sender
    json = {
            'sender': sender.name,
            'icon-source': sender.userIconSource,
            'background': sender.backgroundColor,
            'message': message.text,
            'chatName': chatName
        }
    socketio.emit('message', json, room=reciever.sid)


def add_client(sid, name, backgroundColor, userIconSource, role):
    """
    Adds a client to the list of all clients
    """
    client = Client(sid, name, backgroundColor, userIconSource, role)
    clients.append(client)
    return client


def get_client(sid):
    """
    Returns the client with a session id
    """
    for client in clients:
        if(client.sid == sid):
            return client
    return {}


def run():
    """
    Runs the server
    """
    socketio.run(app, debug=True)

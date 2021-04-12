from typing import Collection
from enum import Enum 
from flask import Flask, render_template, send_from_directory, request
from flask_socketio import SocketIO
import authentication

# The Client class
class Client:
  def __init__(self, sid, name, backgroundColor, userIconSource, role):
    self.sid = sid
    self.name = name
    self.backgroundColor = backgroundColor
    self.userIconSource = userIconSource
    self.authenticated = False
    self.role = role 

# The Chat class
class Chat:
  def __init__(self, clients = []):
    self.history = []
    self.clients = clients
    self.active = True


# The Message class
class Message:
  def __init__(self, sender, text):
    self.sender = sender
    self.text = text

#Enum for roles
class Roles (Enum): 
  odefinierad = 0
  patient = 1
  personal = 2

# Initializes the server
app = Flask(__name__)

# Adds socket support for the server
socketio = SocketIO(app)

# Returns the html start page to the client
@app.route('/')
def index():
  return render_template('index.html')

# Returns the html page from a path to the client
@app.route('/<path:path>')
def open_template(path):
  return render_template(path+ ".html")

# Returns the script from a path to the client
@app.route('/scripts/<path:path>')
def send_js(path):
  return send_from_directory('scripts/compiled-javascript', path)

# Returns the image from a path to the client
@app.route('/images/<path:path>')
def send_images(path):
  return send_from_directory('images', path)
  
# All the connected clients
clients = []

# All the chats
chats = {"huvudchatt":Chat()}


# The event for authenticating clients
@socketio.on('authenticate')
def authenticate_event(methods=['GET', 'POST']):
  client = get_client(request.sid)
  if(not client.authenticated):
    client.authenticated = authentication.authenticate(client)
  if client.authenticated :
    send_info_message(200, "Du är nu autentiserad", request.sid)
  else : 
    send_info_message(400, "Det uppstod ett fel vid autentisering", request.sid)

# Temporary data
names = ["Ludwig", "Sven", "Anna", "Emma", "Peter", "Kalle"]
backgroundColors = ["Green", "Blue", "Red", "#123", "#FFF", "Cyan"]
userIconSources = ["/images/user.png", "/images/bot.png"]

# The event for when clients connect
@socketio.on('connect')
def connect_event(methods=['GET', 'POST']):
  print("\nUser connected: " + request.sid)
  currentSocketId = request.sid
  backgroundColor = "white"
  userIconSource = userIconSources[0]
  name = "anonym"
  role = Roles["odefinierad"]
  add_client(currentSocketId, name, backgroundColor, userIconSource, role)
 
# The event for asigning credentials
@socketio.on('details_assignment')
def details_assignment_event(json, methods=['GET', 'POST']):
  client = get_client(request.sid)
  client.name = json["name"]
  client.backgroundColor = json["backgroundColor"]
  client.userIconSource = json["userIconSource"]
  client.role = Roles[json["role"]]
  send_info_message(200, "Användarinformation satt", request.sid)


# The event for when a message is recieved from a client
@socketio.on('message')
def message_event(json, methods=['GET', 'POST']):
  print("\nMessage: " + json['message'] + "(" + json['chatName'] + ")")
  sender = get_client(request.sid)
  chatName = json["chatName"]
  if chatName in chats :
    chat = chats[chatName]
    if chat.active :
      message = Message(sender, json['message'])
      chat.history.append(message)
      broadcast_message(message, chatName)
    else :
      send_info_message(200, "Chatten är avslutad", request.sid)
  else :
    send_info_message(404, "Chatten finns inte", request.sid)
  

# The event for creating a new chat
@socketio.on('chat_create')
def chat_create_event(json, methods=['GET', 'POST']):
  client = get_client(request.sid)
  if not client.role == Roles["personal"] :
    send_info_message(401, "Du har inte rätt roll för att skapa en chatt")
  elif not client.authenticated :
    send_info_message(401, "Du är inte autentiserad och kan därför inte skapa chattar")
  else:
    chatName = json["chatName"]
    if chatName in chats : 
      send_info_message(400, "Chattnamnet är redan taget", request.sid)
    else : 
      chats[chatName] = Chat([client])
      send_info_message(200, "Chatten är skapad", request.sid)

# The event for removing a chat
@socketio.on('chat_delete')
def chat_delete_event(json, methods=['GET', 'POST']):
  client = get_client(request.sid)
  if not client.role == Roles["personal"] :
    send_info_message(401, "Du har inte rätt roll för att ta bort en chatt")
  elif not client.authenticated :
    send_info_message(401, "Du är inte autentiserad och kan därför inte ta bort chattar")
  else:
    chatName = json["chatName"]
    if chatName in chats : 
      del chats[chatName]
      send_info_message(200, "Chatten är borttagen", request.sid)
    else : 
      send_info_message(404, "Chatten finns inte", request.sid)
  
# The event for ending a chat
@socketio.on('chat_end')
def chat_end_event(json, methods=['GET', 'POST']):
  client = get_client(request.sid)
  if not client.role == Roles["personal"] :
    send_info_message(401, "Du har inte rätt roll för att avsluta en chatt")
  elif not client.authenticated :
    send_info_message(401, "Du är inte autentiserad och kan därför inte avsluta chattar")
  else:
    chatName = json["chatName"]
    if chatName in chats : 
      chats[chatName].active = False
      send_info_message(200, "Chatten är avslutad", request.sid)
    else : 
      send_info_message(404, "Chatten finns inte", request.sid)

# The event for creating a new chat
@socketio.on('chat_join')
def chat_join_event(json, methods=['GET', 'POST']):
  client = get_client(request.sid)
  chatName = json["chatName"]
  if chatName in chats : 
    chats[chatName].clients.append(client)
    send_info_message(200, "Klienten har anslutit till chatten", request.sid)
    send_chat_history(client,chatName)
  else : 
    send_info_message(404, "Chatten finns inte", request.sid)

# Sends the given info message
def send_info_message(statusCode, message, sid):
  json = {'status': statusCode, 'message':message}
  socketio.emit('info', json, room=sid)

# Sends the whole chat history of the given chat to a client
def send_chat_history(reciever,chatName):
  chat = chats[chatName]
  for message in chat.history:
    send_message(message, reciever,chatName) 

# Broadcasts the message to all clients
def broadcast_message(message, chatName, ignoreSender = True):
  sender = message.sender
  json = {'sender': sender.name, 'icon-source': sender.userIconSource, 'background': sender.backgroundColor, 'message':message.text, 'chatName':chatName}
  for client in chats[chatName].clients:
    if(not ignoreSender or not client.sid == sender.sid):
      socketio.emit('message', json, room=client.sid)  

# Sends the message to a client
def send_message(message, reciever, chatName):
  sender = message.sender
  json = {'sender': sender.name, 'icon-source': sender.userIconSource, 'background': sender.backgroundColor, 'message':message.text, 'chatName':chatName}
  socketio.emit('message', json, room=reciever.sid)

# Adds a client to the list of all clients
def add_client(sid, name, backgroundColor, userIconSource, role):
  client = Client(sid, name, backgroundColor, userIconSource, role)
  clients.append(client)
  return client

# Returns the client with a session id
def get_client(sid):
  for client in clients:
    if(client.sid == sid):
      return client
  return {}

def run():
    socketio.run(app, debug=True)
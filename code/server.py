from typing import Collection
from flask import Flask, render_template, send_from_directory, request
from flask_socketio import SocketIO
import authentication

# The Client class
class Client:
  def __init__(self, sid, name, backgroundColor, userIconSource):
    self.sid = sid
    self.name = name
    self.backgroundColor = backgroundColor
    self.userIconSource = userIconSource
    self.authenticated = False

# The Chat class
class Chat:
  def __init__(self, clients = []):
    self.history = []
    self.clients = clients


# The Message class
class Message:
  def __init__(self, sender, text):
    self.sender = sender
    self.text = text

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
chats = [Chat()]


# The event for authenticating clients
@socketio.on('authenticate')
def authenticate_event(methods=['GET', 'POST']):
  client = get_client(request.sid)
  if(not client.authenticated):
    client.authenticated = authentication.authenticate(client)
  json = {'status': 200, 'message':'Du är nu autentiserad.'} if client.authenticated else {'status': 400, 'message':'Det uppstod ett fel vid autentisering!'}
  socketio.emit('info', json, room=request.sid)

# Temporary data
names = ["Ludwig", "Sven", "Anna", "Emma", "Peter", "Kalle"]
backgroundColors = ["Green", "Blue", "Red", "#123", "#FFF", "Cyan"]
userIconSources = ["/images/user.png", "/images/bot.png"]

# The event for when clients connect
@socketio.on('connect')
def connect_event(methods=['GET', 'POST']):
  print("\nUser connected: " + request.sid)
  currentSocketId = request.sid
  name = names[len(clients)%len(names)]
  backgroundColor = backgroundColors[len(clients)%len(backgroundColors)]
  userIconSource = userIconSources[0]
  client = Client(currentSocketId, name, backgroundColor, userIconSource)
  clients.append(client)
  chats[0].clients.append(client)
  send_chat_history(client,chats[0])

# The event for when a message is recieved from a client
@socketio.on('message')
def message_event(json, methods=['GET', 'POST']):
  print("\nMessage: " + json['message'])
  sender = get_client(request.sid)
  message = Message(sender, json['message'])
  chats[0].history.append(message)
  broadcast_message(message)

# Sends the whole chat history of the given chat to a client
def send_chat_history(reciever,chat):
  for message in chat.history:
    send_message(message, reciever) 

# Broadcasts the message to all clients
def broadcast_message(message, ignoreSender = True):
  sender = message.sender
  json = {'sender': sender.name, 'icon-source': sender.userIconSource, 'background': sender.backgroundColor, 'message':message.text}
  for client in clients:
    if(not ignoreSender or not client.sid == sender.sid):
      socketio.emit('message', json, room=client.sid)  

# Sends the message to a client
def send_message(message, reciever):
  sender = message.sender
  json = {'sender': sender.name, 'icon-source': sender.userIconSource, 'background': sender.backgroundColor, 'message':message.text}
  socketio.emit('message', json, room=reciever.sid)

# Returns the client with a session id
def get_client(sid):
  for client in clients:
    if(client.sid == sid):
      return client
  return {}

# Starts the server
if __name__ == '__main__':
  socketio.run(app, debug=True)
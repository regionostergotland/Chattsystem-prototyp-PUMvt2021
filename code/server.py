from flask import Flask, render_template, send_from_directory, request
from flask_socketio import SocketIO

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

# The event for when clients connect
@socketio.on('connect')
def connect_event(methods=['GET', 'POST']):
  currentSocketId = request.sid
  clients.append(currentSocketId)

# The event for when a message is recieved from a client
@socketio.on('message')
def message_event(json, methods=['GET', 'POST']):
  currentSocketId = request.sid
  print(json['message'])
  for sid in clients:
    if(not sid == currentSocketId):
      socketio.emit('message', json, room=sid)  

# Starts the server
if __name__ == '__main__':
  socketio.run(app, debug=True)
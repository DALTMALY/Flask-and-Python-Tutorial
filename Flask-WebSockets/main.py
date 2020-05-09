from flask import Flask,render_template
#Send: Method for send messages to web
from flask_socketio import SocketIO, send

#Star Server
app = Flask(__name__)
#Config required from socketIO docs
app.config['SECRET_KEY'] = 'secret'
#Start connection socketio with server
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

#Received messages from web "Listen Server"

#When server listen's an event called 'message'
@socketio.on('message')
#get and save in 'msg' variable
def handleMessage(msg):
    print("Message: " + msg)
    #all clients will can read, server emit an event
    send(msg,broadcast=True)

if __name__ == "__main__":
    socketio.run(app)
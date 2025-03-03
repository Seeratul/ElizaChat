## channel.py - a simple message channel
##

from flask import Flask, request, render_template, jsonify
import json
import requests
# own imports
from better_profanity import profanity
from datetime import datetime
from eliza import Eliza

# Class-based application configuration
class ConfigClass(object):
    """ Flask application config """

    # Flask settings
    SECRET_KEY = 'This is an INSECURE secret!! DO NOT use this in production!!' # change to something random, no matter what

# Create Flask app
app = Flask(__name__)
app.config.from_object(__name__ + '.ConfigClass')  # configuration
app.app_context().push()  # create an app context before initializing db

HUB_URL = 'http://vm146.rz.uni-osnabrueck.de/hub'
HUB_AUTHKEY = 'Crr-K24d-2N'
CHANNEL_AUTHKEY = '0987654321' 
CHANNEL_NAME = "Group Therapy with Eliza"
CHANNEL_ENDPOINT = "http://vm146.rz.uni-osnabrueck.de/u032/channel.wsgi/" # don't forget to adjust in the bottom of the file
CHANNEL_FILE = 'messages.json'
CHANNEL_TYPE_OF_SERVICE = 'aiweb24:chat'

@app.cli.command('register')
def register_command():
    global CHANNEL_AUTHKEY, CHANNEL_NAME, CHANNEL_ENDPOINT

    # send a POST request to server /channels
    response = requests.post(HUB_URL + '/channels', headers={'Authorization': 'authkey ' + HUB_AUTHKEY},
                             data=json.dumps({
                                "name": CHANNEL_NAME,
                                "endpoint": CHANNEL_ENDPOINT,
                                "authkey": CHANNEL_AUTHKEY,
                                "type_of_service": CHANNEL_TYPE_OF_SERVICE,
                             }))

    if response.status_code != 200:
        print("Error creating channel: "+str(response.status_code))
        print(response.text)
        return

def check_authorization(request):
    global CHANNEL_AUTHKEY
    # check if Authorization header is present
    if 'Authorization' not in request.headers:
        return False
    # check if authorization header is valid
    if request.headers['Authorization'] != 'authkey ' + CHANNEL_AUTHKEY:
        return False
    return True

@app.route('/health', methods=['GET'])
def health_check():
    global CHANNEL_NAME
    if not check_authorization(request):
        return "Invalid authorization", 400
    return jsonify({'name':CHANNEL_NAME}),  200

# GET: Return list of messages
@app.route('/', methods=['GET'])
def home_page():
    if not check_authorization(request):
        return "Invalid authorization", 400
    # fetch channels from server
    return jsonify(read_messages())

# POST: Send a message
@app.route('/', methods=['POST'])
def send_message():
    # fetch channels from server
    # check authorization header
    if not check_authorization(request):
        return "Invalid authorization", 400
    # check if message is present
    message = request.json
    if not message:
        return "No message", 400
    if not 'content' in message:
        return "No content", 400
    if not 'sender' in message:
        return "No sender", 400
    if not 'timestamp' in message:
        return "No timestamp", 400
    if not 'extra' in message:
        extra = None
    else:
        extra = message['extra']
    # answer
    answer_msg = answer_message(message)
    # filter
    message['content'] = profanity.censor(message['content']) 
    # add message to messages
    messages = read_messages()
    messages.append({'content': message['content'],
                     'sender': message['sender'],
                     'timestamp': message['timestamp'],
                     'extra': extra,
                     })
    # check overflow
    messages = check_msg_overflow(messages)
    save_messages(messages)

    # add message to messages
    messages = read_messages()
    messages.append({'content': answer_msg['content'],
                     'sender': answer_msg['sender'],
                     'timestamp': answer_msg['timestamp'],
                     })
    save_messages(messages)

    return "OK", 200

def answer_message(msg):
    therapist = Eliza()
    reply = therapist.respond(msg['content'], msg['sender'])
    new_msg = {'content': reply,
                'sender': "Eliza",
                'timestamp': datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
                    }
    if new_msg['content'] == None: # if for whatever reason eliza fails
        new_msg = {'content': "I have nothing to say to that",
                'sender': "eliza",
                'timestamp': datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
                }
    return new_msg

def check_msg_overflow(messages, cap=25):
    # delete old messages if cap of messages is reached
    if len(messages) > cap:
        messages.remove(messages[1]) # del 2nd msg (first is welcome msg and should stay!)
        messages.remove(messages[2]) # del 3rd msg (make space for answer msg)
    return messages

def welcome(messages):
    # in case message file is empty send welcome message
    if len(messages) == 0:
        new_msg = {'content': "Welcome to the group therapy channel. I am the therapist Eliza.",
            'sender': "Eliza",
            'timestamp': datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
                }
        messages.append(new_msg)
    return messages

def read_messages():
    global CHANNEL_FILE
    try:
        f = open(CHANNEL_FILE, 'r')
    except FileNotFoundError:
        return []
    try:
        messages = json.load(f)
    except json.decoder.JSONDecodeError:
        messages = []
    f.close()
    # in case message file is empty
    messages = welcome(messages)
    return messages

def save_messages(messages):
    global CHANNEL_FILE
    with open(CHANNEL_FILE, 'w') as f:
        json.dump(messages, f)

# Start development web server
# run flask --app channel.py register
# to register channel with hub

if __name__ == '__main__':
    app.run(debug=True)
    #app.run(port=5001, debug=True)



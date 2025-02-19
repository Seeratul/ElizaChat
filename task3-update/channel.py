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

HUB_URL = 'http://localhost:5555'
HUB_AUTHKEY = '1234567890'
CHANNEL_AUTHKEY = '0987654321'
CHANNEL_NAME = "ElizaChatChannel"
CHANNEL_ENDPOINT = "http://localhost:5001" # don't forget to adjust in the bottom of the file
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
    # filter profanity
    # filter messages that dont contain "I" <- TODO 
    message['content'] = profanity.censor(message['content']) 
    # add message to messages
    messages = read_messages()
    messages.append({'content': message['content'],
                     'sender': message['sender'],
                     'timestamp': message['timestamp'],
                     'extra': extra,
                     })
    save_messages(messages)

    # answer
    answer_msg = answer_message(message)
    # add message to messages
    messages = read_messages()
    messages.append({'content': answer_msg['content'],
                     'sender': answer_msg['sender'],
                     'timestamp': answer_msg['timestamp'],
                   #  'extra': extra,
                     })
    save_messages(messages)

    return "OK", 200

def answer_message(msg):
   # new_msg = {}
    
    if 'HI' in msg['content']: 
        therapist = Eliza()
        reply = therapist.respond(msg['content'])
        new_msg = {'content': reply,
                     'sender': "eliza",
                     'timestamp': msg['timestamp'],
                    # 'extra': extra,
                     }
    elif 'i' in msg['content']:
        new_msg = {'content': "bla",
                     'sender': "eliza",
                     'timestamp': msg['timestamp'],
                    # 'extra': extra,
                     }
    else:
        new_msg = {'content': "I have nothing to say to that",
                'sender': "eliza",
                'timestamp': msg['timestamp'],
            # 'extra': extra,
                }
    return new_msg


def check_msg_age(messages):
    for msg in messages:
        # convert timestamp string to datetime
        timestamp_string = msg['timestamp'] 
        format_string = "%Y-%m-%dT%H:%M:%S.%f" # 2025-02-17T15:43:00.372228
        datetime_msg = datetime.strptime(timestamp_string, format_string)
        datetime_cur = datetime.now()
        age = datetime_cur - datetime_msg
        age_in_seconds = age.total_seconds()
        if age_in_seconds >= 30:
            messages.remove(msg)
    return messages

def read_messages():
    global CHANNEL_FILE
    try:
        f = open(CHANNEL_FILE, 'r')
    except FileNotFoundError:
        return []
    try:
        messages = json.load(f)
        # go through messages
        messages = check_msg_age(messages)
    except json.decoder.JSONDecodeError:
        messages = []
    f.close()
    return messages

def save_messages(messages):
    global CHANNEL_FILE
    with open(CHANNEL_FILE, 'w') as f:
        json.dump(messages, f)

# Start development web server
# run flask --app channel.py register
# to register channel with hub

if __name__ == '__main__':
    app.run(port=5001, debug=True)

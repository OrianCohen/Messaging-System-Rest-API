from flask import Flask, jsonify, request, abort, make_response
from flask_restful import Api
from flask_httpauth import HTTPBasicAuth
app = Flask(__name__)
api = Api(app)
# http://127.0.0.1:5000/message/api/v1.0/messages
# Authentication access for existing user
auth = HTTPBasicAuth()

MESSAGEJSON = [
    {
        "id": 1,
        "sender": "Orian",
        "receiver": "support@apple.com",
        "message": "I would like to know if you working this week? I want to purchase the Iphon 11 PRO",
        "subject": "Purchase new IPHONE",
        "creationDate": "datetime.timestamp(datetime.now())"
    },
    {
        "id": 2,
        "sender": "Loren",
        "receiver": "Bank of America",
        "message": "I would like to open a new bank account",
        "subject": "New account",
        "creationDate": "datetime.timestamp(datetime.now())"
    }

]

# @auth.get_password
# def get_password(username):
#     if username == 'Orian':
#         return 'Hu432!'
#     return None
#
#
# @auth.error_handler
# def unauthorized():
#     return make_response(jsonify({'error': 'Unauthorized access'}), 403)


# If we tried to invoke this function  with curl the access wil be denied, to invoke we need to send out credentials
# $ curl -u Orian:Hu432 -i http://localhost:5000/message/api/v1.0/messages
# @app.route('/message/api/v1.0/messages', methods=['GET'])
# @auth.login_required
# def get_tasks():
#     return jsonify({'Messages': MESSAGEJSON})


# If we will ask for message that not exist in our data
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify(({'error': 'Not found'}), 404))


# Reading all messages in our DATA
@app.route('/message/api/v1.0/messages', methods=['GET'])
def get_messages():
    # return jsonify({'All Messages': AllMessage.get()})
    return jsonify({'All Messages': MESSAGEJSON})


# Read message by ID number
@app.route('/message/api/v1.0/messages/<int:messageId>', methods=['GET'])
def get_message_by_id(messageId):
    message = [message for message in MESSAGEJSON if message['id'] == messageId]
    if len(message) == 0:
        abort(404)
    return jsonify({'Message by ID': message[0]})


# Delete message by name
@app.route('/message/api/v1.0/messages/<name>', methods=['DELETE'])
def delete_message(name):
    message = [message for message in MESSAGEJSON if (message['sender'] == name or message['receiver'] == name)]
    if len(message) == 0:
        abort(404)
    MESSAGEJSON.remove(message[0])
    return jsonify({'Result': True})


# curl -i -H "Content-Type: application/json" -X POST -d http://localhost:5000/message/api/v1.0/messages
# Write a new message
@app.route('/message/api/v1.0/messages', methods=['POST'])
def new_message():
    if not request.json or not 'title' in request.json:
        abort(400)
    create_message = {
        'id': MESSAGEJSON[-1]['id'] + 1,
        'sender': request.json.get('sender', ""),
        'receiver': request.json.get('receiver', ""),
        'message': request.json.get('message', ""),
        'subject': request.json.get('subject', ""),
        'creationDate': request.json.get('creationDate', "")
    }
    MESSAGEJSON.append(create_message)
    return jsonify({'New Message': create_message}), 201


if __name__ == "__main__":
    app.run(debug=True)

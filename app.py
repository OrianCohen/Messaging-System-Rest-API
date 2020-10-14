from flask import Flask, jsonify, request, abort, make_response
from flask_restful import Resource, Api, reqparse
from datetime import datetime
import requests

app = Flask(__name__)
api = Api(app)

MESSAGEJSON = [
    {
        "id": 1,
        "sender": "Orian",
        "receiver": "support@apple.com",
        "message": "I would like to know if you working this week? I want to purchase the Iphon 11 PRO",
        "subject": "Purchase new IPHONE",
        "creationDate": "datetime.timestamp(datetime.now())",
        "readStatus": True

    },
    {
        "id": 2,
        "sender": "Loren",
        "receiver": "Bank of America",
        "message": "I would like to open a new bank account",
        "subject": "New account",
        "creationDate": "datetime.timestamp(datetime.now())",
        "readStatus": True
    },
    {
        "id": 3,
        "sender": "Loren",
        "receiver": "Orian",
        "message": "XXXXX",
        "subject": "New account",
        "creationDate": "datetime.timestamp(datetime.now())",
        "readStatus": False
    },
    {
        "id": 4,
        "sender": "Loren",
        "receiver": "Coral",
        "message": "XXXXX",
        "subject": "New account",
        "creationDate": "datetime.timestamp(datetime.now())",
        "readStatus": False
    }
]

message_put_args = reqparse.RequestParser()
message_put_args.add_argument("sender", type=str)
message_put_args.add_argument("receiver", type=str)
message_put_args.add_argument("message", type=str)
message_put_args.add_argument("subject", type=str)

#
# def abort_if_user_exist(user_name):
#     abort(409, message="")
#
#
# def abort_if_user_name_doesnt_exist(user_name):
#     for item in MESSAGEJSON:
#         if user_name not in item:
#             abort(409, message="User nor exist")


class Message(Resource):
    # read a random messages
    @staticmethod
    def get():
        return MESSAGEJSON[0]


class ReadMessage(Resource):
    # get all the messages from sender or receiver (for specific name)
    def get(self, user_name):
        message = [[message for message in MESSAGEJSON if
                    (message['sender'].lower() == user_name.lower() or message[
                        'receiver'].lower() == user_name.lower())]]
        if len(message) == 0:
            abort(404)
        return jsonify({'Message by user name': message[0]})

    # add new message to our data
    def put(self, user_name):
        new_message = message_put_args.parse_args()
        new_message['id'] = MESSAGEJSON[-1]['id'] + 1
        new_message['creationDate'] = str(datetime.now())
        new_message['readStatus'] = False
        MESSAGEJSON.append(new_message)
        return MESSAGEJSON[new_message['id'] -1]

    # delete message as receiver or sender (for specific name)
    def delete(self, user_name):
        # abort_if_user_name_doesnt_exist(user_name)
        message = [message for message in MESSAGEJSON if
                   (message['sender'].lower() == user_name.lower() or message['receiver'].lower() == user_name.lower())]
        if len(message) == 0:
            abort(404)
        MESSAGEJSON.remove(message[0])
        return jsonify({'Result': True})

# get all unread messages by name
class UnreadMessage(Resource):
    def get(self, user_name):
        message = [[message for message in MESSAGEJSON if
                    (message['receiver'].lower() == user_name.lower()) and (
                                message['readStatus'] == False)]]
        if len(message) == 0:
            abort(404)
        return jsonify({'Unread Messages': message[0]})


# return all messages (it can be only 1 message as well)
api.add_resource(Message, '/messages')

# return all messages for specific user + delete message + add new message
api.add_resource(ReadMessage, '/messages/read/<user_name>')

# return all unread messages for specific user
api.add_resource(UnreadMessage, '/messages/unread/<user_name>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

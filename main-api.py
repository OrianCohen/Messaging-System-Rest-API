import requests
from flask import Flask, jsonify, request, abort, make_response, json
from flask_httpauth import HTTPBasicAuth
from flask_restful import Resource, Api, reqparse
from datetime import datetime

app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth

message_put_args = reqparse.RequestParser()
message_put_args.add_argument("sender", type=str)
message_put_args.add_argument("receiver", type=str)
message_put_args.add_argument("message", type=str)
message_put_args.add_argument("subject", type=str)

with open('data.json', 'rb') as f:
    jsondata = json.load(f)


class ReadMessage(Resource):
    # Read a random messages
    @staticmethod
    def get():
        return jsondata['restapi'][2]


class Message(Resource):
    # Get all the messages by user name (for sender or receiver)
    def get(self, user_name):
        messages = []
        for message_ in jsondata['restapi']:
            if str(user_name).lower() == str(message_['sender']).lower() or str(user_name).lower() == str(
                    message_['receiver']).lower():
                messages.append(message_)
        if messages:
            return jsonify({'Message by user name': messages})
        else:
            abort(404, "User not exist in our data")

    # Write new message
    def post(self, user_name):
        url = 'https://mighty-savannah-89613.herokuapp.com'
        new_message = message_put_args.parse_args()
        new_message['id'] = jsondata['restapi'][-1]['id'] + 1
        new_message['creationDate'] = str(datetime.now())
        new_message['readStatus'] = False
        requests.post(url, json=jsondata)
        return jsonify({'Result': True})

    # Delete message as receiver or sender (for specific name)
    def delete(self, user_name):
        flag = False
        # remove all messages from our data(JSON) by user name (only sender)
        for elemnt in jsondata['restapi']:
            if str(user_name).lower() == str(elemnt['sender']).lower():
                # jsondata['restapi'].remove(elemnt)
                flag = True
        # if user not exist
        if not flag:
            abort(404, "User not exist")
        else:
            return jsonify({'Result': True})


# Get all unread messages by user name (only receiver)
class UnreadMessage(Resource):
    def get(self, user_name):
        messages = []
        for message_ in jsondata['restapi']:
            if str(user_name).lower() == str(message_['receiver']).lower() and message_['readStatus'] == "False":
                messages.append(message_)
                message_['readStatus'] = True
        if messages:
            return jsonify({'Unread Messages': messages})
        else:
            abort(404, "There aren't unread messages to this user")


# return all messages (it can be only 1 message as well)
api.add_resource(ReadMessage, '/messages')

# return all messages for specific user + delete message + add new message
api.add_resource(Message, '/messages/read/<user_name>')

# return all unread messages for specific user
api.add_resource(UnreadMessage, '/messages/unread/<user_name>')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)

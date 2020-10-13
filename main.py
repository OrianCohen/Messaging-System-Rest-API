from flask import Flask, jsonify, request, abort
from flask_restful import Resource, Api, reqparse
from datetime import datetime

app = Flask(__name__)
api = Api(app)

MESSAGE = {
    'message1': {'sender': 'Oriancohen@gmail.com',
                 'receiver': 'support@apple.com',
                 'message': 'I would like to know if you working this week? I want to purchase the Iphon 11 PRO',
                 'subject': 'Purchase new IPHONE',
                 'creationDate': datetime.timestamp(datetime.now())
                 },
    'message2': {'sender': 'Loren',
                 'receiver': 'Bank of America',
                 'message': 'I would like to open a new bank account',
                 'subject': 'New account',
                 'creationDate': datetime.timestamp(datetime.now())
                 }
}


# If message do not exist ERROR
def abort_if_todo_doesnt_exist(messageId):
    if messageId not in MESSAGE:
        abort(404, message="message1 {} doesn't exist".format(messageId))


parser = reqparse.RequestParser()
parser.add_argument('new_message')


# Find an existing message, delete message by message ID, add new message
class ReadMessage(Resource):
    def get(self, messageId):
        abort_if_todo_doesnt_exist(messageId)
        return {messageId: MESSAGE[messageId]}

    def delete(self, messageId):
        abort_if_todo_doesnt_exist(messageId)
        del MESSAGE[messageId]
        return '', 204

    def put(self, messageId):
        args = parser.parse_args()
        new_message = {'messageNew': args['new_message']}
        MESSAGE[messageId] = new_message
        return new_message, 201


# Shows a list of all messages and lets you POST to add new message
class AllMessage(Resource):
    def get(self):
        return MESSAGE

    def post(self):
        args = parser.parse_args()
        message_id = int(max(MESSAGE.keys()).lstrip('message')) + 1
        message_id = 'message%i' % message_id
        MESSAGE[message_id] = {'messageNew': args['new_message']}
        return MESSAGE[message_id], 201


api.add_resource(AllMessage, '/messages')
api.add_resource(ReadMessage, '/messages/<messageId>')

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from datetime import  datetime
from flask import jsonify

app = Flask(__name__)
api = Api(app)

class Message(Resource):
    def serialize(self):
        return jsonify({
            'sender': self.sender,
            'receiver': self.receiver,
            'message': self.message,
            'subject': self.subject,
            'creationDate': self.creationDate,
        })

api.add_resource(Message)

# @app.route('/')
# @app.route('/messageApi', methods =['GET', 'POST'])
# def messageFunction():
#     if request.method == 'GET': #return all the messaged in our json file
#         return jsonify()
#     elif request.method == 'POST':
#         sender = request.args.get('sender', '')
#         receiver = request.args.get('receiver', '')
#         message = request.args.get('message', '')
#         subject = request.args.get('subject', '')
#         now = datetime.now()
#         creationDate = datetime.timestamp(now)
#         return jsonify({'sender': sender, 'receiver': receiver, 'message': message, 'subject':subject, 'creationDate':creationDate})
#
# @app.route('/messageApi', methods =['GET', 'POST'])
# def messageFunctionId(id):
#     if request.method == 'GET': #return the filtered message by ID
#         return jsonify(Message.get())
#     elif request.method == 'PUT':
#         sender = request.args.get('sender', '')
#         receiver = request.args.get('receiver', '')
#         message = request.args.get('message', '')
#         subject = request.args.get('subject', '')
#         now = datetime.now()
#         creationDate = datetime.timestamp(now)
#         return jsonify({'id': id, 'sender': sender, 'receiver': receiver, 'message': message, 'subject':subject, 'creationDate':creationDate})
#     elif request.method == 'NEW':
#         return jsonify(Message=api.add_resource())

if __name__ == "__main__":
    app.run(debug=True)

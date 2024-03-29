from flask import request, jsonify, Flask

from incollege.annotations.TokenRequired import token_required
from incollege.entity.AuthJWT import AuthJWT
from incollege.services import MessagesService

def configure_messages_routes(app: Flask):
    
    @app.route('/send_message', methods = ['POST'])
    @token_required
    def handle_send_message(token: AuthJWT):
        data = request.get_json()
        user1 = token.user_id
        chat_id = data.get('chat_id')
        content = data.get('content')
        MessagesService.create_message(user1, chat_id, content)
        return jsonify()
    
    @app.route('/delete_message', methods = ['POST'])
    @token_required
    def handle_delete_message(token: AuthJWT):
        data = request.get_json()
        user1 = token.user_id
        message_id = data.get('message_id')
        MessagesService.delete_message(user1, message_id)
        return jsonify({'message': 'Message deleted successfully'}), 200
    
    @app.route('/get_messages', methods=['POST'])
    @token_required
    def handle_get_messages(token: AuthJWT):
        data = request.get_json()
        user1 = token.user_id
        chat_id = data.get('chat_id')
        messages_in_chat = MessagesService.get_messages(user1, chat_id)
        messages_serial = [vars(message) for message in messages_in_chat]
        return jsonify({'message': messages_serial})
    
    @app.route('/change_read_status', methods = ['POST'])
    @token_required
    def handle_change_read_status(token: AuthJWT):
        data = request.get_json()
        user1 = token.user_id
        chat_id = data.get('chat_id')
        status = data.get('status')
        message_id = data.get('message_id')
        MessagesService.change_read_status(user1, chat_id, message_id, status)
        return jsonify()
    
    @app.route('/get_unread', methods = ['POST'])
    @token_required
    def handle_get_unread(token: AuthJWT):
        data = request.get_json()
        user1 = token.user_id
        chat_id = data.get('chat_id')
        MessagesService.get_unread(user1, chat_id)
        unread_messages = MessagesService.get_unread(user1, chat_id)
        unread_messages_serial = [vars(message) for message in unread_messages]
        return jsonify({'message': unread_messages_serial})
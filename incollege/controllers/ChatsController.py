from flask import request, jsonify, Flask

from incollege.annotations.TokenRequired import token_required
from incollege.entity.AuthJWT import AuthJWT
from incollege.services import ChatsService

def configure_chats_routes(app: Flask):
    
    @app.route('/create_chat', methods = ['POST'])
    @token_required
    def handle_create_chat(token: AuthJWT):
        data = request.get_json()
        user1 = token.user_id
        user2 = data.get('user2')
        
        ChatsService.create_chat(user1, user2)
        return jsonify()
    
    @app.route('/get_chat_list', methods = ['POST'])
    @token_required
    def handle_get_chat_list(token: AuthJWT):
        data = request.get_json()
        user1 = token.user_id
        chats = ChatsService.get_chat_list(user1)
        chats_serial = [vars(chat) for chat in chats]
        return jsonify({'message': chats_serial})
    
    @app.route('/chat_fetch', methods=['POST'])
    def handle_chat_fetch():

        data = request.get_json()
        chat_id = data.get('chat_id')
        chat = ChatsService.get_chat(chat_id)
        chat_serial = vars(chat)
        return jsonify({'message': chat_serial})
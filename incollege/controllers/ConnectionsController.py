from flask import jsonify, request

from incollege.annotations.TokenRequired import token_required
from incollege.services import ConnectionsService, AuthService


def configure_connection_routes(app):

    @app.route('/send_request', methods=['POST'])
    @token_required
    def send_connection_request(token_data):
        data = request.get_json()
        sender_userID = token_data['usr']
        receiver_userID = data.get('receiver_userID')

        result = ConnectionsService.send_connection_request(sender_userID, receiver_userID)
        return jsonify(result)
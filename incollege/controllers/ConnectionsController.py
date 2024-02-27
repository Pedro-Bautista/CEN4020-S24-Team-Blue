from flask import jsonify, request

from incollege.annotations.TokenRequired import token_required
from incollege.services import ConnectionsService, AuthService


def configure_connection_routes(app):

    @app.route('/send_request', methods=['POST'])
    @token_required
    def send_connection_request(token_data):
        data = request.get_json()
        sender_userID = token_data['usr']
        print("\n TOKENNNNN: ", sender_userID)
        receiver_userID = data.get('receiver_userID')

        ConnectionsService.send_connection_request(sender_userID, receiver_userID)
        return jsonify()

    
    @app.route('/get_requests_list', methods=['POST'])
    @token_required
    def handle_requests_list(token_data):
        user_id = token_data['usr']
        requests = ConnectionsService.get_requests_list(user_id)
        requests_serial = [vars(request) for request in requests]
        return jsonify({'message': requests_serial})

    @app.route('/get_accepted_list', methods=['POST'])
    @token_required
    def handle_accepted_list(token_data):
        user_id = token_data['usr']
        requests = ConnectionsService.get_accepted_list(user_id)
        requests_serial = [vars(request) for request in requests]
        return jsonify({'message': requests_serial})

    @app.route('/change_conn_status', methods=['POST'])
    def handle_conn_status_change():
        data = request.get_json()
        requestID = data.get('request_id')
        status = data.get('status')
        ConnectionsService.change_conn_status(requestID, status)
        return jsonify()
        

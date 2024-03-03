from flask import jsonify, request

from incollege.annotations.TokenRequired import token_required
from incollege.services import ConnectionsService


def configure_connection_routes(app):
    @app.route('/send_request', methods=['POST'])
    @token_required
    def send_connection_request(token):
        data = request.get_json()
        sender_user_id = token.user_id
        recipient_user_id = data.get('recipient_user_id')

        ConnectionsService.send_connection_request(sender_user_id, recipient_user_id)
        return jsonify()

    @app.route('/get_requests_list', methods=['POST'])
    @token_required
    def handle_requests_list(token):
        user_id = token.user_id
        connection_requests = ConnectionsService.get_pending_requests_by_recipient_user_id(user_id)
        connection_requests_serial = [vars(connection_request) for connection_request in connection_requests]
        return jsonify({'message': connection_requests_serial})

    @app.route('/get_accepted_list', methods=['POST'])
    @token_required
    def handle_accepted_list(token):
        user_id = token.user_id
        connection_requests = ConnectionsService.get_connections_by_user_id(user_id)
        connection_requests_serial = [vars(connection_request) for connection_request in connection_requests]
        return jsonify({'message': connection_requests_serial})

    @app.route('/get_connection_profiles', methods=['POST'])
    @token_required
    def handle_connection_profiles(token):
        user_id = token.user_id
        connection_users = ConnectionsService.get_connection_profiles_by_user_id(user_id)
        connection_users_serial = [vars(connection_user) for connection_user in connection_users]
        return jsonify({'message': connection_users_serial})

    @app.route('/change_conn_status', methods=['POST'])
    @token_required
    def handle_conn_status_change(token):
        data = request.get_json()
        sender_user_id = data.get('sender_user_id')
        recipient_user_id = token.user_id
        status = data.get('status')
        ConnectionsService.update_connection_request(sender_user_id, recipient_user_id, status)
        return jsonify()

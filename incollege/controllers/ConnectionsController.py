# from flask import jsonify, request

# from incollege.annotations.TokenRequired import token_required
# from incollege.services import ConnectionsService


# def configure_connection_routes(app):

#     @app.route('/send_request', methods=['POST'])
#     def send_connection_request():
#         data = request.get_json()
#         sender_userID = data.get('sender_userID')
#         receiver_userID = data.get('receiver_userID')

#         result = ConnectionsService.send_connection_request(sender_userID, receiver_userID)
#         return jsonify(result)
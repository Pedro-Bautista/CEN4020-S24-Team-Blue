# User Controller
# Provides endpoints for interacting with user data
from flask import jsonify, request

from incollege.annotations.TokenRequired import token_required
from incollege.services import UserService


def configure_user_routes(app):
    @app.route('/user_search', methods=['POST'])
    def handle_user_search():
        data = request.get_json()
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        university = data.get('university')
        major = data.get('major')

        users = UserService.search_users(first_name, last_name, university, major)
        users_serial = [vars(user) for user in users]

        return jsonify({'message': users_serial})

    @app.route('/update_preferences', methods=['POST'])
    @token_required
    def handle_update_pref(token):
        data = request.get_json()
        preference_name = data.get('preference_name')
        preference_value = data.get('preference_value')
        user_id = token.user_id

        UserService.update_preference(user_id, preference_name, preference_value)

        return jsonify({'Message': f'{preference_name} Updated successfully to {preference_value}'}), 200

    @app.route('/get_user_data', methods=['POST'])
    @token_required
    def get_user_data(token):
        user_id = token.user_id
        user_data = UserService.get_user_data(user_id)
        users_serial = vars(user_data)
        return jsonify({'user': users_serial})
    
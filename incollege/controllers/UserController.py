# User Controller
# Provides endpoints for interacting with user data
from flask import jsonify, request, Flask

from incollege.annotations.TokenRequired import token_required
from incollege.services import UserService


def configure_user_routes(app: Flask):
    """Invoked to bind routes pertaining to this controller class.

    Args:
        app: The currently running Flask app instance.
    """

    @app.route('/user_search', methods=['POST'])
    def handle_user_search():
        """Route for user search requests.

        Returns:
            Response: A JSON-serialized list of :obj:`User`.
        """
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
        """Route for handling preference updates. Expects a preference name and value to set.

        Args:
            token (AuthJWT): A valid authentication token for the sending user.

        Returns:
            Response: A basic success message with status code 200.
        """
        data = request.get_json()
        preference_name = data.get('preference_name')
        preference_value = data.get('preference_value')
        user_id = token.user_id

        UserService.update_preference(user_id, preference_name, preference_value)

        return jsonify({'Message': f'{preference_name} Updated successfully to {preference_value}'}), 200

    @app.route('/get_user_data', methods=['POST'])
    @token_required
    def handle_get_user_data(token):
        """Route for obtaining user profile data.

        Args:
            token (AuthJWT): A valid authentication token for the sending user.

        Returns:
            Response: A JSON-serialized list of :obj:`User`.
        """
        user_id = token.user_id
        user_data = UserService.get_user(user_id)
        users_serial = vars(user_data)
        return jsonify({'user': users_serial})

    @app.route('/get_user_profile_status', methods=['POST'])
    @token_required
    def handle_get_profile_status(token):
        user_id = token.user_id
        profile_status = UserService.get_user_profile_status(user_id)
        return jsonify(profile_status)
# Authentication Controller
# Handles sign in and sign up requests

from flask import request, jsonify, Flask

from incollege.annotations.TokenRequired import token_required
from incollege.entity.AuthJWT import AuthJWT
from incollege.services import JobService


def configure_job_routes(app: Flask):
    """Invoked to bind routes pertaining to this controller class.

    Args:
        app: The currently running Flask app instance.
    """

    @app.route('/job_post', methods=['POST'])
    @token_required
    def handle_job_post(token: AuthJWT):
        """Route for job posting. Expects all parameters to :class:`~Job` other than job_id.

        Args:
            token (AuthJWT): A valid authentication token for the sending user.

        Returns:
            Response: A basic placeholder response indicating success with status code 201.
        """
        data = request.get_json()
        user_id = token.user_id
        title = data.get('title')
        desc = data.get('desc')
        employer = data.get('employer')
        location = data.get('location')
        salary = data.get('salary')

        JobService.post_job(user_id, title, desc, employer, location, salary)

        return jsonify({'message': 'Job posted successfully'}), 201

    @app.route('/job_delete', methods=['POST'])
    @token_required
    def handle_job_delete(token: AuthJWT):
        """Route for job deletion. Expects job_id.

        Args:
            token (AuthJWT): A valid authentication token for the sending user.

        Returns:
            Response: A basic placeholder response indicating success with status code 200.
        """
        data = request.get_json()
        user_id = token.user_id
        job_id = data.get('job_id')

        JobService.delete_job(job_id, user_id)

    @app.route('/job_fetch_all', methods=['POST'])
    def handle_job_fetch_all():
        """Route for fetching all jobs.

        Returns:
            Response: A JSON-serialized list of all job records.
        """
        jobs = JobService.get_all_jobs()
        jobs_serial = [vars(job) for job in jobs]
        return jsonify({'message': jobs_serial})

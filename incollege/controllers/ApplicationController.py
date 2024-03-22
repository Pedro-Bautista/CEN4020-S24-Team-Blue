from flask import jsonify, request, Flask

from incollege.annotations.TokenRequired import token_required
from incollege.entity.AuthJWT import AuthJWT
from incollege.services import ApplicationService


def configure_application_routes(app: Flask):
    """Invoked to bind routes pertaining to this controller class.

        Args:
            app: The currently running Flask app instance.
        """

    @app.route('/application_fetch_by_job_id', methods=['POST'])
    def handle_application_fetch_by_job_id():
        data = request.get_json()
        job_id = data.get('job_id')
        applications = ApplicationService.get_applications_by_job_id(job_id)
        applications_serial = [vars(application) for application in applications]
        return jsonify({'message': applications_serial})

    @app.route('/applications_fetch_by_user_id', methods=['POST'])
    @token_required
    def handle_application_fetch_by_user_id(token: AuthJWT):
        data = request.get_json()
        user_id = token.user_id
        applications = ApplicationService.get_applications_by_user_id(user_id)
        applications_serial = [vars(application) for application in applications]
        return jsonify({'message': applications_serial})

    @app.route('/application_create', methods=['POST'])
    @token_required
    def handle_application_create(token: AuthJWT):
        data = request.get_json()
        applied_job_id = data.get('job_id')
        applicant_user_id = token.user_id
        graduation_date = data.get('graduation_date')
        start_working_date = data.get('start_working_date')
        application_paragraph = data.get('application_paragraph')
        ApplicationService.create_application(applied_job_id, applicant_user_id, graduation_date,
                                              start_working_date, application_paragraph)
        return jsonify()


from flask import jsonify, request, Flask

from incollege.annotations.TokenRequired import token_required
from incollege.entity.AuthJWT import AuthJWT
from incollege.services import JobSaveService


def configure_job_save_routes(app: Flask):
    """Invoked to bind routes pertaining to this controller class.

        Args:
            app: The currently running Flask app instance.
        """

    @app.route('/save_job', methods=['POST'])
    @token_required
    def handle_save_job(token: AuthJWT):
        data = request.get_json()
        saving_user_id = token.user_id
        saved_job_id = data.get('job_id')
        JobSaveService.create_job_save(saving_user_id, saved_job_id)
        return jsonify()

    @app.route('/unsave_job', methods=['POST'])
    @token_required
    def handle_unsave_job(token: AuthJWT):
        data = request.get_json()
        saving_user_id = token.user_id
        saved_job_id = data.get('job_id')
        JobSaveService.delete_job_save(saving_user_id, saved_job_id)
        return jsonify()

    @app.route('/saved_jobs_fetch', methods=['POST'])
    @token_required
    def handle_saved_jobs_fetch(token: AuthJWT):
        saving_user_id = token.user_id
        job_saves = JobSaveService.get_saved_jobs_by_user_id(saving_user_id)
        job_saves_serial = [vars(job_save) for job_save in job_saves]
        return jsonify({'message': job_saves_serial})

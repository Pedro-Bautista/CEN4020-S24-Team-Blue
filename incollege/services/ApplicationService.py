from incollege.entity.Application import Application
from incollege.entity.enum.ApplicationStatus import ApplicationStatus
from incollege.exceptions.ContentException import ContentException
from incollege.repositories import ApplicationRepository, JobRepository, UserRepository


def get_applications_by_job_id(applied_job_id: str) -> 'List[Application] | None':
    if not applied_job_id:
        raise ContentException('Required job identifier information not provided.', 400)
    applications = ApplicationRepository.get_applications_by_job_id(applied_job_id)
    if not applications:
        raise ContentException('No such applications.', 404)
    return applications


def get_applications_by_user_id(applicant_user_id: str) -> 'List[Application] | None':
    if not applicant_user_id:
        raise ContentException('Required user identifier information not provided.', 400)
    applications = ApplicationRepository.get_applications_by_user_id(applicant_user_id)
    if not applications:
        raise ContentException('No such applications.', 400)
    return applications


def create_application(applied_job_id: str, applicant_user_id: str, graduation_date: str,
                       start_working_date: str, application_paragraph: str):
    if not (applied_job_id and applicant_user_id and graduation_date and start_working_date
            and application_paragraph):
        raise ContentException('Required application submission information not provided.', 400)
    job = JobRepository.get_job(applied_job_id)
    if not job:
        raise ContentException('No such job.', 404)
    user = UserRepository.get_user(applicant_user_id)
    if not user:
        raise ContentException('No such user.', 404)
    existing = ApplicationRepository.get_application_by_job_and_user_id(applied_job_id, applicant_user_id)
    if existing:
        raise ContentException('Application already exists.', 400)
    application = Application(applied_job_id, applicant_user_id, graduation_date, start_working_date,
                              application_paragraph, ApplicationStatus.PENDING)
    ApplicationRepository.create_application(application)

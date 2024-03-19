from incollege.entity.Application import Application
from incollege.entity.Job import Job
from incollege.entity.User import User
from incollege.repositories.UniversalRepositoryHelper import UniversalRepositoryHelper

UNIVERSAL = UniversalRepositoryHelper(Application.__class__, 'applications', ['applied_job_id', 'applicant_user_id'])


def get_application_count() -> int:
    return UNIVERSAL.get_record_count()


def create_application(obj: Application):
    UNIVERSAL.create_object(obj)


def update_application(obj: Application):
    UNIVERSAL.insert_update_object(obj)


def delete_application(obj: Application):
    UNIVERSAL.delete_object(obj)


def get_applications_by_job_id(applied_job_id: str) -> 'List[Application] | None':
    return UNIVERSAL.get_objects_intersection({'applied_job_id': applied_job_id})


def get_applications_by_user_id(applicant_user_id: str) -> 'List[Application] | None':
    return UNIVERSAL.get_objects_intersection({'applicant_user_id': applicant_user_id})


def get_application_by_job_and_user_id(applied_job_id: str, applicant_user_id: str) -> 'Application | None':
    result = UNIVERSAL.get_objects_intersection({'applied_job_id': applied_job_id,
                                                 'applicant_user_id': applicant_user_id})
    if result:
        return result[0]


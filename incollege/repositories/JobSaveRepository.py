from incollege.entity.JobSave import JobSave
from incollege.repositories.UniversalRepositoryHelper import UniversalRepositoryHelper

UNIVERSAL = UniversalRepositoryHelper(JobSave, 'job_saves', ['saving_user_id', 'saved_job_id'])


def get_job_saves_count() -> int:
    return UNIVERSAL.get_record_count()


def create_job_save(obj: JobSave):
    UNIVERSAL.create_object(obj)


def delete_job_save(obj: JobSave):
    UNIVERSAL.delete_object(obj)


def get_job_saves_by_saving_user_id(saving_user_id: str) -> 'List[JobSave] | None':
    return UNIVERSAL.get_objects_intersection({'saving_user_id': saving_user_id})

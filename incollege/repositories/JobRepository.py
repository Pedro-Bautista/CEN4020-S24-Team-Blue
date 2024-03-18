from incollege.entity.Job import Job
from incollege.repositories.UniversalRepositoryHelper import UniversalRepositoryHelper

UNIVERSAL = UniversalRepositoryHelper(Job, 'jobs', ['job_id'])


def create_job(job):
    UNIVERSAL.create_object(job)


def get_job_count():
    return UNIVERSAL.get_record_count()

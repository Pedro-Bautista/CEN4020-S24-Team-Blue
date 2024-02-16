from incollege.entity.Job import Job
from incollege.repositories.UniversalRepositoryHelper import UniversalRepositoryHelper

UNIVERSAL = UniversalRepositoryHelper('jobs', Job)


def create_job(title, desc, employer, location, salary):
    job = Job(title, desc, employer, location, salary)
    UNIVERSAL.create_object(job)


def get_job_count():
    UNIVERSAL.get_record_count()

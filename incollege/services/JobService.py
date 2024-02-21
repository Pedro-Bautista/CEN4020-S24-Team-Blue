import uuid

from incollege.config import Config
from incollege.entity.Job import Job
from incollege.exceptions.AuthException import AuthException
from incollege.exceptions.ContentException import ContentException
from incollege.repositories import JobRepository


def create_job_id():
    return str(uuid.uuid4())


def post_job(user_id, title, desc, employer, location, salary):
    if not user_id:
        raise AuthException("Not authorized.", 401)
    if not title or not desc or not employer or not location or not salary:
        raise ContentException("Required job posting information not provided.", 400)
    if JobRepository.get_job_count() >= Config.JOB_LIMIT:
        raise ContentException("Job posting limit reached.", 507)

    job_id = create_job_id()
    job = Job(job_id, user_id, title, desc, employer, location, salary)

    JobRepository.create_job(job)

import uuid
from typing import List

from incollege.config import Config
from incollege.entity.Job import Job
from incollege.exceptions.AuthException import AuthException
from incollege.exceptions.ContentException import ContentException
from incollege.repositories import JobRepository


def create_job_id():
    """Create a unique job identifier.

    Returns:
        str: The unique identifier.
    """
    return str(uuid.uuid4())


def post_job(user_id: str, title: str, desc: str, employer: str, location: str, salary: str):
    """Create a job in the system based on the provided parameters.

    Args:
        user_id (str): The transacting user id.
        title (str): The title for the job.
        desc (str): The description for the job.
        employer (str): The employer name for the job.
        location (str): The location for the job.
        salary (str): The salary for the job.
    """
    if not user_id:
        raise AuthException('Not authorized.', 401)
    if not title or not desc or not employer or not location or not salary:
        raise ContentException('Required job posting information not provided.', 400)
    if JobRepository.get_job_count() >= Config.JOB_LIMIT:
        raise ContentException('Job posting limit reached.', 507)
    try:
        salary_float = float(salary)
    except ValueError as e:
        raise ContentException('Salary must be a real number.', 400)

    job_id = create_job_id()
    job = Job(job_id, user_id, title, desc, employer, location, salary_float)

    JobRepository.create_job(job)


def get_job(job_id: str) -> 'Job | None':
    if not job_id:
        raise ContentException('Required job identifier information not provided.', 400)
    job = JobRepository.get_job(job_id)
    if not job:
        raise ContentException('No such job.', 404)
    return job


def get_all_jobs() -> List[Job]:
    jobs = JobRepository.get_all_jobs()
    if not jobs:
        raise ContentException('No jobs found.', 404)
    return jobs


def delete_job(job_id: str, user_id: str):
    if not job_id:
        raise ContentException('Required job identifier information not provided.', 400)
    if not user_id:
        raise AuthException('Not authorized.', 401)
    job = JobRepository.get_job(job_id)
    if not job:
        raise ContentException('No such job.', 404)
    if job.owner_user_id != user_id:
        raise AuthException('Only the content owner may delete this content.', 403)
    JobRepository.delete_job(job)

from incollege.config import Config
from incollege.exceptions.ContentException import ContentException
from incollege.repositories import JobRepository


def post_job(title, desc, employer, location, salary):
    if not title or not desc or not employer or not location or not salary:
        raise ContentException("Required job posting information not provided.", 400)
    if JobRepository.get_job_count() >= Config.JOB_LIMIT:
        raise ContentException("Job posting limit reached.", 507)

    JobRepository.create_job(title, desc, employer, location, salary)
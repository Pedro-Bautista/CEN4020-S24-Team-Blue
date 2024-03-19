from typing import Generic, List

from incollege.entity.Job import Job
from incollege.repositories.UniversalRepositoryHelper import UniversalRepositoryHelper

UNIVERSAL = UniversalRepositoryHelper(Job, 'jobs', ['job_id'])


def create_job(job: Job):
    """Create a row in the database recording job.

    Args:
        job: The job to be recorded.
    """
    UNIVERSAL.create_object(job)


def get_job_count() -> int:
    """Get the total number of job rows in the table.

    Returns:
        int: Number of rows in the job table.
    """
    return UNIVERSAL.get_record_count()


def get_job(job_id: str) -> Job:
    """Get a job based in the job_id.

    Args:
        job_id: The job_id to match.

    Returns:
        Job: The matching job, if exists
        None: If no such job exists.
    """
    result = UNIVERSAL.get_objects_intersection({'job_id': job_id})
    if result:
        return result[0]


def get_all_jobs() -> List[Job]:
    """Retrieves all jobs from the database.

    Returns:
        List[Job]: All jobs on record.
        None: If no jobs exist.
    """
    return UNIVERSAL.get_all_records()


def delete_job(job: Job):
    """Deletes the matching job entry in the table based on job_id.

    Args:
        job: The job to delete.
    """
    UNIVERSAL.delete_object(job)

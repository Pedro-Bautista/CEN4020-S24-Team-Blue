from incollege.entity.JobSave import JobSave
from incollege.exceptions.ContentException import ContentException
from incollege.repositories import UserRepository, JobRepository, JobSaveRepository


def create_job_save(saving_user_id: str, saved_job_id: str):
    if not saving_user_id or not saved_job_id:
        raise ContentException('Required job saving information not provided.', 400)
    user = UserRepository.get_user(saving_user_id)
    if not user:
        raise ContentException('No such user.', 404)
    job = JobRepository.get_job(saved_job_id)
    if not job:
        raise ContentException('No such job', 404)
    job_save = JobSave(saving_user_id, saved_job_id)
    JobSaveRepository.create_job_save(job_save)


def delete_job_save(saving_user_id: str, saved_job_id: str):
    if not saving_user_id or not saved_job_id:
        raise ContentException('Required job saving information not provided.', 400)
    user = UserRepository.get_user(saving_user_id)
    if not user:
        raise ContentException('No such user.', 404)
    job = JobRepository.get_job(saved_job_id)
    if not job:
        raise ContentException('No such job', 404)
    job_save = JobSave(saving_user_id, saved_job_id)
    JobSaveRepository.delete_job_save(job_save)


def get_saved_jobs_by_user_id(saving_user_id: str) -> 'List[JobSave] | None':
    if not saving_user_id:
        raise ContentException('Required job save information not provided.', 400)
    user = UserRepository.get_user(saving_user_id)
    if not user:
        raise ContentException('No such user.', 404)
    job_saves = JobSaveRepository.get_job_saves_by_saving_user_id(saving_user_id)
    if not job_saves:
        raise ContentException('No such job saves.', 404)
    return job_saves

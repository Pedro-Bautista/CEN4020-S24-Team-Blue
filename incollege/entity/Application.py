from incollege.entity.enum.ApplicationStatus import ApplicationStatus


class Application:
    """Stores data relating to job applications.

    Attributes:
        applied_job_id (str): job_id for the :obj:`Job` applied to.
        applicant_user_id (str): user_id for the :obj:`Student` applying.
        status (int): Current status for this application, as provided by :class:`~ApplicationStatus.py`
        graduation_date (str): Date of graduation as supplied by applicant.
        start_working_date (str): Date of first availability as supplied by applicant.
        application_paragraph (str): Application text body as supplied by applicant.
    """

    def __init__(self, applied_job_id: str, applicant_user_id: str, graduation_date: str,
                 start_working_date: str, application_paragraph: str,
                 status: int = ApplicationStatus.PENDING):
        self.applied_job_id = applied_job_id
        self.applicant_user_id = applicant_user_id
        self.graduation_date = graduation_date
        self.start_working_date = start_working_date
        self.application_paragraph = application_paragraph
        self.status = status

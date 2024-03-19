class Job:
    """This object stores data relating to Jobs posted by users.

    Attributes:
        job_id (str): Unique identifier for this Job.
        owner_user_id (str): Unique identifier for the posting :obj:`User`
        title (str): Job title.
        desc (str): Job description.
        employer (str): Job employer.
        location (str): Job location.
        salary (float): Job salary.
    """

    def __init__(self, job_id: str, owner_user_id: str, title: str, desc: str, employer: str,
                 location: str, salary: float):
        """Generate an instance based on the specified parameters.

        Args:
            job_id (str): Unique identifier for this Job.
            owner_user_id (str): Unique identifier for the posting :obj:`User`
            title (str): Job title.
            desc (str): Job description.
            employer (str): Job employer.
            location (str): Job location.
            salary (float): Job salary.
        """
        self.job_id = job_id
        self.owner_user_id = owner_user_id
        self.title = title
        self.desc = desc
        self.employer = employer
        self.location = location
        self.salary = salary

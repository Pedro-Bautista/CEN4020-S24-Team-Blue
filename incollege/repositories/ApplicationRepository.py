from incollege.entity.Application import Application
from incollege.repositories.UniversalRepositoryHelper import UniversalRepositoryHelper

UNIVERSAL = UniversalRepositoryHelper(Application.__class__, 'applications', ['applied_job_id', 'applicant_user_id'])


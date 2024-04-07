import pytest
from unittest.mock import MagicMock, patch

from incollege.entity.Job import Job
from incollege.entity.User import User
from incollege.exceptions import ContentException
from incollege.services.ApplicationService import *


@pytest.fixture
def mock_application_repository():
    return MagicMock()


@pytest.fixture
def mock_job_repository():
    return MagicMock()


@pytest.fixture
def mock_user_repository():
    return MagicMock()


test_job = Job('some_job_id', 'some_owner_user_id', 'some_title', 'some_desc', 'some_employer',
               'some_location', 123456)
test_user = User('some_user_id', 'some_username', 'some_first', 'some_last')


@patch('incollege.repositories.ApplicationRepository.get_applications_by_job_id')
def test_get_applications_by_job_id_valid(mock_get_applications_by_job_id, mock_application_repository):
    mock_application = Application("job_id", "user_id", "grad_date", "start_date", "paragraph")
    mock_get_applications_by_job_id.return_value = [mock_application]
    with patch('incollege.repositories.ApplicationRepository', mock_application_repository):
        result = get_applications_by_job_id("job_id")
        assert result is not None


@patch('incollege.repositories.ApplicationRepository.get_applications_by_job_id')
def test_get_applications_by_job_id_invalid(mock_get_applications_by_job_id):
    with pytest.raises(ContentException):
        get_applications_by_job_id("")


@patch('incollege.repositories.ApplicationRepository.get_applications_by_job_id')
def test_get_applications_by_job_id_no_applications(mock_get_applications_by_job_id):
    mock_get_applications_by_job_id.return_value = []
    with pytest.raises(ContentException):
        get_applications_by_job_id("job_id")


@patch('incollege.repositories.ApplicationRepository.get_applications_by_user_id')
def test_get_applications_by_user_id_valid(mock_get_applications_by_user_id, mock_application_repository):
    mock_application = Application("job_id", "user_id", "grad_date", "start_date", "paragraph")
    mock_get_applications_by_user_id.return_value = [mock_application]
    with patch('incollege.repositories.ApplicationRepository', mock_application_repository):
        result = get_applications_by_user_id("user_id")
        assert result is not None


@patch('incollege.repositories.ApplicationRepository.get_applications_by_user_id')
def test_get_applications_by_user_id_invalid(mock_get_applications_by_user_id):
    with pytest.raises(ContentException):
        get_applications_by_user_id("")


@patch('incollege.repositories.ApplicationRepository.get_applications_by_user_id')
def test_get_applications_by_user_id_no_applications(mock_get_applications_by_user_id):
    mock_get_applications_by_user_id.return_value = []
    with pytest.raises(ContentException):
        get_applications_by_user_id("user_id")


@patch('incollege.repositories.ApplicationRepository.create_application')
@patch('incollege.repositories.JobRepository.get_job')
@patch('incollege.repositories.UserRepository.get_user')
@patch('incollege.repositories.ApplicationRepository.get_application_by_job_and_user_id')
def test_create_application_valid(mock_get_application_by_job_and_user_id, mock_get_user, mock_get_job,
                                  mock_create_application, mock_application_repository):
    mock_get_job.return_value = test_job
    mock_get_user.return_value = test_user
    mock_create_application.return_value = None
    mock_get_application_by_job_and_user_id.return_value = None
    with patch('incollege.repositories.ApplicationRepository', mock_application_repository), \
            patch('incollege.repositories.JobRepository', MagicMock()), \
            patch('incollege.repositories.UserRepository', MagicMock()):
        create_application("job_id", "user_id", "grad_date", "start_date", "paragraph")
        assert mock_create_application.called


@patch('incollege.repositories.ApplicationRepository.create_application')
def test_create_application_invalid(mock_create_application):
    with pytest.raises(ContentException):
        create_application("", "", "", "", "")


@patch('incollege.repositories.JobRepository.get_job')
def test_create_application_job_not_found(mock_get_job, mock_user_repository):
    mock_get_job.return_value = None
    with patch('incollege.repositories.UserRepository', MagicMock()):
        with pytest.raises(ContentException):
            create_application("job_id", "user_id", "grad_date", "start_date", "paragraph")


@patch('incollege.repositories.UserRepository.get_user')
@patch('incollege.repositories.JobRepository.get_job')
def test_create_application_user_not_found(mock_get_job, mock_get_user, mock_job_repository):
    mock_get_user.return_value = None
    mock_get_job.return_value = test_job
    with patch('incollege.repositories.JobRepository', MagicMock()):
        with pytest.raises(ContentException):
            create_application("job_id", "user_id", "grad_date", "start_date", "paragraph")


@patch('incollege.repositories.JobRepository.get_job')
@patch('incollege.repositories.ApplicationRepository.get_application_by_job_and_user_id')
@patch('incollege.repositories.UserRepository.get_user')
def test_create_application_existing_application(mock_get_application_by_job_and_user_id, mock_get_job,
                                                 mock_get_user, mock_job_repository, mock_user_repository):
    mock_job_repository.get_job.return_value = {}
    mock_get_user.return_value = test_user
    mock_get_job.return_value = test_job
    mock_get_application_by_job_and_user_id.return_value = Application(
        "job_id", "user_id", "grad_date", "start_date", "paragraph"
    )
    with patch('incollege.repositories.ApplicationRepository', MagicMock()), \
            patch('incollege.repositories.JobRepository', mock_job_repository), \
            patch('incollege.repositories.UserRepository', mock_user_repository):
        with pytest.raises(ContentException):
            create_application("job_id", "user_id", "grad_date", "start_date", "paragraph")

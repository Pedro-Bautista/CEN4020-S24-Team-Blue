import pytest
from unittest.mock import patch, MagicMock
from incollege.exceptions.ContentException import ContentException
from incollege.services.JobSaveService import create_job_save, delete_job_save, get_saved_jobs_by_user_id


@pytest.fixture
def mock_get_user():
    return MagicMock()


@pytest.fixture
def mock_get_job():
    return MagicMock()


@pytest.fixture
def mock_job_save_repository():
    return MagicMock()


@patch('incollege.repositories.UserRepository.get_user', return_value=MagicMock())
@patch('incollege.repositories.JobRepository.get_job', return_value=MagicMock())
@patch('incollege.repositories.JobSaveRepository.create_job_save')
def test_create_job_save_success(mock_create_job_save, mock_get_job, mock_get_user):
    create_job_save('user_id', 'job_id')
    assert mock_create_job_save.called


@patch('incollege.repositories.UserRepository.get_user', return_value=None)
def test_create_job_save_missing_user(mock_get_user):
    with pytest.raises(ContentException) as exc_info:
        create_job_save('', 'job_id')
    assert str(exc_info.value) == 'Required job saving information not provided.'


@patch('incollege.repositories.UserRepository.get_user', return_value=MagicMock())
@patch('incollege.repositories.JobRepository.get_job', return_value=None)
def test_create_job_save_missing_job(mock_get_job, mock_get_user):
    with pytest.raises(ContentException) as exc_info:
        create_job_save('user_id', 'blah')
    assert str(exc_info.value) == 'No such job'


@patch('incollege.repositories.UserRepository.get_user', return_value=None)
def test_delete_job_save_missing_user(mock_get_user):
    with pytest.raises(ContentException) as exc_info:
        delete_job_save('', 'job_id')
    assert str(exc_info.value) == 'Required job saving information not provided.'


@patch('incollege.repositories.UserRepository.get_user', return_value=MagicMock())
@patch('incollege.repositories.JobRepository.get_job', return_value=None)
def test_delete_job_save_missing_job(mock_get_job, mock_get_user):
    with pytest.raises(ContentException) as exc_info:
        delete_job_save('user_id', 'blah')
    assert str(exc_info.value) == 'No such job'


@patch('incollege.repositories.UserRepository.get_user', return_value=None)
def test_get_saved_jobs_by_user_id_missing_user(mock_get_user):
    with pytest.raises(ContentException) as exc_info:
        get_saved_jobs_by_user_id('')
    assert str(exc_info.value) == 'Required job save information not provided.'


@patch('incollege.repositories.UserRepository.get_user', return_value=MagicMock())
@patch('incollege.repositories.JobSaveRepository.get_job_saves_by_saving_user_id', return_value=None)
def test_get_saved_jobs_by_user_id_missing_job_saves(mock_get_job_saves_by_saving_user_id, mock_get_user):
    with pytest.raises(ContentException) as exc_info:
        get_saved_jobs_by_user_id('user_id')
    assert str(exc_info.value) == 'No such job saves.'

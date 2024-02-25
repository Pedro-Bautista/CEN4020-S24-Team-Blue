from unittest import mock
import pytest

from incollege.services.JobService import *

test_job = Job('some_job_id', 'some_owner_user_id', 'some_title', 'some_desc', 'some_employer',
               'some_location', 123456)


def test_create_job_id():
    result = create_job_id()

    assert result is not None


@mock.patch('incollege.repositories.JobRepository.create_job')
def test_post_job_no_user_id(mock_create_job):
    with pytest.raises(AuthException) as e:
        post_job('', 'some_title', 'some_desc', 'some_employer', 'some_location', 123456)

        assert e == AuthException("Not authorized.", 401)

    mock_create_job.assert_not_called()


@mock.patch('incollege.repositories.JobRepository.create_job')
def test_post_job_missing_data(mock_create_job):
    with pytest.raises(ContentException) as e:
        post_job('some_id', '', 'some_desc', '', 'some_location', 123456)

        assert e == ContentException("Required job posting information not provided.", 400)

    mock_create_job.assert_not_called()


@mock.patch('incollege.repositories.JobRepository.get_job_count', return_value=Config.JOB_LIMIT)
@mock.patch('incollege.repositories.JobRepository.create_job')
def test_post_job_limit_reached(mock_create_job, mock_get_job_count):
    with pytest.raises(ContentException) as e:
        post_job('some_id', 'some_title', 'some_desc', 'some_employer', 'some_location', 123456)

        assert e == ContentException('Job posting limit reached.', 507)

    mock_create_job.assert_not_called()


@mock.patch('incollege.repositories.JobRepository.get_job_count', return_value=Config.JOB_LIMIT-1)
@mock.patch('incollege.repositories.JobRepository.create_job')
def test_post_job(mock_create_job, mock_get_job_count):
    result = post_job('some_id', 'some_title', 'some_desc', 'some_employer', 'some_location', 123456)

    mock_create_job.assert_called_once()

from unittest import mock

from incollege.repositories.JobRepository import *

job_description = (
    ('job_id',),
    ('owner_user_id',),
    ('title',),
    ('desc',),
    ('employer',),
    ('location',),
    ('salary',)
)
test_job_data = [
    ('some_uuid', 'some_user_uuid', 'some_title', 'some_desc', 'some_employer', 'some_location', 'some_salary',
     'some_sms_pref', 'some_targeted_adv_pref')
]
test_job = Job(**dict(zip([key[0] for key in job_description], test_job_data[0])))


@mock.patch('incollege.repositories.UniversalRepositoryHelper.get_connection')
def test_create_job(mock_get_connection):
    mock_cursor = mock.MagicMock()
    mock_get_connection.return_value.cursor.return_value = mock_cursor

    result = create_job(test_job)

    assert result is None


@mock.patch('incollege.repositories.UniversalRepositoryHelper.get_connection')
def test_get_job_count(mock_get_connection):
    mock_cursor = mock.MagicMock()
    mock_get_connection.return_value.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = (1, )

    result = get_job_count()

    assert result == 1

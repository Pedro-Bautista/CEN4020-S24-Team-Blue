from unittest import mock

from incollege.repositories.UserRepository import *

user_description = (
    ('user_id',),
    ('username',),
    ('first_name',),
    ('last_name',),
    ('language_pref',),
    ('email_pref',),
    ('sms_pref',),
    ('targeted_adv_pref',)
)
test_user_data = [
    ('some_uuid', 'some_username', 'some_first_name', 'some_last_name', 'some_language', 'some_email_pref',
     'some_sms_pref', 'some_targeted_adv_pref')
]



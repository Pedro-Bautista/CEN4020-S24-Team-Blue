class User:
    def __init__(self, user_id, username, first_name, last_name, language = 'english', email_pref = 1, SMS_pref = 1, targeted_adv = 1):
        self.user_id = user_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.language = language
        self.email_pref = email_pref
        self.SMS_pref = SMS_pref
        self.targeted_adv = targeted_adv

class User:
    def __init__(self, user_id, username, first_name, last_name, university, major, language_pref='english',
                 email_pref=1, sms_pref=1,
                 targeted_adv_pref=1):
        self.user_id = user_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.university = university
        self.major = major
        self.language_pref = language_pref
        self.email_pref = email_pref
        self.sms_pref = sms_pref
        self.targeted_adv_pref = targeted_adv_pref

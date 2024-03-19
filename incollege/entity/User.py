class User:
    """Stores data pertaining to system users.

    Attributes:
        user_id (str): Unique identifier for user.
        username (str): Username for user.
        first_name (str): First name provided by user.
        last_name (str): Last name provided by user.
        university (str, optional): University name provided by user.
            Defaults to ''.
        major (str): Major provided by user.
            Defaults to ''.
        bio (str): Brief autobiography provided by user.
            Defaults to ''.
        experience (str): Experience section provided by user.
            Defaults to ''.
        education (str): Education section provided by user.
            Defaults to ''.
        language_pref (str): Preferred language of user.
            Defaults to 'english'.
        email_pref (int): Email communications preference of user.
            Defaults to 1.
        sms_pref (int): SMS communications preference of user.
            Defaults to 1.
        targeted_adv_pref (int): Targeted advertising preference of user.
            Defaults to 1.
    """

    def __init__(self, user_id: str, username: str, first_name: str, last_name: str, university: str = '',
                 major: str = '', bio: str = '', experience: str = '', education: str = '',
                 language_pref: str = 'english', email_pref: int = 1, sms_pref: int = 1,
                 targeted_adv_pref: int = 1):
        """Generate an instance based on the specified parameters.

        Args:
            user_id (str): Unique identifier for user.
            username (str): Username for user.
            first_name (str): First name provided by user.
            last_name (str): Last name provided by user.
            university (str, optional): University name provided by user.
                Defaults to ''.
            major (str, optional): Major provided by user.
                Defaults to ''.
            bio (str, optional): Brief autobiography provided by user.
                Defaults to ''.
            experience (str, optional): Experience section provided by user.
                Defaults to ''.
            education (str, optional): Education section provided by user.
                Defaults to ''.
            language_pref (str, optional): Preferred language of user.
                Defaults to 'english'.
            email_pref (int, optional): Email communications preference of user.
                Defaults to 1.
            sms_pref (int, optional): SMS communications preference of user.
                Defaults to 1.
            targeted_adv_pref (int, optional): Targeted advertising preference of user.
                Defaults to 1.
        """
        self.user_id = user_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.university = university
        self.major = major
        self.bio=bio
        self.experience = experience
        self.education = education
        self.language_pref = language_pref
        self.email_pref = email_pref
        self.sms_pref = sms_pref
        self.targeted_adv_pref = targeted_adv_pref

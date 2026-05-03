API_PREFIX = "/api/v1"
CONTACTS_PREFIX = "/contacts"

NAME_MAX_LENGTH = 30
EMAIL_MAX_LENGTH = 50
PHONE_MAX_LENGTH = 20
ADDITIONAL_INFO_MAX_LENGTH = 150

EMAIL_REGEX = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
PHONE_REGEX = r"^\+?[0-9]{7,20}$"
PASSWORD_REGEX = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$"